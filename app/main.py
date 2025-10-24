"""
Main Entry Point - Punto de entrada principal de la aplicación
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path para imports
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from frames.inicio import InicioFrame
from udp_sync import udp_sync

def main():
    """Función principal que inicia la aplicación"""
    try:
        # Iniciar sincronización UDP en background
        udp_sync.start()
        print("🚀 Sistema de sincronización UDP iniciado")
        
        # Iniciar con la pantalla de inicio
        app = InicioFrame()
        app.show()
        
    except KeyboardInterrupt:
        print("\n⏹️  Cerrando aplicación...")
        udp_sync.stop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
    finally:
        udp_sync.stop()

if __name__ == "__main__":
    main()
