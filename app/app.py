
"""
App Configuration - Configuración y constantes de la aplicación
"""
from pathlib import Path
from dataclasses import dataclass

# Directorios del proyecto
PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / "assets"
FRAMES_DIR = PROJECT_ROOT / "frames"
COMPONENTS_DIR = PROJECT_ROOT / "components"
UTILS_DIR = PROJECT_ROOT / "utils"

# Configuración de ventana
@dataclass
class WindowConfig:"""
App Configuration - Configuración y constantes de la aplicación
"""
from pathlib import Path
from dataclasses import dataclass

# Directorios del proyecto
PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / "assets"
FRAMES_DIR = PROJECT_ROOT / "frames"
COMPONENTS_DIR = PROJECT_ROOT / "components"
UTILS_DIR = PROJECT_ROOT / "utils"

# Configuración de ventana
@dataclass
class WindowConfig:
    """Configuración de la ventana principal"""
    width: int = 1440
    height: int = 1024
    resizable: bool = False
    title: str = "Mantel Datacenter's"

# Colores del tema
class Colors:
    """Paleta de colores de la aplicación"""
    PRIMARY_DARK = "#153573"
    PRIMARY_LIGHT = "#B1CCFF"
    SECONDARY_DARK = "#0C2658"
    WIDGET_DARK = "#0E1D3A"
    WIDGET_MEDIUM = "#142D5D"
    WIDGET_LIGHT = "#152D5D"
    ACCENT_YELLOW = "#F8BC04"
    TEXT_WHITE = "#FFFFFF"
    TEXT_DARK = "#000716"
    INPUT_BG = "#D9D9D9"
    BLACK = "#000000"

# Fuentes
class Fonts:
    """Definición de fuentes utilizadas"""
    TITLE_LARGE = ("Arial BoldMT", 96)
    TITLE_MEDIUM = ("Arial BoldMT", 40)
    TITLE_SMALL = ("Arial BoldMT", 32)
    TEXT_LARGE = ("ArialMT", 32)
    TEXT_MEDIUM = ("ArialMT", 24)
    TEXT_SMALL = ("ArialMT", 20)
    TEXT_TINY = ("ArialMT", 15)

# Configuración de frames
FRAME_ASSETS = {
    "inicio": "frame0",
    "login": "frame1",
    "dashboard": "frame2",
    "alarmas": "frame3",
    "datos": "frame4",
    "historial": "frame5",
    "conexiones": "frame6"
}

# Validación de estructura de directorios
def validate_project_structure():
    """Valida que existan todos los directorios necesarios"""
    required_dirs = [ASSETS_DIR, FRAMES_DIR, COMPONENTS_DIR, UTILS_DIR]
    missing_dirs = [d for d in required_dirs if not d.exists()]
    
    if missing_dirs:
        raise FileNotFoundError(
            f"Directorios faltantes: {[str(d) for d in missing_dirs]}"
        )
    
    # Validar que existan las carpetas de assets para cada frame
    for frame_name, asset_folder in FRAME_ASSETS.items():
        asset_path = ASSETS_DIR / asset_folder
        if not asset_path.exists():
            print(f"Advertencia: Carpeta de assets no encontrada: {asset_path}")

# Configuración de base de datos (para futuro)
class DatabaseConfig:
    """Configuración de base de datos (placeholder)"""
    DB_PATH = PROJECT_ROOT / "data" / "mantel.db"
    USE_DATABASE = False  # Cambiar a True cuando se implemente

# Configuración de logging
class LogConfig:
    """Configuración de logging"""
    LOG_DIR = PROJECT_ROOT / "logs"
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

if __name__ == "__main__":
    # Validar estructura al importar
    try:
        validate_project_structure()
        print("✓ Estructura del proyecto validada correctamente")
    except Exception as e:
        print(f"✗ Error en la estructura del proyecto: {e}")
