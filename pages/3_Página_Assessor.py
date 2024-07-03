import streamlit as st
import pandas as pd
from relatorio_receita import gerar_relatorio_receita
from relatorio_historico_receita import gerar_historico_receita_assessor, get_directories, get_files
from relatorio_captacao_ativacao import gerar_relatorio_captacao, gerar_relatorio_evasao, gerar_tabela_evasao
import plotly.express as px
import plotly.graph_objects as go
from relatorio_comissoes import gerar_historico_comissao
import datetime

st.set_page_config(page_title='Assessor Ceres Capital', page_icon=':rocket:' , layout="wide", initial_sidebar_state='auto', menu_items=None)

selecao_de_datas = st.empty()
comissao = st.empty()
captacao_container = st.empty()
comissoes_historico = st.empty()
assessor = st.query_params.get('assessor')
# Your directories
hist_dirs = {
    'positivador': 'dirhist/positivadorhist',
    'compromissadas': 'dirhist/compromissadashist',
    'estruturadas': 'dirhist/estruturadashist',
}

if assessor is None:
    st.title('Nenhum assessor selecionado.')

else:

    ##Importando e lidando com dados apenas se o assessor estiver selecionado

    with selecao_de_datas.container():    
        ##FAZENDO A SELEÇÃO DE DATAS FUNCIONAR

        filtro_de_data = None
        caminho_positivador = 'dir/positivador/positivador.xlsx'
        positivador_antigo = pd.read_excel(caminho_positivador)
        lista_data_posicao = positivador_antigo['Data Posição'].unique().tolist()
        index_lista = len(lista_data_posicao) - 1

        filtro_de_data = st.selectbox('Data do Positivador', lista_data_posicao, index = index_lista)

        final_data, final_data_liq, data_posicao_positivador, final_data_liq_esc = gerar_relatorio_receita(filtro_de_data)
        data_posicao_positivador = filtro_de_data
        ####

    final_data = final_data.loc[assessor]
    ativacao_rf = final_data['Receita RF Bancários'] + final_data['Receita RF Privados'] + final_data['Receita RF Públicos']
    ativacao_rv = final_data['Receita Bovespa'] + final_data['Receita Futuros'] + final_data['Receita Aluguel'] + final_data['Receita Estruturadas']
    final_data_liq = final_data_liq.round(2)
    final_data_liq = final_data_liq.drop(columns=['Receita no Mês', 'Receita PF', 'Receita PJ'])
    final_data_liq = final_data_liq.loc[assessor]
    with comissao.container():
        col1_comissao, col2_comissao = st.columns(2)
    
   
        with col1_comissao:
            st.title(f'Simulador de Comissão - {assessor}')
            st.subheader('Comissão Líquida')
            st.caption(f'Data de Atualização: {data_posicao_positivador}')
            st.caption('Bovespa, RF, Estruturadas e Compromissadas são estimativas com base nos dados do positivador e HUB. Dados de XPCS, XPVP, Fundos e Fee Fixo são baseados no mês anterior')
            st.table(final_data_liq)

        # Create a dropdown menu for the YYYYMM directories
        with col2_comissao:
            
            st.title(f'Indicadores de ativação')
            # # Get the directories in the selected directory
            # dirs = get_directories(hist_dirs['positivador'])  # Assuming all directories have the same dates
            # data = st.selectbox('Select a date', dirs, index =len(dirs)-1)
            # final_data_person, final_data_person_liq = gerar_historico_receita_assessor(data, assessor)
            # st.table(final_data_person)
            # st.table(final_data_person_liq)
            # # Create a Plotly figure

            # fig_ev_rec = px.line(final_data_person_liq, x=final_data_person_liq.index, y='Comissão Total Líquida', title='Evolução da Comissão Líquida')

            # # Display the figure with streamlit
            # st.plotly_chart(fig_ev_rec)
            ativacao_rf = ativacao_rf.round(0)
            ativacao_rv = ativacao_rv.round(0)
            st.caption('Meta para Ativação em Renda Fixa: Receita Bruta acima de R$4.500')
            if ativacao_rf > 4500:
                st.success('Ativo em Renda Fixa (Receita Bruta Acima de R$4.500)')
            else:
                st.error(f'Inativo em Renda Fixa, faltam R${(4500 - ativacao_rf).round(2)} em receita bruta para ativação.')

            st.caption('Meta para Ativação em Renda Variável: Receita Variável acima de R$6.500')
            if ativacao_rv > 6500:
                st.success('Ativo em Renda Variável')
            else:
                st.error(f'Inativo em Renda Variável, faltam R${6500 - ativacao_rv} em receita bruta para ativação.')

    

    
