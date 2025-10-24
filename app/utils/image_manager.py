"""
Image Manager - Gestiona la carga y caché de imágenes para la aplicación
"""
from pathlib import Path
from tkinter import PhotoImage
from typing import Dict, Optional

class ImageManager:
    """Administrador centralizado de imágenes para evitar recargas"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).parent.parent
        self.cache: Dict[str, PhotoImage] = {}
    
    def get_image(self, frame_name: str, image_name: str) -> PhotoImage:
        """
        Obtiene una imagen del caché o la carga si no existe
        
        Args:
            frame_name: Nombre del frame (frame0, frame1, etc.)
            image_name: Nombre del archivo de imagen
        
        Returns:
            PhotoImage object
        """
        cache_key = f"{frame_name}/{image_name}"
        
        if cache_key not in self.cache:
            image_path = self.base_path / "assets" / frame_name / image_name
            
            if not image_path.exists():
                raise FileNotFoundError(f"Imagen no encontrada: {image_path}")
            
            self.cache[cache_key] = PhotoImage(file=str(image_path))
        
        return self.cache[cache_key]
    
    def clear_cache(self):
        """Limpia el caché de imágenes"""
        self.cache.clear()
    
    def preload_frame_images(self, frame_name: str, image_names: list[str]):
        """
        Precarga todas las imágenes de un frame
        
        Args:
            frame_name: Nombre del frame
            image_names: Lista de nombres de imágenes a precargar
        """
        for image_name in image_names:
            self.get_image(frame_name, image_name)
