import streamlit as st
import os
import shutil
from datetime import datetime

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

def save_file_to_hist(uploadedfile, upload_dir, new_name, date):
    # Format the date in 'YYYYMM' format
    date_str = date.strftime("%Y%m")
    # Create the new directory path
    new_dir_path = os.path.join(upload_dir, date_str)
    # Create the directory if it doesn't exist
    os.makedirs(new_dir_path, exist_ok=True)
    # Save the file with the new name
    with open(os.path.join(new_dir_path, new_name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to {}".format(new_name, new_dir_path))




# Define your directories
upload_dirs = {
    'positivador': 'dir/positivador',
    'compromissadas': 'dir/compromissadas',
    'estruturadas': 'dir/estruturadas',
    'captacao': 'dir/captacao',
    'xpcs': 'dir/xpcs',
    'xpvp': 'dir/xpvp',
    'fundos': 'dir/fundos'
}

hist_dirs = {
    'positivador': 'dirhist/positivadorhist',
    'compromissadas': 'dirhist/compromissadashist',
    'estruturadas': 'dirhist/estruturadashist',
    'captacao': 'dirhist/captacaohist',
    'xpcs': 'dirhist/xpcshist',
    'xpvp': 'dirhist/xpvphist',
    'fundos': 'dirhist/fundoshist'
}

# Add a date selector
selected_date = st.date_input("Select a date", datetime.now())
selected_date_str = selected_date.strftime("%Y%m%d")

# Check if the selected date is today
is_today = selected_date == datetime.now().date()
st.caption('Para atualizar os dashboards atuais, deixar marcado. Para atualizar os dashboards históricos, deixar desmarcado.')
update_dir = st.checkbox("Atualizar Dashboard", value=True)

# Then in your loop where you call save_file_to_hist, pass the selected_date as an argument
for key in upload_dirs.keys():
    file = st.file_uploader(f"Upload {key.upper()}", type=['xlsx'])
    if file is not None:
        # If the selected date is today, save to both directories
        if update_dir:
            save_uploadedfile(file, upload_dirs[key], f'{key}.xlsx')
            
        # If the selected date is not today, save only to the hist directory
        else:
            save_file_to_hist(file, hist_dirs[key], f'{selected_date_str}.xlsx', selected_date)

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


