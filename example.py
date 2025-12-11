"""
Example usage of the Point dataclass from Mapeador de Conectividade.
"""

from mapeador_conectividade import Point


def main():
    """Demonstrate basic usage of the Point class."""
    
    # Create some points representing locations in a network
    sao_paulo = Point(
        id="sp",
        name="São Paulo",
        lat=-23.5505,
        lon=-46.6333,
        neighbors=["rj", "bh"]
    )
    
    rio_de_janeiro = Point(
        id="rj",
        name="Rio de Janeiro",
        lat=-22.9068,
        lon=-43.1729,
        neighbors=["sp", "bh"]
    )
    
    belo_horizonte = Point(
        id="bh",
        name="Belo Horizonte",
        lat=-19.9167,
        lon=-43.9345,
        neighbors=["sp", "rj"]
    )
    
    # Display the points
    points = [sao_paulo, rio_de_janeiro, belo_horizonte]
    
    print("Connectivity Network Points:")
    print("-" * 50)
    
    for point in points:
        print(f"\nID: {point.id}")
        print(f"Name: {point.name}")
        print(f"Location: ({point.lat}, {point.lon})")
        print(f"Connected to: {', '.join(point.neighbors)}")
    
    print("\n" + "-" * 50)
    print(f"Total points: {len(points)}")
    print(f"Total connections: {sum(len(p.neighbors) for p in points) // 2}")


if __name__ == "__main__":
    main()
