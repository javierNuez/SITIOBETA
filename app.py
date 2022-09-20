

from locale import normalize
from random import randint
from audioop import add
from datetime import datetime
from lib2to3.pytree import convert
from unicodedata import numeric
from flask import Flask, jsonify
from flask import render_template, request, redirect, flash
from flaskext.mysql import MySQL
from datetime import date
import json
from datetime import date
from datetime import datetime

# Día actual
# today = date.today()

# Fecha actual y hora
# now = datetime.now()


app = Flask(__name__)


app.secret_key = "vigoray"
mysql = MySQL()


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sitiobeta'
mysql.init_app(app)


@app.route('/')
def inicio():

    return render_template('sitio/index.html')


# @app.route('/admin/')
# def open():

#    return render_template('admin/index.html')


@app.route('/apms/')
def apms_index():
    return render_template('apms/index.html')


@app.route('/apms/inicio')
def apms_inicio():
    return render_template('apms/inicio.html')


@app.route('/admin/inicio')
def admin_inicio():
    return render_template('admin/inicio.html')


@app.route('/sup/inicio')
def sup_inicio():
    return render_template('sup/inicio.html')


@ app.route('/admin/conformarOferta00')
def cargaOferta():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ofertas ORDER BY o_modulo;")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion.commit()
    # , usuarios=usuarios, _usuario=_usuario
    return render_template('admin/conformarOferta00.html', ofertas=ofertas, droguerias=droguerias, clientes=clientes)


@ app.route('/admin/conformarOferta01/drogueria/', methods=['POST'])
def ofer01():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cod_drogueria = %s;", (_drogueria))
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('admin/conformarOferta02.html', clientes=clientes, droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas)


@ app.route('/admin/conformarOferta02/cliente/', methods=['POST'])
def ofer02():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()
    conexion.commit()

    if _cliente == "Nuevo":
        return redirect('/admin/clientes')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cuenta = %s;", (_cliente))
    clientes = cursor.fetchall()

    conexion.commit()
    return render_template('admin/conformarOferta04.html', droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas, clientes=clientes)


@ app.route('/admin/conformarOferta04/cliente/', methods=['POST'])
def ofer04():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    _drogueria = request.form['txtDrogueria2']

    _cliente = request.form['txtCliente2']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()
    listaUnidades = []
    listaOfertaVigente = []
    for i in ofertas:
        uniList = {}
        uniList[f'{i[0]}'] = request.form[f'unidades{i[0]}']
        listaUnidades.append(uniList)
        listaOfertaVigente.append(i)
    # print(listaUnidades)
    ancho = len(ofertas)
    #print("Ancho:", ancho)
    conexion.commit()
    # print(usuarios)
    # print(listaOfertaVigente)
    # aca saco los modulos unicos
    modulos_ofertas = set()
    for i in ofertas:
        modulos_ofertas.add(i[1])
    # ---------------------------
    listaModOfer = list(modulos_ofertas)
    listaModOfer.sort()
    modulosT = len(listaModOfer)
    # print(listaModOfer)
    listaFinal = []
    for i in listaModOfer:
        listaModulo = []
        for x in ofertas:
            if i == x[1]:
                listaModulo.append(x)
        listaFinal.append(listaModulo)
    listaTerminal = zip(listaModOfer, listaFinal)
    salidaModulos = list(listaTerminal)
    print(salidaModulos)
    anchoModulos = len(salidaModulos)
    listaInput = []
    modulosFuncion = list(zip(listaModOfer, listaFinal))
    count = 0
    for i in modulosFuncion:
        m = i[0]  # el_modulo
        e = i[1]
        listaScript = []
        for x in e:  # elementos
            q = x[0]  # elemento
            listaScript.append(q)
        scriptTxt = str(listaScript)
        elScript = f"{scriptTxt}"
        listaInput.append(f'{m}:{elScript}')

    print(anchoModulos)
    listaInput = json.dumps(listaInput)
    print(listaInput)

    return render_template('admin/conformarOferta05.html', listaInput=listaInput, anchoModulos=anchoModulos, drogueria=_drogueria, cliente=_cliente, usuarios=usuarios, usuario=usuario, unidades=listaUnidades, ofertas=ofertas, salidas=salidaModulos)

# Aca esta la magia para devolver la pantalla segun el usuario----------------------------


