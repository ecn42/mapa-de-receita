import os
import pandas as pd
import streamlit as st
import json

with open('dict_nomes.json', 'r') as f:
    dict_nomes = json.load(f)


with open('dict_repasse.json', 'r') as w:
    dict_repasse = json.load(w)

def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        return df
    return None

def multiply_by_dict(row, dict_repasse):
    return row * dict_repasse[row.name]

assessor = st.query_params.get('assessor')

def gerar_historico_comissao():
    # Read 'gerencial.xlsx' into a DataFrame
    # Define the base directory and the date
    base_dir = 'historicocomissoes'
    sub_dirs = ['gerencial', 'cambio', 'credito', 'xpcs', 'xpvp']

    dates = os.listdir(base_dir)

    # Initialize a list to hold all dataframes
    all_dfs_combined_list = []
    all_dfs_grouped_combined_list = []

    # List of subdirectories
    
    for date in dates:
        # Initialize a dictionary to hold the dataframes
        dfs = {}

        # Loop over the subdirectories
        for sub_dir in sub_dirs:
            # Construct the file path
            file_path = os.path.join(base_dir, date, sub_dir, sub_dir + '.xlsx')
            
            # Read the Excel file into a dataframe
            df = pd.read_excel(file_path)
            
            # Store the dataframe in the dictionary
            dfs[sub_dir] = df

        df_gerencial = dfs['gerencial']
        df_cambio = dfs['cambio']
        df_credito = dfs['credito']
        df_xpcs = dfs['xpcs']
        df_xpvp = dfs['xpvp']
            
    


        #DF GERENCIAL:    
        df_gerencial['Cód. Assessor Direto'] = df_gerencial['Cód. Assessor Direto'].str[1:]
        df_gerencial = df_gerencial[['Cód. Assessor Direto','Produto', 'Receita (R$)', 'Comissão Bruta (R$) Escritório']]
        df_gerencial.columns = ['Código Assessor', 'Categoria', 'Receita Líquida', 'Comissão Escritório']

        # Group by 'Cód. Assessor' and calculate the sum
        grouped_df_gerencial = df_gerencial.groupby('Código Assessor').sum().reset_index()
        grouped_df_gerencial = grouped_df_gerencial[['Código Assessor','Receita Líquida', 'Comissão Escritório']]
        # Delete the first character in the 'Cód. Assessor' column
        df_gerencial.set_index('Código Assessor', inplace=True)
        grouped_df_gerencial.set_index('Código Assessor', inplace=True)

    
    
        
        #DF XPCS:
        df_xpcs['Código Assessor'] = df_xpcs['Código Assessor'].str[1:]
        df_xpcs = df_xpcs[['Código Assessor', 'Categoria','Receita Líquida', 'Comissão Escritório']]
        grouped_df_xpcs = df_xpcs.groupby('Código Assessor').sum().reset_index()
        grouped_df_xpcs = grouped_df_xpcs[['Código Assessor','Receita Líquida', 'Comissão Escritório']]
        df_xpcs.set_index('Código Assessor', inplace=True)
        grouped_df_xpcs.set_index('Código Assessor', inplace=True)

        #DF XPVP:
        df_xpvp['Código Assessor'] = df_xpvp['Código Assessor'].str[1:]
        df_xpvp = df_xpvp[['Código Assessor', 'Categoria','Receita Líquida', 'Comissão Escritório']]
        grouped_df_xpvp = df_xpvp.groupby('Código Assessor').sum().reset_index()
        grouped_df_xpvp = grouped_df_xpvp[['Código Assessor','Receita Líquida', 'Comissão Escritório']]
        df_xpvp.set_index('Código Assessor', inplace=True)
        grouped_df_xpvp.set_index('Código Assessor', inplace=True)

        #DF Credito:
        df_credito['Código Assessor'] = df_credito['Código Assessor'].str[1:]
        df_credito = df_credito[['Código Assessor', 'Categoria','Receita Líquida', 'Comissão Escritório']]
        grouped_df_credito = df_credito.groupby('Código Assessor').sum().reset_index()
        grouped_df_credito = grouped_df_credito[['Código Assessor','Receita Líquida', 'Comissão Escritório']]
        df_credito.set_index('Código Assessor', inplace=True)
        grouped_df_credito.set_index('Código Assessor', inplace=True)

        #DF CAMBIO:
        df_cambio['Código Assessor'] = df_cambio['Código Assessor'].str[1:]
        df_cambio = df_cambio[['Código Assessor', 'Categoria','Receita Líquida', 'Comissão Escritório']]
        grouped_df_cambio = df_cambio.groupby('Código Assessor').sum().reset_index()
        grouped_df_cambio = grouped_df_cambio[['Código Assessor','Receita Líquida', 'Comissão Escritório']]
        df_cambio.set_index('Código Assessor', inplace=True)
        grouped_df_cambio.set_index('Código Assessor', inplace=True)

        dfs = [df_gerencial, df_cambio, df_credito, df_xpcs, df_xpvp]
        dfs_grouped = [grouped_df_gerencial, grouped_df_cambio, grouped_df_credito, grouped_df_xpcs, grouped_df_xpvp]

        dfs_combined = pd.concat(dfs)
        dfs_grouped_combined = pd.concat(dfs_grouped)

        all_dfs_combined_list.append(dfs_combined.assign(Date=date))
        all_dfs_grouped_combined_list.append(dfs_grouped_combined.assign(Date=date))

    all_dfs_combined = pd.concat(all_dfs_combined_list)
    all_dfs_grouped_combined = pd.concat(all_dfs_grouped_combined_list)
    

    multiplicador_ir = (1-0.2)
    multiplicador_mesa = (1-0.1)
    
    all_dfs_combined['Comissão Escritório Líquida'] = all_dfs_combined['Comissão Escritório'].apply(lambda x: x * multiplicador_mesa * multiplicador_ir)
    all_dfs_combined['Comissão Assessor'] = all_dfs_combined['Comissão Escritório Líquida'] * all_dfs_combined.index.map(dict_repasse)

    all_dfs_grouped_combined['Comissão Escritório Líquida'] = all_dfs_grouped_combined['Comissão Escritório'].apply(lambda x: x * multiplicador_mesa * multiplicador_ir)
    all_dfs_grouped_combined['Comissão Assessor'] = all_dfs_grouped_combined['Comissão Escritório Líquida'] * all_dfs_grouped_combined.index.map(dict_repasse)
    all_dfs_grouped_combined = all_dfs_grouped_combined.groupby(['Date', all_dfs_grouped_combined.index]).sum()
    
    return all_dfs_combined, all_dfs_grouped_combined