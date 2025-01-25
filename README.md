# AI Chatbot and Web Scraper 

## Overview
This project features an AI-powered chatbot with message queuing and a custom web scraper, demonstrating web communication and content extraction.

## Project Components

### 1. Chatbot (task1.ipynb and task1.py)
- Utilizes LangChain and Ollama for conversational AI
- WebSocket-based communication 
- Processes inputs sequentially to manage multiple messages
- Uses DeepSeek R1 1.5B language model

#### Key Dependencies
- langchain
- ollama
- websockets

### 2. Web Interface (UI_task1.html)
- Tailwind CSS-styled chat interface
- WebSocket integration
- Real-time messaging
- Message queuing mechanism

### 3. Web Scraper (webscraper.py)
- Custom web scraping without external libraries
- HTTP/HTTPS support
- Heading and paragraph extraction

## Installation

### Prerequisites
- Python 3.8+
- Ollama
- WebSocket-compatible browser

### Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install langchain websockets
   pip install -U ollama
   ```
3. Install Ollama and pull DeepSeek R1 model

## Running the Project

### Option 1: Interactive Notebook
- Open `task1.ipynb`
- Run cells using Shift+Enter

### Option 2: WebSocket Server + Web Interface
1. Start WebSocket server:
   ```bash
   python task1.py
   ```
2. Open `UI_task1.html` using Live Server
   - Connects to backend on port 8765

## Demo
[View Project Demo on YouTube](https://youtube.com/your-demo-link)
