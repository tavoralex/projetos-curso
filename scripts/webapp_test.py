import streamlit as st
import pandas as pd
import numpy as np
import time
import seaborn as sns
import matplotlib.pyplot as plt
import os

#configurando layout da página:
st.set_page_config(page_title = 'SINASC Rondônia', layout = 'wide', page_icon = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Bandeira_de_Rond%C3%B4nia.svg/1024px-Bandeira_de_Rond%C3%B4nia.svg.png')
st.title('**Módulo 15 - Atividade 01**')
st.markdown('---')

st.header('Criando um webapp')
st.markdown('---')

def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao='nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig = plt)
    return None

st.subheader('Plotando dataframe SINASC_RO_2019:')
sinasc = pd.read_csv('.\SINASC_RO_2019.csv')
st.dataframe(sinasc)

#convertendo siansc.DTNASC para formato data/tempo:
sinasc.DTNASC = pd.to_datetime(sinasc.DTNASC)

#verificando datas mínimas e máximas para verificar se dataframe está completo:
min_data = sinasc.DTNASC.min()
max_data = sinasc.DTNASC.max()
datas = sinasc.DTNASC.unique()
st.dataframe(datas)
min_data
max_data

st.subheader('Plotando filtro de seleção de data para o df:')
data_inicial = st.sidebar.date_input('Data inicial:', 
                value = min_data, 
                min_value = min_data, 
                max_value = max_data)
data_final = st.sidebar.date_input('Data final:', 
                value = max_data, 
                min_value = min_data, 
                max_value = max_data)

st.subheader('Plotando dataframe e número de linhas filtrados:')
sinasc = sinasc[(sinasc['DTNASC'] <= pd.to_datetime(data_final)) & (sinasc['DTNASC'] >= pd.to_datetime(data_inicial))]
st.write(sinasc)
st.write(sinasc.shape)

st.subheader('Plotando gráficos do SINASC')
plota_pivot_table(sinasc, 'IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento')
plota_pivot_table(sinasc, 'IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack')
plota_pivot_table(sinasc, 'PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack')
plota_pivot_table(sinasc, 'PESO', 'ESCMAE', 'median', 'PESO mediano','escolaridade mae','sort')
plota_pivot_table(sinasc, 'APGAR1', 'GESTACAO', 'mean', 'apgar1 medio','gestacao','sort')

st.subheader('Plotando uma tabela estática SINASC_RO_2019:')
st.table(sinasc.head()) 

st.subheader('Plotando um mapa de municípios de residência através de latitute e longitude:')
#Necessita de tratamento de dados para remover NaN e exibir corretamente
sinasc = sinasc.dropna()
sinasc['lat'] = sinasc.munResLat
sinasc['lon'] = sinasc.munResLon
st.map(sinasc)

st.subheader('Plotando um sliderbox na sidebar:')
x = st.sidebar.slider('x')
st.write(x, 'log de x:', np.log(x))

st.subheader('Plotando uma caixa de input:')
st.text_input("Digite seu nome:", key="nome")
st.write(st.session_state.nome)

st.subheader('Plotando uma caixa opcional de exibição de dataframe:')
if st.checkbox('Mostrar dataframe:'):
    chart_data = sinasc

    chart_data

st.subheader('Plotando uma caixa de seleção de CODESTAB:')
df = sinasc
option = st.selectbox(
    'Selecione o código do estabelecimento:',
     df.CODESTAB)
'Selecionado: ', option

st.subheader('<-- Plotando uma caixa de opções de contato na sidebar:')
add_selectbox = st.sidebar.selectbox(
    'Como gostaria de ser contatado?',
    ('Email', 'Tel Residencial', 'Celular')
)

st.subheader('Plotando widgets lado a lado:')
left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')
# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

st.subheader('Construindo uma barra de progressão percentual:')
# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)
'...and now we\'re done!'


