Drowsiness Detection System with Spotify Integration

Overview

This project is a drowsiness detection system that uses computer vision to monitor the user's eye aspect ratio (EAR) to detect drowsiness. When drowsiness is detected, the system plays a specific song on Spotify. The project leverages OpenCV for real-time video processing, dlib for facial landmark detection, and the Spotify API for music playback.

 Features

- Real-time Drowsiness Detection: Uses a webcam to monitor the user's eyes and calculate the EAR.
- Spotify Integration: Plays a pre-selected song on Spotify when drowsiness is detected.
-Graphical User Interface (GUI): Simple interface to start and stop the detection process.

 Requirements

- Python 3.6 or higher
- OpenCV
- dlib
- imutils
- scipy
- spotipy
- tkinter

 Setup Instructions

 1. Download and Install Python
Ensure that you have Python 3.6 or higher installed on your system. You can download it from [python.org](https://www.python.org/).

 2. Install Dependencies
Open IDLE and run the following commands in the interactive shell (one by one) to install the required libraries:

```python
import os
os.system('pip install opencv-python dlib imutils scipy spotipy tkinter')
```

 3. Download the Pre-trained Model
Download the `shape_predictor_68_face_landmarks.dat` file from the following Google Drive link and place it in your project directory:

(https://drive.google.com/drive/folders/1eKg_uCW4tM928uyECYqWDF6JggW33aHf?usp=sharing)

 4. Set Up Spotify API Credentials
- Create a Spotify developer account and set up a new application to obtain your `client_id` and `client_secret`.
- Set the `redirect_uri` to `http://localhost:8888/callback`.
- Update the Spotify credentials in the script with your `client_id`, `client_secret`, and `redirect_uri`.

 5. Update the Code with Your Credentials
Replace the placeholders in the `SpotifyOAuth` initialization with your Spotify API credentials.

 How to Run the Project in IDLE

1. Open IDLE:
    - Launch IDLE from your Python installation.

2. Open the Script:
    - In IDLE, go to `File -> Open` and select your Python script file (e.g., `drowsiness_detection.py`).

3. Run the Script:
    - Press `F5` or go to `Run -> Run Module` to execute the script.

4. Start Detection:
    - In the GUI that appears, click on the "Start Detection" button to begin monitoring for drowsiness.

5. Stop Detection:
    - Click on the "Stop Detection" button to end the monitoring process.

6. Quit Application:
    - Click on the "Quit" button to close the application.

 How It Works

 Drowsiness Detection

- The system captures video from the webcam and processes each frame to detect the user's eyes using dlib's facial landmark predictor.
- It calculates the Eye Aspect Ratio (EAR) to determine the openness of the eyes. If the EAR falls below a predefined threshold for a consecutive number of frames, the user is considered drowsy.

 Spotify Integration

- When drowsiness is detected, the system uses the Spotify API to search for a specific song.
- The song is then played on the user's Spotify device.

 GUI

- The graphical user interface, built with tkinter, provides simple controls to start and stop the detection process.

 Acknowledgments

- dlib: For providing the facial landmark detection model.
- OpenCV: For real-time computer vision capabilities.
- Spotify API: For enabling music playback functionality.

