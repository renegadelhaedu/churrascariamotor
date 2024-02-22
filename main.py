from flask import *
import dao
import dataanalise as da
import plotly.express as px

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def cadastrar_usuario():
    nome = str(request.form.get('nome'))
    senha = str(request.form.get('senha'))

    if dao.verificarlogin(nome, senha):
        dados = da.analisar2()
        dados.drop(dados.sort_values(by=['cvli'], ascending=False).head(3).index, inplace=True)
        dados.drop(dados.sort_values(by=['rendapercapita'], ascending=False).head(10).index, inplace=True)
        dados.drop(dados.sort_values(by=['rendapercapita'], ascending=True).head(2).index, inplace=True)
        fig = px.scatter(dados, x='rendapercapita', y='cvli', hover_data=['municipio'])
        fig2 = da.exibirmapacorrelacoes(da.analisar2())

        return render_template('verificado.html', login=nome, plot=fig.to_html(), mapa=fig2.to_html())
    else:
        return render_template('index.html')


@app.route('/')
def motormanda():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)