with captacao_container.container():
    st.header('Captação')
    assessor = int(assessor)  # Assuming 'assessor' is already defined

    captacao = None  # Initialize captacao as None
    capt_data = None
    capt_ass = None
    data_posicao_captacao = None

    try:
        captacao, capt_data, capt_ass, data_posicao_captacao = gerar_relatorio_captacao(assessor)
    except (TypeError, ValueError, NameError, KeyError):  # Handle potential errors from 'gerar_relatorio_captacao'
        st.error(f"Erro ao gerar relatório de captação para o assessor {assessor}.")

    # Now, check if 'captacao' is a valid DataFrame
    if captacao is not None and isinstance(captacao, pd.DataFrame):
        with st.popover('Tabela Captação'):
            st.table(captacao)

        # Reset the index to make 'datetime' a column
        captacao.reset_index(level=0, inplace=True)

        # Calculate the cumulative sum of 'Captação'
        sum_captacao = captacao['Captação'].sum()
        pf_sum = captacao['PF'].sum()
        pj_sum = captacao['PJ'].sum()

        captacao['Captação_cumsum'] = captacao['Captação'].cumsum()

        # Create a plotly graph
        fig_cap = go.Figure()

        # Add line for 'Captação_cumsum'
        fig_cap.add_trace(go.Scatter(x=captacao.index, y=captacao['Captação_cumsum'], mode='lines', name='Captação'))

        # Add bar for 'PF'
        fig_cap.add_trace(go.Bar(x=captacao.index, y=captacao['PF'], name='PF'))

        # Add bar for 'PJ'
        fig_cap.add_trace(go.Bar(x=captacao.index, y=captacao['PJ'], name='PJ'))

        # Update layout for stacked bar chart
        fig_cap.update_layout(
            title=f'''Captação Líquida/Mês: {sum_captacao:,} 
            Captação PF/Mês: {pf_sum:,} 
            Captação PJ/Mês: {pj_sum:,}''', barmode='stack'
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig_cap, use_container_width=True)

        st.subheader('Ativação e Evasão')
        ativacao = gerar_relatorio_evasao(assessor)
        data_ativacao_bruta = gerar_tabela_evasao(assessor)
        with st.popover('Detalhes'):
            st.dataframe(data_ativacao_bruta)
        st.table(ativacao)

    else:
        st.warning(f"O relatório de captação para o assessor {assessor} não contém as colunas 'PF' e 'PJ' ou não foi gerado corretamente.")




    with comissoes_historico.container():
        assessor = str(assessor)
        comissoes = None
        comissoes_agrupadas_assessor = None
        st.header('Histórico de Relatório de Comissões')

        try:
            comissoes, comissoes_agrupadas_assessor = gerar_historico_comissao()
            comissoes = comissoes.loc[assessor]
            comissoes_agrupadas_assessor = comissoes_agrupadas_assessor.xs(assessor, level=1)

        

            
            if comissoes is not None and isinstance(comissoes, pd.DataFrame):
            
                comissoes['Líquido Escritório'] = comissoes['Comissão Escritório Líquida'] - comissoes['Comissão Assessor'] 
                
                comissoes_por_produto = comissoes.groupby(['Date', 'Categoria']).sum().reset_index()

                
                comissao_por_data = comissoes.groupby('Date').sum().reset_index()
                comissao_por_data = comissao_por_data.drop('Categoria', axis = 1)
                comissoes_agrupadas_assessor['Líquido Escritório'] = comissoes_agrupadas_assessor['Comissão Escritório Líquida'] - comissoes_agrupadas_assessor['Comissão Assessor'] 

                # Convert 'Date' to string
                comissao_por_data['Date'] = comissao_por_data['Date'].astype(str)

                # Convert 'Date' to datetime
                comissao_por_data['Date'] = pd.to_datetime(comissao_por_data['Date'], format='%Y%m')

                with st.expander('Tabelas Comissões'):
                    col1_exp_comissoes, col2_exp_comissoes = st.columns(2)
                    with col1_exp_comissoes:
                        st.dataframe(comissao_por_data, hide_index = True)
                    with col2_exp_comissoes:
                        unique_dates_comissao_agrupadas = comissoes_agrupadas_assessor.index.get_level_values(0).unique()

                        # Create a selectbox
                        selected_date = st.selectbox('Select a date', unique_dates_comissao_agrupadas)

                        # Filter the DataFrame
                        filtered_df_comissoes_agrupadas_assessor = comissoes_agrupadas_assessor.loc[selected_date]

                        # Display the filtered DataFrame
                        st.dataframe(filtered_df_comissoes_agrupadas_assessor)
                    
                
                    
                # Create a figure
                fig_comissao_mes= go.Figure()

                # Add bar chart for 'PF' and 'PJ'
                fig_comissao_mes.add_trace(go.Bar(x=comissao_por_data['Date'], y=comissao_por_data['Comissão Escritório'], name='Bruto XP'))
                fig_comissao_mes.add_trace(go.Bar(x=comissao_por_data['Date'], y=comissao_por_data['Comissão Escritório Líquida'], name='Bruto Escritório'))
                fig_comissao_mes.add_trace(go.Bar(x=comissao_por_data['Date'], y=comissao_por_data['Comissão Assessor'], name='Líquido Assessor'))
                fig_comissao_mes.add_trace(go.Bar(x=comissao_por_data['Date'], y=comissao_por_data['Líquido Escritório'], name='Líquido Escritório'))
                # Add line chart for 'Captação'
                # Get the data of the trace

                # Update layout
                fig_comissao_mes.update_layout(
                    title=f'''Comissão
                    ''',
                    xaxis=dict(
                    tickformat="%m/%Y"
                    ),
                )

                # Display the plot in Streamlit
                st.plotly_chart(fig_comissao_mes, use_container_width=True)

                st.subheader('Comissão por Produto')
                
                unique_dates_comissao_produto = comissoes_por_produto['Date'].unique()
                unique_dates_number = len(unique_dates_comissao_produto) - 1

                    # Create a selectbox
                selected_date_produto = st.selectbox('Selecione a Data', unique_dates_comissao_produto, index = unique_dates_number)
                col1_comissao_produto, col2_comissao_produto = st.columns(2)
                with col1_comissao_produto:

                    # Filter the DataFrame
                    filtered_df_comissoes_produto = comissoes_por_produto[comissoes_por_produto['Date'] == selected_date_produto]

                    # Display the filtered DataFrame
                    st.dataframe(filtered_df_comissoes_produto, hide_index = True)
                    # Calculate the total sum for each column
                    st.caption('Soma das Comissões no mês')
                    total_sum = filtered_df_comissoes_produto.sum()
                    
                    total_sum = total_sum.drop(['Date', 'Categoria'])
                    
                    # Display the total sum for each column
                    st.dataframe(total_sum)

                with col2_comissao_produto:
                    percentage_df = filtered_df_comissoes_produto.copy()

                    # Loop through each column in the DataFrame
                    for column in percentage_df.columns:
                        # Skip the 'Date' and 'Categoria' columns
                        if column not in ['Date', 'Categoria']:
                            # Calculate the total sum of the column
                            total_sum = percentage_df[column].sum()
                            # Calculate the percentage for each value in the column
                            percentage_df[column] = percentage_df[column].apply(lambda x: '{:.2f}%'.format((x / total_sum) * 100))

                    # Display the new DataFrame
                    st.dataframe(percentage_df, hide_index = True)
            else:
                st.warning(f"O relatório de comissões passadas para o assessor {assessor} apresentou erros")   

        except (TypeError, ValueError, NameError, KeyError):  # Handle potential errors from 'gerar_relatorio_captacao'
            st.error(f"Erro ao gerar relatório de comissão para o assessor {assessor}.")