# ===========================================
# src/__init__.py
# Inicialización del paquete src
# Autor: Fernando Raúl Robles
# ===========================================

# Este archivo convierte la carpeta "src" en un paquete de Python,
# permitiendo las importaciones relativas como:
#    from src.db_connection import init_connection
#    from src.data_loader import load_data

# (Opcional) Podés centralizar aquí imports si querés exponerlos globalmente.
from .db_connection import init_connection
from .data_loader import load_data
