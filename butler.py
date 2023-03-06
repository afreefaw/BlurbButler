import os
import requests
import json


def match_topic(user_msg, topics, api_key):
    '''Classify input message as one of topics'''
    combined = 'Select the most relevant topic from this list: Be concise. Do not explain. Say "None" if none apply.' + \
        str(topics) + '\nText to choose topic for:' + user_msg
    msgs = [{"role": "user",
                    "content": combined}]
    out = get_msg(get_response(msgs, api_key))
    for c in '\n,.': #chars to remove
        out = out.replace(c, '')
    return out.lower()

def get_response(msgs, api_key):
    '''Call api with messages and blurb as context, return response.'''
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

def load_docs(topic_map):
    '''Use topic:filename mapping to return dict with format topic (str) : blurb (str)
    Values are read from .txt files in blurbs folder'''
    topic_contents = {}
    for topic, filename in topic_map.items():
        with open('blurbs/' + filename, 'r') as f:
            topic_contents[topic] = f.read()
    return topic_contents
    
def get_msg(response):
    '''Returns the message portion of of an API response'''
    if 'choices' in response.json().keys():
        return response.json()['choices'][0]['message']['content']
    else: return None

def build_system_msg(topic, blurbs):
    '''Builds and returns a system message in dict form expected by API'''
    if topic in blurbs.keys():
        system_msg = "SYSTEM found this context relevant to user's query (user does not see this info):\nTOPIC: " + topic + '\n' + blurbs[topic]
        return {'role':'system','content':system_msg}
    else:
        return {'role':'system','content':'No relevant content found'}
    
def build_user_msg(msg):
    '''Builds and returns a user message in dict form expected by API'''
    return {'role':'user','content':msg}

def main():
    API_KEY = open('apikey.txt', 'r').read()
    
    with open('topics.json', 'r') as f:
        TOPIC_MAP = json.load(f)

    BLURBS = load_docs(TOPIC_MAP)
    TOPICS = list(BLURBS.keys())
    msgs = [{'role':'system',
         'content':'You are a concise personal assistant. Help the user, paying special attention to content provided by the SYSTEM, which is not visible to the user but is relevant to their query.'}]
    
    print('Type exit to exit.')
    while True:
        user_msg = input()
        if user_msg.lower() == 'exit': break
        
        msgs.append(build_user_msg(user_msg))
        topic = match_topic(user_msg, TOPICS, API_KEY)
        msgs.append(build_system_msg(topic, BLURBS))
        assist_msg = get_msg(get_response(msgs, API_KEY))
        msgs.append({'role':'assistant','content':assist_msg})
        print(assist_msg)

if __name__ == "__main__":
    main()
    