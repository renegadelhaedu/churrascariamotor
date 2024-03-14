from flask import *
import dao
import dataanalise as da
import plotly.express as px

app = Flask(__name__)


@app.route('/salvarcorrelacaobd', methods=['POST'])
def salvarcorrelacao():
    ind1 = request.form.get('ind1')
    ind2 = request.form.get('ind2')
    correlacao = request.form.get('valorcorrelacao')

    if dao.insert_correlacao(dao.conectardb(), ind1, ind2, correlacao):
        return render_template('paginasucesso.html')
    else:
        return render_template('paginaerro.html')


@app.route('/correlacaoindicadores', methods=['GET', 'POST'])
def calcular_correlacao_individual():
    if request.method == 'GET':
        return render_template('escolherindicadores.html')
    else:
        ind1 = request.form.get('indicador1')
        ind2 = request.form.get('indicador2')
        dados, correlacao = da.correlacionar_indicadores(ind1, ind2)
        dados.columns = [ind1, ind2] #renomeado as colunas
        #normalizei os dados
        dados = (dados-dados.min())/(dados.max()-dados.min())
        fig = px.line(dados, x=dados.index, y=list(dados.columns))
        return render_template('correlacaoresultado.html', plot=fig.to_html(), valor=correlacao, ind1=ind1, ind2=ind2)

#        return f'<h1>{correlacao}</h1>'


@app.route('/cadastrarusuario', methods=['GET', 'POST'])
def redirecionar_cadastro_user():
    if request.method == 'GET':
        return render_template('cadastrarusuario.html')
    elif request.method == 'POST':
        login = str(request.form.get('nome'))
        senha = str(request.form.get('senha'))

        if dao.inseriruser(login, senha, dao.conectardb()):
            return render_template('index2.html')
        else:
            texto= 'e-mail já cadastrado'
            return render_template('cadastrarusuario.html', msg=texto)

@app.route('/login', methods=['POST'])
def cadastrar_usuario():
    nome = str(request.form.get('nome'))
    senha = str(request.form.get('senha'))
    if (dao
            .verificarlogin(nome, senha, dao.conectardb())):
        return render_template('menu.html')
    else:
        return render_template('index2.html')

@app.route('/grafvioleciapib', methods=['POST','GET'])
def gerarGrafViolenciaPib():
    if request.method == 'POST':
        filtro = int(request.form.get('valor'))
    else:
        filtro = 10

    dados = da.lerdados()
    dados.drop(dados.sort_values(by=['cvli'], ascending=False).head(3).index, inplace=True)
    dados.drop(dados.sort_values(by=['rendapercapita'], ascending=False).head(filtro).index, inplace=True)
    dados.drop(dados.sort_values(by=['rendapercapita'], ascending=True).head(2).index, inplace=True)

    fig = px.scatter(dados, x='rendapercapita', y='cvli', hover_data=['municipio'])
    return render_template('grafviolenciapib.html', plot=fig.to_html())

@app.route('/grafcorrelacao')
def gerarGrafCorrelacao():
    dados = da.lerdados()
    fig2 = da.exibirmapacorrelacoes(dados)

    return render_template('grafcorrelacao.html', mapa=fig2.to_html())

@app.route('/melhoresedu')
def exibirmunicipiosedu():
    data = da.lerdados()

    data['somaedu'] = data['idebanosiniciais'] + data['idebanosfinais']
    data.sort_values(by=['somaedu'], ascending=False, inplace=True)
    fig = da.exibirgraficobarraseduc(data.head(15))

    return render_template('melhoresedu.html', figura=fig.to_html())

@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/')
def motormanda():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)