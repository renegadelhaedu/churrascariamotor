from flask import *
import dao
import dataanalise as da
import plotly.express as px

app = Flask(__name__)

@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    nome = str(request.form.get('nome'))
    senha = str(request.form.get('senha'))

    if dao.verificarlogin(nome, senha):
        dados = da.analisar2()
        fig = px.scatter(dados, x='rendapercapita', y='idebanosfinais', hover_data=['municipio'])
        return render_template('verificado.html', login=nome, plot=fig.to_html())
    else:
        return render_template('index.html')


@app.route('/')
def motormanda():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)