import streamlit as st
import pandas as pd
import os

# Carregar dados diretamente dos arquivos CSV na pasta 'csvs'
@st.cache_data
def carregar_dados():
    dados = {}
    caminho_csvs = 'C:\\Users\\wms_1\\Desktop\\PISI3_DSI\\Modelagem_Modificado\\venv\\csvs'  # Substitua pelo caminho real

    # Lista todos os arquivos CSV na pasta 'csvs'
    arquivos_csv = [f for f in os.listdir(caminho_csvs) if f.endswith(".csv")]

    # Carrega cada arquivo CSV em um DataFrame e armazena no dicionário 'dados'
    for arquivo in arquivos_csv:
        chave = os.path.splitext(arquivo)[0]
        caminho_completo = os.path.join(caminho_csvs, arquivo)
        dados[chave] = pd.read_csv(caminho_completo)

    return dados

# Título do aplicativo
st.title("Análise OLAP - Data Warehouse")

# Pergunta Estruturada
st.title('Como varia a porcentagem de valor pago por Fonte e Ação, e qual é a diferença entre o valor pago e o empenhado, considerando a Modalidade de Licitação?')

# Adicione um menu suspenso para seleção da Fonte
fontes = ["Todas as Fontes"] + carregar_dados()['dim_fonte']['nome'].unique().tolist()
fonte_selecionada = st.selectbox("Selecione a Fonte:", fontes)

# Adicione um menu suspenso para seleção da Ação
acoes = ["Todas as Ações"] + carregar_dados()['dim_acao']['nome'].unique().tolist()
acao_selecionada = st.selectbox("Selecione a Ação:", acoes)

# Adicione um menu suspenso para seleção da Modalidade de Licitação
modalidades = ["Todas as Modalidades"] + carregar_dados()['dim_modalidade_licitacao']['nome'].unique().tolist()
modalidade_selecionada = st.selectbox("Selecione a Modalidade de Licitação:", modalidades)

# Modifique a lógica da consulta para considerar as seleções
filtered_df = carregar_dados()['fato_pagamento'].copy()

if fonte_selecionada != "Todas as Fontes":
    filtered_df = filtered_df[filtered_df['cod_fonte'] == carregar_dados()['dim_fonte'][carregar_dados()['dim_fonte']['nome'] == fonte_selecionada]['codigo'].values[0]]

if acao_selecionada != "Todas as Ações":
    filtered_df = filtered_df[filtered_df['cod_acao'] == carregar_dados()['dim_acao'][carregar_dados()['dim_acao']['nome'] == acao_selecionada]['codigo'].values[0]]

if modalidade_selecionada != "Todas as Modalidades":
    filtered_df = filtered_df[filtered_df['cod_modalidade_licitacao'] == carregar_dados()['dim_modalidade_licitacao'][carregar_dados()['dim_modalidade_licitacao']['nome'] == modalidade_selecionada]['codigo'].values[0]]

# Calcular porcentagem_pago e diferenca
filtered_df['porcentagem_pago'] = (filtered_df['valor_pago'] / filtered_df['valor_empenhado']) * 100
filtered_df['diferenca'] = filtered_df['valor_pago'] - filtered_df['valor_empenhado']

# Exibindo os resultados
st.dataframe(filtered_df[['cod_fonte', 'cod_acao', 'cod_modalidade_licitacao', 'valor_pago', 'valor_empenhado', 'porcentagem_pago', 'diferenca']])
