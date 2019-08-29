from flask import Flask, request

app = Flask(__name__)


@app.route('/soma/<int:a>/<int:b>')
def soma(a,b):
    return f'Resultado: {a + b}'

@app.route('/')
def hello():

    nome = request.args.get('nome','desconhecido')

    return f'Hello World, {nome}!'


if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)