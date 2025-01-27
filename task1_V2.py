from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
load_dotenv()
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import HuggingFacePipeline
from transformers import pipeline

app = Flask(__name__)

# Load the environment variable for HF_TOKEN
HF_TOKEN = os.getenv('HF_TOKEN')

# Initialize model and tokenizer
device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save locally
local_model_path = "my_local_model"
model.save_pretrained(local_model_path)
tokenizer.save_pretrained(local_model_path)

local_tokenizer = AutoTokenizer.from_pretrained(local_model_path)
local_model = AutoModelForCausalLM.from_pretrained(local_model_path).to(device)

# LangChain setup
hf_pipeline = pipeline("text-generation", model=local_model, tokenizer=local_tokenizer, device=0 if torch.cuda.is_available() else -1)
llm = HuggingFacePipeline(pipeline=hf_pipeline)
conversation_memory = ConversationBufferMemory(memory_key="history")
chatbot = ConversationChain(memory=conversation_memory, llm=llm)

def chat_with_bot(user_input):
    response = chatbot.predict(input=user_input)
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    if user_input.lower() in ["quit", "bye"]:
        return render_template('index.html', message="Goodbye!")
    
    bot_response = chat_with_bot(user_input)
    return render_template('index.html', user_input=user_input, bot_response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)
