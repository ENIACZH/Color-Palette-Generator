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
![guide](https://github.com/ENIACZH/Color-Palette-Generator/assets/129947787/1adf2fa8-9bad-4476-9389-0d81f5797ddc)


![微信截图_20240118102307](https://github.com/ENIACZH/Color-Palette-Generator/assets/129947787/d68a1266-63ca-4ea7-9ebf-9e85850e74c7)

*High-resolution and high-contrast image.*

![2](https://github.com/ENIACZH/Color-Palette-Generator/assets/129947787/feb97410-3c91-4cc8-a9c1-36a31e350f8b)

*Another example with clear color definition.*

![3](https://github.com/ENIACZH/Color-Palette-Generator/assets/129947787/c2802b23-d2d0-44b8-b3d1-7c9ed13a9526)

Note: Before running the scripts, it is recommended to convert all images to RGB mode in Adobe Bridge. 
This can help avoid potential issues, and the following line in the script is optional:

img = Image.fromarray(img).convert("RGB")


Feel free to use and customize the script to enhance your animation design workflow!

只需修改文件夹路径，kmeans会自动识别主要颜色，保存Java脚本生成色指定，但仍需手动检查，一般在最后几个排位可能有偏差

## 特点

- 适用于简单纯色图像。
- 可调参数以进行定制：
  - `max_colors`：调色板中的最大颜色数（默认：15）。
  - `color_tolerance`：颜色容差，影响相似颜色的过滤，对于对比度不是很高的图像需要减少（默认：32）。
  - `min_cluster_size`：最小聚类大小，影响调色板的简单性和对比度（默认：50），纯色块高对比度可以拉到200，复杂颜色可以降多一点。
  - `min_colors`：调色板中的最小颜色数（默认：5）。

## 用法

1. 确保您的图像适合提取纯色。
2. 根据您的偏好和图像特性调整参数。
3. 替换文件夹路径，运行脚本以生成带有RGB色值的Photoshop JSX 文件。
4. 在 Photoshop 中打开 JSX 文件（`文件` -> `脚本` -> `浏览...`）。
5. 获取一个以原始图像命名的 1080x1080px画布的psd，其中包含分层的rgb色指文本层和方形色块层。

## 重要注意事项

- **max_colors**：取决于图像的颜色范围和您想要控制的内容。不适用于具有阴影和光变化的图像。
- **min_cluster_size**：影响简单性和对比度。建议对简单且高对比度的图像使用更高的值。
- `estimate_color_complexity` 预测 `min_cluster_size` 以避免手动调整。


注意：在运行脚本之前，建议在 Adobe Bridge 中将所有图像转换为 RGB 模式。
这有助于避免潜在问题，脚本中的以下行是可选的：

img = Image.fromarray(img).convert("RGB")

随意使用和定制脚本，以增强您的动画设计工作流程！

