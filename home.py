import pandas as pd
import streamlit as st
import plotly.express as px

# base de dados que irá alimentar o sistema
df = pd.read_csv('academic Stress level - maintainance 1.csv')

# -------- Tratamentos de Dados ----------
# apaga os dados nulos
df = df.dropna()
# retira a coluna timestamp
df.drop(columns=['Timestamp'], inplace=True)

# ---------- Traduções ---------
# # traduzir as colunas do ingles para o portugues
nomes_colunas = {
    'Your Academic Stage': 'Estágio Acadêmico',
    'Peer pressure': 'Pressão dos Colegas',
    'Academic pressure from your home': 'Pressão Acadêmica Familiar',
    'Study Environment': 'Ambiente de Estudo',
    'What coping strategy you use as a student?': 'Estratégia de Enfrentamento',
    'Do you have any bad habits like smoking, drinking on a daily basis?': 'Hábitos Diários (Fumo/Álcool)',
    'What would you rate the academic  competition in your student life': 'Competição Acadêmica',
    'Rate your academic stress index ': 'Índice de Estresse Acadêmico'
}
df.rename(columns=nomes_colunas, inplace=True)
# traduz os registro de estagio academico
df['Estágio Acadêmico'] = df['Estágio Acadêmico'].replace({
    'undergraduate': 'Graduação',
    'high school': 'Ensino Médio',
    'post-graduate': 'Pós-graduação'
})

# traduz os registro de ambiente
df['Ambiente de Estudo'] = df['Ambiente de Estudo'].replace({
    'Peaceful': 'Tranquilo',
    'disrupted': 'Inquieto',
    'Noisy': 'Barulhento'
})
# traduz os registro de estrategia
df['Estratégia de Enfrentamento'] = df['Estratégia de Enfrentamento'].replace({
    'Analyze the situation and handle it with intellect': 'Lidar com inteligência',
    'Emotional breakdown (crying a lot)': 'Crise emocional',
    'Social support (friends, family)': 'Apoio social'
})
# traduz os registro de habitos
df['Hábitos Diários (Fumo/Álcool)'] = df['Hábitos Diários (Fumo/Álcool)'].replace({
    'No': 'Não tem',
    'Yes': 'Tem',
    'prefer not to say': 'Prefere não dizer'
})
# traduz os registro de pressao
df['Pressão dos Colegas'] = df['Pressão dos Colegas'].replace({
    1: 'Muito Baixa',
    2: 'Baixa',
    3: 'Moderada',
    4: 'Alta',
    5: 'Muito Alta'
})
# traduz os registro de pressao familiar
df['Pressão Acadêmica Familiar'] = df['Pressão Acadêmica Familiar'].replace({
    1: 'Muito Baixa',
    2: 'Baixa',
    3: 'Moderada',
    4: 'Alta',
    5: 'Muito Alta'
})
# traduz os registro de competição
df['Competição Acadêmica'] = df['Competição Acadêmica'].replace({
    1: 'Muito Baixa',
    2: 'Baixa',
    3: 'Moderada',
    4: 'Alta',
    5: 'Muito Alta'
})
# traduz os registro de indice
df['Índice de Estresse Acadêmico'] = df['Índice de Estresse Acadêmico'].replace({
    1: 'Muito Baixa',
    2: 'Baixa',
    3: 'Moderada',
    4: 'Alta',
    5: 'Muito Alta'
})

# aba do navegador
st.set_page_config(
    page_title= "Dashboard de Índice de Estresse Acadêmico",
    page_icon= '🤓',
    layout= 'wide'
)

# ------ Filtragem de Dados -------
# sidebar de filtragem de dados
st.sidebar.header('Filtros 🔎')

# Filtro para nível de estresse acadêmico
indices_disponiveis = sorted(df['Índice de Estresse Acadêmico'].unique())
indices_selecionados = st.sidebar.multiselect("Nível de Estresse Acadêmico", indices_disponiveis, default=indices_disponiveis)

# Filtro para estágio acadêmico (graduação, mestrado, doutorado)
estagios_disponiveis = sorted(df['Estágio Acadêmico'].unique())
estagios_selecionados = st.sidebar.multiselect("Estágio Acadêmico", estagios_disponiveis, default=estagios_disponiveis)

# Filtro para pressão exercida pelos colegas
pressao_colegas_disponiveis = sorted(df['Pressão dos Colegas'].unique())
pressao_colegas_selecionados = st.sidebar.multiselect("Pressão dos Colegas", pressao_colegas_disponiveis, default=pressao_colegas_disponiveis)

