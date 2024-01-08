import json
import os
import sys
import random

assert len(sys.argv) == 2, sys.argv

# Read the JSON data from file
data = []
with open(sys.argv[1], 'r') as json_file:
    for line in json_file:
        data.append(json.loads(line))
random.shuffle(data)

# Start the HTML file
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Q&A Visualizer</title>
<style>
body {
    font-family: Arial, sans-serif;
}
.container {
    margin: 20px;
}
.entry {
    border: 1px solid #ddd;
    padding: 15px;
    margin-bottom: 10px;
}
.question,
.solution {
    margin-bottom: 10px;
}
img {
    max-width: 100%;
    height: auto;
}
</style>
</head>
<body>
<h1>Q&A Visualizer</h1>
<div class="container">
"""

# Add each entry to the HTML content
for entry in data:
    question, solution, images, html_file = entry['question'], entry['solution'], entry['images'], entry['html_file']
    html_content += """
    <div class="entry">
        <div class="question">
            <h2>Question:</h2>
            <p>{}</p>
        </div>
        <div class="">
            <h2>HTML:</h2>
            <p>{}</p>
        </div>
        <div class="solution">
            <h3>Solution:</h3>
            <p>{}</p>
        </div>
    """.format(question, html_file, solution)

    # Add the image if it exists and is a file on the system
    if images:
        html_content += '<div class="images">\n'
        for image in images:
            # Add the image if it exists and is a file on the system
            if image and os.path.isfile(image):
                html_content += f'<img src="{image}" alt="Image">\n'
        html_content += '</div>\n'  # Close the images div
    html_content += '</div>\n'  # Close the entry div

    html_content += "</div>\n"  # Close the entry div

html_content += """
</div>
</body>
</html>
"""

# Write the HTML content to an HTML file
with open('outputs.html', 'w') as html_file:
    html_file.write(html_content)

print("HTML file created successfully!")