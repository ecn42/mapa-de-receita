import streamlit as st
from relatorio_receita import gerar_relatorio_receita
from relatorio_captacao_ativacao import gerar_relatorio_captacao, gerar_relatorio_evasao, gerar_tabela_evasao
import plotly.express as px
import plotly.graph_objects as go
import json
from relatorio_comissoes import gerar_historico_comissao
import pandas as pd

with open('dict_nomes.json', 'r') as f:
    dict_nomes = json.load(f)
list_of_names = sorted(dict_nomes.values())
reverse_dict = {v: k for k, v in dict_nomes.items()}

##Configuração da página
st.set_page_config(page_title='Dashboard Ceres Capital', page_icon=':corn:' , layout="wide", initial_sidebar_state="auto", menu_items=None)

##Importando os dados com Funções:

final_data, final_data_liq, data_posicao_positivador, final_data_liq_esc = gerar_relatorio_receita()
final_data_total = final_data.drop(columns=['Nome']).sum().round(0)
final_data_liq_total = final_data_liq.drop(columns=['Nome']).sum().round(0)
final_data_liq_esc_total = final_data_liq_esc.drop(columns=['Nome']).sum().round(0)
assessor = None
captacao, captacao_data, captacao_assessor, data_posicao_captacao = gerar_relatorio_captacao(assessor)
evasao = gerar_relatorio_evasao(assessor)
comissoes, comissoes_agrupadas_assessor = gerar_historico_comissao()
##Layout da página
st.title('Dashboard Ceres Capital')

col1_menu, col2_menu = st.columns(2)
with col1_menu:
    menu = st.selectbox('Navegar para:', ['Upload', 'Asset Allocation'], index = None)
    if menu == 'Upload':
        st.switch_page('pages/2_Upload_Arquivos.py')
    if menu == 'Asset Allocation':
        st.switch_page('pages/4_Carteira.py')

with col2_menu:
    selecao_assessor = st.selectbox('Ir para Página de Assessor:', list_of_names, index = None)
    
    if selecao_assessor is not None:
        codigo_assessor_selecionado = reverse_dict[selecao_assessor]
        st.page_link(f'https://mapa-de-receita-5h2jcogpdq-uc.a.run.app/P%C3%A1gina_Assessor?assessor={codigo_assessor_selecionado}', label= 'Ir para Assessor selecionado')


st.write(f'Data de Atualização do Positivador: {data_posicao_positivador}')
st.subheader('Receita Bruta XP')
visao_receita_bruta = st.empty()

st.subheader('Receita Líquida Escritório')
visao_receita_liquida_escritório = st.empty()

st.subheader('Receita Líquida Assessor')
visao_receita_liquida = st.empty()

st.subheader('Captação')
st.write(f'Data de Atualização das Captações: {data_posicao_captacao}')
visao_captacao = st.empty()

projecoes_mes = st.empty()

st.divider()

comissoes_historico = st.empty()

with visao_receita_bruta.container():
    
    with st.expander('Tabelas'):
        
        col_bruta_1, col_bruta_2 = st.columns(2)
        
        with col_bruta_1:

            st.dataframe(final_data)
        
        with col_bruta_2:

            st.dataframe(final_data_total)
    sum_bruto_xp = final_data['Comissão Total Bruta'].sum().round(0)

    fig_bruto_xp = px.bar(final_data, title=f'Receita Bruta XP: {sum_bruto_xp:,}',  x='Nome', y='Comissão Total Bruta')

    st.plotly_chart(fig_bruto_xp, use_container_width = True)

with visao_receita_liquida.container():
    
    
    with st.expander('Tabelas'):
        
        col_liq_1, col_liq_2 = st.columns(2)

        with col_liq_1:
            st.dataframe(final_data_liq)
        
        with col_liq_2:
            st.dataframe(final_data_liq_total)
    
   # final_data_liq *=2
    sum_liq = final_data_liq['Comissão Total Líquida'].sum().round(0)
    
    fig_liq = px.bar(final_data_liq, title=f'Receita Liq XP: {sum_liq:,}', x='Nome', y='Comissão Total Líquida')

    st.plotly_chart(fig_liq, use_container_width = True)

