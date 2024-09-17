import streamlit as st
import pandas as pd
from datetime import datetime

# Leitura dos dados a partir de um arquivo CSV
df = pd.read_csv('zabbix_problems_atual.csv')

st.set_page_config(page_title='Visualização de Eventos', page_icon=':bar_chart:', layout='wide')

# Convertendo a coluna 'horario' para datetime
df['horario'] = pd.to_datetime(df['horario'])

# Função para calcular a idade do registro em dias, horas, minutos e segundos
def calcular_idade(horario):
    diferenca = datetime.now() - horario
    dias = diferenca.days
    segundos = diferenca.seconds
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60
    return f'{dias}d {horas}h {minutos}m {segundos}s'

# Título da aplicação
st.title("Visualização de Eventos")

# Selectbox para filtrar pelo campo 'Descrição'
descricao_filtro = st.sidebar.selectbox('Selecione a Descrição para Filtrar', ['Todos'] + df['descricao'].unique().tolist())

# Filtrando a grid com base na seleção do selectbox
if descricao_filtro != 'Todos':
    df_filtrado = df[df['descricao'] == descricao_filtro]
else:
    df_filtrado = df

# Exibindo o total de registros
total_registros = df_filtrado.shape[0]
st.write(f"Total de Registros: {total_registros}")

# Exibindo os dados em uma grid original
st.dataframe(df_filtrado)

# Criando nova grid com as colunas host, descricao, horario e idade (em dias, horas, minutos, segundos)
df_filtrado['idade'] = df_filtrado['horario'].apply(calcular_idade)
df_idade = df_filtrado[['nome_host', 'descricao', 'horario', 'idade']]

# Exibindo a nova grid com a coluna de idade
st.write("Grid com Idade dos Registros")
st.dataframe(df_idade)
