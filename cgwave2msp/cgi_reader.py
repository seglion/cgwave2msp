# Archivo: cgi_reader.py
import numpy as np
import matplotlib.pyplot as plt
from cgwave2msp.open_Boundary import OpenBoundary
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

    
    def cartesian_to_meteorological(self,cartesian_angle):

        meteo_angle = (90 - cartesian_angle) % 360
        return meteo_angle


    def calculate_North_Orientation_Mesh(self):
        """
        Ajusta los nodos del OpenBoundary para que el centro del círculo esté en (0, 0) y el semicirculo esté orientado hacia el norte.
        """
        open_boundary = self.open_boundaries[0]
        
        nodes = self.nodes.coordinates

        id_start = open_boundary.node_id[0]
        id_end = open_boundary.node_id[-1]


        start_node = self.nodes.coordinates[id_start - 1]
        end_node = self.nodes.coordinates[id_end - 1]
        
        avg_x = (start_node[1] + end_node[1]) / 2
        avg_y = (start_node[2] + end_node[2]) / 2

        # Calcular el desplazamiento necesario para centrar el OpenBoundary en (0, 0)
        delta_x = -avg_x
        delta_y = -avg_y

        # Aplicar la traslación a los nodos
        adjusted_nodes = []



        for node_id in nodes[:,0]:
            node_index = node_id - 1  # Asumimos que los node_ids son índices 1-based

            if nodes is not None and node_index < len(self.nodes.coordinates):
               
                original_node = nodes[int(node_index)]
                
                adjusted_x = original_node[1] + delta_x
                adjusted_y = original_node[2] + delta_y

                adjusted_nodes.append([original_node[0], adjusted_x, adjusted_y, original_node[3]])
            
            # Orientar hacia el norte (rotación para hacer que initial_angle sea 0)
        print(open_boundary.orientation_angle)
        angle_radians = -np.radians(open_boundary.orientation_angle-90)
        
        rotated_nodes = []
        for node in adjusted_nodes:
            x = node[1]
            y = node[2]
            rotated_x = x * np.cos(angle_radians) - y * np.sin(angle_radians)
            rotated_y = x * np.sin(angle_radians) + y * np.cos(angle_radians)
            rotated_nodes.append([node[0], rotated_x, rotated_y, node[3]])


            # Actualizar los nodos del OpenBoundary
        adjusted_nodes = np.array(adjusted_nodes)
        self.nodesRotaded = Nodes(np.array(rotated_nodes))
           

        print(f"Adjusted OpenBoundary with calculated center between start and end nodes at ({avg_x}, {avg_y}) and oriented north.")
        plt.figure()
        plt.plot(adjusted_nodes[:,1], adjusted_nodes[:,2], 'ro')
        plt.plot(self.nodesRotaded.coordinates [:,1],self.nodesRotaded.coordinates [:,2], 'bo')
        plt.show()


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


