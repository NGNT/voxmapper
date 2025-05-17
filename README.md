# Voxmapper

Voxmapper is a powerful tool for modding Teardown. It generates heightmaps, textures, and grass maps using a variety of advanced noise algorithms and terrain generation techniques.
Built with a modern, intuitive GUI, it lets you craft custom terrain features for your Teardown maps with precise control and real-time preview capabilities.

![Mountain GUI](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/a681515b88684d0894d4a3ac673a7b314f63e43fa276752ba9cc3a6d43fd8a66.webp)
![Grass Map GUI](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/2bc3839024297cd132aaa499c34e14b7e715a55a8ec8fda7ce07a3139c58c9af.webp)
![Image GUI](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/4330f075240b10828159bdb24ac7a7e1d29da6f54822fddbf9274c065adac5ca.webp)
![output](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/6c74d2920207b6e6fe8c132e5a4ea677df227bd965815ac3d5886f458718c7a5.webp)
![output](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/1235a154e0c3ef80d52821b39ea3d86e3b677cdf291fee2f040457058989905a.webp)


## Features

### Heightmap Generation
- **Multiple Noise Types**: Generate terrain using Perlin noise, fractal noise, turbulence noise, and specialized landmass algorithms
- **Realistic Canyon System**: Create complex canyon networks with branching river systems
- **Landmass Generation**: Design islands and continents with realistic shorelines and elevation profiles
- **Interactive Preview**: Pan and zoom to focus on specific areas with real-time feedback
- **Advanced Terrain Controls**: Fine-tune terrain features with octaves, persistence, lacunarity, and more

### Grass Map Creation
- **Procedural Grass Generation**: Create realistic grass distribution patterns with variable density
- **Noise-Based Options**: Choose between uniform grass or noise-based distribution
- **Multiple Noise Systems**: Combine Perlin noise and simple noise with adjustable weights
- **Density & Lightness Controls**: Fine-tune grass appearance with intuitive sliders

### Image Processing
- **Image Import**: Import and process external images for heightmap and texture creation
- **Grayscale Conversion**: Convert color images to game-compatible grayscale heightmaps
- **Channel Manipulation**: Edit red and green channels separately for precise terrain control
- **Effects System**: Apply vignette, blur, and exposure adjustments

### User Interface
- **Modern Styling**: Clean, modern interface with tooltips and organized controls
- **Real-Time Preview**: See changes immediately in the preview panel
- **Multi-Core Processing**: Utilizes parallel processing for faster generation of large heightmaps
- **Export Options**: Save heightmaps in various formats compatible with Teardown


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

2. Choose the appropriate tab for your needs:
- **Mountain Generation**: Create heightmaps with various noise algorithms
- **Grass Map**: Generate grass distribution maps for your terrain
- **Image Import**: Process external images for use as heightmaps

3. Adjust parameters using the sliders in the left panel:
- For heightmaps: modify noise type, scale, octaves, and other terrain features
- For grass maps: set density, noise amounts, and appearance settings
- For image processing: adjust channel values, apply effects

4. Use the interactive preview panel to examine your creation:
- Pan by clicking and dragging
- Zoom using the buttons or mouse wheel
- The position indicator shows your current focus point

5. Generate and export your creation using the buttons at the bottom of the controls panel.


## Advanced Features

### Canyon System
The canyon generation system creates realistic river networks with:
- Adjustable canyon intensity, length, and branch density
- Procedural branching patterns that flow naturally across the terrain
- Independent seed control for consistent canyon patterns

### Landmass Generation
Create realistic island and continent shapes with:
- Control over land-to-water ratio
- Adjustable shore height for beach areas
- Plain factor controls for flat vs. mountainous terrain
- Customizable noise scale and octaves for terrain detail

### Grass Map Controls
Fine-tune your grass maps with:
- Toggle between uniform and noise-based grass distribution
- Adjustable grass density threshold
- Combined noise systems with individual weight controls
- Lightness adjustment for non-grass areas


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
| alienjungle | Alien jungle environment            |
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
| ashlands     | Volcanic ash-covered             |
| mangrove     | Coastal wetland                     |
| cherry       | Cherry blossom landscape            |
| highlands    | Rugged upland terrain               |
| mesa         | Layered red clay formations         |
| wasteland    | Barren environment                  |
| taiga        | Northern coniferous forest       |
| corruption   | Purple magical corruption           |
| candyland    | Sweet-themed landscape              |
| ethereal     | Heavenly blue realm                 |
| cyberpunk    | Urban futuristic landscape       |
| crimson      | Blood-red fantasy theme             |
| vaporwave    | Retro-futuristic aesthetic       |
| neon         | Electric green and yellow           |
| toxic        | Radioactive green environment       |
| glitch    | Digital glitch-themed               |
| underdark    | Fantasy underworld                  |


![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/0e9fe22a53cc4f5059416fa5c67fbe967fe5ebbded59f545f28a511cda0b5a92.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/fc79ba0da9c5f0dad5f102e1216acef272848857982b13f79453c56164cfce16.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/db9ba265ca2c326442fdccfbfbe20b879c86973028ffed2c6f916708c77e67f0.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/2f5f696c954ea77e0c9d77be871a53e3afbade37c1d7188cff5127b622c39c7c.webp)
![example](https://cdn.nostrcheck.me/46025249f65d47dddb0f17d93eb8b0a32d97fe3189c6684bbd33136a0a7e0424/03d1827c9f4e7911647b5ccc52f052c3181f53d8b79c9559b3f8efbba5512df4.webp)


## Performance Notes

- The application uses multiprocessing to speed up generation of large heightmaps.
- For very large maps (>2048px), ensure your system has sufficient RAM.
- Preview generation is optimized to maintain UI responsiveness.

## Version History

Current version: v1.4.1

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

