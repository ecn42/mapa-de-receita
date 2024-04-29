import streamlit as st
from relatorio_receita import gerar_relatorio_receita
from relatorio_captacao_ativacao import gerar_relatorio_captacao, gerar_relatorio_evasao
import plotly.express as px
import plotly.graph_objects as go

##Configuração da página
st.set_page_config(page_title='Dashboard Ceres Capital', page_icon=':corn:' , layout="wide", initial_sidebar_state="auto", menu_items=None)

##Importando os dados com Funções:

final_data, final_data_liq, data_posicao_positivador = gerar_relatorio_receita()
final_data_total = final_data.drop(columns=['Nome']).sum().round(0)
final_data_liq_total = final_data_liq.drop(columns=['Nome']).sum().round(0)
assessor = None
captacao, captacao_data, captacao_assessor, data_posicao_captacao = gerar_relatorio_captacao(assessor)
evasao = gerar_relatorio_evasao(assessor)
proj_liq_assessor = final_data_liq_total

##Layout da página
st.title('Dashboard Ceres Capital')
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
        title=f'''Captação Líquida/Mês: {sum_captacao:,}W 
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
    final_data_liq_esc = final_data_liq
    final_data_liq_esc_total = final_data_liq_total
    

    numeric_columns = final_data_liq_esc.select_dtypes(include='number').columns
    final_data_liq_esc[numeric_columns] *= 2
    final_data_liq_esc_total *= 2

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
        dias_form = st.form(key='my_form')
        dias_uteis = dias_form.number_input('Número de dias passados')
        total_mes = dias_form.number_input('Dias úteis totais no mês atual')
        confirmar_dias = dias_form.form_submit_button(label = 'Atualizar')
    
    daily_average_total = final_data_total / dias_uteis
    daily_average_liq_esc_total = final_data_liq_esc_total/ dias_uteis
    daily_average_assessor = proj_liq_assessor / dias_uteis 

    # Calculate projected totals for the month (assuming 30 days)
    total_for_month_total = daily_average_total * total_mes
    total_for_month_liq_esc_total = daily_average_liq_esc_total * total_mes 
    month_assessor = daily_average_assessor *total_mes / 2

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