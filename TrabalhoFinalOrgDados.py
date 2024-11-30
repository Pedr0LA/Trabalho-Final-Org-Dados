import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import gaussian_kde
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv(r'StudentPerformanceFactors.csv')

st.header('Dashboard: Performance de estudantes')
st.write("Este painel interativo tem como objetivo mostrar a análise feita a partir de dados obtidos no Kaggle.")

# Frequência de notas
st.write("""
         ### 1. Frequência de notas
         Primeiramente, iremos analisar a frequência que cada nota aparece no dataset.
         """)

bin_edges = np.arange(50, 101, 1) 
frequencias, bins = np.histogram(df['Exam_Score'], bins=bin_edges)

grafico_notas = pd.DataFrame({
      'Nota': bins[:-1],
      'Frequência': frequencias
}).set_index('Nota') 

st.write("##### Distribuição de frequência de notas entre 50 e 100")
st.bar_chart(grafico_notas)

st.write("Neste dataset, as notas entre 60-75 pontos no exame final aparecem com maior frequência e notas acima ou abaixo disso são raras.")

# Diferença entre escolas públicas e privadas

soma_publica = 0 # Soma das notas de estudantes instituições de ensino públicas
soma_privada = 0 # Mesma coisa para a privada
quant_alunos_publica = 0 # Quantidade de alunos de instituições de ensino públicas
quant_alunos_privada = 0 # Mesma coisa para a privada

for index, row in df.iterrows():
    if row['School_Type'] == 'Public':
        soma_publica += row['Exam_Score']
        quant_alunos_publica += 1
    else:
        soma_privada += row['Exam_Score']
        quant_alunos_privada += 1

media_publica = soma_publica / quant_alunos_publica
media_privada = soma_privada /quant_alunos_privada

categorias = ['Públicas', 'Privadas']
medias = [media_publica, media_privada]

st.write("### 2. Diferenças entre instituições de ensino públicas e privadas")

st.write("#### 2.1. Há disparidade na qualidade de ensino entre instituições públicas e privadas?")

grafico_qualidade = pd.DataFrame({
    'Instituição': categorias,
    'Média': medias
}).set_index('Instituição')  

st.write("O gráfico abaixo mostra a média dos estudantes em escolas públicas e privadas.")

st.bar_chart(grafico_qualidade)

st.write("No contexto desse dataset, como podemos ver, a diferença de qualidade entre instituições de ensino públicas e instituições de ensino privada não é um fator que implica no rendimento dos alunos.")

st.write(f"A diferença entre as médias dos alunos da privada e da pública é de: {round(media_privada - media_publica, 2)} pontos no exame final, uma diferença quase que irrelevante")

# Há diferença de disponibilidade de recursos educacionais entre estudantes de escolas públicas e privadas?
st.write("#### 2.2. Há diferença de disponibilidade de recursos educacionais entre estudantes de escolas públicas e privadas?")

st.write("Abaixo, temos uma tabela que explicita a quantidade de alunos que possuem acesso a recursos de acordo com o tipo de escola.")
tabela_contingencia = pd.crosstab(
                        df['School_Type'],
                        df['Access_to_Resources'],
                        margins = True,
                        margins_name = "Número total de alunos")

st.dataframe(tabela_contingencia)

st.write("Contudo, é interessante analisar não só números absolutos, mas também o percentual comparativo:")
tabela_contingencia_percentual = pd.crosstab(
                                    df['School_Type'],
                                    df['Access_to_Resources'],
                                    normalize = "index",
                                    margins = True,
                                    margins_name = "Percentual de alunos"
                                    ).mul(100).round(1)

st.dataframe(tabela_contingencia_percentual)

st.write("Olhando apenas os números absolutos podemos tirar falsas conclusões. Por exemplo, a quantidade de alunos de escolas públicas que possuem alto acesso a recursos é o dobro que os de escolas particulares. Porém, levando em consideração a análise percentual, vemos que a disponibilidade de ambas as intituições é quase a mesma")

st.bar_chart(tabela_contingencia_percentual)

