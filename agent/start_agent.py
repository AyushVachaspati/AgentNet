from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from api.agentnet_api import message_received
from simple_agent import create_agent,run_agent
import uvicorn
import argparse
import logging
import time

logging.basicConfig(level=logging.ERROR)

app = FastAPI()
agent = None 

class Message(BaseModel):
    message: str
    address: str
    
@app.post("/send_message")
def handle_message(message: Message):
    print('\033[97m' + f"Recruiter: {message.message}" + '\033[0m')
    print()
    message_received(
        {"role":"user","content":message.message},
        message.address, agent)
    run_agent(agent)


@app.post("/start_conversation")
def start():
    print( '\033[91m'+"Searching for Candidates..." + '\033[0m')
    time.sleep(5)
    print( '\033[95m'+"Starting Candidate Evaluation." + '\033[0m')
    print()
    run_agent(agent)


if __name__=="__main__":
    print('\033[92m' + "Candidate Agent Ready." + '\033[0m')
    parser = argparse.ArgumentParser(
            prog='Create Simple Agent on AgentNet',
            description='This Program starts a simple agent on the AgentNet Network.',
            epilog='')
    parser.add_argument('-sp', '--systemprompt',required=True,help="Text file with system prompt.")
    parser.add_argument('-d', '--datafile',required=True,help="Text file with other relevant data.")
    parser.add_argument('-a', '--address',required=True,help="Address of the other agent to contact.")
    parser.add_argument('-p', '--port',required=True,type=int, help="port to open for server.")
    
    args = parser.parse_args()

    agent = create_agent(args.systemprompt, args.datafile, args.address, args.port)
    uvicorn.run(app, port = args.port, log_level="error")
