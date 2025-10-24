import socket
import json
import sys
import os
from datetime import datetime

# Agregar la ruta del backend al path para poder importar guardar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guardar import guardar_datos, guardar_historial

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

def run_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    sock.bind((UDP_IP, UDP_PORT))
    
    print("=" * 50)
    print(f"✅ Servidor UDP iniciado")
    print(f"👂 Escuchando en {UDP_IP}:{UDP_PORT}")
    print(f"⏹️  Presiona Ctrl+C para detener")
    print("=" * 50)
    print()
    
    while True:
        try:
            # Recibir datos
            data, addr = sock.recvfrom(4096)
            
            # Decodificar
            mensaje = data.decode("utf-8", errors="replace")
            
            # Parsear JSON
            json_data = json.loads(mensaje)
            
            # Mostrar en terminal
            print(f"📨 [{datetime.now().strftime('%H:%M:%S')}] Desde {addr[0]}:{addr[1]}")
            print(f"📊 Datos: {json_data}")
            
            # Guardar en archivo
            guardar_historial(json_data)
            guardar_datos(json_data)
            
            print("-" * 50)
            
        except json.JSONDecodeError:
            print(f"⚠️  [{datetime.now().strftime('%H:%M:%S')}] JSON inválido: {mensaje}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Servidor detenido")
            sock.close()
            break
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("-" * 50)

if __name__ == "__main__":
    run_server()
