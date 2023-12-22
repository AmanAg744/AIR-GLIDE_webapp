# Air-Glide

Air-Glide is a revolutionary web application that transforms the user's interaction with their PC by using hand gestures to control everyday desktop operations. The application leverages computer vision and machine learning techniques to enable gesture-based control, eliminating the need for traditional hardware devices.

## Features

- **Gesture-based Control:** Control your desktop operations using hand gestures captured by your webcam.
- **Virtual Mouse:** Navigate through your computer screen with hand movements, simulating a virtual mouse.
- **Face Recognition:** Log in to your system using face recognition technology, enhancing security.
- **Voice Recognition:** Enable voice recognition to perform actions by speaking commands.
- **Virtual Mouse Functions:**
  - Move the cursor
  - Click and hold
  - Scroll up and down
  - Volume control (up and down)
  - Play/pause
  - Mute
  - Voice command input

## Dependencies

- Python
- OpenCV
- Mediapipe
- Flask
- MySQL
- Face Recognition
- Passlib
- Speech Recognition
- Playsound
- PyAutoGUI
- Win32api

## Getting Started

1. Clone the repository to your local machine.
2. Install the required Python packages listed in the `requirements.txt` file.
3. Set up a MySQL database with the provided schema.
4. Configure the MySQL connection parameters in the Flask application (`app.py`).
5. Run the Flask application using `python app.py`.
6. Access the application through the provided URLs.

## Usage

1. **Signup:** Create an account by providing your full name, email, and password.
2. **Login:** Use your credentials to log in. Face recognition is used for authentication.
3. **Capture:** Capture your facial features for recognition.
4. **Main Interface:** Interact with the system using hand gestures and voice commands.


## Contributors

- Aman Agarwal - GitHub ID - AmanAg744
- Anirudh Agrawal - GitHub ID - AnirudhA124
- Yashika Goyal - GitHub ID - yashikax

## Mentor

- Siddharta Bhat - GitHub ID - SBhat2615

## Acknowledgments

- Thanks to the open-source community for providing essential libraries and tools.
- Special thanks to my teammates for their dedication and support throughout the project.
- Heartfelt gratitude to our mentor for providing valuable guidance and insights.
- Special thanks to [Mediapipe](https://mediapipe.dev/) for the hand and face recognition models.
- Face recognition powered by [face_recognition](https://github.com/ageitgey/face_recognition).
- Voice recognition powered by [SpeechRecognition](https://pypi.org/project/SpeechRecognition/).

Feel free to contribute, report issues, or suggest improvements!
