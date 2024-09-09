# Integrating Speech-Enabled Service into Web Application

This project involves embedding a speech recognition service into a web application for efficient navigation.

## Project Overview
The goal of this project is to leverage the power of **Automatic Speech Recognition (ASR)** to simplify the user experience within a banking web application.

To achieve this, the **Whisper-small ASR model by OpenAI** was utilized. The model was fine-tuned specifically for this project, ensuring optimal performance for recognizing bank service requests.

## Fine-Tuning Process
The fine-tuning process involved creating a specialized dataset tailored to the requirements of banking services. This dataset was used in conjunction with voice transcription data to train the model.

## Voice Extraction System
A voice extraction system was developed, allowing users to record their voices and receive accurate transcriptions. This system was essential for evaluating the efficiency of the fine-tuned model before its integration into the web application.

## Web Application Development
The web application was built using **HTML/CSS and JavaScript** and includes the following pages:
- **Login Page**
- **Home Page**
- **Borrow Loan Page**
- **Transfer Page**
- **Check Balance Page**

At the backend, **Flask** was used to integrate the pre-trained Whisper ASR model with the banking web application, enabling speech recognition functionality.

## Repository Contents
- **Python Notebook**: For fine-tuning the Whisper-small ASR model.
- **Python Script**: For the voice extraction system.
- **HTML/CSS/JavaScript Files**: For the frontend of the web application.
- **Flask Script**: For the integration of the model with the frontend.

## Contact Me
- **Oladele Bidemi A**
- ajayioladeleb@gmail.com