# Filtro para pressão acadêmica vinda da família
pressao_familia_disponiveis = sorted(df['Pressão Acadêmica Familiar'].unique())
pressao_familia_selecionados = st.sidebar.multiselect('Pressão Acadêmica Familiar', pressao_familia_disponiveis, default=pressao_familia_disponiveis)

# Filtro para nível de competição acadêmica
competicoes_disponiveis = sorted(df['Competição Acadêmica'].unique())
competicoes_selecionados = st.sidebar.multiselect('Competição Acadêmica', competicoes_disponiveis, default=competicoes_disponiveis)

# Filtro para tipo de ambiente de estudo
ambientes_disponiveis = sorted(df['Ambiente de Estudo'].unique())
ambientes_selecionados = st.sidebar.multiselect('Ambiente de Estudo', ambientes_disponiveis, default=ambientes_disponiveis)

# Filtro para estratégias de enfrentamento utilizadas
estrategias_disponiveis = sorted(df['Estratégia de Enfrentamento'].unique())
estrategias_selecionadas = st.sidebar.multiselect(
    "Estratégia de Enfrentamento", 
    estrategias_disponiveis, 
    default=estrategias_disponiveis
)

# Filtro para hábitos de consumo (fumo/álcool)
habitos_disponiveis = sorted(df['Hábitos Diários (Fumo/Álcool)'].unique())
habitos_selecionados = st.sidebar.multiselect(
    "Hábitos Diários (Fumo/Álcool)", 
    habitos_disponiveis, 
    default=habitos_disponiveis
)

# -------- DF filtrado ----------
df_filtrado = df[
    (df['Índice de Estresse Acadêmico'].isin(indices_selecionados)) &
    (df['Estágio Acadêmico'].isin(estagios_selecionados)) &
    (df['Pressão dos Colegas'].isin(pressao_colegas_selecionados)) &
    (df['Pressão Acadêmica Familiar'].isin(pressao_familia_selecionados)) &
    (df['Ambiente de Estudo'].isin(ambientes_selecionados)) &
    (df['Competição Acadêmica'].isin(competicoes_selecionados)) & 
    (df['Estratégia de Enfrentamento'].isin(estrategias_selecionadas)) &
    (df['Hábitos Diários (Fumo/Álcool)'].isin(habitos_selecionados))
]

# --------- Conteúdo Principal ----------
# titulo
st.title('🤓 Dashboard de Índice de Estresse Acadêmico')

# subtitulo
st.markdown('Este Dashboard foi criado para analisar o nível de estresse acadêmico entre 139 alunos. O conjunto de dados coletados são respostas de alunos em relação a pressão acadêmica de casa, educação de estudo e estratégias de enfrentamento ao estresse acadêmico geral.')

# subtitulo dos dashs
st.subheader('Métricas Gerais dos Níveis de Estresse Acadêmico')

# dados que aparecerão, caso não estiver vazia.
if not df_filtrado.empty:
    # shape indica o numero de [linhas, colunas], o [0] retorna apenas as linhas
    total_alunos = df_filtrado.shape[0]
    # mode() é a moda dos níveis
    nivel_estresse_mais_comum = df_filtrado['Índice de Estresse Acadêmico'].mode()[0]
    # isin verifica se o valor está na lista ou no campo especificado (retorna True ou False)
    # o sum() conta quantos Trues tem
    estresse_alto_alunos = (df_filtrado['Índice de Estresse Acadêmico'].isin(['Alta', 'Muito Alta']).sum()) / total_alunos * 100 
    estresse_baixo_alunos = (df_filtrado['Índice de Estresse Acadêmico'].isin(['Baixa', 'Muito Baixa']).sum()) / total_alunos * 100 
#caso esteja vazia
else:
    total_alunos, nivel_estresse_mais_comum, estresse_alto_alunos, estresse_baixo_alunos = 0, "", 0, 0

# dispor tudo em colunas
col1, col2, col3, col4 = st.columns(4)    
col1.metric("Quantos Alunos foram Entrevistados", total_alunos)
col2.metric("Nível de Estresse Acadêmico Mais Comum", nivel_estresse_mais_comum)
col3.metric("Quantos Alunos Têm Estresse Nível Alto", f"{estresse_alto_alunos:.1f}%")
col4.metric("Quantos Alunos Têm Estresse Nível Baixo", f"{estresse_baixo_alunos:.1f}%")