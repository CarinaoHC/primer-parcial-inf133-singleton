import requests
url = "http://localhost:8000/"

ruta_get = url + "partidas"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

# Crear una partida.
ruta_post = url + "partidas"
nuevo_partida = {
    "nombre": "Juanito",
    "apellido": "Pérez",
    "carrera": "Ingeniería Agronomica",
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_partida)
print(post_response.text)


# Buscar una partida por su id.
# Buscar una partida por el nombre del jugador.
# Actualizar los intentos de una partida.
# Eliminar una partida.


# GET filtrando por nombre con query params
ruta_get = url + "partidas?nombre=Pedrito"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
