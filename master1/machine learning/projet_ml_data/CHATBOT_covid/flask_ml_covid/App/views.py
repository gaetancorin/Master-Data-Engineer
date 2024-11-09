from flask import *
from flask_cors import CORS

import pandas as pd
import logging
import App.model as model
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
# pd.set_option('display.max_rows', 50)
# pd.set_option('display.min_rows', 50)
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)

# http://127.0.0.1:5000/

def user_reinitialisation(user):
    user["Sore throat"] = None
    user["Dry Cough"] = None
    user["Abroad travel"] = None
    user["Breathing Problem"] = None
    user["Attended Large Gathering"] = None
    user["Contact with COVID Patient"] = None
    user["Fever"] = None
    user["Family working in Public Exposed Places"] = None
    user["Visited Public Exposed Places"] = None
    user["Hyper Tension"] = None
    user["Asthma"] = None
    user["Diabetes"] = None
    return user

RFC = model.create_model_and_fit()

user = {}
user_reinitialisation(user)

@app.route('/hello', methods=['GET'])
def hello():
    return 'hello you'

@app.route('/', methods=['GET'])
def index():
    chat_text = "bonjour, je suis monsieur chatbot. J'analyse vos symptômes et vous indique les potentiels risques de COVID-19"
    return render_template('index.html', chat_text=chat_text)

@app.route('/analysing', methods=['POST'])
def analysing():
    user_input = request.form.get('user-input')
    result = None
    if user_input == 'oui' or user_input == 'Oui' or user_input == 'OUI':
        result = 1
    if user_input == 'non' or user_input == 'Non' or user_input == 'NON':
        result = 0

    if result == None and user["Sore throat"] == None:
        session['chat_text'] = "En répondant par 'oui' ou par 'non', ressentez vous un mal de gorge ?"
    elif result == None:
        return render_template('analysing.html', chat_text=session['chat_text'])
    elif user["Sore throat"] == None:
        user["Sore throat"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non', avez vous une toux sèche ?"
    elif user["Dry Cough"] == None:
        user["Dry Cough"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non', avez vous voyagez à l'étranger ?"
    elif user["Abroad travel"] == None:
        user["Abroad travel"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non', ressentez vous des problèmes de respiration ?"
    elif user["Breathing Problem"] == None:
        user["Breathing Problem"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non', avez vous participer à un grand rassemblement de personnes ?"
    elif user["Attended Large Gathering"] == None:
        user["Attended Large Gathering"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non', avez vous été en contact avec une personne ayant eu le COVID ?"
    elif user["Contact with COVID Patient"] == None:
        user["Contact with COVID Patient"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non', avez vous de la fièvre ?"
    elif user["Fever"] == None:
        user["Fever"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non', est ce que un membre de votre famille travail dans un lieu public exposé ?"
    elif user["Family working in Public Exposed Places"] == None:
        user["Family working in Public Exposed Places"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non', avez vous récemment visité un lieu public exposé ?"
    elif user["Visited Public Exposed Places"] == None:
        user["Visited Public Exposed Places"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non', faite vous de l'hypertension ?"
    elif user["Hyper Tension"] == None:
        user["Hyper Tension"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non',  faite vous de l'asthme ?"
    elif user["Asthma"] == None:
        user["Asthma"] = result
        session['chat_text'] = "En répondant par 'oui' ou par 'non', faite vous du diabète ?"
    elif user["Diabetes"] == None:
        user["Diabetes"] = result
        result, confiance = model.get_target_by_model(RFC, user)
        user_reinitialisation(user)
        if result == 1:
            session['chat_text'] = f"D'après nos analyses, vous êtes potentiellement POSITIF au COVID-19 avec une confiance de {confiance[0][1]*100} %, nous vous invitons a aller consulter"
        else:
            session['chat_text'] = f"D'après nos analyses, vous êtes potentiellement NEGATIF au COVID-19 avec une confiance de {confiance[0][0]*100} %. N'hésitez pas a refaire le test en cas de nouveaux symptomes ou  critères"
        return render_template('display_result.html', chat_text=session['chat_text'])

    print(user)
    return render_template('analysing.html', chat_text=session['chat_text'])
