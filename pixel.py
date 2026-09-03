from color import Color


class Pixel:
    """Class representing a pixel with coordinates and color"""
    
    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.color = color
    
    def has_same_color(self, other_pixel: 'Pixel', tolerance: int = None) -> bool:
        """Check if this pixel has the same color as another pixel"""
        if tolerance is None:
            return self.color.are_close(other_pixel.color)
        return self.color.are_close(other_pixel.color, tolerance)
    
    def is_higher(self, other_pixel: 'Pixel') -> bool:
        """Check if this pixel is higher (smaller y) than another pixel"""
        return self.y < other_pixel.y
    
    def is_lower(self, other_pixel: 'Pixel') -> bool:
        """Check if this pixel is lower (larger y) than another pixel"""
        return self.y > other_pixel.y
    
    def is_left_of(self, other_pixel: 'Pixel') -> bool:
        """Check if this pixel is to the left (smaller x) of another pixel"""
        return self.x < other_pixel.x
    
    def is_right_of(self, other_pixel: 'Pixel') -> bool:
        """Check if this pixel is to the right (larger x) of another pixel"""
        return self.x > other_pixel.x
    
    def distance_to(self, other_pixel: 'Pixel') -> float:
        """Calculate the Euclidean distance to another pixel"""
        return ((self.x - other_pixel.x) ** 2 + (self.y - other_pixel.y) ** 2) ** 0.5
    
    def __repr__(self) -> str:
        """String representation of the pixel"""
        return f"Pixel({self.x}, {self.y}, {self.color.get_color()})"
    
    def __str__(self) -> str:
        """User-friendly string representation"""
        return f"Pixel at ({self.x}, {self.y}) with color {self.color.get_color()}"
