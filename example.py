"""Example usage of the Point dataclass."""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from mapeador_conectividade import Point


def main():
    """Demonstrate the usage of the Point dataclass."""
    
    # Create some example points
    point1 = Point(
        id="p1",
        name="São Paulo",
        lat=-23.5505,
        lon=-46.6333,
        neighbors=["p2", "p3"]
    )
    
    point2 = Point(
        id="p2",
        name="Rio de Janeiro",
        lat=-22.9068,
        lon=-43.1729,
        neighbors=["p1", "p3"]
    )
    
    point3 = Point(
        id="p3",
        name="Belo Horizonte",
        lat=-19.9167,
        lon=-43.9345,
        neighbors=["p1", "p2"]
    )
    
    # Display the points
    print("=== Mapeador de Conectividade - Example ===\n")
    
    points = [point1, point2, point3]
    
    for point in points:
        print(f"Point ID: {point.id}")
        print(f"  Name: {point.name}")
        print(f"  Location: ({point.lat}, {point.lon})")
        print(f"  Connected to: {', '.join(point.neighbors)}")
        print()


if __name__ == "__main__":
    main()
