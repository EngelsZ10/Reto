import face_recognition
from PIL import Image
import numpy as np
from io import BytesIO
import base64
from flask import Flask, jsonify, request, Response

app = Flask(__name__)

def crop_image(img, coordinates):
    top, right, bottom, left = coordinates
    box = (left, top, right, bottom)
    cropped_img = img.crop(box)
    return cropped_img



@app.route('/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/pruebas', methods=['GET', 'POST'])
def pruebas():
    return Response(open('pruebas.html').read(), mimetype="text/html")

@app.route('/get_encoding', methods=['post'])
def getEncodings():
    imgBase64 = request.json['img']
    im_bytes = base64.b64decode(imgBase64[imgBase64.index(",")+1:])
    im_file = BytesIO(im_bytes)  
    image = Image.open(im_file)
    load = np.array(image)
    face_locations = face_recognition.face_locations(load)
    result = []
    for i in face_locations:
        cropped_img = crop_image(image, i)
        load = np.array(cropped_img)
        try:
            encoding = list(face_recognition.face_encodings(load)[0])
        except:
            continue
        img_byte_array = BytesIO()
        cropped_img.save(img_byte_array, format="JPEG")
        base64_image = base64.b64encode(img_byte_array.getvalue())
        result.append({"face":'data:image/JPEG;base64,' + str(base64_image)[2:-1], "encoding":encoding})
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=105)