st.write("Apesar da porcentagem de alunos com disponibilidade de recursos alta ser 3,4% maior nas escolas privadas, pode-se dizer que o tipo de escola (pública ou privada) não interfere muito no acesso a recursos nesse dataset. É notório que em ambas as intituições de ensino a disponibilidade de materiais de estudo é considerado médio.")


# internet e recursos educacionais
st.write("""
         ### 3. Relação entre Internet e recursos educacionais
         Sabemos que no mundo atual o acesso a Internet possiblita um maior alcance de recursos relacionados à educação. Faremos à seguir uma análise em relação ao tipo de instituição e dificuldade de aprendizado.
         """)

st.write("#### 3.1. Qual diferença a Internet faz nos estudos?")

soma_sem_net = 0 # soma das notas dos estudantes sem internet
soma_com_net = 0 # mesma coisa para os sem internet
quant_sem_net = 0 # quantidade acumulativa de estudantes sem internet
quant_com_net = 0 # mesma coisa para os sem internet

for index, row in df.iterrows():
    if row['Internet_Access'] == 'Yes':
        soma_com_net += row['Exam_Score']
        quant_com_net += 1
    else:
        soma_sem_net += row['Exam_Score']
        quant_sem_net += 1

media_sem = soma_sem_net/quant_sem_net
media_com = soma_com_net/quant_com_net

categorias = ['Sem acesso', 'Com acesso']
medias = [media_sem, media_com]

grafico_net = pd.DataFrame({
    'Acesso a internet': categorias,
    'Média': medias
}).set_index('Acesso a internet')  

st.write("O gráfico abaixo mostra a média dos estudantes com e sem acesso à internet.")

st.bar_chart(grafico_net)

st.write("A diferença média de pontos entre pessoas que tem acesso a Internet e pessoas que não tem acesso a Internet: 0.75 pontos no exame final. Portanto, a Internet não é um grande impecílio para os estudos no contexto do dataset, uma vez que a diferença de pontos no exame final é pequena")

st.write("#### 3.2. Estudantes que possuem dificuldade de aprendizado possuem acesso a recursos?")

tabela_contingencia_percentual_total = pd.crosstab(
                                        df['Learning_Disabilities'],
                                        df['Access_to_Resources'],
                                        normalize = True,
                                        margins = True,
                                        margins_name = "Percentual de alunos"
                                        ).mul(100).round(1)

st.dataframe(tabela_contingencia_percentual_total)

st.write("Nesse contexto, apenas 10,5% dos estudantes possuem dificuldade de aprendizado.")

tabela_contingencia_dif_aprend = pd.crosstab(
                                    df['Learning_Disabilities'],
                                    df['Access_to_Resources'],
                                    normalize = "index",
                                    margins = True,
                                    margins_name = "total"
                                    ).mul(100).round(1)

tabela_contingencia_dif_aprend.drop('total', axis=0, inplace=True)

st.write("O gráfico abaixo mostra a distribuição de recursos de acesso à internet para estudantes com deficiência de aprendizagem.")

st.bar_chart(tabela_contingencia_dif_aprend)

st.write("Independentemente de o aluno ter ou não deficiência de aprendizagem, os percentuais de acesso a recursos são bem parecidos, sendo esse acesso médio para ambas as categorias.")

# Rendimento dos alunos baseado na quantidade de aulas de reforço

qtd_alunos_aulas_por_semana = [0, 0, 0, 0, 0, 0, 0, 0] # Quantidade de alunos que fazem x aulas de reforço por semana x[0, 8]
soma_nota_alunos = [0, 0, 0, 0, 0, 0, 0, 0] # Soma das notas dos alunos

# Conta quantos alunos e soma suas notas
for index, row in df.iterrows():
    match row['Tutoring_Sessions']:
        case 0:
            qtd_alunos_aulas_por_semana[0] += 1
            soma_nota_alunos[0] += row['Exam_Score']
        case 1:
            qtd_alunos_aulas_por_semana[1] += 1
            soma_nota_alunos[1] += row['Exam_Score']
        case 2:
            qtd_alunos_aulas_por_semana[2] += 1
            soma_nota_alunos[2] += row['Exam_Score']
        case 3:
            qtd_alunos_aulas_por_semana[3] += 1
            soma_nota_alunos[3] += row['Exam_Score']
        case 4:
            qtd_alunos_aulas_por_semana[4] += 1
            soma_nota_alunos[4] += row['Exam_Score']
        case 5:
            qtd_alunos_aulas_por_semana[5] += 1
            soma_nota_alunos[5] += row['Exam_Score']
        case 6:
            qtd_alunos_aulas_por_semana[6] += 1
            soma_nota_alunos[6] += row['Exam_Score']
        case 7:
            qtd_alunos_aulas_por_semana[7] += 1
            soma_nota_alunos[7] += row['Exam_Score']

