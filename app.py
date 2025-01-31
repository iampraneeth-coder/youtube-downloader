from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
import os

app = Flask(__name__)

# Temporary directory to store downloaded files
DOWNLOAD_FOLDER = './downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        download_type = request.form['download_type']

        try:
            yt = YouTube(url)
            title = yt.title

            if download_type == 'video':
                # Download the highest resolution video
                stream = yt.streams.get_highest_resolution()
                file_path = stream.download(output_path=DOWNLOAD_FOLDER)
            elif download_type == 'audio':
                # Download audio only
                stream = yt.streams.filter(only_audio=True).first()
                file_path = stream.download(output_path=DOWNLOAD_FOLDER)
                # Rename to .mp3
                base, ext = os.path.splitext(file_path)
                new_file = base + '.mp3'
                os.rename(file_path, new_file)
                file_path = new_file

            return send_file(file_path, as_attachment=True)

        except Exception as e:
            return f"An error occurred: {e}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
