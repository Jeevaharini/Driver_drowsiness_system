import cv2
import dlib
import imutils
from imutils import face_utils
from scipy.spatial import distance
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import tkinter as tk
from tkinter import ttk
import threading

# Initialize Spotify client with necessary scopes
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='ff002ee7920145139e43e51b960af33d',
                                               client_secret='dc05d970557346a5a01c19d6c97c417b',
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='user-modify-playback-state user-read-playback-state'))

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

thresh = 0.25
frame_check = 10
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
cap = None
flag = 0
total_frames = 0
drowsy_frames = 0
detection_running = False

# Search for a song on Spotify
def search_spotify(song_name):
    results = sp.search(q=song_name, type='track')
    if results['tracks']['items']:
        return results['tracks']['items'][0]['uri']
    else:
        return None

# Get the device ID associated with your device
def get_device_id():
    devices = sp.devices()
    if devices['devices']:
        return devices['devices'][0]['id']  # Assuming we use the first available device
    else:
        return None

# Play a song on the specified device
def play_song(song_uri, device_id):
    if device_id:
        try:
            sp.start_playback(device_id=device_id, uris=[song_uri])
        except spotipy.SpotifyException as e:
            print("An error occurred:", e)
    else:
        print("No device found.")

# Start detection function
def start_detection():
    global flag, total_frames, drowsy_frames, detection_running, cap

    if detection_running:
        return

    detection_running = True
    flag = 0
    total_frames = 0
    drowsy_frames = 0
    cap = cv2.VideoCapture(0)  # Reinitialize the video capture

    while detection_running:
        ret, frame = cap.read()
        if ret:
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            subjects = detect(gray, 0)
            for subject in subjects:
                shape = predict(gray, subject)
                shape = face_utils.shape_to_np(shape)
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0

                # Draw contours around the eyes
                cv2.drawContours(frame, [leftEye], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEye], -1, (0, 255, 0), 1)

                if ear < thresh:
                    flag += 1
                    drowsy_frames += 1
                    print(flag)
                    if flag >= frame_check:
                        cv2.putText(frame, "*****ALERT!*****", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.putText(frame, "*****ALERT!*****", (10, 325),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        # Search for a specific song
                        song_uri = search_spotify("Thoongathe Thambi Thoongathe(Original Motion Picture Soundtrack)")
                        if song_uri:
                            # Get the device ID
                            device_id = get_device_id()
                            # Add a delay before sending the playback command
                            time.sleep(2)  # Adjust the delay as needed
                            # Play the song on the specified device
                            play_song(song_uri, device_id)
                        else:
                            print("Song not found on Spotify.")
                else:
                    flag = 0
                total_frames += 1

            # Calculate accuracy
            accuracy = (1 - (drowsy_frames / total_frames)) * 100 if total_frames != 0 else 100

            # Display accuracy
            cv2.putText(frame, f"Accuracy: {accuracy:.2f}%", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                detection_running = False
                break

    cap.release()
    cv2.destroyAllWindows()

# Stop detection function
def stop_detection():
    global detection_running
    detection_running = False

# GUI setup
root = tk.Tk()
root.title("Drowsiness Detection System")
root.geometry("400x150")

# Create a label widget for displaying instructions
instructions_label = ttk.Label(root, text="Press 'Start Detection' to begin monitoring for drowsiness.")
instructions_label.pack(pady=10)

def start_thread():
    thread = threading.Thread(target=start_detection)
    thread.start()

start_button = tk.Button(root, text="Start Detection", command=start_thread)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Detection", command=stop_detection)
stop_button.pack(pady=5)

quit_button = tk.Button(root, text="Quit", command=lambda: (stop_detection(), root.quit()))
quit_button.pack(pady=5)

root.mainloop()
