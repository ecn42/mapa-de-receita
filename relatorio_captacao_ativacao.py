import streamlit as st
import pandas as pd
import json

with open('dict_nomes.json', 'r') as f:
    dict_nomes = json.load(f)

def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        return df
    return None

# def gerar_relatorio_captacao():
   
captacao = 'dir/captacao/captacao.xlsx'
ativacao = 'dir/positivador/positivador.xlsx'

def gerar_relatorio_captacao(assessor):
    if captacao is not None:
    
        ##LIDANDO COM A PLANILHA DO POSITIVADOR
        data_captacao = load_data(captacao)
        data_posicao_captacao = data_captacao['Data Atualização'].iloc[0]

        # Convert 'Data' column to datetime
        data_captacao['Data'] = pd.to_datetime(data_captacao['Data'])

        # Filter data_captacao to only include rows where 'Assessor' is equal to the variable assessor
        if assessor is not None:
            data_captacao = data_captacao[data_captacao['Assessor'] == assessor]

        # Group by 'Assessor' and 'Data' columns and calculate the sum of 'Captação' column
        grouped_data_captacao = data_captacao.groupby(['Assessor', 'Data']).sum().reset_index().round(0)
        
        # Create a pivot table with 'Assessor' and 'Data' as index, 'Tipo Pessoa' as columns, and the sum of 'Captação' as values
        pivot_table_captacao = data_captacao.pivot_table(values='Captação', index=['Assessor', 'Data'], columns='Tipo Pessoa', aggfunc='sum', fill_value=0).round(0)

        # Rename the columns as per your requirement
        pivot_table_captacao.columns = ['PF', 'PJ']

        # Merge the grouped data and pivot table
        final_data_captacao = pd.merge(grouped_data_captacao, pivot_table_captacao, on=['Assessor', 'Data'])

        final_data = final_data_captacao

        final_data['Assessor'] = final_data['Assessor'].astype(str)
        final_data.set_index(['Assessor', 'Data'], inplace=True)


        final_data['Nome'] = final_data.index.get_level_values('Assessor').map(dict_nomes)
        final_data = final_data[['Nome', 'Captação', 'PF', 'PJ']]
        final_data_cpt = final_data
         # Calculate the total by date
        final_data_cpt_date = final_data_cpt.groupby('Data').sum()
        final_data_cpt_date = final_data_cpt_date.drop(columns='Nome')

        # Calculate the total by assessor
        final_data_cpt_assessor = final_data_cpt.groupby('Assessor').sum(numeric_only=True)
        final_data_cpt_assessor['Nome'] = final_data_cpt_assessor.index.get_level_values('Assessor').map(dict_nomes)
        final_data_cpt_assessor = final_data_cpt_assessor[['Nome', 'Captação', 'PF', 'PJ']]
        
    return final_data_cpt, final_data_cpt_date, final_data_cpt_assessor, data_posicao_captacao

def gerar_relatorio_evasao(assessor):

    if ativacao is not None:
        
        ##LIDANDO COM A PLANILHA DO POSITIVADOR
        data_ativacao = load_data(ativacao)
        data_ativacao_bruta = data_ativacao.copy()
        data_ativacao['Ativou em M?'] = data_ativacao['Ativou em M?'].apply(lambda x: 1 if x == 'Sim' else 0)
        data_ativacao['Evadiu em M?'] = data_ativacao['Evadiu em M?'].apply(lambda x: 1 if x == 'Sim' else 0)    

        

        # Group by 'Assessor' column and calculate the sum of 'Receita no Mês' column
        grouped_data_ativacao = data_ativacao.groupby('Assessor').sum().reset_index().round(0)
        grouped_data_ativacao = grouped_data_ativacao[['Assessor', 'Ativou em M?', 'Evadiu em M?']]
        
        # Create a pivot table with 'Assessor' as index, 'Tipo Pessoa' as columns, and the sum of 'Receita no Mês' as values
        pivot_table_ativacao = data_ativacao.pivot_table(values='Ativou em M?', index='Assessor', columns='Tipo Pessoa', aggfunc='sum', fill_value=0).round(0)

        # Rename the columns as per your requirement
        pivot_table_ativacao.columns = ['Ativação PF', 'Ativação PJ']

        # Create a pivot table with 'Assessor' as index, 'Tipo Pessoa' as columns, and the sum of 'Receita no Mês' as values
        pivot_table_evasao = data_ativacao.pivot_table(values='Evadiu em M?', index='Assessor', columns='Tipo Pessoa', aggfunc='sum', fill_value=0).round(0)

        # Rename the columns as per your requirement
        pivot_table_evasao.columns = ['Evasão PF', 'Evasão PJ']


        # Merge the grouped data and pivot table
        final_data_ativacao = pd.merge(grouped_data_ativacao, pivot_table_ativacao, on='Assessor')
        final_data_ativacao = pd.merge(final_data_ativacao, pivot_table_evasao, on='Assessor')

        final_data_atv = final_data_ativacao

        final_data_atv['Assessor'] = final_data_atv['Assessor'].astype(str)
        final_data_atv.set_index('Assessor', inplace=True)

        final_data_atv['Nome'] = final_data_atv.index.map(dict_nomes)
        final_data_atv = final_data_atv[['Nome', 'Ativou em M?', 'Ativação PF', 'Ativação PJ', 'Evadiu em M?', 'Evasão PF', 'Evasão PJ']]

        # return final_data, final_data_liq
        if assessor is not None:
            assessor = str(assessor)
            final_data_atv = final_data_atv.loc[final_data_atv.index == assessor]

        return final_data_atv