@app.route('/sup')
def sup_of():
    usuario = request.form["hashUsuario"]

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidos` WHERE o_usuario_hash=%s;", (usuarios))
    pedidos = cursor.fetchall()
    conexion.commit()
    print(pedidos)

    return render_template('sup/pedidos.html', pedidos=pedidos)
    # return render_template('sup/index.html')


@app.route('/sup')
def sup_index():
    usuario = request.form['hasUsuario']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    conexion.commit()

    return render_template('sup/index.html', usuarios=usuarios)


# Aca esta la magia para devolver la pantalla segun el usuario----------------------------


@app.route('/admin/', methods=['POST'])
def admin_index():
    now = datetime.now()
    usuario = request.form['txtUsuario']
    contraseña = request.form['txtPassword']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "select * FROM usuarios where u_rrdzz =%s and u_pass =%s;", (usuario, contraseña))
    _usuario = cursor.fetchall()
    print(_usuario)
    conexion.commit()
    no = 'no'

    if _usuario:
        _fechaD = datetime.strptime(f"{_usuario[0][5]}", "%Y-%m-%d")
        _fechaH = datetime.strptime(f"{_usuario[0][6]}", "%Y-%m-%d")

        if _fechaD >= now or _fechaH <= now:
            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute(
                "UPDATE usuarios SET u_habilitado=%s WHERE u_hash=%s;", (no, _usuario[0][9]))
            conexion.commit()
            flash('Usuario bloqueado.')
            return redirect('/sitio/loguin')
        if _usuario[0][10] == "no":
            flash('Usuario no habilitado.')
            return redirect('/sitio/loguin')

        if _usuario[0][8] == "ADM":
            us = _usuario[0][9]
            return render_template('/admin/index.html', usuarioStorage=us)
        elif _usuario[0][8] == "SUP":
            us = _usuario[0][9]
            return render_template('/sup/index.html', usuarioStorage=us)

        elif _usuario[0][8] == "APM":
            us = _usuario[0][9]
            return render_template('/apms/index.html', usuarioStorage=us)
    else:
        flash('¡Usuario o contraseña, no válido!')
        return redirect('/sitio/loguin')


@app.route('/sitio/loguin')
def admin_loguin():
    return render_template('sitio/loguin.html')
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
    datos_modulo = [_modulo.split('#')]
    datos_producto = [_producto.split('#')]
    _obligatorio = request.form['txtObligatorio']
    if _modulo == '' or _producto == '' or _minima == '' or _descuento == '':
        flash('¡Por favor llenar todos los campos!')
        return redirect('/admin/ofertas')
    sql = "INSERT INTO `ofertas` (`id_o`, `o_modulo`,`o_mod_nom`,`o_mod_tit`,`o_mod_pie`,`o_mod_d`,`o_mod_h`, `o_mod_minima`, `o_producto`,`o_prod_cod`,`o_prod_des`,`o_prod_d`,`o_prod_h`, `o_minima`, `o_descuento`, `o_obligatorio`) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (datos_modulo[0][0], datos_modulo[0][1], datos_modulo[0][2], datos_modulo[0][3], datos_modulo[0][4], datos_modulo[0][5], datos_modulo[0][6],
             datos_producto[0][0], datos_producto[0][1], datos_producto[0][2], datos_producto[0][3], datos_producto[0][4], _minima, _descuento, _obligatorio)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/ofertas')


@app.route('/admin/ofertas')
def admin_ofertas():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `ofertas` ORDER BY 'o_mod_nom';")
    ofertas = cursor.fetchall()

    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()

    cursor.execute("SELECT * FROM `productos`;")
    productos = cursor.fetchall()

    conexion.commit()

    return render_template('admin/ofertas.html', ofertas=ofertas, modulos=modulos, productos=productos)


@ app.route('/admin/editarOfertas/<int:id>')
def admin_ofertas_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas` WHERE id_o=%s;", (id))
    ofertas = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarOferta.html', ofertas=ofertas)


# funciones de usuarios:
# Aca esta la magia para devolver la pantalla segun el usuario----------------------------
@ app.route('/sup/pedidos/')
def sup_pedidos_layout():
    """
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `pedidos` WHERE p_usuario=%s;", (usuario))
    ofertas = cursor.fetchall()
    conexion.commit()
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    conexion.commit()
    """
    return render_template('sup/pedidos.html')

