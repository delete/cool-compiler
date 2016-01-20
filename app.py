from flask import Flask
from flask import render_template, request

from analise_lex import MyLex
from analise_sint import syntactic as syn


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/lexico", methods=['GET', 'POST'])
def lexico():
    llex = ()
    lerror = ()
    code = ''

    if request.method == 'POST':
        code = request.form['code']
        l = MyLex()
        llex, lerror = l.tokenize(code)

    return render_template(
        'lexico.html', llex=llex, lerror=lerror, code=code
    )


@app.route("/sintatico", methods=['GET', 'POST'])
def syntactic():
    code = ''
    result = []
    serror = []

    if request.method == 'POST':
        code = request.form['code']
        result, serror = syn(code)

    return render_template(
        'syntactic.html', result=result, serror=serror, code=code
    )

if __name__ == "__main__":
    app.run(debug=True)
