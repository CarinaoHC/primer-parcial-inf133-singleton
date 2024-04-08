from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

class Guess:
    _instance = None

    def __new__(cls, player):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.player = player
            cls._instance.number = 50
            cls._instance.attempts = []
            cls._instance.status = "En Progreso"
        return cls._instance
    
    def to_dict(self):
        return {"player": self.player, "number": self.number, "attempts": self.attempts, "status": self.status}
    
    def take_player(self, player):
        self.player = player
        
    def player_by_name(self, player):
        if self.player == player:
            return player
    
    def player_attempts(self, attempt):
        self.attemts.append(attempt)
        
    def player_status(self):
        self.status = "Finalizado"
    
    def take_partida(self, number):
        if self.number == number:
            return "Felicitaciones! Has adivinado elnumero"
        elif self.number > number:
            return "El numero a adivinar es mayor"
        else:
            return "El numero a adivinar es menor"

class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
        
class GuessHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        if parsed_path.path == "/guess":
            guess_data = json.dumps(guess.to_dict())
            HTTPResponseHandler.handle_response(self, 200, guess_data)
        elif parsed_path.path == "/guess":
            if "player" in query_params:
                player = query_params["player"][0]
                if guess.player_by_name(player):
                    HTTPResponseHandler.handle_response(self, 200, guess)
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(self, 404, [])

    def do_POST(self):
        if self.path == "/guess":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            player = json.loads(post_data.decode("utf-8"))["player"]
            guess.take_player(player)
            self.send_response(201)
            self.end_headers()
            guess_data = json.dumps(guess.to_dict())
            self.wfile.write(guess_data.encode("utf-8"))
        elif self.path == "/guess/damage":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            damage = json.loads(post_data.decode("utf-8"))["damage"]
            guess.take_damage(damage)
            self.send_response(201)
            self.end_headers()
            guess_data = json.dumps(guess.to_dict())
            self.wfile.write(guess_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def main():
    global guess
    guess = Guess("None")

    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, GuessHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()