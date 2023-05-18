from flask import Flask,current_app, g, request, jsonify
import sqlite3
import click

app = Flask(__name__)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Helper function to initialize the database schema
def initialize_database():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Usuario (
            IDUser INTEGER PRIMARY KEY,
            Token TEXT,
            Fecha DATE
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS Descuentos (
            IDDescuento INTEGER PRIMARY KEY,
            Valor INTEGER
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS UsuarioDescuento (
            ID INTEGER PRIMARY KEY,
            IDUser INTEGER,
            IDDescuento INTEGER,
            FOREIGN KEY (IDUser) REFERENCES Usuario(IDUser),
            FOREIGN KEY (IDDescuento) REFERENCES Descuentos(IDDescuento)
        )
    ''')
    conn.commit()

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/test', methods=['GET'])
def test():
    if request.method == "GET":
        return jsonify({"response": "Get Request Called"})

@app.route('/usuario', methods=['POST'])
def create_usuario():
    conn = get_db_connection()
    print("a")
    token = request.json.get('token')
    fecha = request.json.get('fecha')
    print(token, fecha)
    conn.execute('INSERT INTO Usuario (Token, Fecha) VALUES (?, ?)', (token, fecha))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Usuario created successfully'})

# Route to get all Usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM Usuario').fetchall()
    conn.close()
    usuarios_list = [dict(usuario) for usuario in usuarios]
    return jsonify(usuarios_list)

@app.route('/usuario/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Usuario WHERE IDUser = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Usuario deleted successfully'})

# Route to create a new Descuento
@app.route('/descuento', methods=['POST'])
def create_descuento():
    conn = get_db_connection()
    valor = request.json.get('valor')
    conn.execute('INSERT INTO Descuentos (Valor) VALUES (?)', (valor,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Descuento created successfully'})
# Route to get all Descuentos
@app.route('/descuentos', methods=['GET'])
def get_descuentos():
    conn = get_db_connection()
    descuentos = conn.execute('SELECT * FROM Descuentos').fetchall()
    conn.close()
    descuentos_list = [dict(descuento) for descuento in descuentos]
    return jsonify(descuentos_list)

# Route to update an existing Descuento
@app.route('/descuento/<int:id>', methods=['PUT'])
def update_descuento(id):
    conn = get_db_connection()
    valor = request.json.get('valor')
    conn.execute('UPDATE Descuentos SET Valor = ? WHERE IDDescuento = ?', (valor, id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Descuento updated successfully'})

# Route to delete an existing Descuento
@app.route('/descuento/<int:id>', methods=['DELETE'])
def delete_descuento(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM Descuentos WHERE IDDescuento = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Descuento deleted successfully'})

initialize_database()