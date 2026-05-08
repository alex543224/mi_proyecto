from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la Base de Datos
database_url = os.getenv("DATABASE_URL", "sqlite:///local.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

# --- NUEVOS ENDPOINTS ---

# 1. Menú Principal
@app.route('/')
def index():
    return render_template('index.html')

# 2. Añadir un usuario nuevo
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        nuevo_usuario = Usuario(
            nombre=request.form['nombre'],
            apellidos=request.form['apellidos']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect(url_for('manage_users')) # Tras añadir, vamos a ver la lista
    
    return render_template('add.html')

# 3. Ver y gestionar usuarios
@app.route('/manage')
def manage_users():
    usuarios = Usuario.query.all()
    return render_template('manage.html', usuarios=usuarios)

# 4. Editar un usuario existente
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    # Buscamos al usuario por su ID
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        # Actualizamos sus datos
        usuario.nombre = request.form['nombre']
        usuario.apellidos = request.form['apellidos']
        db.session.commit()
        return redirect(url_for('manage_users'))
        
    return render_template('edit.html', usuario=usuario)

# 5. Borrar un usuario
@app.route('/delete/<int:id>', methods=['POST'])
def delete_user(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('manage_users'))

if __name__ == '__main__':
    app.run(debug=True)