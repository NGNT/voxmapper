# Voxmapper

Voxmapper is a graphical user interface (GUI) application for generating textures and grass maps using various noise algorithms. It utilizes the power of Perlin, Fractal and Turbulence noise types to create visually appealing heightmaps for use in Teardown.

![main GUI](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/580dbb6f88cb9da44cd863dcd0c887427d95b4d96dab2a0baa57547519bf383e.webp)


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

In order for these to visualize properly on your ground, you must utilize the "file" input field and the "grass" input field appropriately.
Your generated heightmap goes into the "file" field, while your generated grassmap goes into the "grass" field.
You can either use a greyscaled heightmap for the "grass" field, or you can use your a generated noise grassmap.

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


![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/0e9fe22a53cc4f5059416fa5c67fbe967fe5ebbded59f545f28a511cda0b5a92.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/fc79ba0da9c5f0dad5f102e1216acef272848857982b13f79453c56164cfce16.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/db9ba265ca2c326442fdccfbfbe20b879c86973028ffed2c6f916708c77e67f0.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/2f5f696c954ea77e0c9d77be871a53e3afbade37c1d7188cff5127b622c39c7c.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/03d1827c9f4e7911647b5ccc52f052c3181f53d8b79c9559b3f8efbba5512df4.webp)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

