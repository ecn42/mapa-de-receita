import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Asset Allocation', page_icon=':chart_with_upwards_trend:' , layout="wide", initial_sidebar_state="auto", menu_items=None)
# Load the data
df = pd.read_excel('assetallocation/data/data.xlsx')
col1, col2 = st.columns(2)
# Get the unique profiles
profiles = df['Perfil'].unique()

with col1:
    # Create a dropdown menu for profiles
    st.header('Asset Allocation Sugerido:')
    selected_profile = st.selectbox('Select a profile', profiles)

    # Filter the dataframe based on the selected profile and non-zero allocation
    df_filtered = df[(df['Perfil'] == selected_profile) & (df['Alocação'] != 0)]

    # Group by 'Ativo' and sum 'Alocação'
    df_grouped = df_filtered.groupby('Ativo')['Alocação'].sum().reset_index()

    # Create a pie chart with plotly
    fig = px.pie(df_grouped, values='Alocação', names='Ativo', title='Asset Allocation sugerida para perfil ' + selected_profile)

    st.plotly_chart(fig)

# Load the suggestions data from 'ativos.xlsx'
df_suggestions = pd.read_excel('assetallocation/ativos/ativos.xlsx')

# Filter the suggestions data based on the selected profile
df_suggestions = df_suggestions[df_suggestions['Perfil'] == selected_profile]

# Get the unique 'Carteira' in the suggestions data
carteiras = df_suggestions['Carteira'].unique()

with col2:
    # Display each 'Carteira' in a separate column
    for i in range(len(carteiras)):
        st.header(carteiras[i])
        df_to_display = df_suggestions[df_suggestions['Carteira'] == carteiras[i]]
        df_to_display = df_to_display.iloc[:, :-2]  # Drop the last column

    
        st.dataframe(df_to_display, hide_index=True, column_config={
            'Link': st.column_config.LinkColumn(
            "Link", display_text="Acessar"
            )
        })
