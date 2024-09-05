from openai import OpenAI
import requests


def call_openAI(agent):
    client = OpenAI(api_key='sk-2qnihlmm3K1aLQnigXnNJaA_U6gHpQ-JUcmphhOs1XT3BlbkFJ0e4tccgZwAWjbuAIPLd9VKUC0Q6tq0T-O441koDl4A')
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=agent["messages"],
        tools=agent["tools"],
        tool_choice="required",
    )
    client.close()
    return response


def send_message(message, address, agent):
    print( '\033[34m' + f"Recruiter: {message}" + '\033[0m')
    print()
    agent['messages'].append({"role":"assistant", "content":message})

    url = address+"/send_message"
    myobj = {'message': message,
             'address': f"http://127.0.0.1:{agent['port']}"}  # callback address

    #stupid hack to make it non blocking
    try:
        requests.post(url, json = myobj,timeout=0.5)
    except:
        pass

def message_received(message, sender_address, agent):
    agent['messages'].append(message)
    agent['address'] = sender_address

def stop_conversation(result):
    print()
    print('\033[32m' + "Candidate Evaluation Complete" + '\033[0m')
    print(f"Result: {result}")
    