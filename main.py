from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel

app = FastAPI()

ARCHIVO = "albums.json"

class Album(BaseModel):
    titulo: str
    artista: str
    anio: int


def leer():
    with open(ARCHIVO, encoding="utf-8") as f:
        return json.load(f)


def guardar(albums):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(albums, f, indent=2, ensure_ascii=False)


@app.get("/")
def inicio():
    return {"mensaje": "Hola, FastAPI"}

@app.get("/albums")
def listar():
    return leer()

@app.get("/albums/{id}")
def buscar(id: int):
    for album in leer():
        if album["id"] == id:
            return album
    raise HTTPException(status_code=404, detail="Ese álbum no existe")

@app.post("/albums")
def agregar(album: Album):
    albums = leer()
    id_mas_alto = 0
    for a in albums:
        if a["id"] > id_mas_alto:
            id_mas_alto = a["id"]
    nuevo = {
        "id": id_mas_alto + 1,
        "titulo": album.titulo,
        "artista": album.artista,
        "anio": album.anio,
    }
    albums.append(nuevo)
    guardar(albums)
    return nuevo

@app.put("/albums/{id}")
def editar(id: int, datos: Album):
    albums = leer()
    for album in albums:
        if album["id"] == id:
            album["titulo"] = datos.titulo
            album["artista"] = datos.artista
            album["anio"] = datos.anio
            guardar(albums)
            return album
    raise HTTPException(status_code=404, detail="Ese álbum no existe")

@app.delete("/albums/{id}")
def borrar(id: int):
    albums = leer()
    for album in albums:
        if album["id"] == id:
            albums.remove(album)
            guardar(albums)
            return {"mensaje": "Álbum borrado"}
    raise HTTPException(status_code=404, detail="Ese álbum no existe")