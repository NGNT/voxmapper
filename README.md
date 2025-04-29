# Voxmapper

Voxmapper is a simple but powerful tool for modding Teardown. It generates textures and grass maps using a variety of noise algorithms.  
Built with a clean GUI, it lets you craft custom heightmaps and textures for your Teardown maps easily and flawlessly.  

![main GUI](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/580dbb6f88cb9da44cd863dcd0c887427d95b4d96dab2a0baa57547519bf383e.webp)
![output](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/6c74d2920207b6e6fe8c132e5a4ea677df227bd965815ac3d5886f458718c7a5.webp)
![output](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/1235a154e0c3ef80d52821b39ea3d86e3b677cdf291fee2f040457058989905a.webp)


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

1. Run the application

2. Use the sliders in the GUI to adjust parameters for noise generation and grass map creation.

3. Click on the "Generate Noise", "Generate Greyscale Heightmap" or "Generate Grass Map" buttons to create your textures.

4. Use the "Export" buttons to save your generated images.


## Biome Tags

To get the most out of your maps, use these fields correctly:  

    '**file**' field → for your heightmap.  

    '**grass**' field → for your grassmap (either a greyscale heightmap or a noise-generated grassmap).  

In your biome_ground.lua, assign a tag to the '**biome**' input:  

| Tag          | Description                         |
|--------------|-------------------------------------|
| default      | Default terrain                     |
| desert       | Sandy desert                        |
| snowy        | Snow-covered ground                 |
| swamp        | Wet, swampy area                    |
| forest       | Temperate forest                    |
| volcano      | Volcanic rocks                      |
| tundra       | Arctic tundra                       |
| alienjungle  | Alien jungle environment            |
| crystalfields| Crystal formations                  |
| beach        | Sandy beach                         |
| savanna      | Golden grasslands                   |
| canyon       | Red desert canyon                   |
| mushroom     | Fungal landscape                    |
| cave         | Dark cave system                    |
| alpine       | Mountain environment                |
| bambooforest | Green bamboo forest                 |
| meadow       | Lush grass with wildflowers         |
| icelands     | Glacial environment                 |
| jungle       | Dense tropical rainforest           |
| ashlands     | Volcanic ash-covered                |
| mangrove     | Coastal wetland                     |
| cherry       | Cherry blossom landscape            |
| highlands    | Rugged upland terrain               |
| mesa         | Layered red clay formations         |
| wasteland    | Barren environment                  |
| taiga        | Northern coniferous forest          |
| corruption   | Purple magical corruption           |
| candyland    | Sweet-themed landscape              |
| ethereal     | Heavenly blue realm                 |
| cyberpunk    | Urban futuristic landscape          |
| crimson      | Blood-red fantasy theme             |
| vaporwave    | Retro-futuristic aesthetic          |
| neon         | Electric green and yellow           |
| toxic        | Radioactive green environment       |
| glitch       | Digital glitch-themed               |
| underdark    | Fantasy underworld                  |


![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/0e9fe22a53cc4f5059416fa5c67fbe967fe5ebbded59f545f28a511cda0b5a92.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/fc79ba0da9c5f0dad5f102e1216acef272848857982b13f79453c56164cfce16.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/db9ba265ca2c326442fdccfbfbe20b879c86973028ffed2c6f916708c77e67f0.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/2f5f696c954ea77e0c9d77be871a53e3afbade37c1d7188cff5127b622c39c7c.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/03d1827c9f4e7911647b5ccc52f052c3181f53d8b79c9559b3f8efbba5512df4.webp)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

