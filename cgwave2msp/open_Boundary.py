
# Archivo: open_boundary.py
class OpenBoundary:
    def __init__(self, boundary_type, num_nodes, center_x, center_y, initial_angle, orientation_angle, node_id):
        self.boundary_type = boundary_type
        self.num_nodes = num_nodes
        self.center_x = center_x
        self.center_y = center_y
        self.initial_angle = initial_angle
        self.orientation_angle = orientation_angle
        self.node_id = node_id

    def show_boundary_info(self):
        """
        Muestra la información del límite abierto.
        """
        print(f"Type of Open Boundary: {self.boundary_type}")
        print(f"Number of Nodes: {self.num_nodes}")
        print(f"Center of Circle - X: {self.center_x}")
        print(f"Center of Circle - Y: {self.center_y}")
        print(f"Initial Angle: {self.initial_angle}")
        print(f"Orientation Angle: {self.orientation_angle}")
        print(f"Node ID: {self.node_id}")