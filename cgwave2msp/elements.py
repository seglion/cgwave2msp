import numpy as np
class Elements:
    def __init__(self, elements):
        if isinstance(elements, np.ndarray) and elements.shape[1] == 4:
            self.elements = elements
        else:
            raise ValueError("Elements must be a numpy array with 4 columns")

    def show_elements_info(self):
        """
        Muestra la información de los elementos (array de 4 columnas).
        """
        print(f"Elements Array (4 columns):\n{self.elements}")