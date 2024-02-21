import pandas as pd

def analisar():
    dados = pd.read_html('https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_taxa_de_homic%C3%ADdios')

    mais250 = dados[0]
    menores = dados[1]

    print(dados[0])

def analisar2():
    dados = pd.read_csv('dadosindicadoresPB3.csv')
    dados.drop(columns=['code'],inplace=True)
    return dados

'''
['Municípios', 'Gentílico',
       'Salário médio mensal dos trabalhadores formais', 'PIB per capita',
       'IDEB – Anos finais do ensino fundamental (Rede pública)',
       'População no último censo']
'''