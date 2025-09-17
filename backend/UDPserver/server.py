import socket
import json
from guardar import guardar_datos
from datetime import datetime

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

# Función principal que ejecuta el servidor UDP
def run_server():
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.bind((UDP_IP, UDP_PORT))
    print(f"Servidor UDP escuchando en {UDP_IP}:{UDP_PORT}...")

    while True:
        
        data, addr = sock.recvfrom(4096)
        try:
            mensaje = data.decode("utf-8", errors="replace")
            json_data = json.loads(mensaje)
            print(f"[{datetime.now()}] {addr} -> {json_data}")
            guardar_datos(json_data)
        except json.JSONDecodeError:
            print(f"[{datetime.now()}] {addr} -> RAW: {mensaje}")

if __name__ == "__main__":
    run_server()
