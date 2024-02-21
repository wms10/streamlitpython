import streamlit as st
import pandas as pd
import numpy as np



# Carregando os dados diretamente dos arquivos CSV
df_acao = pd.read_csv(r'C:\Users\wms_1\Desktop\PISI3_DSI\Modelagem_Modificado\venv\csvs\dim_acao.csv')
df_credor = pd.read_csv(r'C:\Users\wms_1\Desktop\PISI3_DSI\Modelagem_Modificado\venv\csvs\dim_credor.csv')
df_data = pd.read_csv(r'C:\Users\wms_1\Desktop\PISI3_DSI\Modelagem_Modificado\venv\csvs\dim_data.csv')
df_empenho = pd.read_csv(r'C:\Users\wms_1\Desktop\PISI3_DSI\Modelagem_Modificado\venv\csvs\dim_empenho.csv')
df_fonte = pd.read_csv(r'C:\Users\wms_1\Desktop\PISI3_DSI\Modelagem_Modificado\venv\csvs\dim_fonte.csv')
df_modalidade_licitacao = pd.read_csv(r'C:\Users\wms_1\Desktop\PISI3_DSI\Modelagem_Modificado\venv\csvs\dim_modalidade_licitacao.csv')
df_pagamento = pd.read_csv(r'C:\Users\wms_1\Desktop\PISI3_DSI\Modelagem_Modificado\venv\csvs\fato_pagamento.csv')


# Título do aplicativo
st.title("Análise OLAP - Data Warehouse")

# Pergunta Estruturada
st.title('Como varia a porcentagem de valor pago por Fonte e Ação, e qual é a diferença entre o valor pago e o empenhado, considerando a Modalidade de Licitação?')

# Adicione um menu suspenso para seleção da Fonte
fontes = ["Todas as Fontes"] + df_fonte['nome'].unique().tolist()
fonte_selecionada = st.selectbox("Selecione a Fonte:", fontes)

# Adicione um menu suspenso para seleção da Ação
acoes = ["Todas as Ações"] + df_acao['nome'].unique().tolist()
acao_selecionada = st.selectbox("Selecione a Ação:", acoes)

# Adicione um menu suspenso para seleção da Modalidade de Licitação
modalidades = ["Todas as Modalidades"] + df_modalidade_licitacao['nome'].unique().tolist()
modalidade_selecionada = st.selectbox("Selecione a Modalidade de Licitação:", modalidades)

# Modifique a lógica da consulta para considerar as seleções
filtered_df = df_pagamento.copy()

if fonte_selecionada != "Todas as Fontes":
    filtered_df = filtered_df[filtered_df['cod_fonte'] == df_fonte[df_fonte['nome'] == fonte_selecionada]['codigo'].values[0]]

if acao_selecionada != "Todas as Ações":
    filtered_df = filtered_df[filtered_df['cod_acao'] == df_acao[df_acao['nome'] == acao_selecionada]['codigo'].values[0]]

if modalidade_selecionada != "Todas as Modalidades":
    filtered_df = filtered_df[filtered_df['cod_modalidade_licitacao'] == df_modalidade_licitacao[df_modalidade_licitacao['nome'] == modalidade_selecionada]['codigo'].values[0]]

# Calcular porcentagem_pago e diferenca
filtered_df['porcentagem_pago'] = (filtered_df['valor_pago'] / filtered_df['valor_empenhado']) * 100
filtered_df['diferenca'] = filtered_df['valor_pago'] - filtered_df['valor_empenhado']

# Exibindo os resultados
st.dataframe(filtered_df[['cod_fonte', 'cod_acao', 'cod_modalidade_licitacao', 'valor_pago', 'valor_empenhado', 'porcentagem_pago', 'diferenca']])
