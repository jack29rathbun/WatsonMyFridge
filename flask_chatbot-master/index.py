from flask import Flask, request, jsonify, render_template
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1
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
          for result in self.getRecipesFromIngredients(ingredients)["results"]:
            titles.append(result["title"])
          return titles

    def getFullRecipeFromTitle(self, title):
        return Recipe(self.query(environment_id='a68f0894-50a5-4e91-9f4d-11780877141d', collection_id='eacea543-c7f3-45a1-98fa-9fe86c4b34f6',query="title::" + title).get_result())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    disc = DiscoveryContainer()
    ingredients = request.form["message"].split(",")
    titles = str(disc.getTitlesFromIngredients(ingredients))
    return {"message": titles}

# run Flask app
if __name__ == "__main__":
    app.run()