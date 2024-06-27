import streamlit as st
import pandas as pd
import pyperclip
import io
import datetime

now = datetime.datetime.now().strftime("%Y%m%d %H%M%S")
buffer = io.BytesIO()

st.header('Carteirador - Carteira Fundamentalista')

arquivo_posicoes = st.file_uploader('Posição Custódia Bull', type='xlsx')
caminho_posicoes = 'carteirador/posicoes.xlsx'
caminho_lista = 'carteirador/lista_clientes_fundamentalista.csv'

if arquivo_posicoes:
    arquivo_posicoes = pd.read_excel(arquivo_posicoes)
    arquivo_posicoes.to_excel(caminho_posicoes, index=False)
    st.success(f'Posicoes atualizadas')


# Sample data (replace with your actual DataFrames)
posicoes = pd.read_excel(caminho_posicoes)
boleta = pd.read_excel('carteirador/carteira_fundamentalista.xlsx')
df_lista = pd.read_csv(caminho_lista)
st.data_editor(df_lista, num_rows = 'dynamic')

lista_fundamentalista = df_lista['Clientes'].tolist()
boleta_fundamentalista = pd.DataFrame(boleta)  # Your 'boleta_fundamentalista' DataFrame
clientes_fundamentalista = pd.DataFrame(lista_fundamentalista)  # Your 'clientes_fundamentalista' DataFrame
posicao_clientes = pd.DataFrame(posicoes)  # Your 'posicao_clientes' DataFrame

unique_ativos = boleta_fundamentalista['Ativo(PnT- Giro de Carteira)'].unique().tolist()
boleta_fundamentalista_dict = {}

# Step 1: Lookup 'COD CLIENTE' value for each 'cod'
for cod in lista_fundamentalista:
    cod = int(cod)
    # Get all 'COD CLIENTE' values for the current 'cod'
   
    filtered_df = posicao_clientes[posicao_clientes['COD. CLIENTE'] == cod].copy()
  
     # Create a copy of 'boleta_fundamentalista'
    df_copy = boleta_fundamentalista.copy()
   
        # Update 'Qtd.' column based on 'ATIVO' and 'QTD. TOTAL' from 'posicao_clientes'
    for ativo in unique_ativos:
        qtd_total = filtered_df.loc[filtered_df['ATIVO'] == ativo, 'QTD. TOTAL'].sum()
        df_copy.loc[df_copy['Ativo(PnT- Giro de Carteira)'] == ativo, 'Qtd.'] = qtd_total
   

    # Set the 'Conta Cliente' value to the first 'COD CLIENTE' for consistency
    df_copy.loc[0, 'Conta cliente'] = cod

    # Add the DataFrame to the dictionary
    boleta_fundamentalista_dict[f'boleta_fundamentalista_{cod}'] = df_copy
# Convert the dictionary of DataFrames to a list of DataFrames
df_list = list(boleta_fundamentalista_dict.values())

# Concatenate the DataFrames vertically
result_df = pd.concat(df_list, ignore_index=True)

# 'result_df' now contains all the individual DataFrames combined into one
result_df.to_excel('boleta_completa.xlsx', index=False)

st.dataframe(result_df)

if st.button("Copy to Clipboard"):
    # Convert DataFrame to tab-separated string
    # Convert DataFrame to tab-separated string with "," as the thousands separator and pt-BR encoding
    result_df['Conta cliente'].fillna(0, inplace=True)
    result_df['Conta cliente'] = result_df['Conta cliente'].astype(int)
    result_df['Qtd.'] = result_df['Qtd.'].astype(int)
    result_df.loc[result_df['Conta cliente'] == 0, 'Conta cliente'] = ''




    df_str = result_df.to_csv(sep="\t", index=False, encoding="utf-8-sig")

    # Copy to clipboard
    pyperclip.copy(df_str)
    st.success("Boleta copiada com sucesso!")

with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    xlsx = result_df.to_excel(writer, sheet_name='Sheet1', index=False)

download2 = st.download_button(
        label="Download data as Excel",
        data=buffer,
        file_name=f'boleta_fundamentalista_{now}.xlsx',
        mime='application/vnd.ms-excel'
)
