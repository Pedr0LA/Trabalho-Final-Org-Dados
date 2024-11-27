import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv(r'trabalhoFinal\StudentPerformanceFactors.csv')

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

st.write("A diferença média de pontos entre pessoas que tem acesso a Internet e pessoas que não tem acesso a Internet: 0.75 pontos no exame final. Logo, a Internet não é um grande impecílio para os estudos no contexto do dataset, uma vez que a diferença de pontos no exame final é pequena.")

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
