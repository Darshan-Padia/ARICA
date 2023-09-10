import face_recognition
import cv2
import os
import threading
import text_to_speech as mytts

# Directory path where the images are stored
image_dir = "images"

# Initialize a dictionary to store known faces and their corresponding names
known_people = {}

# Loop through all files in the image directory
for filename in os.listdir(image_dir):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        # Load and encode the known faces
        image_path = os.path.join(image_dir, filename)
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]

        # Extract the name from the file name (excluding the file extension)
        name = os.path.splitext(filename)[0]

        known_people[name] = face_encoding

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

# Function to play sound
def play_sound(name):
    text_to_speech = mytts.TextToSpeech(name)
    text_to_speech.convert_to_audio()

# Set the accuracy threshold (adjust this value as needed)
accuracy_threshold = 0.5
i=0
while True:
    # Capture a frame from the webcam
    ret, frame = video_capture.read()

    # Find all face locations and face encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each detected face
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Initialize the name as "Unknown" and accuracy as None
        name = "Unknown"
        accuracy = None

        # Compare the face with known faces and calculate accuracy
        for known_name, known_face_encoding in known_people.items():
            face_distances = face_recognition.face_distance([known_face_encoding], face_encoding)
            if face_distances[0] < accuracy_threshold:
                name = known_name
                accuracy = 1 - face_distances[0]  # Convert distance to accuracy score (closer to 1 is better)

        # Draw a rectangle around the face and display the name and accuracy
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        # text = f"{name} ({accuracy:.2f})" if accuracy is not None else name
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Play sound if a known face is detected
        if i==0 and name != "Unknown":
            threading.Thread(target=play_sound, args=(name,)).start()
            i+=1    
    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
video_capture.release()
cv2.destroyAllWindows()
