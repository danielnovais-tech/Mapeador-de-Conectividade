"""
Tests for the Point dataclass.
"""

import unittest
from mapeador_conectividade.point import Point


class TestPoint(unittest.TestCase):
    """Test cases for the Point dataclass."""
    
    def test_point_creation(self):
        """Test that a Point can be created with all required fields."""
        point = Point(
            id="p1",
            name="Point 1",
            lat=-23.5505,
            lon=-46.6333,
            neighbors=["p2", "p3"]
        )
        
        self.assertEqual(point.id, "p1")
        self.assertEqual(point.name, "Point 1")
        self.assertEqual(point.lat, -23.5505)
        self.assertEqual(point.lon, -46.6333)
        self.assertEqual(point.neighbors, ["p2", "p3"])
    
    def test_point_empty_neighbors(self):
        """Test that a Point can be created with an empty neighbors list."""
        point = Point(
            id="p1",
            name="Isolated Point",
            lat=0.0,
            lon=0.0,
            neighbors=[]
        )
        
        self.assertEqual(point.neighbors, [])
        self.assertIsInstance(point.neighbors, list)
    
    def test_point_equality(self):
        """Test that two Points with the same data are equal."""
        point1 = Point(
            id="p1",
            name="Point 1",
            lat=-23.5505,
            lon=-46.6333,
            neighbors=["p2"]
        )
        point2 = Point(
            id="p1",
            name="Point 1",
            lat=-23.5505,
            lon=-46.6333,
            neighbors=["p2"]
        )
        
        self.assertEqual(point1, point2)
    
    def test_point_string_representation(self):
        """Test the string representation of a Point."""
        point = Point(
            id="p1",
            name="Test Point",
            lat=10.0,
            lon=20.0,
            neighbors=["p2"]
        )
        
        # Dataclasses provide a default __repr__
        repr_str = repr(point)
        self.assertIn("p1", repr_str)
        self.assertIn("Test Point", repr_str)


if __name__ == '__main__':
    unittest.main()
