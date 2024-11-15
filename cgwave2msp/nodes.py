import numpy as np
class Nodes:
    def __init__(self, coordinates):
        if isinstance(coordinates, np.ndarray) and coordinates.shape[1] == 4:
            self.coordinates = coordinates
        else:
            raise ValueError("Coordinates must be a numpy array with 4 columns")

    def show_nodes_info(self):
        """
        Muestra la información de los nodos (coordenadas y profundidad).
        """
        print(f"Node Coordinates and Depth (4 columns):\n{self.coordinates}")