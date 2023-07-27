from flask import Flask, request
import threading
import cv2
import logging

app = Flask(__name__)

recording = False
recorder = None
cap = cv2.VideoCapture(0) # Capture video from default camera

logging.basicConfig(level=logging.DEBUG)  # Setup logging

lock = threading.Lock()  # Add this line at the beginning of your code

@app.route('/record', methods=['POST'])
def record():
    global recording
    global recorder
    global cap
    global lock  # Add this line

    action = request.form.get('action')
    logging.debug(f'Received action: {action}')  # Log the received action

    if action == 'start':
        if not recording: # Start recording if not already recording
            logging.debug('Starting recording.')  # Log recording start
            # 現在の日時を取得
            now = datetime.datetime.now()
            # ファイル名に使用する日時文字列を作成
            filename = 'rec/' + now.strftime('%Y%m%d_%H%M%S') + '.mp4'
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = int(cap.get(cv2.CAP_PROP_FPS))                    # カメラのFPSを取得
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))              # カメラの横幅を取得
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cv2.VideoWriter(filename, fourcc, fps, (width, height))
            recording = True
    elif action == 'stop':
        with lock:  # Add this line
            if recording: # Stop recording if currently recording
                logging.debug('Stopping recording.')  # Log recording stop
                recording = False
                recorder.release() # Release the VideoWriter
                recorder = None

    return '', 200

def capture_video():
    global recording
    global recorder
    global cap
    global lock  # Add this line

    while True:
        ret, frame = cap.read() # Capture a frame from the camera

        with lock:  # Add this line
            if recording and ret:
                logging.debug('Recording frame.')  # Log frame recording
                recorder.write(frame)  # Write the frame to the file if recording
if __name__ == '__main__':
    video_thread = threading.Thread(target=capture_video) # Create a thread that captures video
    logging.debug('Starting video capture thread.')  # Log thread start
    video_thread.start() # Start the video capture thread
    app.run(host='0.0.0.0',port=5000)