# Aca esta la magia para devolver la pantalla segun el usuario----------------------------


@app.route('/sup/ofertas/')
def sup_ofertas():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias`")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM ofertas ORDER BY o_modulo;")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion.commit()
    # , usuarios=usuarios, _usuario=_usuario
    return render_template('sup/ofertas.html', ofertas=ofertas, droguerias=droguerias, clientes=clientes)


@ app.route('/sup/cargaOfert01/drogueria/', methods=['POST'])
def sup_cargaOferta01_droguerias():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cod_drogueria = %s;", (_drogueria))
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('sup/cargaOferta02.html', clientes=clientes, droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas)


@ app.route('/sup/cargaOferta02/cliente/', methods=['POST'])
def sup_cargaOferta02_droguerias():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()

    _drogueria = request.form['txtDrogueria2']
    _cliente = request.form['txtCliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `droguerias` where d_cod = %s;", (_drogueria))
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()
    conexion.commit()

    if _cliente == "Nuevo":
        return redirect('/sup/clientes/')

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `clientes` where c_cuenta = %s;", (_cliente))
    clientes = cursor.fetchall()

    conexion.commit()
    return render_template('sup/cargaOferta04.html', droguerias=droguerias, usuario=usuario, usuarios=usuarios, ofertas=ofertas, clientes=clientes)


@ app.route('/sup/cargaOferta04/cliente/', methods=['POST'])
# @ app.route('/sup/cargaOfert02/cliente/', methods=['POST'])
def sup_cargaOferta04_d_c():
    usuario = request.form['hashUsuarioO']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    _drogueria = request.form['txtDrogueria2']

    _cliente = request.form['txtCliente2']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `ofertas`")
    ofertas = cursor.fetchall()
    listaUnidades = []
    listaOfertaVigente = []
    for i in ofertas:
        uniList = {}
        uniList[f'{i[0]}'] = request.form[f'unidades{i[0]}']
        listaUnidades.append(uniList)
        listaOfertaVigente.append(i)
    # print(listaUnidades)
    ancho = len(ofertas)
    #print("Ancho:", ancho)
    conexion.commit()
    # print(usuarios)
    # print(listaOfertaVigente)
    # aca saco los modulos unicos
    modulos_ofertas = set()
    for i in ofertas:
        modulos_ofertas.add(i[1])
    # ---------------------------
    listaModOfer = list(modulos_ofertas)
    listaModOfer.sort()
    modulosT = len(listaModOfer)
    # print(listaModOfer)
    listaFinal = []
    for i in listaModOfer:
        listaModulo = []
        for x in ofertas:
            if i == x[1]:
                listaModulo.append(x)
        listaFinal.append(listaModulo)
    listaTerminal = zip(listaModOfer, listaFinal)
    salidaModulos = list(listaTerminal)
    print(salidaModulos)
    anchoModulos = len(salidaModulos)
    listaInput = []
    modulosFuncion = list(zip(listaModOfer, listaFinal))
    count = 0
    for i in modulosFuncion:
        m = i[0]  # el_modulo
        e = i[1]
        listaScript = []
        for x in e:  # elementos
            q = x[0]  # elemento
            listaScript.append(q)
        scriptTxt = str(listaScript)
        elScript = f"{scriptTxt}"
        listaInput.append(f'{m}:{elScript}')

    print(anchoModulos)
    listaInput = json.dumps(listaInput)
    print(listaInput)

    return render_template('sup/cargaOferta05.html', listaInput=listaInput, anchoModulos=anchoModulos, drogueria=_drogueria, cliente=_cliente, usuarios=usuarios, usuario=usuario, unidades=listaUnidades, ofertas=ofertas, salidas=salidaModulos)


@ app.route('/sup/clientes/')
def sup_clientes():

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`;")
    usuarios = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`;")
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('sup/clientes.html', clientes=clientes, droguerias=droguerias, usuarios=usuarios)


@ app.route('/sup/clientes/editar', methods=['POST'])
def sup_clientes_editar():
    usuario = request.form['hashUsuario']
    cliente = request.form['id_cliente']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios` where u_hash = %s;", (usuario))
    usuarios = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes` where id_c = %s;", (cliente))
    clientes = cursor.fetchall()

    conexion.commit()

    return render_template('sup/editarClientes.html', clientes=clientes, droguerias=droguerias, usuarios=usuarios)


@ app.route('/sup/clientes/guardar/<int:usuario>', methods=['POST'])
def sup_clientes_guardar(usuario):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`")
    clientes = cursor.fetchall()

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios` WHERE u_hash=%s;", (usuario))
    usuarios = cursor.fetchall()
    conexion.commit()
    _drogueria = request.form['txtDrogueria']
    _cuenta = request.form['txtCuenta']
    _nombre = request.form['txtNombre']
    _cuit = request.form['txtCuit']
    _localidad = request.form['txtLocalidad']
    _postal = request.form['txtPostal']
    datos_drogueria = [_drogueria.split('#')]
    if _drogueria == 'Seleccione':
        flash('¡Por favor elija una Droguería!')
        return redirect(f'../{usuario}')

    sql = "INSERT INTO `clientes` (`id_c`, `c_id_drogueria`, `c_cod_drogueria`, `c_desc_drogueria`, `c_cuenta`, `c_nombre`, `c_cuit`, `c_localidad`, c_postal) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (datos_drogueria[0][0], datos_drogueria[0][1],
             datos_drogueria[0][2], _cuenta, _nombre, _cuit, _localidad, _postal)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect(f'../{usuario}')


@ app.route('/admin/usuarios')
def admin_usuarios():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT * FROM `usuarios`;")
    usuarios = cursor.fetchall()
    conexion.commit()

    return render_template('admin/usuarios.html', usuarios=usuarios)


@ app.route('/admin/usuariosj')
def admin_usuariosJ():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id_u, u_nombre,u_apellido, u_rrdzz, u_mail FROM `usuarios`;")
    usuarios = cursor.fetchall()

    conexion.commit()
    usuariosJ = json.dumps(usuarios)
    return render_template('admin/usuariosJ.html', usuariosJ=usuariosJ)


@ app.route('/admin/editarUsuarios/<int:id>')
def admin_usuarios_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios` WHERE id_u=%s;", (id))
    usuarios = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarUsuario.html', usuarios=usuarios)


