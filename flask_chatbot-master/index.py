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

    def getNumberFromIngredients(self, ingredients):
        return self.getRecipesFromIngredients(ingredients)["matching_results"]

    def getTitlesFromIngredients(self, ingredients):
          titles = []
          for result in self.getRecipesFromIngredients(ingredients)["results"]:
            titles.append(result["title"])
          return titles

    def getFullRecipeFromTitle(self, title):
        return Recipe(self.discovery.query(environment_id='a68f0894-50a5-4e91-9f4d-11780877141d', collection_id='eacea543-c7f3-45a1-98fa-9fe86c4b34f6',query="title::" + title).get_result())


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_number', methods=['POST'])
def get_number():
    disc = DiscoveryContainer()
    ingredients = request.form["message"].split(",")
    msg = str(disc.getNumberFromIngredients(ingredients))
    return {"message": msg}

@app.route('/get_titles', methods=['POST'])
def get_titles():
    disc = DiscoveryContainer()
    ingredients = request.form["message"].split(",")
    titles = disc.getTitlesFromIngredients(ingredients)
    msg = "<ol>"
    for recipe in titles:
        msg += f'<li>{recipe}</li>'
    msg += '</ol>'
    msg += 'Enter a recipe number to see the full recipe.'
    return {"message": msg}

@app.route('/get_full', methods=['POST'])
def get_full():
    disc = DiscoveryContainer()
    ingredients = request.form["message"].split(",")
    index = int(ingredients.pop(-1)) - 1
    titles = disc.getTitlesFromIngredients(ingredients)
    if len(titles) < index + 1:
        return {"message": "Please enter a valid number."}
    recipe = disc.getFullRecipeFromTitle(titles[index])
    recipe.ingredients.pop(-1)
    msg = recipe.title
    msg += "<br>Ingredients:"
    msg += "<ol>"
    for ingredient in recipe.ingredients:
        msg += f'<li>{ingredient}</li>'
    msg += "</ol>"
    msg += "Instructions:<br> "
    msg += recipe.instructions
    return {"message": msg}


# run Flask app
if __name__ == "__main__":
    app.run()