media_nota_alunos = [0, 0, 0, 0, 0, 0, 0, 0] # Média das notas dos alunos

# Calcula a média
for i in range(8):
    media_nota_alunos[i] = soma_nota_alunos[i] / qtd_alunos_aulas_por_semana[i]


data = {
    "Categorias": ["Nenhuma", "Uma aula", "Duas aulas", "Três aulas", "Quatro aulas", "Cinco aulas", "Seis aulas", "Sete aulas"],
    "Valores": qtd_alunos_aulas_por_semana
}

fig = pd.DataFrame(data)
fig["Categorias"] = pd.Categorical(
    fig["Categorias"], 
    categories=["Nenhuma", "Uma aula", "Duas aulas", "Três aulas", "Quatro aulas", "Cinco aulas", "Seis aulas", "Sete aulas"],
    ordered=True
)

fig = fig.set_index("Categorias")

st.write("#### 3.3. As aulas de roforços geram resultados no desempenho dos alunos?")

st.write("O Gráfico abaixo relaciona a quantidade de alunos com a quantidade de aulas de reforço semanais frequentadas.")
st.bar_chart(fig)


st.write("O Gráfico abaixo mostra o impacto das aulas de reforço nas notas dos alunos.")

data = {
    "Categorias": ["Nenhuma", "Uma aula", "Duas aulas", "Três aulas", "Quatro aulas", "Cinco aulas", "Seis aulas", "Sete aulas"],
    "Valores": media_nota_alunos
}

fig = pd.DataFrame(data)
fig["Categorias"] = pd.Categorical(
    fig["Categorias"], 
    categories=["Nenhuma", "Uma aula", "Duas aulas", "Três aulas", "Quatro aulas", "Cinco aulas", "Seis aulas", "Sete aulas"],
    ordered=True
)
fig = fig.set_index("Categorias")
st.bar_chart(fig)

st.write("A partir disso, podemos concluir que aulas de reforço extra fazem diferença consideravel na nota final do estudantes, sendo seis aulas o 'Número ótimo', talvez sete aulas sejam demais, pois é necessário que o estudante tenha tempo para estudar sozinho.")

# Distribuição de notas no exame final

st.write("### 4.  Distribuição de notas no exame final")
st.write("O gráfico abaixo mostra a distribuição de frequência de notas")

data = {
    "Notas": df["Exam_Score"]
}

notas = pd.DataFrame(data)

# Criar o gráfico de distribuição
fig, ax = plt.subplots(figsize=(8, 6))
ax.hist(notas['Notas'], bins=45, color='blue', alpha=0.7)
ax.set_title('Distribuição de Frequência de Notas')
ax.set_xlabel('Nota')
ax.set_ylabel('Frequência')

# Mostrar o gráfico no Streamlit
st.pyplot(fig)

st.write("Vemos que nesse dataset, são muito comuns as notas entre 60-75 pontos no exame final e poquíssimas notas acima ou abaixo disso.")

# Analisando horas de estudo e seu impacto

st.write("""
         ### 5. Analisando horas de estudo e seu impacto
         Atualmente, uma das grandes habilidades a se ter é de ser eficiente com o seu tempo ao longo do dia. Para os estudos não é diferente, então, nesse tópico, serão abordadas algumas análises sobre o seu gasto de tempo com diferentes tarefas, como o estudo ou o sono e a sua determinada eficácia.
         """)

# Distribuição das horas de estudo por nota no exame

st.write("""
#### 5.1 Distribuição das horas de estudo por nota no exame
Aqui analisamos a relação entre as notas dos exames e as horas estudadas, usando um gráfico de densidade 3D interativo.
""")

