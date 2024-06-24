import os
import pandas as pd
import streamlit as st
import json

with open('dict_nomes.json', 'r') as f:
    dict_nomes = json.load(f)


with open('dict_repasse.json', 'r') as w:
    dict_repasse = json.load(w)

assessor = st.query_params.get('assessor')

# Your directories
hist_dirs = {
    'positivador': 'dirhist/positivadorhist',
    'compromissadas': 'dirhist/compromissadashist',
    'estruturadas': 'dirhist/estruturadashist',
}

def gerar_historico_receita(df_positivador, df_compromissadas, df_estruturadas):
    # Define the directory path


    
        ##LIDANDO COM A PLANILHA DO POSITIVADOR
        data_positivador = df_positivador

        # Group by 'Assessor' column and calculate the sum of 'Receita no Mês' column
        grouped_data_positivador = data_positivador.groupby('Assessor').sum().reset_index()
        grouped_data_positivador = grouped_data_positivador[['Assessor','Receita no Mês','Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos', 'Receita Aluguel']]
        
        # Create a pivot table with 'Assessor' as index, 'Tipo Pessoa' as columns, and the sum of 'Receita no Mês' as values
        pivot_table_positivador = data_positivador.pivot_table(values='Receita no Mês', index='Assessor', columns='Tipo Pessoa', aggfunc='sum', fill_value=0)

        # Rename the columns as per your requirement
        pivot_table_positivador.columns = ['Receita PF', 'Receita PJ']


        # Merge the grouped data and pivot table
        final_data_positivador = pd.merge(grouped_data_positivador, pivot_table_positivador, on='Assessor')
        final_data_positivador['Assessor'] = final_data_positivador['Assessor'].astype(str)


    ##LIDANDO COM A PLANILHA DAS COMPROMISSADAS
    
            
        data_compromissadas = df_compromissadas

        # Drop the first character in the 'Código' column
        data_compromissadas['Código'] = data_compromissadas['Código'].str[1:]
        data_compromissadas = data_compromissadas.drop(data_compromissadas.tail(3).index)
        data_compromissadas['Código'] = data_compromissadas['Código'].astype(str)
        final_data = pd.merge(final_data_positivador, data_compromissadas[['Código', 'Receita a Dividir']], left_on='Assessor', right_on='Código', how='left')
        final_data = final_data.drop(columns='Código')
        # Assuming data_estruturadas is your DataFrame
    

    
        ##LIDANDO COM OS DADOS DAS ESTRUTURADAS
        data_estruturadas = df_estruturadas

        data_estruturadas['Cod A'] = data_estruturadas['Cod A'].str[1:]
        data_estruturadas = data_estruturadas.drop(data_estruturadas.tail(3).index)
        data_estruturadas = data_estruturadas[data_estruturadas['Status da Operação'] != 'Cancelado']
        data_estruturadas = data_estruturadas.groupby('Cod A')['Comissão'].sum().reset_index()
        data_estruturadas['Cod A'] = data_estruturadas['Cod A'].astype(str)
        final_data = pd.merge(final_data, data_estruturadas[['Cod A', 'Comissão']], left_on = 'Assessor', right_on='Cod A', how='left')
        final_data = final_data.drop(columns='Cod A')
        
        final_data.rename(columns={'Receita a Dividir': 'Receita Compromissadas', 'Comissão':'Receita Estruturadas'}, inplace=True)
        
        final_data.set_index('Assessor', inplace=True)




        colunas_multiplicar_repasse_50 = ['Receita no Mês', 'Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita PF', 'Receita PJ', 'Receita Compromissadas']
      
        final_data_liq = final_data.copy()
        final_data_liq_esc = final_data.copy()

        ##Visão Bruto XP
        multiplicador_imposto_xp = (1-0.05)
        ##Visão Bruto Escritório
        multiplicador_repasse_xp_50 = (1-0.5)
        multiplicador_repasse_xp_100 = 1
        multiplicador_ir = (1-0.2)
        ##Visão Liquido Escritório
        multiplicador_mesa = (1-0.1)
        
        final_data_liq_esc[colunas_multiplicar_repasse_50] = final_data_liq_esc[colunas_multiplicar_repasse_50].apply(lambda x: x * multiplicador_imposto_xp * multiplicador_repasse_xp_50 * multiplicador_ir)
        # final_data_liq_esc[colunas_multiplicar_repasse_100] = final_data_liq_esc[colunas_multiplicar_repasse_100].apply(lambda x: x * multiplicador_imposto_xp * multiplicador_repasse_xp_100 * multiplicador_ir)
        final_data_liq_esc['Comissão Total Líquida'] = final_data_liq_esc[['Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas']].sum(axis=1)

        
        final_data_liq[colunas_multiplicar_repasse_50] = final_data_liq[colunas_multiplicar_repasse_50].apply(lambda x: x * multiplicador_imposto_xp * multiplicador_repasse_xp_50 * multiplicador_ir* multiplicador_mesa)
        
        final_data_liq['Comissão Total Líquida'] = final_data_liq[['Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas']].sum(axis=1)
        final_data['Comissão Total Bruta'] = final_data[['Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas']].sum(axis=1)

        final_data['Nome'] = final_data.index.map(dict_nomes)
        final_data_liq['Nome'] = final_data_liq.index.map(dict_nomes) 

        final_data_liq = final_data_liq[['Nome', 'Comissão Total Líquida', 'Receita no Mês', 'Receita PF', 'Receita PJ', 'Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas']]
        final_data = final_data[['Nome', 'Comissão Total Bruta', 'Receita no Mês', 'Receita PF', 'Receita PJ', 'Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas']]
        final_data_liq = final_data_liq.fillna(0)
        final_data = final_data.fillna(0)

        return final_data, final_data_liq


