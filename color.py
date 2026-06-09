class Color:

    # Allowed color difference
    COLOR_TOLERANCE = 10

    """Class representing a color"""
    def __init__(self, r : int, g : int, b : int):
        self.__r = r
        self.__g = g
        self.__b = b
    
    def get_color(self) -> tuple:
        return (self.__r, self.__g, self.__b)
    
    def are_close(self, other_color : Color, tolerance : int = COLOR_TOLERANCE) -> bool:
        """Check if this color is close to another color within a given tolerance."""
        r1, g1, b1 = self.get_color()
        r2, g2, b2 = other_color.get_color() if isinstance(other_color, Color) else other_color
        return all(abs(a - b) <= tolerance for a, b in zip((r1, g1, b1), (r2, g2, b2)))