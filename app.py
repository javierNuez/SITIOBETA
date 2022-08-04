
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
    return render_template('admin/pedidos.html')


@app.route('/admin/clientes')
def admin_clientes():
    return render_template('admin/clientes.html')


@app.route('/admin/productos')
def admin_productos():
    return render_template('admin/productos.html')


@app.route('/admin/droguerias')
def admin_droguerias():
    return render_template('admin/droguerias.html')


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
    return render_template('admin/modulos.html')
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



if __name__ == '__main__':
    app.run(debug=True)
