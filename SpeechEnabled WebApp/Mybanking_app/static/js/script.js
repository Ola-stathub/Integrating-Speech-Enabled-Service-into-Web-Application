document.addEventListener('DOMContentLoaded', function() {
    const micButton = document.querySelector('.record-button'); // Make sure the class name matches
    let mediaRecorder;
    let audioChunks = [];

    micButton.addEventListener('click', function() {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
        } else {
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    mediaRecorder = new MediaRecorder(stream);
                    mediaRecorder.start();

                    mediaRecorder.addEventListener('dataavailable', event => {
                        audioChunks.push(event.data);
                    });

                    mediaRecorder.addEventListener('stop', () => {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        const formData = new FormData();
                        formData.append('audio', audioBlob, 'audio.wav');

                        fetch('/recognize', {
                            method: 'POST',
                            body: formData
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.page) {
                                window.location.href = data.page;
                            } else {
                                alert("No valid command recognized.");
                            }
                        })
                        .catch(error => {
                            console.error('Error processing audio:', error);
                            alert("Failed to process the audio.");
                        });

                        audioChunks = [];
                    });
                })
                .catch(error => {
                    console.error('Error accessing microphone:', error);
                    alert("Microphone access denied or not available.");
                });
        }
    });
});
