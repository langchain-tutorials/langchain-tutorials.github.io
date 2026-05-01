---
title: "LangChain Streaming Responses in Production with FastAPI & WebSockets (Full Guide)"
description: "Learn to implement LangChain streaming responses in production using FastAPI and WebSockets. This full guide covers everything for efficient, real-time AI."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain streaming responses in production]
featured: false
image: '/assets/images/langchain-streaming-fastapi-websockets-guide.webp'
---

## Bringing Your AI Chatbots to Life: LangChain Streaming Responses in Production with FastAPI & WebSockets

Imagine asking a question to an AI, and instead of waiting a long time for the full answer, you see the words appear one by one, almost like someone typing in real-time. This is called streaming, and it makes AI applications feel much faster and more engaging. It's a game-changer for user experience.

Today, we're going to explore how to build these kinds of smart, real-time AI applications. We will learn how to use LangChain for generating AI responses, FastAPI for building a super-fast web server, and WebSockets for keeping that real-time connection alive. By the end, you'll know exactly how to deploy LangChain streaming responses in production.

### What is Streaming and Why Does It Matter for AI?

Think about watching a video online. You don't download the whole movie before it starts playing, right? Instead, pieces of the video arrive continuously, and your player shows them as they come. This is streaming!

In the world of AI, especially with large language models, it means you get bits of the AI's answer as it thinks, rather than waiting for the entire reply. This makes the AI feel much quicker and more responsive. You can start reading the answer right away, improving how you interact with the system.

This approach is super important when you want your AI tools to feel natural and immediate. Waiting several seconds for a full AI response can be frustrating for users. Streaming fixes this by making the interaction smoother and more interactive.

### The Magic of LangChain for Streaming AI Answers

LangChain is a fantastic toolkit that helps you build powerful applications with language models. It makes it easy to connect different AI parts together. One of its best features is built-in support for streaming.

This means you don't have to invent complex ways to get partial answers from your AI model. LangChain handles this for you, letting you focus on what your AI should do. It turns a long wait into a dynamic conversation.

You can set up LangChain to work with many different AI models, like OpenAI's GPT or Google Gemini. When you ask LangChain to stream, it will deliver tokens, which are small pieces of text, one after another. This is key for achieving LangChain streaming responses in production.

#### Simple LangChain Streaming Example

Let's see a basic example of how LangChain streams responses directly in Python. We'll use a simple language model for this. This snippet shows how to get an instant stream of tokens.

First, you need to install LangChain and a model provider like OpenAI.

{% raw %}
```bash
pip install langchain-openai python-dotenv
```
{% endraw %}

Now, here's how you can make a simple LangChain chain stream.

{% raw %}
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Make sure you have your OpenAI API key set as an environment variable
# os.environ["OPENAI_API_KEY"] = "your-api-key"

def run_simple_langchain_stream():
    model = ChatOpenAI(temperature=0, streaming=True)
    prompt = ChatPromptTemplate.from_template("Tell me a long story about {topic}.")
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    print("Starting stream...")
    for chunk in chain.stream({"topic": "a brave knight and a dragon"}):
        print(chunk, end="", flush=True)
    print("\nStream finished.")

if __name__ == "__main__":
    run_simple_langchain_stream()
```
{% endraw %}

In this code, the `for chunk in chain.stream(...)` part is where the magic happens. LangChain sends us small pieces of the story as it's generated. This is what we want to send to your users in real-time.

### FastAPI: Your Speedy Server for AI Applications

FastAPI is a modern, fast (hence the name!), and easy-to-use web framework for building APIs with Python. It's built on top of standard Python type hints, which makes your code more robust and easier to understand. If you're building an API to serve your AI models, FastAPI is an excellent choice.

It's super efficient, especially for handling many requests at once, thanks to its asynchronous capabilities. This is vital when you're looking to serve LangChain streaming responses in production. FastAPI lets you write `async` and `await` code easily, which is perfect for tasks that involve waiting, like getting responses from an AI model or a database.

FastAPI is perfect for `FastAPI streaming` data because it natively supports `StreamingResponse`. This allows you to send data back to the client as it becomes available. This is crucial for making your AI applications feel instant and responsive.

#### Setting Up FastAPI

First, you need to install FastAPI and an ASGI server like Uvicorn. Uvicorn is what runs your FastAPI application.

{% raw %}
```bash
pip install fastapi uvicorn
```
{% endraw %}

Now, let's create a very basic FastAPI application.

{% raw %}
```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
{% endraw %}

