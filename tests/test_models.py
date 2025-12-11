"""Tests for the Point dataclass."""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from mapeador_conectividade.models import Point


def test_point_creation():
    """Test that a Point can be created with all required fields."""
    point = Point(
        id="p1",
        name="Ponto Central",
        lat=-23.5505,
        lon=-46.6333,
        neighbors=["p2", "p3"]
    )
    
    assert point.id == "p1"
    assert point.name == "Ponto Central"
    assert point.lat == -23.5505
    assert point.lon == -46.6333
    assert point.neighbors == ["p2", "p3"]
    print("✓ Point creation test passed")


def test_point_empty_neighbors():
    """Test that a Point can be created with empty neighbors list."""
    point = Point(
        id="p2",
        name="Ponto Isolado",
        lat=-23.5505,
        lon=-46.6333,
        neighbors=[]
    )
    
    assert point.neighbors == []
    print("✓ Point with empty neighbors test passed")


def test_point_dataclass_features():
    """Test that Point has dataclass features like equality."""
    point1 = Point("p1", "Point 1", 0.0, 0.0, ["p2"])
    point2 = Point("p1", "Point 1", 0.0, 0.0, ["p2"])
    point3 = Point("p2", "Point 2", 1.0, 1.0, [])
    
    assert point1 == point2
    assert point1 != point3
    print("✓ Dataclass equality test passed")


if __name__ == "__main__":
    test_point_creation()
    test_point_empty_neighbors()
    test_point_dataclass_features()
    print("\nAll tests passed! ✓")
