
# Archivo: main.py
from cgwave2msp.cgi_reader import CGIReader

# Uso de la clase CGIReader
file_path = r'K:\T2024\T2024-47-PECIO_PORTS IB\04.MODELOS\04.SMS/Propuesta_AQ.cgi'
cgi_reader = CGIReader(file_path)


# Mostrar toda la información de las instancias creadas
cgi_reader.show_open_boundaries()