# Verificar se as colunas necessárias estão presentes
if 'Exam_Score' in df.columns and 'Hours_Studied' in df.columns:
    # Dados relevantes
    x = df['Exam_Score']
    y = df['Hours_Studied']

    # Gerar densidade 3D com intervalos fixos
    xy = np.vstack([x, y])
    kde = gaussian_kde(xy)
    x_grid, y_grid = np.meshgrid(np.linspace(60, 75, 30),
                                 np.linspace(10, 30, 30))
    z_grid = kde(np.vstack([x_grid.ravel(), y_grid.ravel()])).reshape(x_grid.shape)

    # Criar gráfico interativo com Plotly
    fig = go.Figure(data=[
        go.Surface(
            z=z_grid,
            x=x_grid,
            y=y_grid,
            colorscale="Viridis",
            showscale=True,
            opacity=0.9
        )
    ])

    # Atualizar layout do gráfico
    fig.update_layout(
        title="Distribuição 3D da frequência de horas estudadas e notas no exame",
        scene=dict(
            xaxis_title="Nota no exame",
            yaxis_title="Horas estudadas",
            zaxis_title="Densidade",
            zaxis=dict(visible=False)  # Ocultar o eixo Z
        ),
    )

    # Mostrar o gráfico interativo no Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
st.write("Podemos ver no gráfico acima que há uma pequena melhora na nota em função da quantidade de estudo vista na frequência de pessoas que estudam mais de 22.5 horas semanais. Além disso, é perceptível que estudar mais do que a média, praticamente anula as chances de obter um resultado considerado ruim na prova")

# Distribuição das horas de sono por horas de estudo (até que ponto vale a pena trocar o sono por estudos?)

st.write("""
#### 5.2 Distribuição das horas de sono por horas de estudo (até que ponto vale a pena trocar o sono por estudos?)
Aqui analisamos a relação entre as notas dos exames e as horas estudadas, usando um gráfico de densidade 3D interativo.
""")

# Definir as variáveis
x = df['Sleep_Hours']
y = df['Hours_Studied']

# Estimativa de densidade de Kernel
xy = np.vstack([x, y])
kde = gaussian_kde(xy)
x_grid, y_grid = np.meshgrid(np.linspace(4, 10, 6), np.linspace(10, 30, 20))
z_grid = kde(np.vstack([x_grid.ravel(), y_grid.ravel()])).reshape(x_grid.shape)

# Criar o gráfico 3D com plotly
fig = go.Figure(data=[go.Surface(z=z_grid, x=x_grid, y=y_grid, colorscale='Viridis')])

