from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuración de la Base de Datos: 
# Si existe una variable en Render, usa Postgres. Si no (en tu PC), usa SQLite local.
database_url = os.getenv("DATABASE_URL", "sqlite:///local.db")
# Render a veces usa 'postgres://', pero SQLAlchemy requiere 'postgresql://'
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definimos la tabla de la Base de Datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)

# Crear la tabla si no existe
with app.app_context():
    db.create_all()

# Ruta principal de la web
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Si el usuario envió el formulario, guardamos los datos
        nuevo_usuario = Usuario(
            nombre=request.form['nombre'],
            apellidos=request.form['apellidos']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect('/') # Recarga la página

    # Si es un GET (entrar normal a la web), leemos los usuarios y los enviamos al HTML
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)