class Coastline:
    def __init__(self, num_nodes, reflection_coefficient, node_id):
        self.num_nodes = num_nodes
        self.reflection_coefficient = reflection_coefficient
        self.node_id = node_id

    def show_coastline_info(self):
        """
        Muestra la información de la línea de costa.
        """
        print(f"Number of Nodes: {self.num_nodes}")
        print(f"Reflection Coefficient: {self.reflection_coefficient}")
        print(f"Node ID: {self.node_id}")