You can run this simple app using `python main.py` and then visit `http://127.0.0.1:8000` in your web browser. You'll see the "Hello from FastAPI!" message. This is the foundation for our more complex AI streaming API.

### WebSocket Integration: The Two-Way Street for Real-time Chat

Imagine talking to someone on a walkie-talkie versus sending letters back and forth. A walkie-talkie allows for instant, two-way communication, right? That's what WebSockets are for your web applications! Unlike traditional HTTP requests, where you send a request and get one response, WebSockets open a continuous, open connection.

This "open line" allows both the client (your web browser or app) and the server (our FastAPI application) to send messages to each other at any time. This makes `WebSocket integration` perfect for applications that need real-time updates, like chat applications, online games, or, in our case, streaming AI responses. You get updates as soon as they are ready, without needing to constantly ask the server "Is it ready yet?".

WebSockets are especially useful when you need bidirectional communication. For simpler streaming, where the server just sends data to the client, Server-Sent Events (SSE) might be enough. However, for interactive chatbots where the client also sends follow-up questions in the middle of a stream, WebSockets are superior.

#### FastAPI and WebSockets

FastAPI makes it incredibly easy to set up `WebSocket integration`. You can define a WebSocket endpoint just like a regular API endpoint. FastAPI handles all the complicated handshake stuff behind the scenes. This allows you to focus on sending and receiving messages.

Here's a basic WebSocket server setup in FastAPI. This example will echo back whatever the client sends it.

{% raw %}
```python
# websocket_server.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from client: {data}")
            await manager.send_personal_message(f"Message text was: {data}", websocket)
            # You could also broadcast:
            # await manager.broadcast(f"Client # says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
{% endraw %}

To test this, you would need a small JavaScript client in an HTML file.

{% raw %}
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Client</title>
</head>
<body>
    <h1>WebSocket Test</h1>
    <input type="text" id="messageInput" placeholder="Type a message">
    <button onclick="sendMessage()">Send</button>
    <div id="messages"></div>

    <script>
        const ws = new WebSocket("ws://localhost:8000/ws");
        const messagesDiv = document.getElementById("messages");
        const messageInput = document.getElementById("messageInput");

        ws.onopen = (event) => {
            messagesDiv.innerHTML += "<p>Connected to WebSocket!</p>";
        };

        ws.onmessage = (event) => {
            messagesDiv.innerHTML += `<p>Server: ${event.data}</p>`;
        };

        ws.onclose = (event) => {
            messagesDiv.innerHTML += "<p>Disconnected from WebSocket.</p>";
        };

        ws.onerror = (error) => {
            messagesDiv.innerHTML += `<p style="color:red;">WebSocket Error: ${error.message}</p>`;
        };

        function sendMessage() {
            const message = messageInput.value;
            if (message) {
                ws.send(message);
                messagesDiv.innerHTML += `<p>Client: ${message}</p>`;
                messageInput.value = '';
            }
        }
    </script>
</body>
</html>
```
{% endraw %}

Save the server code as `websocket_server.py` and run it with `python websocket_server.py`. Then, save the HTML code as `index.html` and open it in your web browser. You can now send messages from the HTML page, and the FastAPI server will echo them back! This is the foundation for our powerful `WebSocket integration`.

### Integrating LangChain Streaming into FastAPI WebSockets

Now comes the exciting part: bringing LangChain's streaming capabilities into our FastAPI WebSocket setup. We want to send each chunk of the AI's response through the WebSocket connection to the user. This is how you achieve LangChain streaming responses in production environments.

The key is to create an asynchronous generator in Python that yields the chunks from LangChain. Then, our WebSocket handler will loop through this generator and send each piece to the connected client. This setup fully leverages `async APIs` for efficient non-blocking operations.

#### Building Our LangChain Chatbot with WebSocket Streaming

Let's combine everything to create a real-time chatbot.

First, make sure you have LangChain and FastAPI installed. You'll also need `langchain-openai` for the example.

{% raw %}
```bash
pip install fastapi uvicorn langchain-openai python-dotenv
```
{% endraw %}

Here's the FastAPI application that orchestrates LangChain streaming over WebSockets.

