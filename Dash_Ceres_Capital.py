import streamlit as st
from relatorio_receita import gerar_relatorio_receita
from relatorio_captacao_ativacao import gerar_relatorio_captacao, gerar_relatorio_evasao
import plotly.express as px
import plotly.graph_objects as go

##Configuração da página
st.set_page_config(page_title='Dashboard Ceres Capital', page_icon=':corn:' , layout="wide", initial_sidebar_state="auto", menu_items=None)

##Importando os dados com Funções:

final_data, final_data_liq = gerar_relatorio_receita()
final_data_total = final_data.drop(columns=['Nome']).sum().round(0)
final_data_liq_total = final_data_liq.drop(columns=['Nome']).sum().round(0)
assessor = None
captacao, captacao_data, captacao_assessor = gerar_relatorio_captacao(assessor)
evasao = gerar_relatorio_evasao(assessor)


##Layout da página
st.title('Dashboard Ceres Capital-3')
st.subheader('Receita Bruta')
visao_receita_bruta = st.empty()

st.subheader('ReceitaLíquida')
visao_receita_liquida = st.empty()

st.subheader('Captação')
visao_captacao = st.empty()



with visao_receita_bruta.container():
    
    with st.expander('Tabelas'):
        
        col_bruta_1, col_bruta_2 = st.columns(2)
        
        with col_bruta_1:
            
            st.dataframe(final_data)
        
        with col_bruta_2:

            st.dataframe(final_data_total)
    
    fig_bruto = px.bar(final_data, x='Nome', y='Comissão Total Bruta')

    st.plotly_chart(fig_bruto, use_container_width = True)

with visao_receita_liquida.container():
    
    with st.expander('Tabelas'):
        
        col_liq_1, col_liq_2 = st.columns(2)

        with col_liq_1:
            st.dataframe(final_data_liq)
        
        with col_liq_2:
            st.dataframe(final_data_liq_total)
    
    fig_liq = px.bar(final_data_liq, x='Nome', y='Comissão Total Líquida')

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

    # Create a figure
    fig_cap_total = go.Figure()

    # Add bar chart for 'PF' and 'PJ'
    fig_cap_total.add_trace(go.Bar(x=captacao_data.index, y=captacao_data['PF'], name='PF'))
    fig_cap_total.add_trace(go.Bar(x=captacao_data.index, y=captacao_data['PJ'], name='PJ'))

    # Add line chart for 'Captação'
    fig_cap_total.add_trace(go.Scatter(x=captacao_data.index, y=captacao_data['Captação_cumsum'], name='Captação'))

    # Update layout
    fig_cap_total.update_layout(
        title=f'Captação Líquida/Mês: {sum_captacao:,}',  # set title as the sum of 'Captação'
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