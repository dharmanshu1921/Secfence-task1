import asyncio
import websockets
import json
import logging
import re
from langchain_ollama import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

system_prompt = "you are an AI assistant, just answer the query of user in minimum words possible and keep it crisp. Do not show any internal thinking process."

custom_prompt = PromptTemplate(
    input_variables=["history", "input"], 
    template=f"{system_prompt}\n\nCurrent conversation:\n{{history}}\nHuman: {{input}}\nAI:"
)

llm = ChatOllama(
    model="deepseek-r1:1.5b",
    max_tokens=200, 
    temperature=0.2
)

conversation = ConversationChain(
    llm=llm,
    verbose=False,
    memory=ConversationBufferMemory(),
    prompt=custom_prompt
)

def clean_response(response):
    cleaned = re.sub(r'<think>.*?</think>\s*', '', response, flags=re.DOTALL)
    return cleaned.strip()

async def handle_websocket(websocket, path=None):
    try:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            user_input = data.get('message', '').strip()
            
            if not user_input:
                await websocket.send(json.dumps({'error': 'Empty input received'}))
                continue
            
            if user_input.lower() in ["quit", "bye"]:
                await websocket.send(json.dumps({'message': "Goodbye!"}))
                break
            
            try:
                response = conversation.predict(input=user_input)
                cleaned_response = clean_response(response)
                await websocket.send(json.dumps({'message': cleaned_response}))
            except Exception as e:
                logger.error(f"Prediction error: {e}")
                await websocket.send(json.dumps({'error': 'An error occurred during processing'}))
    
    except websockets.exceptions.ConnectionClosed:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

async def main():
    server = await websockets.serve(handle_websocket, "localhost", 8765)
    logger.info("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())