{% raw %}
```python
# main_chatbot.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
import os

app = FastAPI()

# Make sure you have your OpenAI API key set as an environment variable
# os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"Client connected: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Client disconnected: {websocket.client}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

# LangChain setup for streaming
def get_langchain_chain() -> Runnable:
    model = ChatOpenAI(temperature=0.7, streaming=True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Respond concisely."),
        ("user", "{question}")
    ])
    output_parser = StrOutputParser()
    chain = prompt | model | output_parser
    return chain

async def stream_langchain_response(question: str) -> AsyncGenerator[str, None]:
    """Asynchronously streams chunks from a LangChain chain."""
    chain = get_langchain_chain()
    async for chunk in chain.astream({"question": question}):
        yield chunk
    
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await manager.send_personal_message("Hello! I'm your AI assistant. Ask me anything!", websocket)
    try:
        while True:
            # Client sends a message (question)
            data = await websocket.receive_text()
            print(f"Received question from client: {data}")
            
            # Start streaming LangChain response
            await manager.send_personal_message("AI: ", websocket) # Prefix for AI's response
            async for chunk in stream_langchain_response(data):
                await manager.send_text(chunk) # Send each chunk
                
            await manager.send_personal_message(" ", websocket) # Add a newline or separator after AI response
            print("Finished streaming response.")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("Client disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")
        await manager.send_personal_message(f"An error occurred: {e}", websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```
{% endraw %}

To test this, modify the `index.html` from before to connect to `/ws/chat`:

{% raw %}
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>LangChain WebSocket Chatbot</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        #chatbox { border: 1px solid #ccc; padding: 10px; height: 400px; overflow-y: scroll; margin-bottom: 10px; }
        .user-message { color: blue; }
        .ai-message { color: green; }
    </style>
</head>
<body>
    <h1>LangChain AI Chatbot</h1>
    <div id="chatbox"></div>
    <input type="text" id="messageInput" placeholder="Type your question here...">
    <button onclick="sendMessage()">Send</button>

    <script>
        const ws = new WebSocket("ws://localhost:8000/ws/chat");
        const chatbox = document.getElementById("chatbox");
        const messageInput = document.getElementById("messageInput");

        let currentAIMessageElement = null;

        ws.onopen = (event) => {
            chatbox.innerHTML += "<p><em>Connected to AI chatbot!</em></p>";
        };

        ws.onmessage = (event) => {
            const message = event.data;
            if (message.startsWith("Hello! I'm your AI assistant") || message.startsWith("An error occurred")) {
                chatbox.innerHTML += `<p class="ai-message">${message}</p>`;
            } else if (message.startsWith("AI: ")) {
                // This is the start of a new AI response, create a new paragraph
                currentAIMessageElement = document.createElement("p");
                currentAIMessageElement.className = "ai-message";
                currentAIMessageElement.textContent = message; // Add the prefix
                chatbox.appendChild(currentAIMessageElement);
            } else if (message.trim() === "") {
                 // End of AI stream, reset currentAIMessageElement
                 currentAIMessageElement = null;
            }
            else {
                // Append subsequent chunks to the current AI message
                if (currentAIMessageElement) {
                    currentAIMessageElement.textContent += message;
                } else {
                    // Fallback, if somehow a chunk arrives without a prefix
                    chatbox.innerHTML += `<p class="ai-message">${message}</p>`;
                }
            }
            chatbox.scrollTop = chatbox.scrollHeight; // Scroll to bottom
        };

        ws.onclose = (event) => {
            chatbox.innerHTML += "<p><em>Disconnected from AI chatbot.</em></p>";
        };

        ws.onerror = (error) => {
            chatbox.innerHTML += `<p style="color:red;"><em>WebSocket Error: ${error.message}</em></p>`;
        };

        function sendMessage() {
            const message = messageInput.value;
            if (message) {
                ws.send(message);
                chatbox.innerHTML += `<p class="user-message">You: ${message}</p>`;
                messageInput.value = '';
            }
            chatbox.scrollTop = chatbox.scrollHeight; // Scroll to bottom
        }

        messageInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                sendMessage();
            }
        });
    </script>
