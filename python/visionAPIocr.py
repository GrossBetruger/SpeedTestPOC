import json
import requests
import base64
import sys


def encode_image(img_file_name):
    with open(img_file_name, 'rb') as f:
        return base64.b64encode(f.read())


def create_json(encoded_img, dump_filename):
    jsn = {
        "requests": [
            {
                "image": {
                    "content": encoded_img
                },
                "features": [
                    {
                        "type": "TEXT_DETECTION",
                        "maxResults": "10"
                    }
                ]
            }
        ]
    }
    with open(dump_filename, 'wb') as f:
        json.dump(jsn, f)


def askGoogle():
    data = open('vision.json', 'rb').read()
    print data
    response = requests.post(
        url='https://vision.googleapis.com/v1/images:annotate?key=AIzaSyBrkKNc_7vNBvlY6P83atDavKvZGJKQTms',
        data=data,
        headers={'Content-Type': 'application/json'})
    return response


def extract_float_from_response(google_response):
    mbps = google_response["responses"][0]["textAnnotations"][2]['description']
    return mbps


encoded = encode_image(sys.argv[1])
create_json(encoded, 'vision.json')
r = askGoogle()

print extract_float_from_response(r.json())
