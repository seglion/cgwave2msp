# Archivo: test_cgi_reader.py
import unittest
import numpy as np
from cgwave2msp.cgi_reader import CGIReader
from cgwave2msp.open_boundary import OpenBoundary
from cgwave2msp.coastline import Coastline
from cgwave2msp.nodes import Nodes
from cgwave2msp.elements import Elements
from unittest.mock import patch, mock_open

class TestCGIReader(unittest.TestCase):
    def setUp(self):
        # Datos simulados para la prueba
        self.mock_data = """
        &C
        1 100 0.0 0.0 30.0 90.0
        1 2 3 4 5 6 7 8 9
        10 11 12 13 14 15 16 17 18
        &B
        5 0.5
        20 21 22 23 24
        &N
        4
        1.0 2.0 3.0 4.0 5.0 6.0
        7.0 8.0 9.0 10.0 11.0 12.0
        &E
        3
        1 2 3 4
        5 6 7 8
        9 10 11 12
        """

    @patch("builtins.open", new_callable=mock_open, read_data="""
        &C
        1 100 0.0 0.0 30.0 90.0
        1 2 3 4 5 6 7 8 9
        10 11 12 13 14 15 16 17 18
        &B
        5 0.5
        20 21 22 23 24
        &N
        4
        1.0 2.0 3.0 4.0 5.0 6.0
        7.0 8.0 9.0 10.0 11.0 12.0
        &E
        3
        1 2 3 4
        5 6 7 8
        9 10 11 12
        """)
    def test_read_file(self, mock_file):
        # Crear instancia del CGIReader con el archivo simulado
        reader = CGIReader("fake_path.cgi")

        # Pruebas para OpenBoundary
        self.assertEqual(len(reader.open_boundaries), 1)
        self.assertIsInstance(reader.open_boundaries[0], OpenBoundary)
        self.assertEqual(reader.open_boundaries[0].boundary_type, 1)
        self.assertEqual(reader.open_boundaries[0].num_nodes, 100)
        self.assertEqual(len(reader.open_boundaries[0].node_id), 18)
        
        # Pruebas para Coastline
        self.assertEqual(len(reader.coastlines), 1)
        self.assertIsInstance(reader.coastlines[0], Coastline)
        self.assertEqual(reader.coastlines[0].num_nodes, 5)
        self.assertEqual(len(reader.coastlines[0].node_id), 5)
        
        # Pruebas para Nodes
        self.assertIsNotNone(reader.nodes)
        self.assertIsInstance(reader.nodes, Nodes)
        self.assertEqual(reader.nodes.coordinates.shape, (4, 4))  # Incluye ID de nodo
        
        # Pruebas para Elements
        self.assertIsNotNone(reader.elements)
        self.assertIsInstance(reader.elements, Elements)
        self.assertEqual(reader.elements.elements.shape, (3, 4))  # 3 elementos, 4 valores cada uno

    @patch("builtins.open", new_callable=mock_open, read_data="""
        &C
        1 100 0.0 0.0 30.0 90.0
        1 2 3 4 5 6 7 8 9
        10 11 12 13 14 15 16 17 18
        &B
        5 0.5
        20 21 22 23 24
        &N
        4
        1.0 2.0 3.0 4.0 5.0 6.0
        7.0 8.0 9.0 10.0 11.0 12.0
        &E
        3
        1 2 3 4
        5 6 7 8
        9 10 11 12
        """)
    def test_show_methods(self, mock_file):
        # Crear instancia del CGIReader con el archivo simulado
        reader = CGIReader("fake_path.cgi")

        # Probar los métodos show
        with patch("builtins.print") as mocked_print:
            reader.show_open_boundaries()
            reader.show_coastlines()
            # Verificar que se llamó a la función print
            self.assertTrue(mocked_print.called)

if __name__ == "__main__":
    unittest.main()