</body>
</html>
```
{% endraw %}

Run `python main_chatbot.py`, then open `index.html` in your browser. You now have a real-time AI chatbot using LangChain streaming responses in production! Notice how the AI's answer appears word by word. This is a powerful demonstration of `WebSocket integration`.

### Handling Errors and Making Your Production System Robust

When you put your application into production, things can go wrong. It's important to prepare for this. Error handling makes your application reliable and user-friendly.

For our LangChain streaming setup, we need to consider network issues, AI model errors, and unexpected disconnections. FastAPI helps with handling exceptions, and WebSockets have their own disconnection events. You must gracefully handle these events to ensure your `async APIs` stay available.

#### Strategies for Robustness:

1.  **Try-Except Blocks:** Wrap your LangChain calls and WebSocket send/receive operations in `try...except` blocks. This catches errors before they crash your application.
2.  **Graceful Disconnection:** The `WebSocketDisconnect` exception in FastAPI is designed for this. Use it to clean up resources when a client leaves.
3.  **Client-Side Reconnection Logic:** Your JavaScript client should also try to reconnect if the WebSocket connection drops. This makes for a more resilient user experience.
4.  **Logging:** Log important events and errors. This helps you understand what's happening when something goes wrong in production.
5.  **Timeouts:** Implement timeouts for AI model calls to prevent your application from hanging indefinitely if the model is slow or unresponsive.

Let's enhance our WebSocket endpoint with more robust error handling.

{% raw %}
```python
# main_chatbot_robust.py (excerpt of the websocket_endpoint function)
# ... (imports and ConnectionManager are the same as before) ...

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await manager.send_personal_message("Hello! I'm your AI assistant. Ask me anything!", websocket)
        while True:
            try:
                data = await websocket.receive_text()
                print(f"Received question from client: {data}")

                await manager.send_personal_message("AI: ", websocket)
                
                # Use a specific error message if LangChain streaming fails
                stream_failed = False
                try:
                    async for chunk in stream_langchain_response(data):
                        await manager.send_text(chunk)
                except Exception as e:
                    print(f"Error during LangChain streaming: {e}")
                    await manager.send_personal_message(f"Oops! The AI encountered an error while responding. Please try again or rephrase.", websocket)
                    stream_failed = True
                
                if not stream_failed:
                    await manager.send_personal_message(" ", websocket) # Separator
                    print("Finished streaming response.")

            except WebSocketDisconnect:
                # This is handled by the outer try-except, but good to know it exists here
                raise # Re-raise to be caught by the outer block

            except Exception as e:
                # Catching other potential issues during message reception/processing
                print(f"Error processing client message: {e}")
                await manager.send_personal_message(f"An internal error occurred: {e}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client {websocket.client} disconnected gracefully.")
    except Exception as e:
        print(f"Unexpected error with client {websocket.client}: {e}")
        # Optionally try to send an error message before closing connection
        try:
            await manager.send_personal_message(f"A severe server error occurred. Please refresh.", websocket)
        except RuntimeError:
            # Client might already be gone
            pass
```
{% endraw %}

This updated `websocket_endpoint` is more robust. It differentiates between client disconnects and other errors. It also provides feedback to the user if something goes wrong during the AI's response generation. These practices are essential for keeping LangChain streaming responses in production stable.

### Scaling Your Streaming AI with FastAPI and WebSockets

When your application becomes popular, you'll have many users asking questions at the same time. You need your system to handle this without slowing down. This is called scalability. FastAPI and WebSockets are excellent choices for building scalable `async APIs`.

FastAPI's asynchronous nature means it can handle many connections concurrently. While one AI model is generating a response, FastAPI can be busy receiving questions from other users. This prevents bottlenecks.

#### Tips for Scaling in Production:

1.  **Asynchronous Everything:** Ensure all I/O-bound operations (like talking to the AI model, databases) are `async/await`. This prevents blocking the event loop.
2.  **Uvicorn Workers:** Use multiple Uvicorn workers. This allows your FastAPI application to run multiple Python processes, each handling requests. You can typically run `uvicorn main:app --workers 4`.
3.  **Load Balancers:** Put a load balancer in front of multiple FastAPI instances. This distributes incoming requests evenly across your servers.
4.  **External AI Services:** Rely on cloud AI services (like OpenAI, Google Gemini) which are themselves highly scalable. Your FastAPI app just needs to make requests to them.
5.  **Monitoring:** Keep an eye on your server's CPU, memory, and network usage. This helps you spot problems before they affect users.
6.  **LangChain Cache:** For RAG applications or chains with repeated steps, consider using LangChain's caching mechanisms to avoid re-computing results. This can significantly speed up responses.

When building `async APIs` for LangChain streaming responses in production, thinking about scalability from the start will save you a lot of headaches later.

### Advanced Use Cases and Optimizations for Streaming

The power of LangChain streaming doesn't stop at simple chat. You can use it for more complex AI applications, like agents that can use tools or sophisticated Retrieval Augmented Generation (RAG) systems.

#### Streaming with LangChain Agents

LangChain Agents can decide what to do next, like searching the web or using a calculator, before giving you an answer. You can still stream their thought process and final response. Imagine seeing an agent think aloud in real-time! This provides transparency and a more dynamic user experience. For more on building agents, check out [LangChain Google Gemini Function Calling Agent Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}) or [LangGraph StateGraph Multi-step AI Agent]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

#### Streaming with RAG Applications

RAG applications combine an AI model with your own data (like documents or articles) to give more informed answers. When streaming, the AI can start answering while it's still processing or retrieving more information. This means users don't have to wait for the entire RAG process to complete. You can learn more about RAG with LangChain in [Build RAG Applications LangChain Vector Store 2026]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).

#### Custom Streaming Callbacks

LangChain allows you to create custom callbacks that run at different stages of your chain. You can use these to send more detailed information over your WebSocket, not just the final text chunks. For example, you could send updates when an agent starts a tool, finishes a step, or when a document is retrieved in a RAG system. This gives you fine-grained control over the `FastAPI streaming` output. To explore custom output handling, see [LangChain Custom Output Parser Tutorial]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}).

#### Example: Streaming Agent Thoughts

Imagine an agent that needs to search for information. You could stream not just its final answer, but also messages like "Thinking...", "Searching the web for X...", "Found results...". This keeps the user engaged even during complex operations.

To implement this, you would use LangChain's `StreamingStdOutCallbackHandler` or create a custom `BaseCallbackHandler` that sends messages to your WebSocket.

{% raw %}
```python
# Part of an agent setup, showing a custom callback for WebSocket
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List, Union
from uuid import UUID

