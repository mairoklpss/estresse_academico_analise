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
st.markdown('##### Este Dashboard foi criado para analisar o nível de estresse acadêmico entre 139 alunos. O conjunto de dados coletados são respostas de alunos em relação a pressão acadêmica de casa, educação de estudo e estratégias de enfrentamento ao estresse acadêmico geral.')
st.markdown('> Explore os níveis de estresse acadêmico dos estudantes atualmente. Utilize os filtros à esquerda para refinar sua análise.')

st.markdown('----')

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
col1.metric("Quantos Alunos foram Entrevistados", f"{total_alunos} alunos")
col2.metric("Nível de Estresse Acadêmico Mais Comum", nivel_estresse_mais_comum)
col3.metric("Quantos Alunos Têm Estresse Nível Alto", f"{estresse_alto_alunos:.1f}%")
col4.metric("Quantos Alunos Têm Estresse Nível Baixo", f"{estresse_baixo_alunos:.1f}%")

st.markdown('----')

st.subheader('Gráficos')

# criação das colunas para dispor os gráficos
col_graf1, = st.columns(1)
col3_graf3, col4_graf4, col5_graf5 = st.columns(3)
col_insight_ambiente, = st.columns(1)
col7_graf7, = st.columns(1)
col_insight_competicao, = st.columns(1)
col6_graf6, col8_graf8 = st.columns(2)
col_insight_estagio, = st.columns(1)

