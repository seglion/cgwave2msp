# Archivo: cgi_reader.py
import numpy as np
from cgwave2msp.open_boundary import OpenBoundary
from cgwave2msp.coastline import Coastline
from cgwave2msp.nodes import Nodes
from cgwave2msp.elements import Elements

class CGIReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.parameters = {}
        self.open_boundaries = []  # Puede haber múltiples OpenBoundary
        self.coastlines = []  # Puede haber múltiples Coastline
        self.nodes = None
        self.elements = None
        self._read_file()

    def _read_file(self):
        """
        Lee el archivo CGI y extrae los comentarios y sus valores correspondientes.
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as file:
                
                lines = file.readlines()
                
                i = 0

                while i < len(lines):
                    
                    line = lines[i].strip()
                    
                    # Identificamos un bloque de OpenBoundary
                    if line.startswith('&C'):
                        
                        i += 1
                        # La primera línea después de &C contiene todos los valores
                        values = lines[i].strip().split()

                        # Verificamos que haya suficientes valores
                        if len(values) < 6:
                            
                            
                            
                            continue

                        # Crear la instancia de OpenBoundary
                        try:
                            open_boundary = OpenBoundary(
                                boundary_type=int(values[0]),
                                num_nodes=int(values[1]),
                                center_x=float(values[2]),
                                center_y=float(values[3]),
                                initial_angle=float(values[4]),
                                orientation_angle=float(values[5]),
                                node_id=[]  # Inicialmente vacío, se llenará más adelante
                            )
                        except ValueError as ve:
                            
                            
                            continue

                        # Leer los nodos asociados
                        nodes = []
                            
                        while True:
                            
                            i += 1  # Incrementamos antes de cualquier verificación para evitar bucles infinitos
                            
                            if i >= len(lines):
                                break
                            node_line = lines[i].strip()

                            if node_line.startswith('&'):
                                
                                    i -= 1
                                    break
                            if node_line.startswith('%') or not node_line:
                                
                                # Si se encuentra otro bloque, no incrementar i para procesarlo

                                # Termina la lectura de nodos si llega un comentario, otro bloque, o una línea vacía
                                break
                            nodes.extend(node_line.split())

                        open_boundary.node_id = [int(node) for node in nodes]
                        self.open_boundaries.append(open_boundary)
                    # Identificamos un bloque de Elementos
                    elif line.startswith('&E'):
                        i += 1
                        # La siguiente línea contiene el número de nodos
                        num_elements = int(lines[i].strip())
                        elements = []
                        # Leer las coordenadas de los nodos
                        while True:
                            i += 1
                            if i >= len(lines):
                                break
                            elements_line = lines[i].strip()
                            if elements_line.startswith('&'):
                                i -= 1
                                break
                            if elements_line.startswith('%') or not node_line:
                                break
                            values = elements_line.split()
                            # Verificar que la cantidad de valores sea múltiplo de 3
                            if len(values) % 4 != 0:
                                print(f"Advertencia: Se esperaban múltiplos de 4 valores en la línea de nodos, pero se encontraron {len(values)}. Se ignorarán los valores restantes.")
                                values = values[:len(values) - (len(values) % 4)]
                            # Cada línea contiene uno o más conjuntos de coordenadas
                            for j in range(0, len(values), 4):
                                try:
                                    elements.append([float(values[j]), float(values[j+1]), float(values[j+2]), float(values[j+3])])
                                except ValueError as e:
                                    print(f"Error al convertir los valores de coordenadas en la línea {i}: {e}")
                        # Crear la instancia de Nodes
                        # coordinates_with_id = [[idx + 1] + coord for idx, coord in enumerate(coordinates)]
                        self.elements = Elements(np.array(elements))
                        print(f"Se leyeron {len(elements)} elementos.")                        
                        

                    # Identificamos un bloque de Nodos
                    elif line.startswith('&N'):
                        i += 1
                        # La siguiente línea contiene el número de nodos
                        num_nodes = int(lines[i].strip())
                        coordinates = []
                        # Leer las coordenadas de los nodos
                        while True:
                            i += 1
                            if i >= len(lines):
                                break
                            node_line = lines[i].strip()
                            if node_line.startswith('&'):
                                i -= 1
                                break
                            if node_line.startswith('%') or not node_line:
                                break
                            values = node_line.split()
                            # Verificar que la cantidad de valores sea múltiplo de 3
                            if len(values) % 3 != 0:
                                print(f"Advertencia: Se esperaban múltiplos de 3 valores en la línea de nodos, pero se encontraron {len(values)}. Se ignorarán los valores restantes.")
                                values = values[:len(values) - (len(values) % 3)]
                            # Cada línea contiene uno o más conjuntos de coordenadas
                            for j in range(0, len(values), 3):
                                try:
                                    coordinates.append([float(values[j]), float(values[j+1]), float(values[j+2])])
                                except ValueError as e:
                                    print(f"Error al convertir los valores de coordenadas en la línea {i}: {e}")
                        # Crear la instancia de Nodes
                        coordinates_with_id = [[idx + 1] + coord for idx, coord in enumerate(coordinates)]
                        self.nodes = Nodes(np.array(coordinates_with_id))
                        print(f"Se leyeron {len(coordinates)} nodos.")

                    elif line.startswith('&B'):
                        
                        
                        i += 1
                        # La línea después de &B contiene los valores de Coastline
                        values = lines[i].strip().split()

                        # Verificamos que haya suficientes valores
                        if len(values) < 2:
                            
                            
                            continue

                        # Crear la instancia de Coastline
                        try:
                            coastline = Coastline(
                                num_nodes=int(values[0]),
                                reflection_coefficient=float(values[1]),
                                node_id=[]  # Inicialmente vacío, se llenará más adelante
                            )
                        except ValueError as ve:
                            
                            continue
                        

                        # Leer los nodos asociados
                        nodes = []
                        while True:
                            i += 1  # Incrementamos antes de cualquier verificación para evitar bucles infinitos
                            if i >= len(lines):
                                break
                            node_line = lines[i].strip()
                            if node_line.startswith('&'):
                                    i -= 1
                                    break  # Dejamos que la iteración principal maneje el nuevo bloque
                            if node_line.startswith('%') or not node_line:
                                # Si se encuentra otro bloque, procesar ese bloque sin incrementar i

                                # Termina la lectura de nodos si llega un comentario, otro bloque, o una línea vacía
                                break
                            nodes.extend(node_line.split())

                        coastline.node_id = [int(node) for node in nodes]
                        self.coastlines.append(coastline)
                        
                    i += 1
                    
                    
        except FileNotFoundError:
            print(f"Error: El archivo {self.filepath} no fue encontrado.")
        except ValueError as ve:
            print(f"Error al convertir un valor: {ve}")
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
    def show_open_boundaries(self):
        """
        Muestra la información de todas las OpenBoundary creadas.
        """
        for idx, open_boundary in enumerate(self.open_boundaries):
            print(f"\n--- Open Boundary Info {idx + 1} ---")
            open_boundary.show_boundary_info()
            print(f"Length of Node ID Array: {len(open_boundary.node_id)}")

    def show_coastlines(self):
        """
        Muestra la información de todas las Coastline creadas.
        """
        for idx, coastline in enumerate(self.coastlines):
            print(f"\n--- Coastline Info {idx + 1} ---")
            coastline.show_coastline_info()
            print(f"Length of Node ID Array: {len(coastline.node_id)}")