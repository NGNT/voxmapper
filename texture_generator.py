import numpy as np
from PIL import Image
import random
import math

class NoiseTypeEnum:
    PERLINNOISE = 0
    FRACTALNOISE = 1
    TURBULENCE = 2
    SHAPE_NOISE = 3

class SimplexNoise:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)
        
        # Initialize gradient tables for 3D and 4D
        self.grad3 = [
            [1,1,0], [-1,1,0], [1,-1,0], [-1,-1,0],
            [1,0,1], [-1,0,1], [1,0,-1], [-1,0,-1],
            [0,1,1], [0,-1,1], [0,1,-1], [0,-1,-1]
        ]
        
        self.grad4 = [
            [0,1,1,1], [0,1,1,-1], [0,1,-1,1], [0,1,-1,-1],
            [0,-1,1,1], [0,-1,1,-1], [0,-1,-1,1], [0,-1,-1,-1],
            [1,0,1,1], [1,0,1,-1], [1,0,-1,1], [1,0,-1,-1],
            [-1,0,1,1], [-1,0,1,-1], [-1,0,-1,1], [-1,0,-1,-1],
            [1,1,0,1], [1,1,0,-1], [1,-1,0,1], [1,-1,0,-1],
            [-1,1,0,1], [-1,1,0,-1], [-1,-1,0,1], [-1,-1,0,-1],
            [1,1,1,0], [1,1,-1,0], [1,-1,1,0], [1,-1,-1,0],
            [-1,1,1,0], [-1,1,-1,0], [-1,-1,1,0], [-1,-1,-1,0]
        ]
        
        # Initialize permutation table
        self.p = list(range(256))
        random.shuffle(self.p)
        self.p = self.p * 2
        
        # Skewing and unskewing factors for 2D
        self.F2 = 0.5 * (math.sqrt(3.0) - 1.0)
        self.G2 = (3.0 - math.sqrt(3.0)) / 6.0
        
        # Skewing and unskewing factors for 3D
        self.F3 = 1.0 / 3.0
        self.G3 = 1.0 / 6.0
        
        # Skewing and unskewing factors for 4D
        self.F4 = (math.sqrt(5.0) - 1.0) / 4.0
        self.G4 = (5.0 - math.sqrt(5.0)) / 20.0

    def dot2(self, g, x, y):
        return g[0]*x + g[1]*y

    def dot3(self, g, x, y, z):
        return g[0]*x + g[1]*y + g[2]*z

    def dot4(self, g, x, y, z, w):
        return g[0]*x + g[1]*y + g[2]*z + g[3]*w

    def noise2d(self, xin, yin):
        # Skew the input space to determine which simplex cell we're in
        s = (xin + yin) * self.F2
        i = int(xin + s)
        j = int(yin + s)
        
        t = (i + j) * self.G2
        X0 = i - t
        Y0 = j - t
        x0 = xin - X0
        y0 = yin - Y0
        
        # For the 2D case, the simplex shape is an equilateral triangle.
        # Determine which simplex we are in.
        i1, j1 = 0, 1
        if x0 > y0:
            i1, j1 = 1, 0
            
        # A step of (1,0) in (i,j) means a step of (1-c,-c) in (x,y), and
        # a step of (0,1) in (i,j) means a step of (-c,1-c) in (x,y), where
        # c = (3-sqrt(3))/6
        x1 = x0 - i1 + self.G2
        y1 = y0 - j1 + self.G2
        x2 = x0 - 1.0 + 2.0 * self.G2
        y2 = y0 - 1.0 + 2.0 * self.G2
        
        # Work out the hashed gradient indices of the three simplex corners
        ii = i & 255
        jj = j & 255
        gi0 = self.p[ii + self.p[jj]] % 12
        gi1 = self.p[ii + i1 + self.p[jj + j1]] % 12
        gi2 = self.p[ii + 1 + self.p[jj + 1]] % 12
        
        # Calculate the contribution from the three corners
        n0, n1, n2 = 0, 0, 0
        
        # Calculate the contribution from the three corners
        t0 = 0.5 - x0*x0 - y0*y0
        if t0 >= 0:
            t0 *= t0
            n0 = t0 * t0 * self.dot2(self.grad3[gi0], x0, y0)
            
        t1 = 0.5 - x1*x1 - y1*y1
        if t1 >= 0:
            t1 *= t1
            n1 = t1 * t1 * self.dot2(self.grad3[gi1], x1, y1)
            
        t2 = 0.5 - x2*x2 - y2*y2
        if t2 >= 0:
            t2 *= t2
            n2 = t2 * t2 * self.dot2(self.grad3[gi2], x2, y2)
            
        # Add contributions from each corner to get the final noise value.
        # The result is scaled to return values in the interval [-1,1].
        return 70.0 * (n0 + n1 + n2)

    def noise4d(self, x, y, z, w):
        # Placeholder for 4D noise
        return 0.0

    def simplexNoise(self, type, size, octaves, persistence, lacunarity, scale, x, y):
        if type == NoiseTypeEnum.PERLINNOISE:
            return self.noise2d(x/scale, y/scale)
        elif type == NoiseTypeEnum.FRACTALNOISE:
            total = 0
            frequency = 1.0
            amplitude = 1.0
            maxValue = 0
            
            for i in range(octaves):
                total += self.noise2d((x/scale) * frequency, (y/scale) * frequency) * amplitude
                maxValue += amplitude
                amplitude *= persistence
                frequency *= lacunarity
                
            return total / maxValue
        elif type == NoiseTypeEnum.TURBULENCE:
            total = 0
            frequency = 1.0
            amplitude = 1.0
            maxValue = 0
            
            for i in range(octaves):
                total += abs(self.noise2d((x/scale) * frequency, (y/scale) * frequency)) * amplitude
                maxValue += amplitude
                amplitude *= persistence
                frequency *= lacunarity
                
            return total / maxValue
        return 0.0

