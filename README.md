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


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

