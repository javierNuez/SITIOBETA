
from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)
mysql=MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitiobeta'
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


@app.route('/admin/pedidos')
def admin_pedidos():
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `pedidos`;")
    pedidos = cursor.fetchall()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()
    conexion.commit()
    
    return render_template('admin/pedidos.html', pedidos=pedidos, droguerias=droguerias)


@app.route('/admin/clientes')
def admin_clientes():
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `clientes`;")
    clientes = cursor.fetchall()
    conexion.commit()
    
    return render_template('admin/clientes.html', clientes=clientes)


@app.route('/admin/productos')
def admin_productos():
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `productos`;")
    productos = cursor.fetchall()
    conexion.commit()
    
    return render_template('admin/productos.html', productos=productos)


@app.route('/admin/droguerias')
def admin_droguerias():
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `droguerias`;")
    droguerias = cursor.fetchall()
    conexion.commit()
    
    return render_template('admin/droguerias.html', droguerias=droguerias)


@app.route('/admin/usuarios')
def admin_usuarios():
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios`;")
    usuarios = cursor.fetchall()
    conexion.commit()
    
    return render_template('admin/usuarios.html', usuarios=usuarios)


@app.route('/admin/modulos')
def admin_modulos():
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `modulos`;")
    modulos = cursor.fetchall()
    conexion.commit()
    
    return render_template('admin/modulos.html', modulos=modulos)
#funciones de usuarios:
@app.route('/admin/usuarios/borrar' , methods=['POST'])
def admin_usuarios_borrar():
    _id=request.form['txtID']
    
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `usuarios` where id_u=%s;",(_id))
    usuario = cursor.fetchall()
    conexion.commit()
    
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM usuarios where id_u=%s;",(_id))
    usuario = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/usuarios')
    
@app.route('/admin/usuarios/guardar' , methods=['POST'])
def admin_usuarios_guardar():

    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _rrdzz=request.form['txtRrdzz']
    _mail=request.form['txtMail']
    _desde=request.form['txtDesde']
    _hasta=request.form['txtHasta']

    sql="INSERT INTO `usuarios` (`id_u`, `u_nombre`, `u_apellido`, `u_rrdzz`, `u_mail`, `u_desde`, `u_hasta`) VALUES (NULL, %s,%s,%s,%s,%s,%s);"
    datos=(_nombre,_apellido,_rrdzz,_mail,_desde,_hasta)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()


    return redirect('/admin/usuarios')
#funciones de productos:
@app.route('/admin/productos/guardar' , methods=['POST'])
def admin_productos_guardar():

    
    _codigo=request.form['p_cod']
    _desc=request.form['p_descripcion']


    sql="INSERT INTO `productos` (`id_p`, `p_cod`, `p_descripcion`) VALUES (NULL, %s,%s);"
    datos=(_codigo,_desc)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()


    return redirect('/admin/productos')

@app.route('/admin/productos/borrar' , methods=['POST'])
def admin_productos_borrar():
    _id=request.form['txtID']
        
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM productos where id_p=%s;",(_id))
    usuario = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/productos')

#funciones de pedidos:
@app.route('/admin/pedidos/guardar' , methods=['POST'])
def admin_pedidos_guardar():

    
    _codigo=request.form['pe_cod']
    _desc=request.form['pe_descripcion']


    sql="INSERT INTO `pedidos` (`id_pe`, `pe_cod`, `pe_descripcion`) VALUES (NULL, %s,%s);"
    datos=(_codigo,_desc)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()


    return redirect('/admin/pedidos')

@app.route('/admin/pedidos/borrar' , methods=['POST'])
def admin_pedidos_borrar():
    _id=request.form['txtID']
        
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM pedidos where id_pe=%s;",(_id))
    pedido = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/pedidos')

#funciones de clientes:
@app.route('/admin/clientes/guardar' , methods=['POST'])
def admin_clientes_guardar():

    
    _codigo=request.form['c_cod']
    _cuenta=request.form['c_cuenta']
    _nombre=request.form['c_nombre']
    _cuit=request.form['c_cuit']
    _localidad=request.form['c_localidad']
    _postal=request.form['c_postal']


    sql="INSERT INTO `clientes` (`id_c`, `c_cod`, `c_cuenta`, c_nombre, c_cuit, c_localidad, c_postal) VALUES (NULL, %s,%s,%s,%s,%s,%s);"
    datos=(_codigo,_cuenta,_nombre,_cuit, _localidad,_postal)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()


    return redirect('/admin/clientes')

@app.route('/admin/clientes/borrar' , methods=['POST'])
def admin_clientes_borrar():
    _id=request.form['txtID']
        
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM clientes where id_c=%s;",(_id))
    cliente = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/clientes')

#funciones de droguerias:
@app.route('/admin/droguerias/guardar' , methods=['POST'])
def admin_droguerias_guardar():

    
    _codigo=request.form['d_cod']
    _desc=request.form['d_descripcion']


    sql="INSERT INTO `droguerias` (`id_d`, `d_cod`, `d_descripcion`) VALUES (NULL, %s,%s);"
    datos=(_codigo,_desc)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()


    return redirect('/admin/droguerias')

@app.route('/admin/droguerias/borrar' , methods=['POST'])
def admin_droguerias_borrar():
    _id=request.form['txtID']
        
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM droguerias where id_d=%s;",(_id))
    droguerias = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/droguerias')

#funciones de módulos:
@app.route('/admin/modulos/guardar' , methods=['POST'])
def admin_modulos_guardar():

    
    _nombre=request.form['m_nombre']
    _titulo=request.form['m_titulo']
    _pie=request.form['m_pie']
    _desde=request.form['m_desde']
    _hasta=request.form['m_hasta']


    sql="INSERT INTO `modulos` (`id_m`, `m_nombre`, `m_titulo`, `m_pie`, `m_desde`, `m_hasta`) VALUES (NULL, %s,%s,%s,%s,%s);"
    datos=(_nombre,_titulo,_pie,_desde,_hasta)

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()


    return redirect('/admin/modulos')

@app.route('/admin/modulos/borrar' , methods=['POST'])
def admin_modulos_borrar():
    _id=request.form['txtID']
        
    conexion = mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM modulos where id_m=%s;",(_id))
    modulos = cursor.fetchall()
    conexion.commit()
    return redirect('/admin/modulos')

if __name__ == '__main__':
    app.run(debug=True)