# Adicionar detalhes ao gráfico
fig.update_layout(
    title='Distribuição 3D da frequência de horas estudadas e horas de sono',
    scene=dict(
        xaxis_title='Horas de sono médio por noite',
        yaxis_title='Horas estudadas',
        zaxis_title='Densidade',
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    # Habilitar zoom interativo
    scene_camera=dict(
        eye=dict(x=1.25, y=1.25, z=0.75)
    )
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

st.write("Pelo que pode-se observar, parece haver um pequeno trade-off entre a quantidade de horas de estudo e a quantidade de sono, podemos ver que a distribuição conjunta é um pouco mais deslocada e elevada no sentido de mais horas de sono e menos horas de estudo, sendo assim, podemos observar uma frequência em estudantes que dormem mais em estudar menos (já que sobra menos tempo aos mesmos para realizar tal). Além dessa análise podemos observar no pico do gráfico que a maioria dos estudantes estuda entre 17 e 22 horas semanais e dorme 7 horas por dia")

# Analisando diferentes distribuições de notas em função do sono

st.write("""
#### 5.3 Analisando diferentes distribuições de notas em função do sono
Aqui analisamos a relação entre as notas dos exames e as horas estudadas, usando um gráfico de densidade 3D interativo.
""")

# Dividir o dataframe por horas de sono
df_7 = df[df['Sleep_Hours'] == 7]
df_8 = df[df['Sleep_Hours'] == 8]
df_4 = df[df['Sleep_Hours'] == 4]
df_10 = df[df['Sleep_Hours'] == 10]

# Função para calcular a densidade KDE
def kde_plot_data(data, grid_points=500):
    kde = gaussian_kde(data)
    grid = np.linspace(data.min(), data.max(), grid_points)
    density = kde(grid)
    return grid, density

# Calcular as densidades para cada grupo de horas de sono
x_7, y_7 = kde_plot_data(df_7['Exam_Score'])
x_8, y_8 = kde_plot_data(df_8['Exam_Score'])
x_4, y_4 = kde_plot_data(df_4['Exam_Score'])
x_10, y_10 = kde_plot_data(df_10['Exam_Score'])

# Criando a figura para o Plotly
fig = go.Figure()

# Adicionando as curvas de densidade para cada grupo de horas de sono
fig.add_trace(go.Scatter(
    x=x_7, y=y_7, mode='lines', name='Sleep = 7 hours', line=dict(width=3)
))
fig.add_trace(go.Scatter(
    x=x_8, y=y_8, mode='lines', name='Sleep = 8 hours', line=dict(width=3)
))
fig.add_trace(go.Scatter(
    x=x_4, y=y_4, mode='lines', name='Sleep = 4 hours', line=dict(width=3)
))
fig.add_trace(go.Scatter(
    x=x_10, y=y_10, mode='lines', name='Sleep = 10 hours', line=dict(width=3)
))

# Ajustando o layout para adicionar título, labels e permitindo zoom
fig.update_layout(
    title='Distribuição de Notas por Horas de Sono',
    xaxis_title='Nota no Exame',
    yaxis_title='Densidade',
    hovermode='closest',
    xaxis=dict(range=[50, 80]),
    yaxis=dict(range=[0, 0.05]),  # Ajustar conforme necessário
)

# Exibindo o gráfico interativo no Streamlit
st.plotly_chart(fig)

st.write("Esse gráfico mostra que surpreendentemente a performance dos estudantes não varia muito em função das horas de sono já que as 4 distribuições são muito parecidas, porém gostariamos de mostrar um gráfico ainda mais interessante, que analisa as notas mais altas do dataset:")

# Filtrar os dados para considerar apenas as notas entre 80 e 100
mask_7 = (x_7 >= 80) & (x_7 <= 100)
mask_8 = (x_8 >= 80) & (x_8 <= 100)
mask_4 = (x_4 >= 80) & (x_4 <= 100)
mask_10 = (x_10 >= 80) & (x_10 <= 100)

# Atualizar os dados filtrados para cada grupo
x_7, y_7 = x_7[mask_7], y_7[mask_7]
x_8, y_8 = x_8[mask_8], y_8[mask_8]
x_4, y_4 = x_4[mask_4], y_4[mask_4]
x_10, y_10 = x_10[mask_10], y_10[mask_10]

# Criando a figura para o Plotly
fig = go.Figure()

# Adicionando as curvas de densidade para cada grupo de horas de sono
fig.add_trace(go.Scatter(
    x=x_7, y=y_7, mode='lines', name='Sleep = 7 hours', line=dict(width=3)
))
fig.add_trace(go.Scatter(
    x=x_8, y=y_8, mode='lines', name='Sleep = 8 hours', line=dict(width=3)
))
fig.add_trace(go.Scatter(
    x=x_4, y=y_4, mode='lines', name='Sleep = 4 hours', line=dict(width=3)
))
fig.add_trace(go.Scatter(
    x=x_10, y=y_10, mode='lines', name='Sleep = 10 hours', line=dict(width=3)
))

# Ajustando o layout para adicionar título, labels e permitindo zoom
fig.update_layout(
    title='Distribuição de Notas por Horas de Sono (Notas entre 80 e 100)',
    xaxis_title='Nota no Exame',
    yaxis_title='Densidade',
    hovermode='closest',
    xaxis=dict(range=[80, 100]),  # Definindo o intervalo do eixo X entre 80 e 100
    yaxis=dict(range=[0, 0.01]),  # Definindo o intervalo do eixo Y
    template="plotly_white"  # Usando um tema claro
)

# Exibindo o gráfico interativo no Streamlit
st.plotly_chart(fig)


st.write("Podemos ver aqui que vários estudantes que dormem 4 horas por noite acabaram com nota 100% (isso é claro, apenas 0.2% de todas as amostras do dataset, sendo basicamente outliers) mas ainda sim isso mostra que esses estudantes provavelmente são do tipo de estudar noites e madrugadas na véspera da prova, a espera de um bom resultado...")

# Matriz Correlacional

st.write("""
         ### 6. Matriz Correlacional
         Com a demonstração dessa matriz, temos o objetivo de entender quais são os fatores que estão mais relacionados com o bom resultado em exames desse dataset.
         """)

# Definir o estilo dark
plt.style.use('dark_background')  # Definindo o estilo de fundo escuro

# Colunas categóricas
categorical_columns = df.select_dtypes(include=['object']).columns

# Codificando variáveis categóricas
df_encoded = pd.get_dummies(df, columns=categorical_columns, drop_first=True)

# Aplicando Label Encoding para variáveis categóricas
label_encoder = LabelEncoder()  # classe para converter strings em categorias numéricas
for col in categorical_columns:
    df[col] = label_encoder.fit_transform(df[col])

# Matriz de correlação
correlation_matrix = df.corr()

# Plotando a matriz de correlação com fundo escuro
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', 
            annot_kws={'size': 8},  # Reduzir o tamanho da fonte
            linewidths=0.5,  # Aumentar o espaçamento entre as células
            cbar_kws={'label': 'Correlacao'}, 
            vmin=-0.1, vmax=1)  # Ajustando os limites para -0.1 até 1

plt.title("Matriz Correlacional", fontsize=16, color='white')  # Título em cor branca
plt.xlabel("Variáveis", fontsize=12, color='white')  # Rótulo do eixo X em branco
plt.ylabel("Variáveis", fontsize=12, color='white')  # Rótulo do eixo Y em branco

# Exibir o gráfico no Streamlit
st.pyplot(plt)

st.write("Podemos ver que os parâmetros mais relevantes para a nota final são: Presença nas aulas e Horas estudadas, já tinhamos atestado isso para horas estudadas em um gráfico anterior, mas não tinhamos feito isso para a presença, vamos plotar algum gráfico referente a isso no próximo tópico")

#  Distribuição Conjunta de Presença nas Aulas e Nota no Exame Final

st.write("### 7. Distribuição Conjunta de Presença nas Aulas e Nota no Exame Final")

# Definindo as variáveis para o gráfico
x = df['Exam_Score']
y = df['Attendance']

# Calculando a densidade usando gaussian_kde
xy = np.vstack([x, y])
kde = gaussian_kde(xy)
x_grid, y_grid = np.meshgrid(np.linspace(60, 75, 30), np.linspace(55, 100, 50))
z_grid = kde(np.vstack([x_grid.ravel(), y_grid.ravel()])).reshape(x_grid.shape)

# Criando uma visualização 3D interativa com Plotly
fig = go.Figure(data=[go.Surface(
    z=z_grid,
    x=x_grid,
    y=y_grid,
    colorscale='Viridis',
    colorbar=dict(title='Densidade'),
)])

# Configuração do layout para o gráfico 3D
fig.update_layout(
    title='Distribuição 3D da Frequência de Presença e Notas no Exame',
    scene=dict(
        xaxis_title='Nota no Exame',
        yaxis_title='Presença nas Aulas',
        zaxis_title='Densidade',
        camera_eye=dict(x=2, y=2, z=2),  # Posição inicial da câmera para visualização
    ),
    margin=dict(l=0, r=0, b=0, t=50),
    width=800, height=600
)

# Exibir o gráfico interativo no Streamlit
st.plotly_chart(fig)

st.write("E depois de olhar o gráfico de cima podemos ver uma clara melhora na nota de acordo com a presença nas aulas:")
st.markdown(""" 
- Alunos que vão a 60%-65% das aulas tendem a ter uma nota entre 62-64 pontos
- Alunos que vão a 95%-100% das aulas tendem a ter uma nota entre 68-72 pontos          
            """)
st.write("Apenas ir a mais aulas (se estivermos falando de 1 semestre por exemplo, ir a mais 2 ou 3 aulas) pode ter render de 4 a 10 pontos a mais no exame final.")


















