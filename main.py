from fastapi import FastAPI
# import requests
import sqlite3

def iniciar_db():
    conn = sqlite3.connect("leterbox.db")
    cursor = conn.cursor()
    consulta = """
        CREATE TABLE IF NOT EXISTS peliculas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        genero TEXT,
        puntaje INTEGER)
    """
    cursor.execute(consulta)
    conn.comit()
    conn.close()

db_peliculas = [{"titulo": "Matrix", "genero": "accion", "puntaje": 5},
                {"titulo": "Esperando la Carroza", "genero": "comedia", "puntaje": 5}]

generos = ["accion", "comedia", "terror"]

# usamos fastapi para armar un endpoint que me traiga la pelicula
app = FastAPI()

@app.get("/peliculas") # creando un get para el endpoint "peliculas"
def obtener_peliculas():
    return db_peliculas

@app.post("/peliculas")
def cargar_una_pelicula(titulo, genero, puntaje):

    if not puntaje.isdigit():
        mensaje_de_error = "El puntaje debe ser un numero entero"
        return mensaje_de_error
    if not genero in generos:
        return "El genero no se encuentra"
    
    nueva_pelicula = {"titulo": titulo, "genero": genero, "puntaje": puntaje}
    db_peliculas.append(nueva_pelicula)
    mensaje_de_retorno = "Pelicula guardada correctamente"
    return mensaje_de_retorno

@app.post("/peliculas_eliminar")
def eliminar_una_pelicula(pelicula):
    for i in range(len(db_peliculas)):
        if db_peliculas[i]["titulo"] == pelicula:
            db_peliculas.remove(db_peliculas[i])
            mensaje_de_retorno = "Pelicula eliminada correctamente"
            return mensaje_de_retorno
    mensaje_de_retorno = "No se encontro la pelicula"
    return mensaje_de_retorno

@app.get("/genero")
def obtener_generos():
    return generos

@app.post("/genero")
def añadir_genero(genero):
    generos.append(genero)
    return "Genero añadido correctamente"

@app.post("/genero_eliminar")
def eliminar_genero(genero):
    if not genero in generos:
        return "No se encuentra el genero"
    else:
        generos.remove(genero)
        return "Genero eliminado exitosamente"

@app.get("/puntaje")
def puntaje(pelicula):
    for i in range(len(db_peliculas)):
        if db_peliculas[i]["titulo"] == pelicula:
            return db_peliculas[i]["puntaje"]
        else:
            return "No esta la pelicula"

# Terminal:
# [ uvicorn main:app --reload ]
# nombramos a nuestra app, nos "crea" el servidor