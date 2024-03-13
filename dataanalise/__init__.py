import pandas as pd
import plotly.express as px

#https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries
def consulta_bc(codigo_bcb):
  url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
  df = pd.read_json(url)
  df['data'] = pd.to_datetime(df['data'], dayfirst=True)
  df.set_index('data', inplace=True)
  return df

def converterIndicadorCodigo(indicador):
    if indicador == 'selic':
        return '432'
    elif indicador == 'ipca':
        return '433'
    elif indicador == 'pib':
        return '4192'

def correlacionar_indicadores(indicador1, indicador2):
    code1 = converterIndicadorCodigo(indicador1)
    code2 = converterIndicadorCodigo(indicador2)

    dados1 = consulta_bc(code1)
    dados2 = consulta_bc(code2)
    dados1 = dados1[dados1.index >= '2014-01-01']
    #dados1 = dados1.resample('1m').mean()

    dados2 = dados2[dados2.index >= '2014-01-01']
    #dados2 = dados2.resample('1m').mean()
    dados2.drop(dados2.index[-1], inplace=True)

    geral = pd.concat([dados1, dados2], axis=1)

    return geral.corr().values[0][1]


def analisar():
    dados = pd.read_html('https://pt.wikipedia.org/wiki/Lista_de_munic%C3%ADpios_do_Brasil_por_taxa_de_homic%C3%ADdios')
    mais250 = dados[0]
    menores = dados[1]
    print(dados[0])

def lerdados():
    dados = pd.read_csv('dadosindicadoresPB3.csv')
    #excluir colunas
    dados.drop(columns=['code'], inplace=True)
    return dados

def exibirmapacorrelacoes(data):
    data.drop(columns=['municipio'], inplace=True)
    fig = px.imshow(data.corr())
    return fig

def exibirgraficobarraseduc(dados):
    fig = px.bar(dados, x='municipio', y='somaedu')
    return fig

