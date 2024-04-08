from http.server import HTTPServer, BaseHTTPRequestHandler
import json, random

from urllib.parse import urlparse, parse_qs

partidas = []

class PartidasService:
    _instance = None
    
    def __new__(cls, player):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.player = player
            cls._instance.number = 0
            cls._instance.attempts = []
            cls._instance.status = False
        return cls._instance
    
    def to_dict(self):
        return {"player": self.player, "number": self.number, "attempts": self.attempts,"status": self.status}
    
    def take_damage(self, damage):
        self.number -= damage
        
    def player_igual(self, number):
        xnum = random.randint(0, 100)
        if number == xnum:
            return "Felicitaciones"
        elif number > xnum:
            return "Numero a adivinar es mayor"
        else:
            return "Numero a adivinar es menor"

    
    def add_partida(data):
        data["id"] = len(partidas) + 1
        partidas.append(data)
        return partidas

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))


class PlayerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/partidas":
            if "nombre" in query_params:
                nombre = query_params["nombre"][0]
                partidas_filtrados = PartidasService.filter_partida_by_player(
                    nombre
                )
                if partidas_filtrados != []:
                    HTTPResponseHandler.handle_response(
                        self, 200, partidas_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, partidas)
        elif self.path.startswith("/partidas/"):
            id = int(self.path.split("/")[-1])
            partida = PartidasService.find_partida(id)
            if partida:
                HTTPResponseHandler.handle_response(self, 200, [partida])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/guess":
            data = self.read_data()
            partidas = PartidasService.add_partida(data)
            HTTPResponseHandler.handle_response(self, 201, partidas)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/partidas/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            partidas = PartidasService.update_partida(id, data)
            if partidas:
                HTTPResponseHandler.handle_response(self, 200, partidas)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "partida no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path == "/partidas":
            partidas = PartidasService.delete_partidas()
            HTTPResponseHandler.handle_response(self, 200, partidas)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data


def run_server(port=8000):
    global player
    player = PartidasService("Karina")
    
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, PlayerHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()