@ app.route('/admin/usuarios/borrar/<int:id>')
def admin_usuarios_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios where id_u=%s;", (id))
    usuarios = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/usuarios')


@ app.route('/sup/clientes/borrar', methods=['POST'])
def sup_clientes_borrar():
    _cliente = request.form['id_cliente']
    _usuario = request.form['usuario_Hash']
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM clientes where id_c=%s;", (_cliente))
    conexion.commit()
    hash = int(_usuario)

    return redirect(f'/sup/clientes/{hash}')


@ app.route('/sup/clientes/editar', methods=['POST'])
def sup_clientes_update():
    _usuario = request.form['usuario_Hash']
    _cuenta = request.form['txtCuenta']
    _nombre = request.form['txtNombre']
    _cuit = request.form['txtCuit']
    _localidad = request.form['txtLocalidad']
    _postal = request.form['txtPostal']
    _id = request.form['txtID']

    sql = "UPDATE clientes SET c_cuenta=%s, c_nombre=%s, c_cuit=%s, c_localidad=%s, c_postal=%s WHERE id_c=%s;"
    datos = (_cuenta, _nombre, _cuit, _localidad, _postal, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()
    hash = int(_usuario)

    return redirect(f'/sup/clientes/{hash}')


@ app.route('/admin/editarUsuario/editar', methods=['POST'])
def admin_usuarios_editar():

    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _rrdzz = request.form['txtRrdzz']
    _mail = request.form['txtMail']
    _desde = request.form['txtDesde']
    _hasta = request.form['txtHasta']
    _pass = request.form['txtPass']
    _roll = request.form['txtRoll']
    _id = request.form['txtID']
    _habilitado = request.form['txtHabilitado']

    sql = "UPDATE usuarios SET u_nombre=%s, u_apellido=%s, u_rrdzz=%s, u_mail=%s, u_desde=%s, u_hasta=%s, u_pass=%s, u_roll=%s , u_habilitado=%s WHERE id_u=%s;"
    datos = (_nombre, _apellido, _rrdzz, _mail,
             _desde, _hasta, _pass, _roll, _habilitado, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/usuarios')


@ app.route('/admin/usuarios/guardar', methods=['POST'])
def admin_usuarios_guardar():
    now = datetime.now()
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _rrdzz = request.form['txtRrdzz']
    _mail = request.form['txtMail']
    _desde = request.form['txtDesde']
    _hasta = request.form['txtHasta']
    _pass = request.form['txtPass']
    _roll = request.form['txtRoll']
    _hash = randint(1000000000, 9999999999)
    _hash = str(_hash)+_rrdzz
    _habilitado = request.form['txtHabilitado']

# condicional para ver si existe usuario en vigencia

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE u_rrdzz=%s;", (_rrdzz))
    _existeUsuario = cursor.fetchall()
    conexion.commit()
    desde = datetime.strptime(f"{_existeUsuario[0][5]}", "%Y-%m-%d")
    hasta = datetime.strptime(f"{_existeUsuario[0][6]}", "%Y-%m-%d")
    if desde <= now and hasta >= now:
        flash('El usuario está vigente, modifique vigencia o elimine el usuario.')
        return redirect('/admin/usuarios')


# condicional para usar mensajes
    sql = "SELECT * FROM usuarios WHERE u_mail=%s;"
    datos = (_mail)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    _existe = cursor.fetchall()
    conexion.commit()

    if _existe:
        flash('Correo, ya registrado')
        return redirect('/admin/usuarios')

    sql = "INSERT INTO `usuarios` (`id_u`, `u_nombre`, `u_apellido`, `u_rrdzz`, `u_mail`, `u_desde`, `u_hasta`, `u_pass`, `u_roll`, `u_hash`, `u_habilitado`) VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    datos = (_nombre, _apellido, _rrdzz, _mail,
             _desde, _hasta, _pass, _roll, _hash, _habilitado)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/usuarios')
# funciones de productos:


@ app.route('/admin/productos')
def admin_productos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `productos`;")
    productos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/productos.html', productos=productos)


@ app.route('/admin/editarProducto/<int:id>')
def admin_producto_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `productos` WHERE id_p=%s;", (id))
    productos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarProducto.html', productos=productos)


@ app.route('/admin/productos/guardar', methods=['POST'])
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


@ app.route('/admin/productos/borrar/<int:id>')
def admin_productos_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos where id_p=%s;", (id))
    productos = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/productos')


@ app.route('/admin/editarProducto/editar', methods=['POST'])
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


@ app.route('/apms/pedidos')
def apms_pedidos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `pedidos`;")
    pedidos = cursor.fetchall()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()
    conexion.commit()
    cursor.execute("SELECT * FROM `ofertas`;")
    ofertas = cursor.fetchall()
    conexion.commit()

    return render_template('apms/pedidos.html', pedidos=pedidos, droguerias=droguerias, ofertas=ofertas)


@ app.route('/admin/pedidos')
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


@ app.route('/admin/pedidos/guardar', methods=['POST'])
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


@ app.route('/admin/pedidos/borrar', methods=['POST'])
def admin_pedidos_borrar():
    _id = request.form['txtID']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pedidos where id_pe=%s;", (_id))
    pedido = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/pedidos')

# funciones de clientes:


@ app.route('/apms/clientes')
def apms_clientes():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`;")
    clientes = cursor.fetchall()
    conexion.commit()

    return render_template('apms/clientes.html', clientes=clientes)


@ app.route('/admin/clientes')
def admin_clientes():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`;")
    clientes = cursor.fetchall()
    conexion.commit()

    return render_template('admin/clientes.html', clientes=clientes)


@ app.route('/admin/editarCliente/<int:id>')
def admin_cliente_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `clientes` WHERE id_c=%s;", (id))
    clientes = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarClientes.html', clientes=clientes)


@ app.route('/admin/editarCliente/editar', methods=['POST'])
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


@ app.route('/admin/clientes/guardar', methods=['POST'])
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


@ app.route('/admin/clientes/borrar/<int:id>')
def admin_clientes_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM clientes where id_c=%s;", (id))
    clientes = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/clientes')

# funciones de droguerias:


@ app.route('/admin/editarDroguerias/<int:id>')
def admin_droguerias_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias` WHERE id_d=%s;", (id))
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarDrogueria.html', droguerias=droguerias)


@ app.route('/admin/droguerias')
def admin_droguerias():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()
    conexion.commit()

    return render_template('admin/droguerias.html', droguerias=droguerias)


@ app.route('/admin/droguerias/guardar', methods=['POST'])
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


@ app.route('/admin/droguerias/borrar/<int:id>')
def admin_droguerias_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM droguerias where id_d=%s;", (id))
    drogueria = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/droguerias')


@ app.route('/admin/editarDrogueria/editar', methods=['POST'])
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


@ app.route('/apms/modulos')
def apms_modulos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    conexion.commit()

    return render_template('apms/modulos.html', modulos=modulos)


@ app.route('/sup/modulos')
def sup_modulos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    conexion.commit()

    return render_template('sup/modulos.html', modulos=modulos)


@ app.route('/admin/modulos')
def admin_modulos():
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/modulos.html', modulos=modulos)

# -------------------------------------------------------------------------


@ app.route('/apibeta', methods=['GET'])
def usuarios_oces():
    try:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `modulos`;")
        modulo = cursor.fetchall()
        listaModulos = []
        for m in modulo:
            modulos = {}
            modulos["id_m"] = m[0]
            modulos["m_nombre"] = m[1]
            modulos["m_titulo"] = m[2]
            modulos["m_pie"] = m[3]
            modulos["m_desde"] = m[4]
            modulos["m_hasta"] = m[5]
            modulos["m_cantidad_minima"] = m[6]
            listaModulos.append(modulos)

        return jsonify({"modulo": listaModulos, "mensaje": "Módulos encontrados"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@ app.route('/apibeta/<int:id>', methods=['GET'])
def usuarios_oces_uno(id):
    try:
        conexion = mysql.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `modulos` where id_m = %s;", (id))
        modulo = cursor.fetchone()
        if modulo != None:
            listaModulos = []
            modulos = {}
            modulos["id_m"] = modulo[0]
            modulos["m_nombre"] = modulo[1]
            modulos["m_titulo"] = modulo[2]
            modulos["m_pie"] = modulo[3]
            modulos["m_desde"] = modulo[4]
            modulos["m_hasta"] = modulo[5]
            modulos["m_cantidad_minima"] = modulo[6]
            listaModulos.append(modulos)

            return jsonify({"modulo": listaModulos, "mensaje": "Modulo encontrado."})
        else:
            return jsonify({"mensaje": "Modulo no encontrado"})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/apibeta', methods=['POST'])
def registrar_modulos_api():
    respuesta = request.json
    try:
        _mensaje = request.json['mensaje']
        _modulo = request.json['modulo']
        count = 0
        for i in _modulo:
            _id = request.json['modulo'][count]['idM']
            sql = "DELETE FROM modulos WHERE id_m = %s;"
            datos = (_id)
            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            conexion.commit()
            count += 1
            nw_mensaje = _mensaje+" OK del server"
        return jsonify({"mensaje": nw_mensaje+" "+respuesta})
    except Exception as ex:
        return jsonify({'mensaje': f"Error {respuesta}"})


@app.route('/apibeta2', methods=['DELETE'])
def registrar_modulos_api_DELETE_():
    respuesta = request.json
    try:
        _mensaje = request.json['mensaje']
        _modulo = request.json['modulo']
        count = 0
        for i in _modulo:
            _id = request.json['modulo'][count]['idM']
            sql = "DELETE FROM modulos WHERE id_m = %s;"
            datos = (_id)
            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            conexion.commit()
            count += 1
            nw_mensaje = _mensaje+" OK del server"
        return jsonify({"mensaje": nw_mensaje+" "+respuesta})
    except Exception as ex:
        return jsonify({'mensaje': f"Error {respuesta}"})


@app.route('/apibeta2', methods=['PUT'])
def registrar_modulos_api_put_():
    try:
        _mensaje = request.json['mensaje']
        _modulo = request.json['modulo']
        count = 0
        for i in _modulo:

            _nombre = request.json['modulo'][count]['Mnombre']
            _titulo = request.json['modulo'][count]['Mtitulo']
            _pie = request.json['modulo'][count]['Mpie']
            _desde = request.json['modulo'][count]['Mdesde']
            _hasta = request.json['modulo'][count]['Mhasta']
            _minima = request.json['modulo'][count]['Mcantidad']
            _id = request.json['modulo'][count]['idM']

            if _nombre != None:
                sql = "UPDATE modulos SET m_nombre=%s WHERE id_m=%s;"
                datos = (_nombre, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'nombre', error"
            if _titulo != None:
                sql = "UPDATE modulos SET m_titulo=%s WHERE id_m=%s;"
                datos = (_titulo, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'titulo', error"
            if _pie != None:
                sql = "UPDATE modulos SET m_pie=%s WHERE id_m=%s;"
                datos = (_pie, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'Pie', error"
            if _desde != None:
                sql = "UPDATE modulos SET m_desde=%s WHERE id_m=%s;"
                datos = (_desde, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'desde', error"
            if _hasta != None:
                sql = "UPDATE modulos SET m_hasta=%s WHERE id_m=%s;"
                datos = (_hasta, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'hasta', error"
            if _minima != None:
                sql = "UPDATE modulos SET m_cantidad_minima = %s WHERE id_m=%s;"
                datos = (_minima, _id)
                conexion = mysql.connect()
                cursor = conexion.cursor()
                cursor.execute(sql, datos)
                conexion.commit()
            else:
                _mensaje = "Campo 'minima', error"
            count += 1
        nw_mensaje = _mensaje+" OK del server: PUT por ID"
        return jsonify({"mensaje": nw_mensaje})
    except Exception as ex:
        return jsonify({'mensaje': "Error"})


@app.route('/apibeta2', methods=['POST'])
def registrar_modulos_api_sin_():

    try:
        _mensaje = request.json['mensaje']
        _modulo = request.json['modulo']
        count = 0
        for i in _modulo:
            _nombre = request.json['modulo'][count]['Mnombre']
            _titulo = request.json['modulo'][count]['Mtitulo']
            _pie = request.json['modulo'][count]['Mpie']
            _desde = request.json['modulo'][count]['Mdesde']
            _hasta = request.json['modulo'][count]['Mhasta']
            _cantidad = request.json['modulo'][count]['Mcantidad']

            sql = "INSERT INTO `modulos` (`id_m`, `m_nombre`, `m_titulo`, `m_pie`, `m_desde`, `m_hasta`, `m_cantidad_minima`) VALUES (NULL, %s,%s,%s,%s,%s,%s);"
            datos = (_nombre, _titulo, _pie, _desde, _hasta, _cantidad)

            conexion = mysql.connect()
            cursor = conexion.cursor()
            cursor.execute(sql, datos)
            conexion.commit()
            count += 1
        return jsonify({"mensaje": _mensaje})

    except Exception as ex:
        return jsonify({'mensaje': "Error"})
# ----------------------------------------------------------------------------------


@ app.route('/admin/editarModulos/editar', methods=['POST'])
def admin_modulo_editar():

    _nombre = request.form['txtNombre']
    _titulo = request.form['txtTitulo']
    _pie = request.form['txtPie']
    _desde = request.form['txtDesde']
    _hasta = request.form['txtHasta']
    _id = request.form['txtID']
    _cantidad = request.form['txtCantidad']

    sql = "UPDATE modulos SET m_nombre=%s, m_titulo=%s, m_pie=%s, m_desde=%s, m_hasta=%s, m_cantidad_minima=%s WHERE id_m=%s;"
    datos = (_nombre, _titulo, _pie, _desde, _hasta, _cantidad, _id)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/modulos')


@ app.route('/admin/modulos/guardar', methods=['POST'])
def admin_modulos_guardar():

    _nombre = request.form['m_nombre']
    _titulo = request.form['m_titulo']
    _pie = request.form['m_pie']
    _desde = request.form['m_desde']
    _hasta = request.form['m_hasta']
    _cantidad = request.form['txtCantidad']

    sql = "INSERT INTO `modulos` (`id_m`, `m_nombre`, `m_titulo`, `m_pie`, `m_desde`, `m_hasta`, `m_cantidad_minima`) VALUES (NULL, %s,%s,%s,%s,%s,%s);"
    datos = (_nombre, _titulo, _pie, _desde, _hasta, _cantidad)

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/modulos')


@ app.route('/admin/modulos/borrar/<int:id>')
def admin_modulos_borrar(id):

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM modulos where id_m=%s;", (id))
    modulos = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/modulos')


@ app.route('/admin/editarModulos/<int:id>')
def admin_modulos_update(id):
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM `modulos` WHERE id_m=%s;", (id))
    modulos = cursor.fetchall()
    conexion.commit()

    return render_template('admin/editarModulo.html', modulos=modulos)


def pagina_no_encontrada(error):
    return "<h2>La página no existe.</h2>", 404


if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host="89.0.0.28", port=8000, debug=True)
# host="192.168.0.117", port=8000,
# host="89.0.0.28", port=8000,
