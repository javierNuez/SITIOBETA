from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('sitio/index.html')


@app.route('/admin')
def admin_index():
    return render_template('admin/index.html')


@app.route('/admin/loguin')
def admin_loguin():
    return render_template('/admin/loguin.html')


@app.route('/pedidos')
def pedidos():
    return render_template('admin/pedidos.html')


@app.route('/clientes')
def clientes():
    return render_template('admin/clientes.html')


@app.route('/productos')
def productos():
    return render_template('admin/productos.html')


@app.route('/droguerias')
def droguerias():
    return render_template('admin/droguerias.html')


@app.route('/usuarios')
def usuarios():
    return render_template('admin/usuarios.html')


@app.route('/modulos')
def modulos():
    return render_template('admin/modulos.html')


if __name__ == '__main__':
    app.run(debug=True)
