import os
import requests
import json
import logging


def match_topic(user_msg: str, topics: list[str], api_key: str) -> str:
    '''
    Classifies the input message as one of the topics using the OpenAI API.
    
    Args:
    - user_msg (str): The user's message to be classified.
    - topics (list[str]): A list of topics to classify the message into.
    - api_key (str): The API key for accessing the OpenAI API.

    Returns:
    - A string representing the topic that the input message was classified into.
    '''
    combined = 'Select the most relevant topic from this list: Be concise. Do not explain. Say "None" if none apply.' + \
        str(topics) + '\nText to choose topic for:' + user_msg
    msgs = [{"role": "user",
                    "content": combined}]
    out = get_msg(get_response(msgs, api_key)).lower()
    for c in '\n,.': #chars to remove
        out = out.replace(c, '')
    logging.info('TOPIC: '+out)
    return out

def get_response(msgs: list[dict], api_key: str) -> requests.Response:
    '''
    Calls the OpenAI API with the given messages and returns the response.

    Args:
    - msgs (list[dict]): A list of messages to send to the API.
    - api_key (str): The API key for accessing the OpenAI API.

    Returns:
    - A requests.Response object representing the response from the API.
    '''
    
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+api_key
    }
    data = {
      "model": "gpt-3.5-turbo",
      "messages": msgs
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

def load_docs(topic_map: dict) -> dict:
    '''
    Loads the blurbs for each topic from a file and returns them as a dictionary.

    Args:
    - topic_map (dict): A dictionary mapping topics to filenames containing their blurbs.

    Returns:
    - A dictionary with topics as keys and their corresponding blurbs as values.
    '''
    topic_contents = {}
    for topic, filename in topic_map.items():
        with open('blurbs/' + filename, 'r') as f:
            topic_contents[topic] = f.read()
    return topic_contents
    
def get_msg(response: requests.Response) -> str:
    '''Returns the message portion of of an API response'''
    if 'choices' in response.json().keys():
        return response.json()['choices'][0]['message']['content']
    else: return None

def build_system_msg(topic: str, blurbs: dict) -> dict:
    '''
    Builds a system message to send to the user using topic-matched blurb.

    Args:
    - topic (str): The topic of the message.
    - blurbs (dict): A dictionary containing the blurbs for each topic.

    Returns:
    - A dictionary representing the system message to send to the user.
    '''
    if topic in blurbs.keys():
        system_msg = ('SYSTEM found this context relevant to user\'s query (user '
        'does not see this info):\nTOPIC: ') + topic + '\n' + blurbs[topic]
        return {'role':'system','content':system_msg}
    else:
        return {'role':'system','content':'No relevant content found'}
    
def build_user_msg(msg: str) -> dict:
    '''Builds a user message in dict form expected by API'''
    return {'role':'user','content':msg}

def log_last_msg(msgs: list[dict]) -> None:
    '''Logs the last message in the list for debugging purposes.'''
    logging.info(str(msgs[-1]))

def main() -> None:
    API_KEY = os.environ.get("OPENAI_API_KEY")
    logging.basicConfig(filename='conversation.log', level=logging.INFO)
    logging.info('\n---NEW CONVERSATION---\n')
    
    with open('topics.json', 'r') as f:
        TOPIC_MAP = json.load(f)

    BLURBS = load_docs(TOPIC_MAP)
    TOPICS = list(BLURBS.keys())
    msgs = [{'role':'system',
         'content':('You are a concise personal assistant. Help the user, paying '
             'special attention to content provided by the SYSTEM, which is not '
             'visible to the user but is relevant to their query.')}]
    
    print('Type exit to exit.')
    while True:
        user_msg = input()
        if user_msg.lower() == 'exit': break
        
        msgs.append(build_user_msg(user_msg))
        log_last_msg(msgs) # Log what the actor sees
        
        topic = match_topic(user_msg, TOPICS, API_KEY)
        msgs.append(build_system_msg(topic, BLURBS))
        log_last_msg(msgs)
        
        assist_msg = get_msg(get_response(msgs, API_KEY))
        msgs.append({'role':'assistant','content':assist_msg})
        log_last_msg(msgs)
        
        print(assist_msg)

if __name__ == "__main__":
    main()
    
    
    