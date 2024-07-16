import streamlit as st
import os
import shutil
from datetime import datetime
import pandas as pd

def save_uploadedfile(uploadedfile, upload_dir, new_name):
    # Check if the directory already exists
    if os.path.exists(upload_dir):
        # If it does, delaete it
        shutil.rmtree(upload_dir)
    # Create the directory
    os.makedirs(upload_dir)
    # Save the file with the new name
    with open(os.path.join(upload_dir, new_name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to {}".format(new_name, upload_dir))


###DEPRECATED
# def save_file_to_hist(uploadedfile, upload_dir, new_name, date):
#     # Format the date in 'YYYYMM' format
#     date_str = date.strftime("%Y%m")
#     # Create the new directory path
#     new_dir_path = os.path.join(upload_dir, date_str)
#     # Create the directory if it doesn't exist
#     os.makedirs(new_dir_path, exist_ok=True)
#     # Save the file with the new name
#     with open(os.path.join(new_dir_path, new_name), "wb") as f:
#         f.write(uploadedfile.getbuffer())
#     return st.success("Saved File:{} to {}".format(new_name, new_dir_path))

# hist_dirs = {
#     'positivador': 'dirhist/positivadorhist',
#     'compromissadas': 'dirhist/compromissadashist',
#     'estruturadas': 'dirhist/estruturadashist',
#     'captacao': 'dirhist/captacaohist',
#     'xpcs': 'dirhist/xpcshist',
#     'xpvp': 'dirhist/xpvphist',
#     'fundos': 'dirhist/fundoshist'
# }



# Define your directories
upload_dirs = {
    #'positivador': 'dir/positivador',
    # 'compromissadas': 'dir/compromissadas',
    # 'estruturadas': 'dir/estruturadas',
    'captacao': 'dir/captacao',
    'xpcs': 'dir/xpcs',
    'xpvp': 'dir/xpvp',
    'fundos': 'dir/fundos'
}

col1, col2 = st.columns(2)

with col1:
    ###upload e check do positivador
    positivador = st.file_uploader(f'Upload Arquivo Positivador')
    caminho_positivador = 'dir/positivador/positivador.xlsx'
    caminho_compromissadas = 'dir/compromissadas/compromissadas.xlsx'
    caminho_estruturadas = 'dir/estruturadas/estruturadas.xlsx'

    
    def load_compromissadas(caminho):
        return pd.read_excel(caminho)
    
    positivador_antigo = load_compromissadas(caminho_positivador)
    
    if positivador is not None:
        positivador = pd.read_excel(positivador)
        check_data = set(positivador['Data Posição']) - set(positivador_antigo['Data Posição'])
        if check_data:
            positivador_concat = pd.concat([positivador_antigo, positivador], axis=0)
            
            compromissadas = st.file_uploader(f'Upload Arquivos Compromissadas')
            
            
            

            compromissadas_antigo = load_compromissadas(caminho_compromissadas)

            if compromissadas is not None:

                compromissadas = pd.read_excel(compromissadas)
                check_data = str(check_data)
                check_data = check_data.replace("{'", "").replace("'}", "")
                compromissadas['Data Posição'] = None
                compromissadas['Data Posição'] = compromissadas['Data Posição'].fillna(check_data)
                compromissadas['Código'] = compromissadas['Código'].str[1:]
                compromissadas = compromissadas.drop(compromissadas.tail(3).index)

                compromissadas_concat = pd.concat([compromissadas_antigo, compromissadas])


                estruturadas = st.file_uploader(f'Upload Arquivos Estruturadas')
                
                estruturadas_antigo = load_compromissadas(caminho_estruturadas)

                if estruturadas is not None:
                    
                    estruturadas = pd.read_excel(estruturadas)
                    estruturadas['Data Posição'] = None
                    estruturadas['Data Posição'] = estruturadas['Data Posição'].fillna(check_data)
                    estruturadas['Cod A'] = estruturadas['Cod A'].str[1:]
                    estruturadas = estruturadas.drop(estruturadas.tail(3).index)
                    estruturadas = estruturadas[
                                                (estruturadas['Status da Operação'] == 'Totalmente executado') | 
                                                (estruturadas['Status da Operação'] == 'Parcialmente executado')
                                            ]

                    
                
                    estruturadas_concat = pd.concat([estruturadas_antigo, estruturadas])
                    
                
                    ###salvar os arquivos
                    if st.button("Processar Dados"):

                        positivador_concat.to_excel(caminho_positivador, index=False)
                        st.success(f'Atualizou arquivo para {check_data} no positivador')
                        compromissadas_concat.to_excel(caminho_compromissadas, index=False)
                        st.success(f'Atualizou arquivo para {check_data} nas compromissadas')
                        estruturadas_concat.to_excel(caminho_estruturadas, index=False)
                        st.success(f'Atualizou arquivo para {check_data} nas estruturadas')
    
        else:
            st.info('Positivador já atualizado')

    with st.expander('Deletar Data Específica - Usar caso precise refazer o upload'):
    
        
        positivador_deletar = pd.read_excel(caminho_positivador)
        compromissadas_deletar = pd.read_excel(caminho_compromissadas)
        estruturadas_deletar = pd.read_excel(caminho_estruturadas)

        unique_dates = positivador_deletar['Data Posição'].unique()

        # Create a selector for unique dates
        
        date_delete = st.selectbox('Select a date to delete:', unique_dates, index = None)
        
        if st.button('Deletar data'):
            positivador_deletar = positivador_deletar[positivador_deletar['Data Posição'] != date_delete]
            
            positivador_deletar.to_excel(caminho_positivador, index=False)

            compromissadas_deletar = compromissadas_deletar[compromissadas_deletar['Data Posição'] != date_delete]
        
            compromissadas_deletar.to_excel(caminho_compromissadas, index=False)
            
            estruturadas_deletar = estruturadas_deletar[estruturadas_deletar['Data Posição'] != date_delete]

            estruturadas_deletar.to_excel(caminho_estruturadas, index=False)

            st.success('Data Deletada!')


with col2:
    # Then in your loop where you call save_file_to_hist, pass the selected_date as an argument
    for key in upload_dirs.keys():
        file = st.file_uploader(f"Upload {key.upper()}", type=['xlsx'])
        if file is not None:
            save_uploadedfile(file, upload_dirs[key], f'{key}.xlsx')
            



# if positivador is not None:
#     save_uploadedfile(positivador, 'dir/positivador', 'positivador.xlsx')




st.divider()

st.header('Arquivos Asset Allocation')

data_assetallocation = st.file_uploader(f'Upload Arquivo "Data"')
if data_assetallocation is not None:
    save_uploadedfile(data_assetallocation, 'assetallocation/data', 'data.xlsx')

ativos_assetallocation = st.file_uploader(f'Upload Arquivo "Ativos"')
if ativos_assetallocation is not None:
    save_uploadedfile(ativos_assetallocation, 'assetallocation/ativos', 'ativos.xlsx')


st.divider()

st.header('Arquivos Histórico de Comissões Realizadas')
data_comissao = st.selectbox('Mês', ['202401','202402','202403','202404', '202405', '202406'], placeholder='Selecione um mês para upload')

gerencial_comissoes = st.file_uploader(f'Upload Arquivo "Gerencial"')
if gerencial_comissoes is not None:
    save_uploadedfile(gerencial_comissoes, f'historicocomissoes/{data_comissao}/gerencial', 'gerencial.xlsx')

cambio_comissoes = st.file_uploader(f'Upload Arquivo "Cambio"')
if cambio_comissoes is not None:
    save_uploadedfile(cambio_comissoes, f'historicocomissoes/{data_comissao}/cambio', 'cambio.xlsx')

credito_comissoes = st.file_uploader(f'Upload Arquivo "credito"')
if credito_comissoes is not None:
    save_uploadedfile(credito_comissoes, f'historicocomissoes/{data_comissao}/credito', 'credito.xlsx')

xpcs_comissoes = st.file_uploader(f'Upload Arquivo "xpcs"')
if xpcs_comissoes is not None:
    save_uploadedfile(xpcs_comissoes, f'historicocomissoes/{data_comissao}/xpcs', 'xpcs.xlsx')
    
xpvp_comissoes = st.file_uploader(f'Upload Arquivo "xpvp"')
if xpvp_comissoes is not None:
    save_uploadedfile(xpvp_comissoes, f'historicocomissoes/{data_comissao}/xpvp', 'xpvp.xlsx')


