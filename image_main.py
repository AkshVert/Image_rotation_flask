from flask import Flask, request, render_template, send_file
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return render_template('index.html', message='No file selected')
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', message='No file selected')

    # Open the uploaded image and convert to RGB format
    img = Image.open(file).convert('RGB')

    # Get user input for rotation angle
    angle = request.form['angle']

    # Rotate the image based on user input
    if angle == 'left':
        img = img.transpose(method=Image.ROTATE_90).transpose(method=Image.FLIP_LEFT_RIGHT)
    elif angle == 'right':
        img = img.transpose(method=Image.ROTATE_270).transpose(method=Image.FLIP_LEFT_RIGHT)
    elif angle == 'horizontal':
        img = img.transpose(method=Image.FLIP_LEFT_RIGHT)
    elif angle == 'vertical':
        img = img.transpose(method=Image.FLIP_TOP_BOTTOM)
    elif angle == '45':
        img = img.rotate(45, expand=True)

    # Save the rotated image to a temporary file
    temp_file = 'temp.jpg'
    img.save(temp_file)

    # Return the rotated image as a response
    return send_file(temp_file, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)

