from google.oauth2 import service_account
import dialogflow
from tools.data_clean import filterpy

# Constants

DIALOGFLOW_PROJECT_ID = 'tigerbot-943ba'
DIALOGFLOW_LANGUAGE_CODE = 'en-US'
GOOGLE_APPLICATION_CREDENTIALS = 'tigerbot-943ba-e785ca33e7a0.json'
SESSION_ID = 'tigerbot'
PROJECT_ID = 'tigerbot-943ba'
credentials = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

# Initialize session
session_client = dialogflow.SessionsClient(credentials=credentials)
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
intents_client = dialogflow.IntentsClient(credentials=credentials)
parent = intents_client.project_agent_path(PROJECT_ID)

def create_intent(display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    training_phrases = []

    for training_phrases_part in training_phrases_parts:
        training_phrases_part = ' '.join(filterpy(training_phrases_part.split(' ')))
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)

    print('Intent created: {}'.format(response))


def get_analyzed_text_response(text_to_be_analyzed):
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response

def get_response(response):
    response_intent = response.query_result.intent.display_name
    response_text = response.query_result.fulfillment_text
    return response_intent, response_text


def print_response(response):
    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text:", response.query_result.fulfillment_text)


if __name__ == "__main__":
    text_to_be_analyzed = "who is the teacher?"
    no_answer_text = "xxx"

    print_response(get_analyzed_text_response(text_to_be_analyzed))
    print_response(get_analyzed_text_response(no_answer_text))
