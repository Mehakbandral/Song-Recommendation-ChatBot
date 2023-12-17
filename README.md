# Song Recommendation Chatbot

## Overview

This project involves the creation of an interactive chatbot system designed to recommend songs based on users' emotions. The chatbot integrates with various APIs, such as Last.fm and IBM Watson NLU (Natural Language Understanding), to enhance the song recommendation process. Last.fm API provides song recommendations, while IBM Watson NLU is used to analyze the emotions expressed by users. Datasets are utilized in JSON format, meticulously crafted for this project.

## Technologies Used

- **Programming Language:** Python
- **Libraries:** NLTK, Keras, NumPy
- **Frontend Development:** HTML, CSS, JavaScript
- **Backend Development:** Flask

## Features

- **Emotion-based Song Recommendations:** The chatbot leverages Last.fm API to recommend songs tailored to the emotions expressed by users.

- **Emotion Analysis:** IBM Watson NLU is employed to analyze user input and determine the emotional context.

- **Custom Datasets:** Datasets are created in JSON format, specifically tailored for this project to enhance the effectiveness of song recommendations.

- **Natural Language Processing (NLP):** Various NLP technologies are integrated to understand and respond to user queries effectively.

## How It Works

1. **User Input:** Users interact with the chatbot by expressing their emotions or preferences.

2. **Last.fm Integration:** The chatbot communicates with the Last.fm API to obtain personalized song recommendations.

3. **IBM Watson NLU:** User input is sent to IBM Watson NLU for emotion analysis to further refine song suggestions.

4. **Dataset Utilization:** Custom datasets in JSON format are utilized to improve the chatbot's understanding of user preferences.

5. **Frontend and Backend Development:** The frontend is developed using HTML, CSS, and JavaScript, while Flask is employed for backend development.

## Dependencies

Ensure you have the following Python libraries installed:

```bash
pip install nltk keras numpy Flask
