"""
Test suite for the Fallero model.
"""

import unittest
from datetime import date
from models.fallero import Fallero


class TestFalleroModel(unittest.TestCase):
    """Test cases for the Fallero model."""
    
    def test_fallero_creation(self):
        """Test creating a Fallero instance."""
        fallero = Fallero(
            nombre="Juan",
            apellidos="García López",
            dni="12345678A",
            fecha_nacimiento=date(1990, 1, 1),
            fecha_alta=date.today(),
            activo=True
        )
        
        self.assertEqual(fallero.nombre, "Juan")
        self.assertEqual(fallero.apellidos, "García López")
        self.assertEqual(fallero.dni, "12345678A")
        self.assertTrue(fallero.activo)
    
    def test_fallero_full_name_property(self):
        """Test the full_name property."""
        fallero = Fallero(
            nombre="Juan",
            apellidos="García López",
            dni="12345678A",
            fecha_nacimiento=date(1990, 1, 1),
            fecha_alta=date.today()
        )
        
        self.assertEqual(fallero.full_name, "Juan García López")
    
    def test_fallero_repr(self):
        """Test string representation of Fallero."""
        fallero = Fallero(
            id=1,
            nombre="Juan",
            apellidos="García López",
            dni="12345678A",
            fecha_nacimiento=date(1990, 1, 1),
            fecha_alta=date.today()
        )
        
        expected = "<Fallero(id=1, nombre='Juan', apellidos='García López')>"
        self.assertEqual(repr(fallero), expected)


if __name__ == '__main__':
    unittest.main()