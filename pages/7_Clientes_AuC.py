import pandas as pd
import streamlit as st
import datetime
import json
from relatorio_captacao_ativacao import gerar_relatorio_captacao, gerar_relatorio_evasao, gerar_tabela_evasao

with open('dict_nomes.json', 'r') as f:
    dict_nomes = json.load(f)
assessor = None
captacao, captacao_data, captacao_assessor, data_posicao_captacao = gerar_relatorio_captacao(assessor)
data = st.date_input('Selecionar Data do Relatório:')
crm = st.file_uploader('Tabela CRM')
crm = pd.read_excel(crm)


crm = crm.iloc[:, 2:-1]
crm.columns = ['Conta', 'PL', 'Assessor', 'Tipo']

crm['Assessor'] = crm['Assessor'].str[1:]
crm['Tipo'] = crm['Tipo'].str[8:]
pl_by_assessor = crm.groupby(['Assessor', 'Tipo'])['PL'].sum().unstack(fill_value=0)
pl_by_assessor.columns = ['PL PF', 'PL PJ']
pl_by_assessor['PL Total'] = pl_by_assessor['PL PF'] + pl_by_assessor['PL PJ']

tipo_by_assessor = crm
tipo_by_assessor = tipo_by_assessor[tipo_by_assessor['PL'] > 100]

tipo_by_assessor = tipo_by_assessor.groupby(['Assessor', 'Tipo']).size().unstack(fill_value=0)
tipo_by_assessor.columns = ['Clientes PF', 'Clientes PJ']
tipo_by_assessor['Clientes Total'] = tipo_by_assessor['Clientes PF'] + tipo_by_assessor['Clientes PJ']


tabela_total = pl_by_assessor.join(tipo_by_assessor, how='left')
tabela_total['Data'] = data

tabela_total['Nome'] = tabela_total.index.map(dict_nomes)
captacao_assessor.drop(captacao_assessor.columns[0], axis=1, inplace=True)
novos_nomes_coluna = ['Captação Total', 'Captação PF', 'Captação PJ']
captacao_assessor = captacao_assessor.set_axis(novos_nomes_coluna, axis=1)
st.table(captacao_assessor)

st.dataframe(tabela_total, column_order=['Data', 'Nome', 'PL PF', 'PL PJ', 'PL Total', 'Clientes PF', 'Clientes PJ', 'Clientes Total'])
joined_df = pd.concat([captacao_assessor, tabela_total], axis=1)
joined_df = joined_df.fillna(0)
st.dataframe(joined_df, column_order=['Data', 'Nome', 'Captação Total', 'Captação PF', 'Captação PJ', 'PL PF', 'PL PJ', 'PL Total', 'Clientes PF', 'Clientes PJ', 'Clientes Total'])
joined_df.to_excel('relatorio_rafa.xlsx')
####

# Lidando com as comissões
# # Assuming you have a DataFrame 'df' with a datetime column 'Date_Time'
# # and a second table 'comissions' with a datetime column 'Comission_Date'

# # Step 1: Extract month and year
# df['Month'] = df['Date_Time'].dt.month
# df['Year'] = df['Date_Time'].dt.year

# # Step 2: Filter 'comissions' table
# comissions_filtered = comissions[
#     (comissions['Comission_Date'].dt.month == df['Month'].iloc[0]) &
#     (comissions['Comission_Date'].dt.year == df['Year'].iloc[0])
# ]

# # Step 3: Calculate cumulative sum
# comissions_filtered['Cumulative_Comission'] = comissions_filtered['Comissions'].cumsum()

# # Merge back into the original DataFrame
# df = pd.merge(df, comissions_filtered[['Comission_Date', 'Cumulative_Comission']],
#               left_on='Date_Time', right_on='Comission_Date', how='left')

# # Fill missing values (for dates without comissions)
# df['Cumulative_Comission'].fillna(method='ffill', inplace=True)

# # Drop intermediate columns
# df.drop(['Month', 'Year', 'Comission_Date'], axis=1, inplace=True)

# # Now 'df' contains the desired 'Cumulative_Comission' column
# print(df)
