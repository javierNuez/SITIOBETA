
from flask import Flask
from flask import render_template, request, redirect, flash
from flaskext.mysql import MySQL

app = Flask(__name__)


app.secret_key = "vigoray"
mysql = MySQL()

mysql = MySQL()


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sitiobeta'
mysql.init_app(app)


@app.route('/')
def inicio():
    return render_template('sitio/index.html')


@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')


@app.route('/admin/loguin')
def admin_loguin():
    return render_template('admin/loguin.html')
# funciones de oferta comercial:


@app.route('/admin/ofertas/borrar', methods=['POST'])
def admin_ofertas_borrar():
    _id = request.form['txtID']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM ofertas where id_o=%s;", (_id))
    pedido = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/ofertas')


@app.route('/admin/ofertas/guardar', methods=['POST'])
def admin_ofertas_guardar():

    _modulo = request.form['txtModulo']
    _producto = request.form['txtProducto']
    _minima = request.form['txtMinima']
    _descuento = request.form['txtDescuento']

    if _modulo == '' or _producto == '' or _minima == '' or _descuento == '':
        flash('¡Por favor llenar todos los campos!')
        return redirect('/admin/ofertas')
    sql = "INSERT INTO `ofertas` (`id_o`, `o_modulo`, `o_producto`, `o_minima`, `o_descuento`) VALUES (NULL, %s,%s,%s,%s);"
    datos = (_modulo, _producto, _minima, _descuento)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/ofertas')


@app.route('/admin/ofertas')
def admin_ofertas():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `ofertas`;")
    ofertas = cursor.fetchall()
    conexion.commit()
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    conexion.commit()
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `productos`;")
    productos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/ofertas.html', ofertas=ofertas, modulos=modulos, productos=productos)


@app.route('/admin/editarOfertas/<int:id>')
def admin_ofertas_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `ofertas` WHERE id_o=%s;", (id))
    ofertas = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarOferta.html', ofertas=ofertas)


# funciones de usuarios:


@app.route('/admin/usuarios')
def admin_usuarios():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios`;")
    usuarios = cursor.fetchall()
    conexion.commit()

    return render_template('admin/usuarios.html', usuarios=usuarios)


@app.route('/admin/editarUsuarios/<int:id>')
def admin_usuarios_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios` WHERE id_u=%s;", (id))
    usuarios = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarUsuario.html', usuarios=usuarios)


@app.route('/admin/usuarios/borrar/<int:id>')
def admin_usuarios_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios where id_u=%s;", (id))
    usuarios = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/usuarios')


