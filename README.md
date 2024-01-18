# Color-Palette-Generator-RGB
Easy-to-use tool for generating color palettes, but manual checking is recommended for optimal results

As a designer in the animation industry, creating a well-defined color palette is crucial. 
This Python script helps streamline the process by automatically generating a color palette from your images.

## Features

- Suitable for solid color images.
- Adjustable parameters for customization:
  - `max_colors`: Maximum number of colors in the palette (default: 15).
  - `color_tolerance`: Tolerance for color difference, affecting the filtering of similar colors (default: 32).
  - `min_cluster_size`: Minimum cluster size, influencing the simplicity and contrast of the palette (default: 50).
  - `min_colors`: Minimum number of colors in the palette (default: 5).

## Usage

1. Ensure your images are suitable for solid color extraction.
2. Adjust parameters based on your preferences and image characteristics.
3. Run the script to generate a Photoshop JSX file.
4. Open the JSX file in Photoshop (`File` -> `Scripts` -> `Browse...`).
5. Obtain a 1080x1080px RGB color palette with solid rectangles and text(layers), named after the original image.

## Important Notes

- **max_colors**: Depends on your image color range and what you want to control. Not suitable for images with shadows and light variations.
- **min_cluster_size**: Influences the simplicity and contrast. A higher value is recommended for simple and high-contrast images.
- `estimate_color_complexity` predicts `min_cluster_size` to avoid manual adjustment.

## Examples


![微信截图_20240118102307](https://github.com/ENIACZH/Color-Palette-Generator/assets/129947787/d68a1266-63ca-4ea7-9ebf-9e85850e74c7)

*High-resolution and high-contrast image.*

![2](https://github.com/ENIACZH/Color-Palette-Generator/assets/129947787/feb97410-3c91-4cc8-a9c1-36a31e350f8b)

*Another example with clear color definition.*

![3](https://github.com/ENIACZH/Color-Palette-Generator/assets/129947787/c2802b23-d2d0-44b8-b3d1-7c9ed13a9526)

Note: Before running the scripts, it is recommended to convert all images to RGB mode in Adobe Bridge. 
This can help avoid potential issues, and the following line in the script is optional:

python
Copy code
img = Image.fromarray(img).convert("RGB")


Feel free to use and customize the script to enhance your animation design workflow!
