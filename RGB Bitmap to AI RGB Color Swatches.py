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

def generate_illustrator_script(colors, output_folder, filename, text_size):
    script_content = '// Adobe Illustrator Script\n'
    script_content += 'function main() {\n'
    script_content += '    var doc = app.documents.add(DocumentColorSpace.RGB, 1080, 1080);\n\n'
    
    script_content += '    var startX = 50;\n'
    script_content += '    var startY = 1030; // Illustrator\'s coordinate system starts from the bottom\n'
    script_content += '    var rectSize = 30;\n'
    script_content += '    var ySpacing = 10;\n'
    script_content += '    var textOffsetX = 10;\n'
    script_content += f'    var textSize = {text_size};\n\n'
    
    script_content += '    var colors = [\n'
    for color in colors:
        script_content += f'        [{color[0]}, {color[1]}, {color[2]}],\n'
    script_content += '    ];\n\n'
    
    script_content += '    for (var i = 0; i < colors.length; i++) {\n'
    script_content += '        var currentY = startY - i * (rectSize + ySpacing);\n'
    script_content += '        var rect = doc.pathItems.rectangle(currentY, startX, rectSize, rectSize);\n'
    script_content += '        rect.filled = true;\n'
    
    script_content += '        rect.fillColor = new RGBColor();\n'
    script_content += '        rect.fillColor.red = colors[i][0];\n'
    script_content += '        rect.fillColor.green = colors[i][1];\n'
    script_content += '        rect.fillColor.blue = colors[i][2];\n\n'
    
    script_content += '        var text = doc.textFrames.add();\n'
    script_content += '        text.contents = "R: " + colors[i][0] + " G: " + colors[i][1] + " B: " + colors[i][2];\n'
    
    script_content += '        text.textRange.size = textSize;\n'
    script_content += '        text.left = startX + rectSize + textOffsetX;\n'
    script_content += '        text.top = currentY - rectSize/2 + textSize/2;\n'
    script_content += '    }\n\n'
    
    script_content += f'    var saveName = new File("{output_folder}/{filename}_RGB.ai");\n'
    script_content += '    var saveOptions = new IllustratorSaveOptions();\n'
    script_content += '    doc.saveAs(saveName, saveOptions);\n'
    script_content += '    doc.close();\n'
    script_content += '}\n'
    script_content += 'main();\n'

    # Save the script content to a .jsx file
    script_path = os.path.join(output_folder, f"{filename}_RGBScript.jsx")
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    print(f"Illustrator RGB script saved to: {script_path}")

# Example usage
input_folder = r"C:/Users/eniac/Desktop/colorSwatch/jpg"
output_folder = r"C:/Users/eniac/Desktop/colorSwatch/jpg"
os.makedirs(output_folder, exist_ok=True)
image_width = 1080
image_height = 1080
model = MobileNetV2(weights='imagenet')

for filename in os.listdir(input_folder):
    if filename.lower().endswith((".jpg", ".png", ".jpeg")):
        image_path = os.path.join(input_folder, filename)
        colors = recognize_color(image_path)
        generate_illustrator_script(colors, output_folder, os.path.splitext(filename)[0], text_size=30)
