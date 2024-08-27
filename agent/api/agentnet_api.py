from openai import OpenAI
import requests


def call_openAI(agent):
    client = OpenAI(api_key='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')
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=agent["messages"],
        tools=agent["tools"],
        tool_choice="required"
    )
    return response


def send_message(message, address, agent):
    print(f"####sending response###\n {message}")

    agent['messages'].append({"role":"assistant", "content":message})

    url = address+"/send_message"
    myobj = {'message': message,
             'address': f"http://127.0.0.1:{agent['port']}"}  # callback address

    requests.post(url, json = myobj)

def message_received(message, sender_address, agent):
    agent['messages'].append(message)
    agent['address'] = sender_address