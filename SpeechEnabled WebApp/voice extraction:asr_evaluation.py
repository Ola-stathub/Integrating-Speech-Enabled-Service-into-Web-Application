##This code uses the pre-trained whisper ASR model to extract voice, transcribs it and prints the word error rate PRR

import torch
import torchaudio
import sounddevice as sd
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from jiwer import wer  

# Paths to my fine tuned model and its processor
model_path = "/Users/mac/Desktop/ASR data/model"
processor_path = "/Users/mac/Desktop/ASR data/model/processor"

# Loading my fine tuned model and processor
model = WhisperForConditionalGeneration.from_pretrained(model_path)
processor = WhisperProcessor.from_pretrained(processor_path)

# Record audio
print("Recording...")
duration = 5  # seconds
sample_rate = 16000
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float32")
sd.wait()
print("Recording finished.")

# Resample audio to 16000 Hz and process it
audio_tensor = torch.tensor(audio, dtype=torch.float32).squeeze()
audio_tensor = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(audio_tensor)

# Prepare input features for the model
inputs = processor(audio_tensor, return_tensors="pt", sampling_rate=16000)
input_features = inputs["input_features"]

# Force the model to generate output in English
forced_decoder_ids = processor.get_decoder_prompt_ids(language="en", task="transcribe")

# Generate transcription with forced language decoding
output = model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
transcription = processor.batch_decode(output, skip_special_tokens=True)[0]

print("Transcription:", transcription)

# Ground truth transcription for comparison (often replaced to test difffernt words under different conditions)
ground_truth = "The Lord is good."

# Calculate Word Error Rate (WER)
error_rate = wer(ground_truth, transcription)
print(f"Word Error Rate (WER): {error_rate * 100:.2f}%")

# Calculate Phrase Recognition Rate (PRR)
def calculate_prr(ground_truth, transcription):
    gt_phrases = ground_truth.split()
    transcribed_phrases = transcription.split()
    correct_phrases = sum(1 for gt, trans in zip(gt_phrases, transcribed_phrases) if gt == trans)
    prr = (correct_phrases / len(gt_phrases)) * 100
    return prr

prr = calculate_prr(ground_truth, transcription)
print(f"Phrase Recognition Rate (PRR): {prr:.2f}%")