@app.route('/admin/editarUsuario/editar', methods=['POST'])
def admin_usuarios_editar():

    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _rrdzz = request.form['txtRrdzz']
    _mail = request.form['txtMail']
    _desde = request.form['txtDesde']
    _hasta = request.form['txtHasta']
    _pass = request.form['txtPass']
    _id = request.form['txtID']

    sql = "UPDATE usuarios SET u_nombre=%s, u_apellido=%s, u_rrdzz=%s, u_mail=%s, u_desde=%s, u_hasta=%s, u_pass=%s WHERE id_u=%s;"
    datos = (_nombre, _apellido, _rrdzz, _mail, _desde, _hasta, _pass, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/usuarios')


@app.route('/admin/usuarios/guardar', methods=['POST'])
def admin_usuarios_guardar():

    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _rrdzz = request.form['txtRrdzz']
    _mail = request.form['txtMail']
    _desde = request.form['txtDesde']
    _hasta = request.form['txtHasta']
    _pass = request.form['txtPass']

# condicional para usar mensajes
    if _nombre == '' or _apellido == '' or _rrdzz == '' or _mail == '' or _desde == '' or _hasta == '' or _pass == '':
        flash('¡Por favor llenar todos los campos!')
        return redirect('/admin/usuarios')

    sql = "INSERT INTO `usuarios` (`id_u`, `u_nombre`, `u_apellido`, `u_rrdzz`, `u_mail`, `u_desde`, `u_hasta`, `u_pass`) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s);"
    datos = (_nombre, _apellido, _rrdzz, _mail, _desde, _hasta, _pass)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/usuarios')
# funciones de productos:


@app.route('/admin/productos')
def admin_productos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `productos`;")
    productos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/productos.html', productos=productos)


@app.route('/admin/editarProducto/<int:id>')
def admin_producto_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `productos` WHERE id_p=%s;", (id))
    productos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarProducto.html', productos=productos)


@app.route('/admin/productos/guardar', methods=['POST'])
def admin_productos_guardar():

    _codigo = request.form['p_cod']
    _desc = request.form['p_descripcion']
    _desde = request.form['p_desde']
    _hasta = request.form['p_hasta']

    sql = "INSERT INTO `productos` (`id_p`, `p_cod`, `p_descripcion`, p_desde, p_hasta) VALUES (NULL, %s,%s,%s,%s);"
    datos = (_codigo, _desc, _desde, _hasta)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/productos')


@app.route('/admin/productos/borrar/<int:id>')
def admin_productos_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos where id_p=%s;", (id))
    usuarios = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/productos')


@app.route('/admin/editarProducto/editar', methods=['POST'])
def admin_productos_editar():

    _cod = request.form['p_cod']
    _desc = request.form['p_descripcion']
    _desde = request.form['p_desde']
    _hasta = request.form['p_hasta']
    _id = request.form['txtID']

    sql = "UPDATE productos SET p_cod=%s, p_descripcion=%s, p_desde =%s, p_hasta=%s WHERE id_p=%s;"
    datos = (_cod, _desc, _desde, _hasta, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/productos')
# funciones de pedidos:


@app.route('/admin/pedidos')
def admin_pedidos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `pedidos`;")
    pedidos = cursor.fetchall()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('admin/pedidos.html', pedidos=pedidos, droguerias=droguerias)


@app.route('/admin/pedidos/guardar', methods=['POST'])
def admin_pedidos_guardar():

    _droguerias = request.form['pe_droguerias']
    _codigo = request.form['pe_cod']
    _cuit = request.form['pe_cuit']
    _postal = request.form['pe_postal']
    _nombre = request.form['pe_nombre']
    _localidades = request.form['pe_localidades']
    _domicilio = request.form['pe_domicilio']

    sql = "INSERT INTO `pedidos` (`id_pe`, `pe_droguerias`, `pe_cod`, `pe_cuit`,`pe_postal`, `pe_nombre`,`pe_localidades`,`pe_domicilio`) VALUES (NULL, %s,%s, %s,%s, %s,%s, %s);"
    datos = (_droguerias, _codigo, _cuit, _postal,
             _nombre, _localidades, _domicilio)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/pedidos')


@app.route('/admin/pedidos/borrar', methods=['POST'])
def admin_pedidos_borrar():
    _id = request.form['txtID']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pedidos where id_pe=%s;", (_id))
    pedido = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/pedidos')

# funciones de clientes:


@app.route('/admin/clientes')
def admin_clientes():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`;")
    clientes = cursor.fetchall()
    conexion.commit()

    return render_template('admin/clientes.html', clientes=clientes)


@app.route('/admin/editarCliente/<int:id>')
def admin_cliente_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes` WHERE id_c=%s;", (id))
    clientes = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarClientes.html', clientes=clientes)


@app.route('/admin/editarCliente/editar', methods=['POST'])
def admin_cliente_editar():

    _cod = request.form['c_cod']
    _cuenta = request.form['c_cuenta']
    _nombre = request.form['c_nombre']
    _cuit = request.form['c_cuit']
    _postal = request.form['c_postal']
    _localidad = request.form['c_localidad']
    _id = request.form['txtID']

    sql = "UPDATE clientes SET c_cod=%s, c_cuenta=%s, c_nombre =%s, c_cuit=%s, c_localidad=%s, c_postal=%s WHERE id_c=%s;"
    datos = (_cod, _cuenta, _nombre, _cuit, _localidad, _postal, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/clientes')


@app.route('/admin/clientes/guardar', methods=['POST'])
def admin_clientes_guardar():

    _codigo = request.form['c_cod']
    _cuenta = request.form['c_cuenta']
    _nombre = request.form['c_nombre']
    _cuit = request.form['c_cuit']
    _localidad = request.form['c_localidad']
    _postal = request.form['c_postal']

    sql = "INSERT INTO `clientes` (`id_c`, `c_cod`, `c_cuenta`, c_nombre, c_cuit, c_localidad, c_postal) VALUES (NULL, %s,%s,%s,%s,%s,%s);"
    datos = (_codigo, _cuenta, _nombre, _cuit, _localidad, _postal)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/clientes')


@app.route('/admin/clientes/borrar/<int:id>')
def admin_clientes_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM clientes where id_c=%s;", (id))
    clientes = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/clientes')

# funciones de droguerias:


@app.route('/admin/editarDroguerias/<int:id>')
def admin_droguerias_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias` WHERE id_d=%s;", (id))
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarDrogueria.html', droguerias=droguerias)


@app.route('/admin/droguerias')
def admin_droguerias():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('admin/droguerias.html', droguerias=droguerias)


@app.route('/admin/droguerias/guardar', methods=['POST'])
def admin_droguerias_guardar():

    _codigo = request.form['d_cod']
    _desc = request.form['d_descripcion']

    sql = "INSERT INTO `droguerias` (`id_d`, `d_cod`, `d_descripcion`) VALUES (NULL, %s,%s);"
    datos = (_codigo, _desc)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/droguerias')


@app.route('/admin/droguerias/borrar/<int:id>')
def admin_droguerias_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM droguerias where id_d=%s;", (id))
    usuarios = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/droguerias')


@app.route('/admin/editarDrogueria/editar', methods=['POST'])
def admin_droguerias_editar():

    _cod = request.form['txtCodigo']
    _desc = request.form['txtDescripcion']
    _id = request.form['txtID']

    sql = "UPDATE droguerias SET d_cod=%s, d_descripcion=%s WHERE id_d=%s;"
    datos = (_cod, _desc, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/droguerias')
# funciones de módulos:


@app.route('/admin/modulos')
def admin_modulos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/modulos.html', modulos=modulos)


@app.route('/admin/editarModulos/editar', methods=['POST'])
def admin_modulo_editar():

    _nombre = request.form['txtNombre']
    _titulo = request.form['txtTitulo']
    _pie = request.form['txtPie']
    _desde = request.form['txtDesde']
    _hasta = request.form['txtHasta']
    _id = request.form['txtID']

    sql = "UPDATE modulos SET m_nombre=%s, m_titulo=%s, m_pie=%s, m_desde=%s, m_hasta=%s WHERE id_m=%s;"
    datos = (_nombre, _titulo, _pie, _desde, _hasta, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/modulos')


@app.route('/admin/modulos/guardar', methods=['POST'])
def admin_modulos_guardar():

    _nombre = request.form['m_nombre']
    _titulo = request.form['m_titulo']
    _pie = request.form['m_pie']
    _desde = request.form['m_desde']
    _hasta = request.form['m_hasta']

    sql = "INSERT INTO `modulos` (`id_m`, `m_nombre`, `m_titulo`, `m_pie`, `m_desde`, `m_hasta`) VALUES (NULL, %s,%s,%s,%s,%s);"
    datos = (_nombre, _titulo, _pie, _desde, _hasta)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/modulos')


@app.route('/admin/modulos/borrar/<int:id>')
def admin_modulos_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM modulos where id_m=%s;", (id))
    modulos = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/modulos')


@app.route('/admin/editarModulos/<int:id>')
def admin_modulos_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos` WHERE id_m=%s;", (id))
    modulos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarModulo.html', modulos=modulos)


if __name__ == '__main__':
    app.run(debug=True)
