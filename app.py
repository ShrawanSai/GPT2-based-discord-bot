from flask import Flask
from flask_restful import Resource, Api
from GPT2Predictor import PythonPredictor

app = Flask(__name__)
api = Api(app)

predictor = PythonPredictor(True)


class StoryGenerator(Resource):
    def post(self,current_text,length):

        text = predictor.predict({"text":current_text,"predictor_length":length})
        return {'gen_text': text}

api.add_resource(StoryGenerator, '/storygen/<string:current_text>/<int:length>')

if __name__ == '__main__':
    app.run(debug=True)
