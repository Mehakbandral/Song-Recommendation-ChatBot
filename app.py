from flask import Flask, request, jsonify, render_template
import random
import os
import requests
import csv
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, EmotionOptions

#import nltk
#from nltk.tokenize import word_tokenize
from Chatbot import Chatbot  # Import the Chatbot class from your module

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"), static_folder='static')

# Last.fm API parameters
LASTFM_API_KEY = "20d219003e2699a85466235f43caa9f9"
LASTFM_API_URL = "http://ws.audioscrobbler.com/2.0/"

# Function to generate a response to user input
def generate_response(user_input):
    # Create an instance of the Chatbot class
    chatbot = Chatbot()

    response = chatbot.respond(user_input)
    #user_input = user_input.lower()
    # Tokenize the user input
    emotions_keywords_fromimb = ibmNLPCall(user_input)

    if response:
        print("FM search "+ emotions_keywords_fromimb +" "+user_input)
        #response = search_song(emotions_keywords_fromimb)
        return response, emotions_keywords_fromimb
    else:
        return "I'm sorry, I didn't quite catch that. Could you please rephrase?", emotions_keywords_fromimb


    # Check if the user's input contains any greetings
    for greeting in greetings:
        if greeting in user_input:
            return random.choice(greeting_responses), ""

    # Check if the user's input contains emotional keywords and search for a song
    """for emotion, keyword in emotions_keywords.items():
        if keyword in user_input:
            response = search_song(keyword)
            return response"""
    #print("caling ibm api for>>" + user_input)
    emotions_keywords_fromimb = ibmNLPCall(user_input)
    #print("FROM IBM I got>>>"+user_input)
    print("FM search "+ emotions_keywords_fromimb +" "+user_input)
    response = search_song(emotions_keywords_fromimb)
    #print("resp ==>"+ response)
    if response is not None:
        return response,emotions_keywords_fromimb
    # If no greeting or emotional keyword is found, return a default response
    return "I'm sorry, I didn't quite understand that. Can you please rephrase?", emotions_keywords_fromimb

def generate_track_table(tracks):
    selected_tracks = random.sample(tracks["track"], 6)  # Select 6 tracks randomly
    
    str_alltracks = "I found a song for you:"
    str_alltracks += "<div class='track-container'>"
    
    # Add CSS style for alternating row colors and columns
    
    str_alltracks += "</div>"
    str_alltracks = "I found a song for you:"
    str_alltracks += "<div class='track-container'>"

    str_alltracks += "<style>"
    str_alltracks += "  .table-container {"
    str_alltracks += "    display: flex;"
    str_alltracks += "    gap: 10px;"
    str_alltracks += "  }"
    str_alltracks += ""
    str_alltracks += "  .table-column {"
    str_alltracks += "    flex: 1;"
    str_alltracks += " }"
    str_alltracks += ""
    str_alltracks += " .song {"
    str_alltracks += "   border: 1px solid #ccc;"
    str_alltracks += "   padding: 5px;"
    str_alltracks += "   margin: 1%;"
    str_alltracks += "   width: 50%;"
    str_alltracks += "   background-color: lightblue;"
    str_alltracks += " }"
    str_alltracks += ""
    str_alltracks += " .song h3,"
    str_alltracks += " .song p {"
    str_alltracks += "   margin: 3px 0;"
    str_alltracks += " }"
    str_alltracks += ""
    str_alltracks += "  .song img {"
    str_alltracks += "    max-width: 100%;"
    str_alltracks += "    height: auto;"
    str_alltracks += "  }"
    str_alltracks += "</style>"
    
    str_alltracks += "<div class='table-container'>"
    #str_alltracks += "    <div class='table-column'>"


    i = 0
    for index, alltracks in enumerate(selected_tracks, start=1):
        artist = alltracks["artist"]["name"]
        title = alltracks["name"]
        url = alltracks["url"]
        image = alltracks["image"][0]["#text"]
        i = i + 1
        cnt = i
        # Construct the row with alternating colors

        if i < 4 :
            if i == 1 :
                str_alltracks += "    <div class='table-column'>"
            if i == 2 : 
                str_alltracks += f"	  <div class='song'>"
            else:
                str_alltracks += f"	  <div class='song' style='background-color: lightgrey;'>"
            #str_alltracks += f"	  <div class='song'>"+str(i)+""
            str_alltracks += f"        <h3>{cnt}: <a href='{url}' title='{title}' target='_blank'>{title}</a></h3>"
            str_alltracks += f"        <p style='margin-left: 30px'>by {artist}</p>"
            #str_alltracks += f"        <img src='{image}' alt='Song Image'>"
            str_alltracks += f"    </div>"
            if i == 3 :
                str_alltracks += f"    </div>"

        else:
            if i == 4 :
                str_alltracks += "    <div class='table-column'>"
            if i == 5 : 
                str_alltracks += f"	  <div class='song'>"
            else:
                str_alltracks += f"	  <div class='song' style='background-color: lightgrey;'>"
            str_alltracks += f""
            str_alltracks += f"      <h3>{cnt}: <a href='{url}' title='{title}' target='_blank'>{title}</a></h3>"
            str_alltracks += f"      <p style='margin-left: 30px'>by {artist}</p>"
            #str_alltracks += f"      <img src='{image}' alt='Song Image'>"
            str_alltracks += f"    </div>"
            if i == 6 :
                str_alltracks += f"    </div>"

    str_alltracks += "  </div>"

    return str_alltracks


# Function to search for a song using Last.fm API
def search_song(keyword):
    params = {
        "method": "tag.gettoptracks",
        "tag": keyword,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit":20
    }
    response = requests.get(LASTFM_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if "tracks" in data :
            tracks = data["tracks"]
            if len(tracks) == 0:
                return "No matching song detected, We can continue the chat."
            
            table_html = generate_track_table(tracks)
            return table_html
    return f"I couldn't find a song related to {keyword}."

@app.route('/')
def index():
    return render_template('indexweb.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['message']
    response , emotion = generate_response(user_input)
    return jsonify({"message": response, "emotion":emotion})

@app.route('/chat/searchsong', methods=['POST'])
def chatsearchsong():
    data = request.json
    user_input = data['message']
    response  = search_song(user_input)
    return jsonify({"message": response})

def ibmNLPCall(text):
        
    authenticator = IAMAuthenticator('bxlMNl8X5yiyzb4qYULuAGL9tUBneEgKTi1UqEiF3jHJ')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/7f0d6eac-7b8a-4683-829f-db19d472c0b5/v1/analyze?version=2019-07-12')

    response = natural_language_understanding.analyze(
        html="<p>"+text+"</p>",
        features=Features(emotion=EmotionOptions())).get_result()

    #print(json.dumps(response, indent=2))
    json_data = json.dumps(response, indent=2)
    data = json.loads(json_data)

    # Extract emotions from the "document" section
    document_emotions = data['emotion']['document']['emotion']

    # Find the emotion with the highest value
    highest_emotion = max(document_emotions, key=document_emotions.get)

    print(f"The emotion with the highest value is: {highest_emotion}")

    return highest_emotion 

# API endpoint to handle form submission
@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    name = request.form.get('name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    rating = request.form.get('rating')
    feedback = request.form.get('feedback')

    # Save the data in a CSV file
    with open('ratings.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([name, email, mobile, rating, feedback])

    return 'Rating submitted successfully!'

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='localhost', port=5000)


# Last.fm API parameters
#LASTFM_API_KEY = "20d219003e2699a85466235f43caa9f9"
