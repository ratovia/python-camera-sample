from flask import Flask, Response
import threading

from VideoCamera import VideoCamera


app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(generate(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def generate(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

if __name__ == '__main__':
    threading.Thread(target=app.run, kwargs={'host':'0.0.0.0','port':5001}).start()
