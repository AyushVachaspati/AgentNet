import argparse
import json
from api.agentnet_api import call_openAI
from api import agentnet_api
def create_agent(system_prompt, datafile, address, port):
    agent = {
        "messages": [],
        "address": address
    }

    with open(system_prompt,"r") as file:
        prompt = file.read()
    
    with open(datafile,"r") as file:
        data = file.read()
    

    system_prompt = f"""{prompt}\n"DOCUMENT START"\n{data}\nDOCUMENT END"""
    system_message = {
        "role": "system",
        "content": system_prompt
    }


    tools = [{
        "type": "function",
        "function": {
            "name": "send_message",
            "description": "Send message to talk to other agents on AgentNet.\n"
                           "This is the primary function to be used to complete tasks assigned to the agent.\n"
                           "This function can also be used to respond to messages from other agents on AgentNet.\n"
                           "Only call this function one time per turn.",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to agent on AgentNet.",
                    },
                },
                "required": ["message"],
            },
        },
        "type": "function",
        "function": {
            "name": "stop_conversation",
            "description": "Stop conversation with other agents on the network and provide final result of the conversation.\n"
                           "Use this function to conclude or stop the current conversation.\n"
                           "Only call this function one time at the end of the conversation. Do not call send_message function along with this function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "result": {
                        "type": "string",
                        "description": "Final Result of the conversation.",
                    },
                },
                "required": ["result"],
            },
        },
        }]

    agent["messages"].append(system_message)
    agent["tools"] = tools
    agent['port'] = port
    return agent


def run_agent(agent):
    response = call_openAI(agent)

    func_args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
    func_name = response.choices[0].message.tool_calls[0].function.name
    # print(f"Calling function {func} with {func_args['message']}")
    func = getattr(agentnet_api, func_name)

    ## arguments are hard coded here and not dependent on which function is called. Right now just assuming that send message is the only function that can be called
    if(func_name == 'send_message'):
        func(func_args['message'], agent["address"],agent)
    elif(func_name == 'stop_conversation'):
        func(func_args['result'])
    else:
        print(f"FUNCTION NOT RECOGNIZED {func_name}")





