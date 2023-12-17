import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, EmotionOptions

authenticator = IAMAuthenticator('bxlMNl8X5yiyzb4qYULuAGL9tUBneEgKTi1UqEiF3jHJ')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)

natural_language_understanding.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/7f0d6eac-7b8a-4683-829f-db19d472c0b5/v1/analyze?version=2019-07-12')

response = natural_language_understanding.analyze(
    html="<p>I feel happy today</p>",
    features=Features(emotion=EmotionOptions())).get_result()

print(json.dumps(response, indent=2))
json_data = json.dumps(response, indent=2)
data = json.loads(json_data)

# Extract emotions from the "document" section
document_emotions = data['emotion']['document']['emotion']

# Find the emotion with the highest value
highest_emotion = max(document_emotions, key=document_emotions.get)

print(f"The emotion with the highest value is: {highest_emotion}")