import pandas as pd
import json
import os

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

def gerar_relatorio_receita():
    positivador = 'dir/positivador/positivador.xlsx'
    compromissadas = 'dir/compromissadas/compromissadas.xlsx'
    estruturadas = 'dir/estruturadas/estruturadas.xlsx'
    xpcs = 'dir/xpcs/xpcs.xlsx'
    xpvp = 'dir/xpvp/xpvp.xlsx'
    fundos = 'dir/fundos/fundos.xlsx'

    

    if positivador is not None:
        
        ##LIDANDO COM A PLANILHA DO POSITIVADOR
        data_positivador = load_data(positivador)
        # Assuming 'Data Posição' is a datetime column
        data_posicao_positivador = data_positivador['Data Posição'].iloc[0]

        # Group by 'Assessor' column and calculate the sum of 'Receita no Mês' column
        grouped_data_positivador = data_positivador.groupby('Assessor').sum().reset_index()
        grouped_data_positivador = grouped_data_positivador[['Assessor','Receita no Mês','Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos', 'Receita Aluguel']]
        
        # Create a pivot table with 'Assessor' as index, 'Tipo Pessoa' as columns, and the sum of 'Receita no Mês' as values
        pivot_table_positivador = data_positivador.pivot_table(values='Receita no Mês', index='Assessor', columns='Tipo Pessoa', aggfunc='sum', fill_value=0)

        # Rename the columns as per your requirement
        pivot_table_positivador.columns = ['Receita PF', 'Receita PJ']


        # Merge the grouped data and pivot table
        final_data_positivador = pd.merge(grouped_data_positivador, pivot_table_positivador, on='Assessor')



        ##LIDANDO COM A PLANILHA DAS COMPROMISSADAS

        data_compromissadas = load_data(compromissadas)

        # Drop the first character in the 'Código' column
        data_compromissadas['Código'] = data_compromissadas['Código'].str[1:]
        data_compromissadas = data_compromissadas.drop(data_compromissadas.tail(3).index)
        # Assuming data_estruturadas is your DataFrame
        


        ##LIDANDO COM OS DADOS DAS ESTRUTURADAS
        data_estruturadas = load_data(estruturadas)

        data_estruturadas['Cod A'] = data_estruturadas['Cod A'].str[1:]
        data_estruturadas = data_estruturadas.drop(data_estruturadas.tail(3).index)
        data_estruturadas = data_estruturadas[data_estruturadas['Status da Operação'] != 'Cancelado']
        data_estruturadas = data_estruturadas.groupby('Cod A')['Comissão'].sum().reset_index()
        

        ##LIDANDO COM OS DADOS DA XPCS

        data_xpcs = load_data(xpcs)
        data_xpcs['Código Assessor'] = data_xpcs['Código Assessor'].str[1:]
        data_xpcs = data_xpcs.groupby('Código Assessor')['Comissão Escritório'].sum().reset_index()

        ##LIDANDO COM OS DADOS DA XPVP

        data_xpvp = load_data(xpvp)
        data_xpvp['Código Assessor'] = data_xpvp['Código Assessor'].str[1:]
        data_xpvp = data_xpvp.groupby('Código Assessor')['Comissão Escritório'].sum().reset_index()

        ##LIDANDO COM OS DADOS DOS FUNDOS

        data_fundos = load_data(fundos)
        data_fundos = data_fundos[data_fundos['Categoria'] == 'Fundos de Investimento']
        data_fundos['Cód. Assessor Direto'] = data_fundos['Cód. Assessor Direto'].str[1:]
        data_fundos = data_fundos.groupby('Cód. Assessor Direto')['Comissão Bruta (R$) Escritório'].sum().reset_index()

        ##LIDANDO COM OS DADOS DOS FEE FIXOS

        data_fee = load_data(fundos)
        data_fee = data_fee[data_fee['Categoria'] == 'Fee Fixo']
        data_fee['Cód. Assessor Direto'] = data_fee['Cód. Assessor Direto'].str[1:]
        data_fee = data_fee.groupby('Cód. Assessor Direto')['Comissão Bruta (R$) Escritório'].sum().reset_index()


        ##JUNTANDO TUDO
            
        # Assuming that 'Código' in data_compromissadas and 'Assessor' in final_data_positivador are of the same type
        data_compromissadas['Código'] = data_compromissadas['Código'].astype(str)
        data_estruturadas['Cod A'] = data_estruturadas['Cod A'].astype(str)
        data_xpcs['Código Assessor'] = data_xpcs['Código Assessor'].astype(str)
        data_xpvp['Código Assessor'] = data_xpvp['Código Assessor'].astype(str)
        data_fundos['Cód. Assessor Direto'] = data_fundos['Cód. Assessor Direto'].astype(str)
        data_fee['Cód. Assessor Direto'] = data_fee['Cód. Assessor Direto'].astype(str)
        final_data_positivador['Assessor'] = final_data_positivador['Assessor'].astype(str)
        

        # Merge the dataframes
        final_data = pd.merge(final_data_positivador, data_compromissadas[['Código', 'Receita a Dividir']], left_on='Assessor', right_on='Código', how='left')
        final_data = final_data.drop(columns='Código')
        
        final_data = pd.merge(final_data, data_estruturadas[['Cod A', 'Comissão']], left_on = 'Assessor', right_on='Cod A', how='left')
        final_data = final_data.drop(columns='Cod A')
        
        final_data = pd.merge(final_data, data_xpcs[['Código Assessor', 'Comissão Escritório']], left_on = 'Assessor', right_on='Código Assessor', how='left')
        final_data = final_data.drop(columns='Código Assessor')
        
        final_data.rename(columns={'Receita a Dividir': 'Receita Compromissadas', 'Comissão':'Receita Estruturadas', 'Comissão Escritório': 'Comissão XPCS'}, inplace=True)
        
        final_data = pd.merge(final_data, data_xpvp[['Código Assessor', 'Comissão Escritório']], left_on = 'Assessor', right_on='Código Assessor', how='left')
        final_data = final_data.drop(columns='Código Assessor')

        final_data = pd.merge(final_data, data_fundos[['Cód. Assessor Direto', 'Comissão Bruta (R$) Escritório']], left_on = 'Assessor', right_on='Cód. Assessor Direto', how='left')
        final_data = final_data.drop(columns='Cód. Assessor Direto')
        
        final_data.rename(columns={'Comissão Escritório': 'Comissão XPVP', 'Comissão Bruta (R$) Escritório': 'Comissão Fundos'}, inplace=True)

        final_data = pd.merge(final_data, data_fee[['Cód. Assessor Direto', 'Comissão Bruta (R$) Escritório']], left_on = 'Assessor', right_on='Cód. Assessor Direto', how='left')
        final_data = final_data.drop(columns='Cód. Assessor Direto')
        final_data.rename(columns={'Comissão Bruta (R$) Escritório': 'Comissão Fee Fixo'}, inplace=True)

        final_data.set_index('Assessor', inplace=True)

        colunas_multiplicar_repasse_50 = ['Receita no Mês', 'Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita PF', 'Receita PJ', 'Receita Compromissadas']
        colunas_multiplicar_repasse_100 = ['Receita Estruturadas', 'Comissão XPCS', 'Comissão XPVP', 'Comissão Fundos', 'Comissão Fee Fixo']
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
        final_data_liq_esc[colunas_multiplicar_repasse_100] = final_data_liq_esc[colunas_multiplicar_repasse_100].apply(lambda x: x * multiplicador_imposto_xp * multiplicador_repasse_xp_100 * multiplicador_ir)
        final_data_liq_esc['Comissão Total Líquida'] = final_data_liq_esc[['Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas', 'Comissão XPCS', 'Comissão XPVP', 'Comissão Fundos', 'Comissão Fee Fixo']].sum(axis=1)



        final_data_liq[colunas_multiplicar_repasse_50] = final_data_liq[colunas_multiplicar_repasse_50].apply(lambda x: x * multiplicador_imposto_xp * multiplicador_repasse_xp_50 * multiplicador_ir * multiplicador_mesa)
        final_data_liq[colunas_multiplicar_repasse_100] = final_data_liq[colunas_multiplicar_repasse_100].apply(lambda x: x * multiplicador_imposto_xp * multiplicador_repasse_xp_100 * multiplicador_ir * multiplicador_mesa)
        final_data_liq['Comissão Total Líquida'] = final_data_liq[['Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas', 'Comissão XPCS', 'Comissão XPVP', 'Comissão Fundos', 'Comissão Fee Fixo']].sum(axis=1)
        final_data_liq = final_data_liq.apply(multiply_by_dict, args=(dict_repasse,), axis=1)

        final_data['Comissão Total Bruta'] = final_data[['Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas', 'Comissão XPCS', 'Comissão XPVP', 'Comissão Fundos', 'Comissão Fee Fixo']].sum(axis=1)

        final_data['Nome'] = final_data.index.map(dict_nomes)
        final_data_liq['Nome'] = final_data_liq.index.map(dict_nomes) 
        final_data_liq_esc['Nome'] = final_data_liq_esc.index.map(dict_nomes) 


        final_data_liq_esc = final_data_liq_esc[['Nome', 'Comissão Total Líquida', 'Receita no Mês', 'Receita PF', 'Receita PJ', 'Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas', 'Comissão XPCS', 'Comissão XPVP', 'Comissão Fundos', 'Comissão Fee Fixo']]
        final_data_liq = final_data_liq[['Nome', 'Comissão Total Líquida', 'Receita no Mês', 'Receita PF', 'Receita PJ', 'Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas', 'Comissão XPCS', 'Comissão XPVP', 'Comissão Fundos', 'Comissão Fee Fixo']]
        final_data = final_data[['Nome', 'Comissão Total Bruta', 'Receita no Mês', 'Receita PF', 'Receita PJ', 'Receita Bovespa', 'Receita Futuros', 'Receita RF Bancários', 'Receita RF Privados', 'Receita RF Públicos','Receita Aluguel', 'Receita Compromissadas', 'Receita Estruturadas', 'Comissão XPCS', 'Comissão XPVP', 'Comissão Fundos', 'Comissão Fee Fixo']]
        final_data_liq = final_data_liq.fillna(0)
        final_data = final_data.fillna(0)
        final_data_liq_esc = final_data_liq_esc.fillna(0)

        return final_data, final_data_liq,data_posicao_positivador, final_data_liq_esc

