from flask import Flask, render_template, request, redirect, url_for, send_file
from gtts import gTTS
import os

app = Flask(__name__)

# Setting a folder for the uploaded files.
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Defining a route for the home page.
@app.route('/')
def index():
    return render_template('index.html')


# Defining a route to handle the text-to-speech conversion.
@app.route('/convert', methods=['POST'])
def convert_text_to_speech():
    if request.method == 'POST':
        # Checks if a file was uploaded.
        if 'textfile' not in request.files:
            return redirect(request.url)

        file = request.files['textfile']

        # Checks if the file has a valid name and extension.
        if file.filename == '':
            return redirect(request.url)

        # Saves the uploaded text file to the upload folder.
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Reads the contents of the uploaded text file.
            with open(filename, 'r') as file:
                text = file.read()

            if text:
                # Creates a gTTS object and generates speech.
                tts = gTTS(text)
                audio_file = 'output.mp3'
                tts.save(audio_file)
                return send_file(audio_file, as_attachment=True)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
