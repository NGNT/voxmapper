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
        """
        Generates a terrain heightmap with optional shadows and colors.

        Args:
            size (int): The size of the terrain (width and height).
            persistence (float): Controls the amplitude of successive octaves.
            scale (float): Controls the frequency of the noise.
            seed (int): The seed for random noise generation.
            min_height (float): The minimum height value.
            sun_position (list): The position of the sun for shadow generation.
            shadow_strength (float): The strength of the shadows.
            colors (list): A list of colors for terrain coloring.

        Returns:
            PIL.Image: The generated terrain as an image.
        """
        # Generate base heightmap
        if self.terrain_type == "mountains":
            height_data = self._generate_mountain_terrain(size, persistence, scale, seed, min_height)
        elif self.terrain_type == "sand":
            height_data = self._generate_sand_terrain(size, persistence, scale, seed, min_height)
        else:
            raise ValueError(f"Unknown terrain type: {self.terrain_type}")

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

    def _generate_mountain_terrain(self, size, persistence, scale, seed, min_height):
        """
        Generates a heightmap for mountain terrain.

        Args:
            size (int): The size of the terrain (width and height).
            persistence (float): Controls the amplitude of successive octaves.
            scale (float): Controls the frequency of the noise.
            seed (int): The seed for random noise generation.
            min_height (float): The minimum height value.

        Returns:
            np.ndarray: A 2D array representing the heightmap.
        """
        noise = SimplexNoise(seed)
        heightmap = np.zeros((size, size), dtype=np.float32)

        for y in range(size):
            for x in range(size):
                height = noise.simplexNoise(
                    type=NoiseTypeEnum.FRACTALNOISE,
                    size=size,
                    octaves=7,
                    persistence=persistence,
                    lacunarity=2.0,
                    scale=scale,
                    x=x,
                    y=y
                )
                height = max(height * (1 + (1 - min_height / 4)) - min_height, 0)
                heightmap[y, x] = height ** 2

        # Normalize to [0, 255]
        heightmap = (heightmap - heightmap.min()) / (heightmap.max() - heightmap.min()) * 255
        return heightmap.astype(np.uint8)

    def _generate_sand_terrain(self, size, persistence, scale, seed, min_height):
        """
        Generates a heightmap for sand terrain.

        Args:
            size (int): The size of the terrain (width and height).
            persistence (float): Controls the amplitude of successive octaves.
            scale (float): Controls the frequency of the noise.
            seed (int): The seed for random noise generation.
            min_height (float): The minimum height value.

        Returns:
            np.ndarray: A 2D array representing the heightmap.
        """
        noise = SimplexNoise(seed)
        heightmap = np.zeros((size, size), dtype=np.float32)

        for y in range(size):
            for x in range(size):
                height = noise.simplexNoise(
                    type=NoiseTypeEnum.FRACTALNOISE,
                    size=size,
                    octaves=7,
                    persistence=persistence,
                    lacunarity=2.0,
                    scale=scale,
                    x=x,
                    y=y
                )
                height = max(height * (1 + (1 - min_height / 4)) - min_height, 0)
                heightmap[y, x] = height ** 2

        # Normalize to [0, 255]
        heightmap = (heightmap - heightmap.min()) / (heightmap.max() - heightmap.min()) * 255
        return heightmap.astype(np.uint8)

    def _generate_shadow(self, size, sun_position, shadow_strength, height_data):
        """
        Generates shadows for the terrain based on the sun position.

        Args:
            size (int): The size of the terrain (width and height).
            sun_position (list): The position of the sun [x, y, z].
            shadow_strength (float): The strength of the shadows.
            height_data (np.ndarray): The heightmap data.

        Returns:
            np.ndarray: A 2D array representing the shadow map.
        """
        shadow_map = np.full((size, size), 255, dtype=np.uint8)
        sun_x, sun_y, sun_z = sun_position

        for y in range(size):
            for x in range(size):
                dx = x - sun_x
                dy = y - sun_y
                dz = sun_z - height_data[y, x]

                if dx == 0 and dy == 0:
                    continue

                distance = math.sqrt(dx ** 2 + dy ** 2)
                shadow = max(0, 255 - shadow_strength * (dz / distance))
                shadow_map[y, x] = min(shadow_map[y, x], shadow)

        return shadow_map

    def _generate_color(self, size, colors, height_data):
        """
        Maps height values to colors.

        Args:
            size (int): The size of the terrain (width and height).
            colors (list): A list of colors and their corresponding height percentages.
            height_data (np.ndarray): The heightmap data.

        Returns:
            np.ndarray: A 3D array representing the colored terrain.
        """
        color_data = np.zeros((size, size, 3), dtype=np.uint8)

        for y in range(size):
            for x in range(size):
                v = height_data[y, x] / 255

                if colors[0][1] > v:
                    color_data[y, x] = colors[0][0]
                else:
                    for col in range(1, len(colors)):
                        if colors[col][1] > v:
                            per = 1 - (v - colors[col - 1][1]) / (colors[col][1] - colors[col - 1][1])
                            color_data[y, x] = (
                                per * np.array(colors[col - 1][0]) +
                                (1.0 - per) * np.array(colors[col][0])
                            ).astype(np.uint8)
                            break

                if v > colors[-1][1]:
                    color_data[y, x] = colors[-1][0]

        return color_data

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