# Function to get all YYYYMM directories in a given path
def get_directories(path):
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]

# Function to get all YYYYMMDD files in a given path
def get_files(path):
    return [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]


def gerar_historico_receita_assessor(dir_date_choice, assessor):
    # Initialize an empty DataFrame for the specific person
    hist_dirs = {
    'positivador': 'dirhist/positivadorhist',
    'compromissadas': 'dirhist/compromissadashist',
    'estruturadas': 'dirhist/estruturadashist',
}
    final_data_person = pd.DataFrame()
    final_data_person_liq = pd.DataFrame()
    if assessor is None:
        st.write('Nenhum Assessor Selecionado')

    else:
        # Initialize DataFrames for each directory
        df_positivador = df_compromissadas = df_estruturadas = None

        # Loop over all the directories
        for dir_choice in hist_dirs.keys():
            # Get the files in the selected directory and date
            files = get_files(os.path.join(hist_dirs[dir_choice], dir_date_choice))

            # Loop over all the files
            for file in files:
                # Read the file into a pandas DataFrame
                df = pd.read_excel(os.path.join(hist_dirs[dir_choice], dir_date_choice, file))

                # Assign the DataFrame to the corresponding variable
                if dir_choice == 'positivador':
                    df_positivador = df
                elif dir_choice == 'compromissadas':
                    df_compromissadas = df
                elif dir_choice == 'estruturadas':
                    df_estruturadas = df

                # Ensure all DataFrames are not None before calling the function
                if df_positivador is not None and df_compromissadas is not None and df_estruturadas is not None:
                    # Generate historical revenue data
                    temp_final_data, temp_final_data_liq = gerar_historico_receita(df_positivador, df_compromissadas, df_estruturadas)
                    # Check if the person with the code 22579 exists in the temp_final_data
                    if assessor in temp_final_data.index:
                        # Transpose the DataFrame and set the index as the filename
                        temp_final_data = temp_final_data.loc[assessor].transpose().to_frame().T
                        # Remove '.xlsx' from the filename and convert it to a date
                        file_date = pd.to_datetime(file.replace('.xlsx', ''), format='%Y%m%d')
                        temp_final_data.index = [file_date]
                        # Append the data of the person to the final_data_person DataFrame
                        final_data_person = pd.concat([final_data_person, temp_final_data])

                    if assessor in temp_final_data_liq.index:
                        # Transpose the DataFrame and set the index as the filename
                        temp_final_data_liq = temp_final_data_liq.loc[assessor].transpose().to_frame().T
                        # Remove '.xlsx' from the filename and convert it to a date
                        file_date = pd.to_datetime(file.replace('.xlsx', ''), format='%Y%m%d')
                        temp_final_data_liq.index = [file_date]
                        # Append the data of the person to the final_data_person DataFrame
                        final_data_person_liq = pd.concat([final_data_person_liq, temp_final_data_liq])

                    nome = final_data_person['Nome'].iloc[0]
                    

        final_data_person = final_data_person.drop(columns=['Nome'])
        final_data_person_liq = final_data_person_liq.drop(columns=['Nome'])

        return final_data_person, final_data_person_liq