class WebSocketCallbackHandler(BaseCallbackHandler):
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.full_response = ""

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        # Send each token as it arrives
        await self.websocket.send_text(token)
        self.full_response += token

    async def on_chain_start(self, serialized: Dict[str, Any], *, run_id: UUID, parent_run_id: Union[UUID, None] = None, tags: Union[List[str], None] = None, metadata: Union[Dict[str, Any], None] = None, **kwargs: Any) -> Any:
        # Inform the client that a chain is starting
        await self.websocket.send_text("SYSTEM: AI Chain started...\n")

    async def on_tool_start(self, serialized: Dict[str, Any], input_str: str, *, run_id: UUID, parent_run_id: Union[UUID, None] = None, tags: Union[List[str], None] = None, metadata: Union[Dict[str, Any], None] = None, **kwargs: Any) -> Any:
        # Inform the client when a tool is being used
        await self.websocket.send_text(f"SYSTEM: Using tool '{serialized.get('name')}' with input: '{input_str}'\n")

    async def on_tool_end(self, output: Any, *, run_id: UUID, parent_run_id: Union[UUID, None] = None, tags: Union[List[str], None] = None, **kwargs: Any) -> Any:
        # Inform the client when a tool finishes
        await self.websocket.send_text(f"SYSTEM: Tool finished with output: '{output}'\n")

# To use this:
# from langchain.agents import AgentExecutor, create_react_agent
# from langchain_community.tools import Tool
# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import PromptTemplate
#
# model = ChatOpenAI(temperature=0, streaming=True)
# tools = [
#     Tool(
#         name="Calculator",
#         func=lambda x: str(eval(x)),
#         description="Useful for when you need to answer questions about math."
#     )
# ]
# prompt = PromptTemplate.from_template("Answer the following questions as best you can. You have access to the following tools:\n\n{tools}\n\nUse the following format:\n\nQuestion: the input question you must answer\nThought: you should always think about what to do\nAction: the action to take, should be one of [{tool_names}]\nAction Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\nThought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\nBegin!\n\nQuestion: {input}\nThought:{agent_scratchpad}")
#
# agent = create_react_agent(model, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False) # verbose=False because we're handling output with callback
#
# # In your websocket_endpoint, you would pass the callback handler:
# # async def websocket_endpoint(websocket: WebSocket):
# #     ...
# #     callback = WebSocketCallbackHandler(websocket)
# #     async for chunk in agent_executor.astream({"input": data}, config={"callbacks": [callback]}):
# #         # The callback handler already sends the tokens, so this part might be for final result or specific parts
# #         # You might process chunks differently here if the callback only sends 'system' messages.
# #         pass
# #     ...
```
{% endraw %}

This example shows how `async APIs` can be used to send rich, real-time feedback from complex LangChain operations. This enhances the user experience, especially for tasks where the AI might take a moment to process.

### Conclusion: Real-time AI is Here to Stay

You've learned how to bring the exciting world of real-time AI to your users. By combining the power of LangChain for smart AI responses, FastAPI for a speedy and efficient server, and WebSockets for constant, two-way communication, you can build incredible applications. Deploying `LangChain streaming responses in production` is not just possible; it's a fantastic way to make your AI tools more engaging and user-friendly.

Remember, the goal is to make AI feel less like a waiting game and more like a conversation. With the techniques covered today, you are well-equipped to build production-ready systems that offer a seamless and interactive AI experience. Start building, experimenting, and bringing your AI ideas to life with `FastAPI streaming` and robust `WebSocket integration`!