class TextureGenerator:
    def __init__(self, seed=None):
        self.noise = SimplexNoise(seed)
        self.terrain_type = "mountains"
        self.terrain_colored = True
        self.terrain_shadow = True
        self.terrain_shadow_x = -1400.0
        self.terrain_shadow_y = -1400.0

    def generate_terrain(self, size, persistence, scale, seed, min_height, 
                        sun_position=None, shadow_strength=0.5, colors=None):
        # Generate base heightmap
        if self.terrain_type == "mountains":
            height_data = self._generate_mountain_terrain(size, persistence, scale, seed, min_height)
        else:
            height_data = self._generate_sand_terrain(size, persistence, scale, seed, min_height)
        
        # Generate shadow if enabled
        shadow_data = None
        if self.terrain_shadow and sun_position is not None:
            shadow_data = self._generate_shadow(size, sun_position, shadow_strength, height_data)
        
        # Generate color if enabled
        color_data = None
        if self.terrain_colored and colors is not None:
            color_data = self._generate_color(size, colors, height_data)
        
        # Combine all layers
        if color_data is not None and shadow_data is not None:
            final_data = (color_data * (shadow_data[:, :, np.newaxis] / 255)).astype(np.uint8)
        elif color_data is not None:
            final_data = color_data
        elif shadow_data is not None:
            final_data = np.stack([shadow_data] * 3, axis=-1).astype(np.uint8)
        else:
            final_data = np.stack([height_data] * 3, axis=-1).astype(np.uint8)
        
        return Image.fromarray(final_data)

    def _generate_color(self, size, colors, height_data):
        color_data = np.zeros((size, size, 3), dtype=np.uint8)
        
        for y in range(size):
            for x in range(size):
                v = height_data[y, x] / 255
                
                if colors[0][1] > v:
                    color_data[y, x] = colors[0][0]
                else:
                    for col in range(1, len(colors)):
                        if colors[col][1] > v:
                            per = 1 - (v - colors[col-1][1]) / (colors[min(col, len(colors)-1)][1] - colors[col-1][1])
                            color_data[y, x] = (
                                per * np.array(colors[col-1][0]) + 
                                (1.0-per) * np.array(colors[min(col, len(colors)-1)][0])
                            ).astype(np.uint8)
                            break
                
                if v > colors[-1][1]:
                    color_data[y, x] = colors[-1][0]
        
        return color_data

    def generate_shape_noise(self, size, shape_type="circle", shape_size=10, spacing=5):
        """
        Vectorized generation of shape-based noise.

        Args:
            size (int): Output resolution (square)
            shape_type (str): "circle", "square", "pyramid"
            shape_size (int): Size of each shape
            spacing (int): Space between shapes

        Returns:
            np.ndarray: 2D float32 array with shape intensity
        """
        noise = np.zeros((size, size), dtype=np.float32)
        yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing='ij')

        for y0 in range(0, size, shape_size + spacing):
            for x0 in range(0, size, shape_size + spacing):
                if shape_type == "circle":
                    diameter = shape_size * 2
                    cy, cx = np.ogrid[:diameter, :diameter]
                    circle_mask = (cx - shape_size)**2 + (cy - shape_size)**2 <= shape_size**2

                    for y0 in range(0, size, shape_size + spacing):
                        for x0 in range(0, size, shape_size + spacing):
                            y1, y2 = y0, min(y0 + diameter, size)
                            x1, x2 = x0, min(x0 + diameter, size)
                            mask_slice_y = slice(0, y2 - y1)
                            mask_slice_x = slice(0, x2 - x1)

                            noise[y1:y2, x1:x2][circle_mask[mask_slice_y, mask_slice_x]] = 1.0
                elif shape_type == "square":
                    x_start = max(0, x0 - shape_size // 2)
                    x_end = min(size, x0 + shape_size // 2)
                    y_start = max(0, y0 - shape_size // 2)
                    y_end = min(size, y0 + shape_size // 2)
                    noise[y_start:y_end, x_start:x_end] = 1.0
                elif shape_type == "pyramid":
                    half = shape_size // 2
                    for dy in range(-half, half + 1):
                        for dx in range(-half, half + 1):
                            px, py = x0 + dx, y0 + dy
                            if 0 <= px < size and 0 <= py < size:
                                height = max(0, half - max(abs(dx), abs(dy)))
                                noise[py, px] = max(noise[py, px], height / half if half else 1.0)
        return noise

def main():
    # Example usage
    generator = TextureGenerator(seed=42)
    
    # Generate mountain terrain
    img = generator.generate_terrain(
        size=512,
        persistence=0.6,
        scale=150.0,
        seed=42,
        min_height=0.3,
        sun_position=[-1400.0, -1400.0, 255],
        shadow_strength=0.5,
        colors=[
            [(180, 140, 100), 0.3],  # Sand
            [(34, 139, 34), 0.6],    # Grass
            [(100, 100, 100), 0.85], # Rock
            [(255, 255, 255), 1.0]   # Snow
        ]
    )
    
    # Save the image
    img.save("terrain_output.png")
    print("Terrain generated and saved as terrain_output.png")

if __name__ == "__main__":
    main() 