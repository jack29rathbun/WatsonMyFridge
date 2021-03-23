from flask import Flask, request, jsonify, render_template
import os
import requests
import json

app = Flask(__name__)

class Recipe:
  def __init__(self, result):
    self.title = result["results"][0]["title"]
    self.ingredients = result["results"][0]["ingredients"]
    self.instructions = result["results"][0]["instructions"]

class DiscoveryContainer:
    def __init__(self):
        authenticator = IAMAuthenticator(os.getenv("WATSON_KEY"))
        self.discovery = DiscoveryV1(
            version='2019-04-30',
            authenticator=authenticator
        )

        self.discovery.set_service_url(os.getenv("WATSON_URL"))

    def getRecipesFromIngredients(self, ingredients):
      queryString = ""
      if len(ingredients) > 0:
        queryString = "ingredients:" + ingredients[0]
        for i in range(1, len(ingredients)):
          queryString += ",ingredients:" + ingredients[i]
      return self.discovery.query(environment_id='a68f0894-50a5-4e91-9f4d-11780877141d', collection_id='eacea543-c7f3-45a1-98fa-9fe86c4b34f6',query=queryString).get_result()

      def getTitlesFromIngredients(self, ingredients):
          titles = []
          for result in self.getRecipesFromIngredients(self.discovery, ingredients)["results"]:
            titles.append(result["title"])
          return titles

    def getFullRecipeFromTitle(self, title):
        return Recipe(self.query(environment_id='a68f0894-50a5-4e91-9f4d-11780877141d', collection_id='eacea543-c7f3-45a1-98fa-9fe86c4b34f6',query="title::" + title).get_result())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_movie_detail', methods=['POST'])
def get_movie_detail():
    data = request.get_json(silent=True)

    try:
        movie = data['queryResult']['parameters']['movie']
        api_key = os.getenv('OMDB_API_KEY')

        movie_detail = requests.get('http://www.omdbapi.com/?t={0}&apikey={1}'.format(movie, api_key)).content
        movie_detail = json.loads(movie_detail)

        response =  """
            Title : {0}
            Released: {1}
            Actors: {2}
            Plot: {3}
        """.format(movie_detail['Title'], movie_detail['Released'], movie_detail['Actors'], movie_detail['Plot'])
    except:
        response = "Could not get movie detail at the moment, please try again"

    reply = { "fulfillmentText": response }

    return jsonify(reply)

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        socketId = request.form['socketId']
    except KeyError:
        socketId = ''

    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = { "message":  fulfillment_text }

    pusher_client.trigger(
        'movie_bot',
        'new_message',
        {
            'human_message': message,
            'bot_message': fulfillment_text,
        },
        socketId
    )

    return jsonify(response_text)

# run Flask app
if __name__ == "__main__":
    app.run()