import streamlit as st
import pandas as pd
from relatorio_receita import gerar_relatorio_receita
from relatorio_historico_receita import gerar_historico_receita_assessor, get_directories, get_files
from relatorio_captacao_ativacao import gerar_relatorio_captacao, gerar_relatorio_evasao
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Assessor Ceres Capital', page_icon=':rocket:' , layout="wide", initial_sidebar_state='auto', menu_items=None)

comissao = st.empty()
captacao_container = st.empty()

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
    final_data, final_data_liq, data_posicao_positivador = gerar_relatorio_receita()
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
            st.caption('Bovespa, RF, Estruturadas e Compromissadas são estimativas com base nos dados do positivador e HUB. Dados de XPCS, XPVP, Fundos e Fee Fixo são baseados no mês anterior')
            st.table(final_data_liq)

        # Create a dropdown menu for the YYYYMM directories
        with col2_comissao:
            st.title(f'Evolução da receita')
            # Get the directories in the selected directory
            dirs = get_directories(hist_dirs['positivador'])  # Assuming all directories have the same dates
            data = st.selectbox('Select a date', dirs, index =len(dirs)-1)
            final_data_person, final_data_person_liq = gerar_historico_receita_assessor(data, assessor)
            

            # Create a Plotly figure

            fig_ev_rec = px.line(final_data_person_liq, x=final_data_person_liq.index, y='Comissão Total Líquida', title='Evolução da Comissão Líquida')

            # Display the figure with streamlit
            st.plotly_chart(fig_ev_rec)
            
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
        assessor = int(assessor)
        captacao, capt_data, capt_ass, data_posicao_captacao= gerar_relatorio_captacao(assessor)
        with st.popover('Tabela Captação'):
            st.table(captacao)
        
                # Assuming 'captacao' is your DataFrame
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

        st.table(ativacao)