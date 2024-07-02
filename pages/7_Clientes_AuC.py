import pandas as pd
import streamlit as st
import datetime


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


tipo_by_assessor = crm.groupby(['Assessor', 'Tipo']).size().unstack(fill_value=0)
tipo_by_assessor.columns = ['Clientes PF', 'Clientes PJ']
tipo_by_assessor['Clientes Total'] = tipo_by_assessor['Clientes PF'] + tipo_by_assessor['Clientes PJ']


tabela_total = pl_by_assessor.join(tipo_by_assessor, how='left')
tabela_total['Data'] = data
st.dataframe(tabela_total)
