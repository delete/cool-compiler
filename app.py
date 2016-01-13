from flask import Flask
from flask import render_template, request

from analise_lex import MyLex

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def hello():
    llex = ()
    lerror = ()
    codigo = ''

    if request.method == 'POST':
        codigo = request.form['codigo']
        l = MyLex()
        llex, lerror = l.tokenize(codigo)

    return render_template(
        'index.html', llex=llex, lerror=lerror, codigo=codigo
    )


if __name__ == "__main__":
    app.run(debug=True)
