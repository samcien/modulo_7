from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Inicializacion de Base de Datos
mongo_url = "mongodb://localhost:27017"
mongo_db = MongoClient(mongo_url)

# Crear base de datos
db = mongo_db["diccionario"]

# Crear coleccion
collection = db.get_collection("Palabras")

if collection is None:
    collection = db.create_collection("Palabras")
else:
    pass


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/agregar_palabra', methods=['GET', 'POST'])
def agregar_palabra():
    if request.method == 'POST':
        palabra = request.form['palabra']
        significado = request.form['significado']
        data = {"Palabra": palabra, "Significado": significado}
        x = collection.insert_one(data).inserted_id
        return render_template('agregar_palabra.html', message='Palabra agregada correctamente')
    return render_template('agregar_palabra.html')


@app.route('/editar_palabra', methods=['GET', 'POST'])
def editar_palabra():
    if request.method == 'POST':
        palabra = request.form['palabra']
        nuevo = request.form['nuevo_significado']
        valor = {"$set": {"Significado": nuevo}}
        q = {"Palabra": palabra}
        collection.update_one(q, valor)
        return render_template('editar_palabra.html', message='Palabra editada correctamente')
    else:
        return render_template('editar_palabra.html')


@app.route('/eliminar_palabra', methods=['GET', 'POST'])
def eliminar_palabra():
    if request.method == 'POST':
        filtro = request.form['palabra']
        data_1 = {"Palabra": filtro}
        collection.delete_one(data_1)
        return render_template('eliminar_palabra.html', message='Palabra eliminada correctamente')
    else:
        return render_template('eliminar_palabra.html')


@app.route('/ver_palabras')
def ver_palabras():
    documentos = collection.find()
    palabras = []
    for documento in documentos:
        palabras.append(documento)
    return render_template('ver_palabras.html', palabras=palabras)


@app.route('/buscar_palabra', methods=['GET', 'POST'])
def buscar_palabra():
    if request.method == 'POST':
        filtro = request.form['palabra']
        data_1 = {"Palabra": filtro}
        documento = collection.find_one(data_1)
        if documento is None:
            return render_template('buscar_palabra.html', message='Palabra no encontrada')
        else:
            return render_template('buscar_palabra.html', documento=documento)
    else:
        return render_template('buscar_palabra.html')


if __name__ == '__main__':
    app.run(debug=True)