with visao_captacao.container():
    
    with st.expander('Tabelas'):

        col_cap_1, col_cap_2 = st.columns(2)
        col_cap_3, col_cap_4 = st.columns(2)

    with col_cap_1:
        st.caption('Captação Total por Assessor/Dia')
        st.dataframe(captacao)
    
    with col_cap_2:
        st.caption('Captação Total Escritório/Dia')
        st.dataframe(captacao_data)
    
    with col_cap_3:
        st.caption('Captação Total por Assessor')
        st.dataframe(captacao_assessor)
    
    with col_cap_4:
        st.caption('Ativação/Evasão Total por Assessor')
        st.dataframe(evasao)


    

    # Assuming 'captacao_assessor' is your DataFrame
    
   # Calculate the sum of 'Captação'
    sum_captacao = captacao_data['Captação'].sum()
    captacao_data['Captação_cumsum'] = captacao_data['Captação'].cumsum()
    pf_sum = captacao_data['PF'].sum()
    pj_sum = captacao_data['PJ'].sum()
    
    # Create a figure
    fig_cap_total = go.Figure()

    # Add bar chart for 'PF' and 'PJ'
    fig_cap_total.add_trace(go.Bar(x=captacao_data.index, y=captacao_data['PF'], name='PF'))
    fig_cap_total.add_trace(go.Bar(x=captacao_data.index, y=captacao_data['PJ'], name='PJ'))

    # Add line chart for 'Captação'
    fig_cap_total.add_trace(go.Scatter(x=captacao_data.index, y=captacao_data['Captação_cumsum'], name='Captação'))

    # Update layout
    fig_cap_total.update_layout(
        title=f'''Captação Líquida/Mês: {sum_captacao:,} 
        Captação PF/Mês: {pf_sum:,} 
        Captação PJ/Mês: {pj_sum:,}''',  # set title as the sum of 'Captação'
        barmode='stack',  # for stacked bar chart
        yaxis=dict(
            title='Captação',
        )
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig_cap_total, use_container_width=True)




    # Format the numbers in the DataFrame to have a thousands separator
    captacao_assessor = captacao_assessor.applymap(lambda x: '{:,.0f}'.format(x) if isinstance(x, (int, float)) else x)

    fig_cap_assessor = go.Figure(data=[
        go.Bar(name='PF', x=captacao_assessor['Nome'], y=captacao_assessor['PF']),
        go.Bar(name='PJ', x=captacao_assessor['Nome'], y=captacao_assessor['PJ'])
    ])

    # Change the bar mode
    fig_cap_assessor.update_layout(barmode='stack')

    # Add text
    fig_cap_assessor.update_traces(text=captacao_assessor['Captação'], textposition='outside')

    st.plotly_chart(fig_cap_assessor, use_container_width = True)


with visao_receita_liquida_escritório.container():

    

    with st.expander('Tabelas'):
        
        col_liq_esc_1, col_liq_esc_2 = st.columns(2)

        with col_liq_esc_1:
            
            st.dataframe(final_data_liq_esc)
        
        with col_liq_esc_2:
            st.dataframe(final_data_liq_esc_total)
    
   # final_data_liq *=2
   # Assuming 'final_data_liq' is your DataFrame
    

    sum_liq_esc = final_data_liq_esc['Comissão Total Líquida'].sum().round(0)
    
    fig_liq_esc = px.bar(final_data_liq_esc, title=f'Receita Liq Escritório: {sum_liq_esc:,}', x='Nome', y='Comissão Total Líquida')

    st.plotly_chart(fig_liq_esc, use_container_width = True)


with projecoes_mes.container():
# Assuming you have extracted the relevant values from your DataFrames
    st.subheader('Projeções')
    col_proj_1, col_proj_2, col_proj_3, col_proj_4 = st.columns(4)
    
    
    with col_proj_1:
        dias_form = st.form(key='dias_formulario')
        dias_uteis = dias_form.number_input('Número de dias passados')
        total_mes = dias_form.number_input('Dias úteis totais no mês atual')
        confirmar_dias = dias_form.form_submit_button(label = 'Atualizar')
    
    daily_average_total = final_data_total / dias_uteis
    daily_average_liq_esc_total = final_data_liq_esc_total/ dias_uteis
    daily_average_assessor = final_data_liq_total / dias_uteis 

    # Calculate projected totals for the month (assuming 30 days)
    total_for_month_total = daily_average_total * total_mes
    total_for_month_liq_esc_total = daily_average_liq_esc_total * total_mes 
    month_assessor = daily_average_assessor * total_mes

    # Print or use the projected totals as needed
    
    with col_proj_2:
        st.write('Projeção Bruta XP:')
        st.dataframe(total_for_month_total) 
    with col_proj_3:
        st.write('Projeção Líquida Escritório:')
        st.dataframe(total_for_month_liq_esc_total)
    with col_proj_4:
        st.write('Projeção Líquida Assessor:')
        st.dataframe(month_assessor)

with comissoes_historico.container():

    st.header('Histórico de Relatório de Comissões')
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
       