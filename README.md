# Voxmapper

Voxmapper is a graphical user interface (GUI) application for generating textures and grass maps using various noise algorithms. It utilizes the power of Perlin, Fractal and Turbulence noise types to create visually appealing heightmaps for use in Teardown.


## Features

- **Noise Generation**: Generate textures using different noise types (Perlin, fractal, turbulence, shape).
- **Grass Map Creation**: Create grass maps with adjustable parameters for density, noise amounts, and lightness.
- **Vignette Effects**: Apply vignette effects to enhance the visual quality of generated textures.
- **Export Options**: Save generated textures and grass maps as PNG files.
- **User-Friendly Interface**: Easy-to-use controls for adjusting parameters and previewing results in real-time.


## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- Pillow (for image processing)
- NumPy (for numerical operations)
- Noise (for noise generation)


## Installation

   Install the required packages:
   ```bash
   pip install pillow numpy noise
   ```


## Basic Usage

1. Run the application:
   ```bash
   python texture_generator_gui.py
   ```

2. Use the sliders in the GUI to adjust parameters for noise generation and grass map creation.

3. Click on the "Generate Noise", "Generate Greyscale Heightmap" or "Generate Grass Map" buttons to create your textures.

4. Use the "Export" buttons to save your generated images.


## Biome Tags

Enter one of these tags into the "biome" input field inside of the biome_ground.lua script in the map editor:

1. "default" - Default terrain
2. "desert" - Sandy desert
3. "snowy" - Snow-covered terrain
4. "swamp" - Wetland environment
5. "forest" - Temperate forest
6. "volcano" - Volcanic landscape
7. "tundra" - Arctic tundra
8. "alienjungle" - Alien jungle environment
9. "crystalfields" - Crystal formations
10. "beach" - Sandy beach
11. "coralreef" - Underwater coral reef
12. "savanna" - Golden grasslands
13. "canyon" - Red desert canyon
14. "mushroom" - Fungal landscape
15. "cave" - Dark cave system
16. "alpine" - Mountain environment
17. "bambooforest" - Green bamboo forest
18. "meadow" - Lush grass with wildflowers
19. "icelands" - Glacial environment
20. "jungle" - Dense tropical rainforest
21. "ashlands" - Volcanic ash-covered landscape
22. "mangrove" - Coastal wetland
23. "cherry" - Cherry blossom landscape
24. "highlands" - Rugged upland terrain
25. "mesa" - Layered red clay formations
26. "wasteland" - Barren environment
27. "taiga" - Northern coniferous forest
28. "corruption" - Purple magical corruption
29. "candyland" - Sweet-themed landscape
30. "ethereal" - Heavenly blue realm
31. "cyberpunk" - Urban futuristic landscape
32. "crimson" - Blood-red fantasy theme
33. "vaporwave" - Retro-futuristic aesthetic
34. "neon" - Electric green and yellow
35. "toxic" - Radioactive green environment
36. "glitch" - Digital glitch-themed
37. "underdark" - Fantasy underworld


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

