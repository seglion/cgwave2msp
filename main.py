
# Archivo: main.py
from cgwave2msp.cgi_reader import CGIReader

# Uso de la clase CGIReader
file_path = r'K:\T2024\T2024-47-PECIO_PORTS IB\04.MODELOS\04.SMS/Propuesta_AQ.cgi'
tide=[0.0,1.0]
key = 'Prueba'
cgi_reader = CGIReader(file_path,key,tide)


# Mostrar toda la información de las instancias creadas
cgi_reader.show_open_boundaries()

# Mostrar toda la información de las Coastlines creadas
cgi_reader.show_coastlines()
cgi_reader.calculate_North_Orientation_Mesh()
cgi_reader.create_mesh_file()
cgi_reader.create_contour_file()