if not df_filtrado.empty:
    with col_graf1:
            dados_maior_menor_indice = df_filtrado['Índice de Estresse Acadêmico'].value_counts().sort_values(ascending=False)
            fig = px.bar(dados_maior_menor_indice.index, #dados
                x='Índice de Estresse Acadêmico', #dados do eixo x
                y=dados_maior_menor_indice.values, #dados do eixo y
                title= "Índice de Estresse Acadêmico", #titulo do grafico
                # labels serve para nomear os rótulos x e y quando é passado o cursor em cima da barra.
                labels= {'Índice de Estresse Acadêmico': 'Nível de Estresse Acadêmico', 'y': 'Quantidade de alunos'},
                color='Índice de Estresse Acadêmico', #colorir barras
                text_auto=True
                )

            # nomear os eixos.
            fig.update_layout(xaxis_title='Nível de Estresse Acadêmico', yaxis_title='Quantidade de aluno', bargap = 1)
            fig.update_traces(width = 0.7)
            st.plotly_chart(fig, use_container_width=True)

    with col3_graf3:
            perfil_alto_estresse = df_filtrado[df_filtrado['Índice de Estresse Acadêmico'].isin(['Alta', 'Muito Alta'])]
            
            # Contar quantos alunos por ambiente de estudo o têm estresse alto
            contagem_ambiente_alto = perfil_alto_estresse.groupby('Ambiente de Estudo').size().reset_index(name='Quantidade').sort_values('Quantidade', ascending=False)
            
            # Criando um novo DataFrame com apenas as colunas de ambiente e índice de estresse
            df_ambiente_estresse = df_filtrado[['Ambiente de Estudo', 'Índice de Estresse Acadêmico']]
            contagem_ambiente_indice = df_ambiente_estresse.groupby(['Ambiente de Estudo', 'Índice de Estresse Acadêmico']).size().reset_index(name='Quantidade')

            # Filtrar os dados apenas para o ambiente 'Barulhento'
            # em relação a variavel criada anteriormente.
            df_barulhento = contagem_ambiente_indice[contagem_ambiente_indice['Ambiente de Estudo'] == 'Barulhento']
            #grafico em pizza mostrando os indices de estresse em ambiente barulhento
            fig3 = px.pie(
                df_barulhento,
                names= 'Índice de Estresse Acadêmico',
                values= 'Quantidade',
                title= 'Índice de Estresse em Ambiente de Estudo Barulhento',
                color= 'Índice de Estresse Acadêmico',
                labels= {'Índice de Estresse Acadêmico': 'Índice de Estresse'}
            )

            # update_traces(textinfo= 'percent+label') adiciona label+porcentagem nos setores
            fig3.update_traces(textinfo= 'percent+label')
            st.plotly_chart(fig3, use_container_width=True)  


    with col4_graf4:
            # Filtrar os dados apenas para o ambiente 'Tranquilo'
            # em relação a variavel criada anteriormente.
            df_tranquilo =  contagem_ambiente_indice[contagem_ambiente_indice['Ambiente de Estudo'] == 'Tranquilo']
            #grafico em pizza mostrando os indices de estresse em ambiente tranquilo
            fig4 = px.pie(
                df_tranquilo,
                names= 'Índice de Estresse Acadêmico',
                values= 'Quantidade',
                color= 'Índice de Estresse Acadêmico',
                title= 'Índice de Estresse em Ambiente de Estudo Tranquilo',
            )

            fig4.update_traces(textinfo= 'percent+label')
            st.plotly_chart(fig4, use_container_width=True)     


    with col5_graf5:
            #grafico em pizza mostrando os indices de estresse em ambiente Inquieto
            df_inquieto = contagem_ambiente_indice[contagem_ambiente_indice['Ambiente de Estudo'] == 'Inquieto']
            fig5 = px.pie(
                df_inquieto,
                names= 'Índice de Estresse Acadêmico',
                values= 'Quantidade',
                color= 'Índice de Estresse Acadêmico',
                title= 'Índice de Estresse em Ambiente de Estudo Inquieto',
            )

            fig5.update_traces(textinfo= 'percent+label')
            st.plotly_chart(fig5, use_container_width=True)  

    with col_insight_ambiente:
        # Adicionar insights abaixo do gráfico
        if not contagem_ambiente_alto.empty:
            ambiente_mais_afetado = contagem_ambiente_alto.iloc[0]['Ambiente de Estudo']
            total_afetados_alunos = contagem_ambiente_alto.iloc[0]['Quantidade']
            st.info(f"💡 **Insight:** O ambiente com maior número de alunos com estresse alto é **{ambiente_mais_afetado}** com {total_afetados_alunos} alunos.") 


    with col6_graf6:
            # Criando um novo DataFrame com apenas as colunas de ambiente e índice de estresse
            df_estagio_estresse = df_filtrado[['Estágio Acadêmico', 'Índice de Estresse Acadêmico']]
            contagem_estagio_indice = df_estagio_estresse.groupby(['Estágio Acadêmico', 'Índice de Estresse Acadêmico']).size().reset_index(name='Quantidade')

            # Criando o gráfico de barras agrupadas
            # Índice de estresse para cada tipo de Estágio Acadêmico
            fig6 = px.bar(contagem_estagio_indice,
                        x="Estágio Acadêmico",
                        y="Quantidade",
                        color="Índice de Estresse Acadêmico",
                        barmode="group", #barmode faz com que as barras fiquem uma do lado do outra
                        title="Índice de Estresse por Estágio Acadêmico",
                        text_auto=True # Adicionado para exibir a quantidade exata nas barras
                        )

            fig6.update_layout(xaxis_title= 'Característica do Estágio Acadêmico', yaxis_title= 'Quantidade de alunos')
            st.plotly_chart(fig6, use_container_width=True)  
           

    with col7_graf7:
            contagem_competicao_alto = perfil_alto_estresse.groupby('Competição Acadêmica').size().reset_index(name='Quantidade').sort_values('Quantidade', ascending=False)


            # Criando um novo DataFrame com apenas as colunas de ambiente e índice de estresse
            df_competicao_estresse = df_filtrado[['Competição Acadêmica', 'Índice de Estresse Acadêmico']]
            contagem_competicao_indice = df_competicao_estresse.groupby(['Competição Acadêmica', 'Índice de Estresse Acadêmico']).size().reset_index(name='Quantidade')

            # Criando o gráfico de barras agrupadas
            # Índice de estresse para cada tipo de Competição Acadêmica
            fig7 = px.bar(contagem_competicao_indice,
                        x="Competição Acadêmica",
                        y="Quantidade",
                        color="Índice de Estresse Acadêmico",
                        barmode="group", #barmode faz com que as barras fiquem uma do lado do outra
                        title="Índice de Estresse por Competição Acadêmica",
                        text_auto=True # Adicionado para exibir a quantidade exata nas barras
                        )

            fig7.update_layout(xaxis_title= 'Característica do Competição Acadêmica', yaxis_title= 'Quantidade de alunos')               
            st.plotly_chart(fig7, use_container_width=True)  

    with col_insight_competicao:
        # Adicionar insights abaixo do gráfico
        if not contagem_competicao_alto.empty:
            competicao_mais_afetada = contagem_competicao_alto.iloc[0]['Competição Acadêmica']
            total_afetados_tadinhos = contagem_competicao_alto.iloc[0]['Quantidade']
            st.info(f"💡 **Insight:** O maior número de alunos com estresse alto são os têm **Competição Acadêmica {competicao_mais_afetada}** com {total_afetados_tadinhos} alunos.")

    with col8_graf8:
        # Contar quantos alunos por estágio acadêmico têm estresse alto
        contagem_estagio_alto = perfil_alto_estresse.groupby('Estágio Acadêmico').size().reset_index(name='Quantidade').sort_values('Quantidade', ascending=False)
        
        # Gráfico de barras mostrando a distribuição
        fig_perfil = px.bar(
            contagem_estagio_alto,
            x='Estágio Acadêmico',
            y='Quantidade',
            title='Perfil de Alunos com Estresse Alto/Muito Alto por Estágio Acadêmico',
            labels={'Estágio Acadêmico': 'Estágio Acadêmico', 'Quantidade': 'Número de Alunos'},
            color='Quantidade',
            color_continuous_scale='Reds',
            text='Quantidade'
        )
        
        fig_perfil.update_traces(
            textposition='outside',
            width= 0.7
        )
        
        fig_perfil.update_layout(
            xaxis_title='Estágio Acadêmico',
            yaxis_title='Quantidade de Alunos com Estresse Alto',
            showlegend=False,
            height = 500
        )
        
        st.plotly_chart(fig_perfil, use_container_width=True)
        
    with col_insight_estagio:
        # Adicionar insights abaixo do gráfico
        if not contagem_estagio_alto.empty:
            estagio_mais_afetado = contagem_estagio_alto.iloc[0]['Estágio Acadêmico']
            total_afetados = contagem_estagio_alto.iloc[0]['Quantidade']
            st.info(f"💡 **Insight:** O estágio com maior número de alunos com estresse alto é **{estagio_mais_afetado}** com {total_afetados} alunos.")
                  
else:
    st.warning('Nenhum dado a mostrar aqui.')    

st.markdown('----')

# base de dados completa
st.subheader('Base de Dados detalhada')
if not df_filtrado.empty:
    st.dataframe(df_filtrado)
else:
    st.warning('Nenhum dado a mostrar aqui.')    