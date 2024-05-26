# Importa as bibliotecas necessárias
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Configura o SQLAlchemy com o URI do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'

# Cria um objeto SQLAlchemy associado à aplicação Flask
db = SQLAlchemy(app)

# Define o modelo de dados para o formulário
class DadosFormulario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cip = db.Column(db.String(200), nullable=False)
    encomenda = db.Column(db.String(20), nullable=False)
    orgao = db.Column(db.String(200), nullable=False)
    datarec = db.Column(db.String(10), nullable=False)
    pi = db.Column(db.String(200), nullable=False)
    motivo = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    novidades = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.String(200), nullable=False)
    audi = db.Column(db.String(200), nullable=False)


# Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()

# Define a rota da página inicial e a função correspondente
@app.route('/')
def home():
    # Renderiza o template do formulário
    return render_template('formulario.html')

# Define a rota para enviar dados do formulário
@app.route('/enviar', methods=['POST'])
def enviar():
    # Obtém os dados do formulário
    cip = request.form['cip']
    encomenda = request.form['encomenda']
    orgao = request.form['orgao']
    datarec = request.form['datarec']
    pi = request.form['pi']
    motivo = request.form['motivo']
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    novidades = request.form['novidades']
    mensagem = request.form['mensagem']
    audi = request.form['audi']

    # Cria um novo registro com os dados recebidos
    novo_dado = DadosFormulario(cip=cip, encomenda=encomenda, orgao=orgao, datarec=datarec, pi=pi, motivo=motivo, nome=nome, telefone=telefone, email=email, novidades=novidades, mensagem=mensagem, audi=audi)

    # Adiciona e salva o novo registro no banco de dados
    db.session.add(novo_dado)
    db.session.commit()

    # Redireciona para a página de listagem
    return redirect(url_for('listar'))

# Define a rota para listar os registros
@app.route('/listar')
def listar():
    # Busca todos os registros no banco de dados
    dados = DadosFormulario.query.all()

    # Renderiza o template de lista, passando os registros
    return render_template('lista.html', dados=dados)

# Define a rota para deletar um registro específico
@app.route('/deletar/<int:id>')
def deletar(id):
    # Busca o registro pelo ID e, se não encontrar, retorna erro 404
    dado_para_deletar = DadosFormulario.query.get_or_404(id)

    # Deleta o registro do banco de dados
    db.session.delete(dado_para_deletar)
    db.session.commit()

    # Redireciona para a página de listagem
    return redirect(url_for('listar'))

# Verifica se o script é o principal e executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)