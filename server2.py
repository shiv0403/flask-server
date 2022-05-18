from flask import Flask, request, Response
from flask_restful import Api, Resource
import object_detection_api
import os
from PIL import Image
import json

app = Flask(__name__)
api = Api(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    # Put any other methods you need here
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


class Home(Resource):
    def get(self):
        return "This is home route"


class Test(Resource):
    def post(self):
        PATH_TO_TEST_IMAGES_DIR = 'object_detection/test_img'  # cwh
        TEST_IMAGE_PATHS = [os.path.join(
            PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 4)]

        image = Image.open(TEST_IMAGE_PATHS[2])
        objects = object_detection_api.get_objects(image)

        return (objects)


class ImagePost(Resource):
    def post(self):
        try:
            image_file = request.files['image']  # get the image

            # Set an image confidence threshold value to limit returned data
            threshold = request.form.get('threshold')
            if threshold is None:
                threshold = 0.5
            else:
                threshold = float(threshold)

            # finally run the image through tensor flow object detection`
            image_object = Image.open(image_file)
            objects = object_detection_api.get_objects(image_object, threshold)
            return objects

        except Exception as e:
            print('POST /image error: %e' % e)
            return e


api.add_resource(Home, "/")
api.add_resource(Test, "/test")
api.add_resource(ImagePost, "/image")


if __name__ == "__main__":
    app.run(debug=True)
