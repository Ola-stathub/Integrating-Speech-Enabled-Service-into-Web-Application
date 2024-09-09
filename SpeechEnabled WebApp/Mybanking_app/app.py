from flask import Flask, render_template, request, jsonify
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import os
import librosa
import concurrent.futures
import audioread
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Define paths
audio_dir = 'static/audio'

# Function to ensure the directory exists
def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Ensure the audio directory exists
ensure_directory_exists(audio_dir)

# Loading my fine-tuned Whisper model and processor
model_path = "/Users/mac/Desktop/ASR data/model"
processor_path = "/Users/mac/Desktop/ASR data/model/processor"
model = WhisperForConditionalGeneration.from_pretrained(model_path)
processor = WhisperProcessor.from_pretrained(processor_path)

# Use a ThreadPoolExecutor for asynchronous audio processing
executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file uploaded'}), 400
        
        audio_file = request.files['audio']
        file_path = os.path.join(audio_dir, 'audio.wav')
        audio_file.save(file_path)

        # Process the audio asynchronously
        future = executor.submit(process_audio_file, file_path)
        page = future.result()

        return jsonify({'page': f'/{page}'})
    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({'page': '/'})

###processing audio
def process_audio_file(file_path):
    try:
        print(f"Processing audio file at: {file_path}")

        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            print(f"File is missing or empty: {file_path}")
            return "index"

        # Load and preprocess audio with librosa, ensuring it is resampled to 16 kHz
        audio, sr = librosa.load(file_path, sr=16000)  # Force resampling to 16 kHz
        
        print(f"Audio length: {len(audio)}")
        print(f"Sampling rate: {sr}")

        # Preprocess the audio
        input_features = processor(audio, return_tensors="pt", sampling_rate=16000)
        
        # Generate the output
        outputs = model.generate(input_features['input_features'], language='en')  # Specify language for translation
        transcription = processor.decode(outputs[0], skip_special_tokens=True).lower()

        print(f"Transcription: {transcription}")

        # Determine the page based on the transcription
        if any(keyword in transcription for keyword in ["log out", "log", "logout"]):
            return "login"
        elif any(keyword in transcription for keyword in ["login", "log in", "sign in", "home page", "dashboard", "home"]):
            return "index"
        elif any(keyword in transcription for keyword in ["account home", "my account"]):
            return "index"
        elif any(keyword in transcription for keyword in ["send", "transfer"]):
            return "transfer"
        elif any(keyword in transcription for keyword in ["balance", "account balance", "account", "my balance"]):
            return "balance"
        elif any(keyword in transcription for keyword in ["loan", "borrow", "borrow loan", "boro", "lend", "need money"]):
            return "borrowloan"
        else:
            return "index"
    except Exception as e:
        print(f"Error in process_audio_file: {e}")
        return "index"




@app.route('/<page_name>')
def render_page(page_name):
    if page_name in ['index', 'balance', 'borrowloan', 'login', 'transfer']:
        return render_template(f'{page_name}.html')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)

@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file uploaded'}), 400
        
        audio_file = request.files['audio']
        file_path = os.path.join(audio_dir, 'audio.wav')
        audio_file.save(file_path)

        print(f"Audio file saved to: {file_path}")

        # Process the audio asynchronously
        future = executor.submit(process_audio_file, file_path)
        page = future.result()

        print(f"Determined page: {page}")

        return jsonify({'page': f'/{page}'})
    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({'page': '/'})
