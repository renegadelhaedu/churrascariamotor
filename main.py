from flask import *
import dao

app = Flask(__name__)

@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    nome = str(request.form.get('nome'))
    senha = str(request.form.get('senha'))

    if dao.verificarlogin(nome, senha):
        return render_template('verificado.html', login=nome)
    else:
        return render_template('index.html')


@app.route('/')
def motormanda():
    return render_template('index.html')

app.run(debug=True)