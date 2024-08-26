import os
import numpy as np
from keras.applications.mobilenet_v2 import MobileNetV2
from PIL import Image
from sklearn.cluster import MiniBatchKMeans
from skimage import color, segmentation, exposure
from skimage.io import imread

def estimate_color_complexity(image_path):
    img = imread(image_path)
    lab_img = color.rgb2lab(img)
    gradient_magnitude = exposure.rescale_intensity(np.linalg.norm(np.gradient(lab_img)[0:2], axis=0))
    segments = segmentation.felzenszwalb(gradient_magnitude, scale=100, sigma=0.5, min_size=50)
    color_complexity = len(np.unique(segments))
    return color_complexity

def determine_optimal_clusters(img):
    # Implement your logic for determining optimal clusters based on image properties
    # You can use MiniBatchKMeans or any other method suitable for your needs
    kmeans = MiniBatchKMeans(n_clusters=15)
    return kmeans

def recognize_color(image_path, max_colors=15, color_tolerance=32, min_cluster_size=50, min_colors=5):
    color_complexity = estimate_color_complexity(image_path)
    adjusted_max_colors = min(max_colors, max(min_colors, color_complexity))

    img = Image.open(image_path)
    small_img = img.resize((100, 100))
    img_array = np.array(small_img)

    if img_array.shape[-1] != 3:
        img_array = img_array[:, :, :3]

    pixels = img_array.reshape((-1, 3))

    kmeans = determine_optimal_clusters(img)
    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)
    cluster_sizes = np.bincount(kmeans.labels_)

    color_sizes = list(zip(colors, cluster_sizes))
    filtered_color_sizes = [(color, size) for color, size in color_sizes if size > min_cluster_size]

    sorted_color_sizes = sorted(filtered_color_sizes, key=lambda x: x[1], reverse=True)

    for i in range(len(sorted_color_sizes)):
        if sorted_color_sizes[i][1] <= color_tolerance:
            sorted_color_sizes[i] = ((255, 255, 255), sorted_color_sizes[i][1])

    sorted_colors = [color for color, _ in sorted_color_sizes]

    filtered_colors = []
    for color in sorted_colors:
        if all(np.linalg.norm(color - existing_color) > color_tolerance for existing_color in filtered_colors):
            filtered_colors.append(color)

    while len(filtered_colors) < min_colors:
        filtered_colors.append((255, 255, 255))

    return np.array(filtered_colors)

def generate_photoshop_script(colors, output_folder, filename, text_size):
    script_content = '// Create new document\n'
    script_content += 'var newDocument = app.documents.add(1080, 1080, 72, "Color Rectangles", NewDocumentMode.RGB, DocumentFill.WHITE);\n\n'
    
    script_content += '// Set initial coordinates\n'
    script_content += 'var startX = 50;\n'
    script_content += 'var startY = 50;\n\n'

    script_content += '// Set initial Y-axis spacing\n'
    script_content += 'var ySpacing = 10;\n\n'

    script_content += '// Set text font and size\n'
    script_content += 'var textFont = "Arial";\n'
    script_content += f'var textSize = {text_size};  // Text font size\n\n'

    script_content += '// Initial color array\n'
    script_content += 'var colors = [\n'
    for color in colors:
        script_content += f'    {{ red: {color[0]}, green: {color[1]}, blue: {color[2]} }},\n'
    script_content += '    // Add more colors... these colors are from your color recognition\n];\n\n'

    script_content += '// Create color rectangles and text\n'
    script_content += 'for (var i = 0; i < colors.length; i++) {\n'
    script_content += '    var currentColor = colors[i];\n\n'

    script_content += '    // Create color rectangle\n'
    script_content += '    var colorRectangle = newDocument.artLayers.add();\n'
    script_content += '    createColorRectangle(colorRectangle, currentColor, startX, startY + i * (30 + ySpacing));\n\n'

    script_content += '    // Create color explanation text\n'
    script_content += '    var textContent = "R: " + currentColor.red + " G: " + currentColor.green + " B: " + currentColor.blue;\n'
    script_content += '    createColorText(newDocument, textContent, startX + 30 + 10, startY + i * (30 + ySpacing) + (30 - textSize) / 2, textFont, textSize);\n}\n\n'


    script_content += '// Set document save path\n'
    script_content += f'var savePath = "{output_folder}";\n'
    script_content += f'var saveFile = new File(savePath + "/{filename}.psd");\n\n'

    script_content += '// Save document\n'
    script_content += 'newDocument.saveAs(saveFile);\n'
    script_content += 'newDocument.close(SaveOptions.DONOTSAVECHANGES);\n\n'

    script_content += '// Function to create color rectangle\n'
    script_content += 'function createColorRectangle(layer, color, x, y) {\n'
    script_content += '    app.activeDocument.selection.select([[x, y], [x + 30, y], [x + 30, y + 30], [x, y + 30]]);\n'
    script_content += '    layer.bounds = app.activeDocument.selection.bounds;\n\n'
    script_content += '    // Fill rectangle color\n'
    script_content += '    var fillColor = new SolidColor();\n'
    script_content += '    fillColor.rgb.red = color.red;\n'
    script_content += '    fillColor.rgb.green = color.green;\n'
    script_content += '    fillColor.rgb.blue = color.blue;\n\n'
    script_content += '    app.activeDocument.selection.fill(fillColor);\n}\n\n'

    script_content += '// Function to create color text\n'
    script_content += 'function createColorText(document, text, x, y, font, size) {\n'
    script_content += '    var textLayer = document.artLayers.add();\n'
    script_content += '    textLayer.kind = LayerKind.TEXT;\n'
    script_content += '    textLayer.textItem.contents = text;\n'
    script_content += '    textLayer.textItem.position = [x, y + 26];  // Adjust the Y position\n'
    script_content += f'    textLayer.textItem.size = {text_size};\n'
    script_content += f'}}\n\n'

    # Save the script content to a .jsx file
    script_path = os.path.join(output_folder, f"{filename}Script.jsx")
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    print(f"Photoshop script saved to: {script_path}")

# Example usage
input_folder = r"your path"
output_folder = r"your path"
image_width = 1080
image_height = 1080
model = MobileNetV2(weights='imagenet')

for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".png")):
        image_path = os.path.join(input_folder, filename)
        colors = recognize_color(image_path)
        generate_photoshop_script(colors, output_folder, os.path.splitext(filename)[0], text_size=30)
