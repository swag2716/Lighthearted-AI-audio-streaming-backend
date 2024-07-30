from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from audio_processor import process_audio
from pdf_generator import create_pdf
from aws_service import upload_to_s3

app = Flask(__name__)

@app.route('/process_audio', methods=['POST'])
def process_audio_route():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if audio_file:
        filepath = os.path.join('media')
        if not os.path.isdir(filepath):
            os.mkdir(filepath)
        app.config['file_path'] = filepath


        filename = secure_filename(audio_file.filename)
        file_path = os.path.join(app.config['file_path'], filename)
        audio_file.save(file_path)

        # Process audio and get duration and wave data
        duration, wave_data = process_audio(file_path)

        # Create PDF
        pdf_path = create_pdf(filename, duration, wave_data)

        # Upload audio to S3
        s3_audio_url = upload_to_s3(file_path, 'audio/' + filename)

        # Upload PDF to S3
        s3_pdf_url = upload_to_s3(pdf_path, 'pdf/' + os.path.basename(pdf_path))

        # Clean up temporary files
        os.remove(file_path)
        os.remove(pdf_path)

        return jsonify({
            'pdf_url': s3_pdf_url,
            'audio_url': s3_audio_url
        })

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)