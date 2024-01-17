# Color-Palette-Generator
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
5. Obtain a 1080x1080px RGB color palette with solid rectangles and text, named after the original image.

## Important Notes

- **max_colors**: Depends on your image color range and what you want to control. Not suitable for images with shadows and light variations.
- **min_cluster_size**: Influences the simplicity and contrast. A higher value is recommended for simple and high-contrast images.
- `estimate_color_complexity` predicts `min_cluster_size` to avoid manual adjustment.

## Examples

![Example 1](example1.jpg)
*High-resolution and high-contrast image.*

![Example 2](example2.jpg)
*Another example with clear color definition.*

![Example 3](example3.jpg)
*Example with high color complexity.*

Feel free to use and customize the script to enhance your animation design workflow!
