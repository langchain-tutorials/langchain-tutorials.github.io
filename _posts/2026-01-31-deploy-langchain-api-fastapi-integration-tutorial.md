---
title: "Deploy LangChain API: FastAPI Integration Tutorial with Examples"
description: "Master LangChain API deployment using FastAPI! This essential tutorial provides practical examples for robust integration and production readiness."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [deploy langchain api fastapi tutorial]
featured: false
image: '/assets/images/deploy-langchain-api-fastapi-integration-tutorial.webp'
---

## Make Your AI Smart: Build a LangChain API with FastAPI!

Hey there! Have you ever wanted to build your own smart helper that can answer questions or write stories, and then share it with others? Well, today you're going to learn how to do just that. We'll show you how to take a powerful AI tool called LangChain and make it available as an API using FastAPI.

This guide is like a recipe for making your smart AI tool accessible to any app. We'll cover everything from getting started to making sure your tool works perfectly. By the end, you'll have a working example of how to deploy LangChain API using this FastAPI tutorial.

### What is FastAPI and Why Use It?

Imagine you want to build a restaurant where people can order food. FastAPI is like a super-fast and easy way to build the kitchen and hire the waiters for your digital restaurant. It helps you create web APIs, which are like special doorways for different computer programs to talk to each other.

FastAPI is very quick and makes writing code simple. It automatically creates cool documentation for your API, so everyone knows how to use it. This makes it a great choice when you want to deploy LangChain API easily.

### What is LangChain and Why Use It?

Now, imagine you want your restaurant's waiter to be super smart. They should understand complex orders, suggest new dishes, or even tell stories while you wait. LangChain is like that smart brain for your AI projects.

LangChain helps you connect different powerful AI models, like the ones that understand human language. You can build cool tools that chat, summarize text, or answer questions. It's fantastic for making your AI projects smarter and more connected, especially when you deploy LangChain API for real-world use.

### Getting Ready: Your FastAPI Setup

Before we build our smart waiter, we need to set up our kitchen. This is where we will create our working area and install the tools we need. This section will guide you through the initial FastAPI setup.

First, you need Python installed on your computer. Python is the language we will use. You can get it from the [official Python website](https://www.python.org/downloads/).

#### Setting Up Your Project Folder

Let's make a new folder for our project. You can call it `langchain_fastapi_app`. Open your terminal or command prompt and type these commands:

```bash
mkdir langchain_fastapi_app
cd langchain_fastapi_app
```

Now you are inside your new project folder. This is where all your files will live.

#### Creating a Virtual Environment

It's a good idea to create a "virtual environment." Think of it as a clean, separate toolbox for your project. This prevents your project's tools from messing with other projects on your computer. Type this in your terminal:

```bash
python -m venv venv
```

This command creates a folder named `venv` inside your project folder. This `venv` folder contains your isolated Python environment.

#### Activating Your Virtual Environment

Now, you need to "activate" this toolbox so your computer knows to use its tools.

*   **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
*   **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```
When activated, you'll usually see `(venv)` at the beginning of your terminal prompt. This means you're using your isolated environment.

#### Installing FastAPI and Other Tools

With your virtual environment active, let's install the main tools. We need `fastapi` itself, `uvicorn` (which runs our FastAPI app), and `langchain` (our smart AI brain).

```bash
pip install fastapi uvicorn langchain openai
```

We also install `openai` because LangChain often uses models from OpenAI for its smart functions. If you want to use a different AI model, you might install a different package instead. Now your FastAPI setup is complete, and you're ready to write some code.

### Your First FastAPI App: Creating Endpoints

Let's start by building a very simple FastAPI app. This will be like setting up a single ordering counter in our digital restaurant. We'll learn about creating endpoints, which are like specific menu items people can request.

Create a new file called `main.py` inside your `langchain_fastapi_app` folder.

#### A Simple "Hello" Endpoint

Open `main.py` and put this code inside:

```python
# main.py
from fastapi import FastAPI

# Create a FastAPI app instance
app = FastAPI()

# Define a simple endpoint
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

Here's what this code does:
*   `from fastapi import FastAPI`: We bring in the FastAPI tool.
*   `app = FastAPI()`: We create our FastAPI application.
*   `@app.get("/")`: This tells FastAPI to run the `read_root` function when someone visits the main web address (`/`). This is an example of creating endpoints.
*   `def read_root():`: This is our function that runs when the endpoint is hit.
*   `return {"message": "Hello, FastAPI!"}`: It sends back a message.

#### Running Your FastAPI App

To see this working, go back to your terminal (with the virtual environment active!) and type:

```bash
uvicorn main:app --reload
```

*   `uvicorn main:app`: This tells Uvicorn to run the `app` object from your `main.py` file.
*   `--reload`: This is super helpful! If you change your code, Uvicorn will automatically restart the server.

You should see something like this in your terminal:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Now, open your web browser and go to `http://127.0.0.1:8000`. You should see the message: `{"message": "Hello, FastAPI!"}`. Congratulations, you've made your first FastAPI endpoint!

### Building with Async Route Handlers and Request/Response Models

Now, let's make our FastAPI app a bit more complex, like taking a more detailed order. We'll use `async` functions for better performance and define what kind of information we expect to receive and send back. This involves `async route handlers` and `request/response models`.

#### Understanding Asynchronous Code

In simple terms, `async` (asynchronous) code means your program can do other things while it's waiting for one task to finish. Imagine our smart waiter taking an order from one customer, and while the kitchen is making that food, the waiter can take another order from a different customer, instead of just standing still and waiting. This is great for an API that might talk to slow external services, like an AI model.

#### Using Request and Response Models with Pydantic

To make sure everyone sends and receives the right kind of information, we use `request/response models`. These models are like pre-printed order forms. They define exactly what details an order should have and what details the kitchen will send back. FastAPI uses a library called Pydantic for this, which makes it super easy.

Let's update `main.py`:

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a request model for what we expect to receive
class MessageRequest(BaseModel):
    message: str
    user_name: str = "Guest" # Default value

# Define a response model for what we will send back
class MessageResponse(BaseModel):
    greeting: str
    length_of_message: int

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/greet")
async def create_greeting(request: MessageRequest) -> MessageResponse:
    """
    Greets the user and provides information about their message.
    This is an async route handler.
    """
    full_message = f"Hello, {request.user_name}! You said: '{request.message}'"
    msg_length = len(request.message)
    return MessageResponse(greeting=full_message, length_of_message=msg_length)

```

Let's break down the new parts:

*   `from pydantic import BaseModel`: We import `BaseModel` to create our data forms.
*   `class MessageRequest(BaseModel):`: This is our incoming order form. It says we expect a `message` (which must be text) and an optional `user_name` (also text, defaulting to "Guest").
*   `class MessageResponse(BaseModel):`: This is our outgoing confirmation slip. It says we will send back a `greeting` (text) and `length_of_message` (a whole number).
*   `@app.post("/greet")`: This creates a new endpoint. `@app.post` means we expect data to be "posted" (sent) to this address.
*   `async def create_greeting(request: MessageRequest) -> MessageResponse:`:
    *   `async def`: This tells Python this is an `async route handler`.
    *   `request: MessageRequest`: This tells FastAPI to expect data that matches our `MessageRequest` model. FastAPI automatically checks if the incoming data is correct.
    *   `-> MessageResponse`: This tells FastAPI what kind of data our function will send back.
*   Inside the function, we use the `request` object to get the message and user name, then create our response.

If your Uvicorn server is still running with `--reload`, it would have restarted automatically. Now, go to `http://127.0.0.1:8000/docs`. You will see amazing interactive documentation generated by FastAPI! You can try out your new `/greet` endpoint right there.

For example, you can send:
```json
{
  "message": "What a lovely day!",
  "user_name": "Alice"
}
```
And you'll get back:
```json
{
  "greeting": "Hello, Alice! You said: 'What a lovely day!'",
  "length_of_message": 19
}
```
This shows how easy it is to manage data using `request/response models` in FastAPI.

### Making AI Smart: LangChain Integration

Now for the exciting part: bringing our smart AI helper, LangChain, into our FastAPI app! This is where we truly begin to deploy LangChain API. We'll set up a simple LangChain pipeline to answer questions.

#### Setting Up Your OpenAI API Key

LangChain often uses AI models from OpenAI. To use them, you need an API key from OpenAI. If you don't have one, visit [OpenAI's website](https://platform.openai.com/account/api-keys) to get yours. Keep this key secret!

The best way to use your API key is to put it in an environment variable. This means your code won't directly show the key.
In your terminal (with `venv` activated):

*   **On Windows (for current session):**
    ```bash
    set OPENAI_API_KEY="your_openai_api_key_here"
    ```
*   **On macOS/Linux (for current session):**
    ```bash
    export OPENAI_API_KEY="your_openai_api_key_here"
    ```
Replace `"your_openai_api_key_here"` with your actual key. For permanent setup, you might add this to your system's environment variables or use a `.env` file and `python-dotenv`.

#### Integrating a Simple LangChain Model

Let's modify `main.py` again. We will add a new endpoint that takes a question and uses LangChain to get an answer. This is our core LangChain integration.

```python
# main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = FastAPI()

# --- Pydantic Models (from previous section) ---
class MessageRequest(BaseModel):
    message: str
    user_name: str = "Guest"

class MessageResponse(BaseModel):
    greeting: str
    length_of_message: int

# New models for LangChain integration
class LangChainQuestionRequest(BaseModel):
    question: str

class LangChainAnswerResponse(BaseModel):
    answer: str
    source: str = "LangChain OpenAI Model"

# --- LangChain Setup ---
# Check if API key is set
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it to your OpenAI API key.")

# Initialize OpenAI LLM
llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)

# Create a simple prompt template for our Q&A
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful AI assistant. Answer the following question:\n{question}"
)

# Create a simple LLMChain
qa_chain = LLMChain(llm=llm, prompt=prompt_template)


# --- FastAPI Endpoints ---
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/greet")
async def create_greeting(request: MessageRequest) -> MessageResponse:
    full_message = f"Hello, {request.user_name}! You said: '{request.message}'"
    msg_length = len(request.message)
    return MessageResponse(greeting=full_message, length_of_message=msg_length)

@app.post("/ask_ai", response_model=LangChainAnswerResponse)
async def ask_ai(request: LangChainQuestionRequest):
    """
    Takes a question and uses LangChain with an OpenAI model to get an answer.
    This demonstrates LangChain integration.
    """
    try:
        # Run the LangChain QA chain
        # The 'run' method directly takes the input variable for simple chains
        ai_answer = await qa_chain.arun(request.question) # Use arun for async execution
        return LangChainAnswerResponse(answer=ai_answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting AI answer: {str(e)}")

```

Let's break down the new LangChain integration parts:

*   `import os`: We need this to get our `OPENAI_API_KEY` from the environment.
*   `from langchain.llms import OpenAI`: Imports the OpenAI language model from LangChain.
*   `from langchain.prompts import PromptTemplate`: Imports `PromptTemplate` to define how we talk to the AI.
*   `from langchain.chains import LLMChain`: Imports `LLMChain` to link our model and prompt.
*   **API Key Check**: We safely get the `OPENAI_API_KEY` and raise an error if it's missing.
*   `llm = OpenAI(...)`: We create an instance of the OpenAI language model. `temperature` controls how creative the AI is (0 is very factual, higher is more creative).
*   `prompt_template = PromptTemplate(...)`: We define a simple instruction for the AI. We tell it to be a helpful assistant and then insert the user's `question`.
*   `qa_chain = LLMChain(llm=llm, prompt=prompt_template)`: We combine the `llm` (the brain) and the `prompt_template` (the instruction) into a `chain`. This is our simple LangChain pipeline.
*   `@app.post("/ask_ai", response_model=LangChainAnswerResponse)`: We create a new `POST` endpoint for our AI questions. It uses `LangChainQuestionRequest` for input and `LangChainAnswerResponse` for output.
*   `ai_answer = await qa_chain.arun(request.question)`: This is where we run our LangChain. `arun` is the asynchronous version of `run`, fitting nicely with our `async def` FastAPI endpoint. It sends the user's `question` to our `qa_chain` and waits for the AI's `answer`.
*   `return LangChainAnswerResponse(answer=ai_answer)`: We return the AI's answer using our defined response model.
*   **Error Handling**: We added a `try...except` block to catch any issues when talking to the AI and return a helpful error message.

Restart your `uvicorn` server if it didn't reload automatically. Go to `http://127.0.0.1:8000/docs` again. You'll now see the `/ask_ai` endpoint. Try it out!

Send a request like:
```json
{
  "question": "What is the capital of France?"
}
```
You should get an answer like:
```json
{
  "answer": "The capital of France is Paris.",
  "source": "LangChain OpenAI Model"
}
```
This is a core example of how you can deploy LangChain API, enabling interaction with powerful AI models through a simple web interface.

### Detailed API Documentation

One of FastAPI's best features is its automatic API documentation. This is like having a perfectly organized menu for your digital restaurant, explaining every dish (endpoint) and how to order it. This section focuses on `API documentation`.

FastAPI uses OpenAPI (formerly Swagger) to generate this documentation. You get two main interfaces automatically:

1.  **Swagger UI**: This is an interactive page where you can see all your endpoints, their expected inputs, and outputs. You can even try them out directly from the browser!
2.  **ReDoc**: This provides a more compact and readable documentation view, great for quickly browsing.

You don't need to write any extra code to get these. Just visiting specific URLs will show them.

#### Accessing Your API Documentation

When your FastAPI app is running (e.g., with `uvicorn main:app --reload`), you can open your web browser and go to:

*   **Swagger UI**: `http://127.0.0.1:8000/docs`
*   **ReDoc**: `http://127.0.0.1:8000/redoc`

Take some time to explore these pages. You'll see:
*   A list of all your endpoints (like `/`, `/greet`, `/ask_ai`).
*   The HTTP method for each (GET, POST).
*   Descriptions for each endpoint (from your function's docstrings, like the one for `ask_ai`).
*   The `request/response models` you defined (like `MessageRequest`, `LangChainQuestionRequest`), showing their fields and types.
*   Buttons to "Try it out" and send requests directly from the browser.

#### Enhancing Documentation with Metadata

You can add more details to your overall API documentation, like a title, description, or version number. This makes your documentation even more professional and helpful. You can do this when you create your `FastAPI` app instance.

Let's modify the `app = FastAPI()` line in `main.py`:

```python
# main.py
# ... (imports and existing code) ...

app = FastAPI(
    title="My Awesome LangChain API",
    description="A simple API to demonstrate LangChain integration with FastAPI. "
                "You can greet users or ask questions to an AI model.",
    version="1.0.0",
    contact={
        "name": "Your Name/Company",
        "url": "http://yourwebsite.com/contact",
        "email": "contact@yourwebsite.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# ... (rest of your code) ...
```

Save `main.py` and let Uvicorn reload. Now, visit `/docs` or `/redoc` again. You'll see your custom title, description, version, and contact info at the top. This extra information helps others understand your API better, making it truly ready to deploy LangChain API to a wider audience.

### Handling Cross-Origin Requests: CORS Configuration

Imagine your digital restaurant has a website where customers can place orders. But what if that website is on a different domain (like `my-cool-app.com`) than your API server (like `api.my-restaurant.com`)? Browsers have a security rule that usually stops these kinds of cross-domain requests. This rule is called "Cross-Origin Resource Sharing," or CORS. If you don't set it up, your website might not be able to talk to your API.

To allow your website (or any other frontend application) to talk to your FastAPI API, you need to set up `CORS configuration`. FastAPI provides a simple way to do this using `CORSMiddleware`.

#### Adding CORSMiddleware

Let's modify `main.py` to add CORS support. We'll add this right after we create the `FastAPI` app.

```python
# main.py
# ... (imports and existing code) ...
from fastapi.middleware.cors import CORSMiddleware # New import

app = FastAPI(
    title="My Awesome LangChain API",
    description="A simple API to demonstrate LangChain integration with FastAPI. "
                "You can greet users or ask questions to an AI model.",
    version="1.0.0",
    contact={
        "name": "Your Name/Company",
        "url": "http://yourwebsite.com/contact",
        "email": "contact@yourwebsite.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# --- CORS Configuration ---
# List of origins (domains) that are allowed to make requests to your API
origins = [
    "http://localhost",
    "http://localhost:8080", # Example for a Vue/React dev server
    "http://localhost:3000", # Another example for a React dev server
    "http://my-frontend-app.com", # Your actual frontend domain
    # You can also use "*" to allow all origins, but this is less secure for production.
    # It's better to list specific origins.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # List of allowed origins
    allow_credentials=True, # Allow cookies to be sent with requests
    allow_methods=["*"], # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allow all headers
)

# ... (rest of your code, including LangChain setup and endpoints) ...
```

Here's what we added for `CORS configuration`:

*   `from fastapi.middleware.cors import CORSMiddleware`: This imports the special tool for CORS.
*   `origins = [...]`: This is a list of all the websites (or "origins") that are allowed to talk to your API.
    *   `http://localhost` and `http://localhost:8080`, `http://localhost:3000` are common for local development.
    *   `http://my-frontend-app.com` would be your real website's address once deployed.
    *   **Important**: Using `allow_origins=["*"]` allows *any* website to access your API. While easy for development, this is generally **not recommended for production** because it's less secure. Always specify your actual frontend origins in a real application.
*   `app.add_middleware(...)`: This adds the `CORSMiddleware` to our FastAPI app. Middleware is like a gatekeeper that checks every request coming into your API before it reaches your endpoints.
    *   `allow_origins`: Set to our `origins` list.
    *   `allow_credentials=True`: If your frontend needs to send cookies or authorization headers with the requests, set this to `True`.
    *   `allow_methods=["*"]`: Allows all standard HTTP methods (GET, POST, PUT, DELETE, etc.). You could list specific methods if you prefer.
    *   `allow_headers=["*"]`: Allows all standard headers.

With this `CORS configuration` in place, any frontend application running on the domains listed in `origins` will be able to successfully make requests to your FastAPI and deploy LangChain API without encountering browser security errors. This is crucial for making your API usable by web applications.

### Enhancing Your API with Middleware Setup

We just saw `CORSMiddleware` as an example. Middleware in FastAPI is like a series of checkpoints that every request passes through before reaching your API endpoint, and every response passes through before being sent back to the user. It's a powerful way to add common functionalities to your API without repeating code in every endpoint. This section focuses on `middleware setup`.

Think of it this way: when you order food (make a request), it first goes to the entrance (middleware), then to the waiter (your endpoint), then back through the entrance (middleware) with your food (response).

Common uses for middleware include:
*   **Logging**: Recording details about every request (who, when, what).
*   **Authentication**: Checking if a user is logged in before letting them access certain parts.
*   **Rate Limiting**: Preventing too many requests from one user in a short time.
*   **CORS**: As we just saw, handling cross-origin requests.
*   **Response Compression**: Making responses smaller for faster delivery.

Let's add a simple logging middleware to our `main.py` to see `middleware setup` in action.

```python
# main.py
import time # New import for time tracking
import logging # New import for logging
# ... (other existing imports) ...
from fastapi.middleware.cors import CORSMiddleware

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="My Awesome LangChain API",
    description="A simple API to demonstrate LangChain integration with FastAPI. "
                "You can greet users or ask questions to an AI model.",
    version="1.0.0",
    contact={
        "name": "Your Name/Company",
        "url": "http://yourwebsite.com/contact",
        "email": "contact@yourwebsite.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# --- CORS Configuration (from previous section) ---
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://my-frontend-app.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Custom Logging Middleware Setup ---
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request) # This calls the actual route handler
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request: {request.method} {request.url.path} | Process Time: {process_time:.4f}s | Status: {response.status_code}")
    return response

# ... (rest of your code, including LangChain setup and endpoints) ...
```

Here's what we added for `middleware setup`:

*   `import time` and `import logging`: We need these for timing and logging messages.
*   `logging.basicConfig(...)` and `logger = ...`: Basic setup for our logger.
*   `@app.middleware("http")`: This is how you register your own custom middleware. `"http"` means it applies to all HTTP requests.
*   `async def add_process_time_header(request: Request, call_next):`:
    *   `request: Request`: FastAPI gives you the incoming request object.
    *   `call_next`: This is a special function that you *must* call. It passes the request to the next middleware in the chain, or finally to your actual endpoint function. It then waits for the response from that function.
*   `start_time = time.time()`: We record the time when the request enters the middleware.
*   `response = await call_next(request)`: We wait for the actual endpoint to process the request and give us a response. This `await` is important because `call_next` is an `async` function.
*   `process_time = time.time() - start_time`: We calculate how long it took for the request to be processed.
*   `response.headers["X-Process-Time"] = str(process_time)`: We add a new header to the response, telling the client how long the request took. This is a common practice.
*   `logger.info(...)`: We log useful information about the request to our console.
*   `return response`: Finally, we return the (potentially modified) response back to the client.

Restart Uvicorn and make some requests to your API (e.g., `/docs` or `/ask_ai`). You'll now see log messages in your terminal for every request, showing the processing time and status code. If you check the network tab in your browser's developer tools, you'll also see the `X-Process-Time` header in the response.

This example of `middleware setup` shows how you can neatly add cross-cutting concerns like logging or authentication to your FastAPI app, making it more robust and easier to maintain when you deploy LangChain API in a complex system. For more advanced middleware examples, you might refer to the [FastAPI documentation on Middleware](https://fastapi.tiangolo.com/tutorial/middleware/).

### Smart Component Sharing: Dependency Injection

Imagine your digital restaurant has a special spice mix that many dishes use. Instead of giving each chef their own bag of spices, you have a central jar that chefs can take from whenever they need it. `Dependency Injection` in FastAPI works similarly. It's a way for your API endpoints to easily get "ingredients" or "tools" they need without having to create them themselves.

This is super useful for:
*   **Sharing resources**: Like our LangChain `qa_chain` or a database connection.
*   **Testing**: You can easily swap out a real database for a fake one during tests.
*   **Organizing code**: Keeps your endpoint functions clean and focused on their main job.

Let's refactor our `ask_ai` endpoint to use `dependency injection` for our LangChain `qa_chain`.

#### Setting Up a Global LangChain Instance

First, we need to ensure our `qa_chain` is created only once when the application starts, not every time an endpoint is called. We already did this by defining it at the top level of our `main.py`.

```python
# main.py
# ... (existing imports and app setup) ...

# --- LangChain Setup (as before) ---
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please set it to your OpenAI API key.")

llm = OpenAI(openai_api_key=openai_api_key, temperature=0.7)
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="You are a helpful AI assistant. Answer the following question:\n{question}"
)
qa_chain = LLMChain(llm=llm, prompt=prompt_template) # Our "shared spice mix"
```

#### Creating a Dependency Function

Now, we'll create a small function that "provides" this `qa_chain`. This is our dependency.

```python
# main.py
# ... (existing code up to qa_chain definition) ...

# --- Dependency Function ---
def get_qa_chain():
    """
    Returns the initialized LangChain QA chain.
    This function acts as a dependency injector.
    """
    return qa_chain

# --- FastAPI Endpoints ---
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}

@app.post("/greet")
async def create_greeting(request: MessageRequest) -> MessageResponse:
    full_message = f"Hello, {request.user_name}! You said: '{request.message}'"
    msg_length = len(request.message)
    return MessageResponse(greeting=full_message, length_of_message=msg_length)

@app.post("/ask_ai", response_model=LangChainAnswerResponse)
async def ask_ai(
    request: LangChainQuestionRequest,
    langchain_chain: LLMChain = Depends(get_qa_chain) # Dependency injected here
):
    """
    Takes a question and uses LangChain with an OpenAI model to get an answer,
    demonstrating dependency injection for LangChain integration.
    """
    try:
        ai_answer = await langchain_chain.arun(request.question)
        return LangChainAnswerResponse(answer=ai_answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting AI answer: {str(e)}")

```

Let's look at the changes for `dependency injection`:

*   `from fastapi import Depends`: We import `Depends` which is the magic FastAPI uses for dependencies.
*   `def get_qa_chain():`: This new function simply returns our `qa_chain`. FastAPI will call this function automatically when an endpoint needs it.
*   `langchain_chain: LLMChain = Depends(get_qa_chain)`: This is the key line in our `ask_ai` endpoint.
    *   `langchain_chain: LLMChain`: We tell FastAPI that we expect an object of type `LLMChain` here.
    *   `= Depends(get_qa_chain)`: This tells FastAPI: "Before running `ask_ai`, please call `get_qa_chain()`, and whatever it returns, put it into the `langchain_chain` variable."

Now, our `ask_ai` function is cleaner. It doesn't need to know *how* `qa_chain` is created; it just asks for it, and FastAPI provides it. This makes it easier to test or change the `qa_chain` implementation later without touching the `ask_ai` function itself. This is a very common and powerful pattern when you deploy LangChain API in larger applications. For more on this topic, refer to the [FastAPI documentation on Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/).

### Ensuring Quality: Testing FastAPI Apps

Making sure your API works correctly is super important, just like a restaurant taste-testing its food before serving. `Testing FastAPI apps` helps you catch mistakes early and ensures your API behaves as expected. FastAPI makes testing quite straightforward.

We'll use `pytest` for testing, which is a popular Python testing tool.

#### Installing Pytest

First, if you haven't already, install `pytest` in your virtual environment:

```bash
pip install pytest httpx
```
We also install `httpx`, which is a powerful HTTP client that FastAPI's testing utilities use.

#### Creating a Test File

Create a new file named `test_main.py` in your `langchain_fastapi_app` folder (next to `main.py`).

```python
# test_main.py
import pytest
from httpx import AsyncClient
from main import app, get_qa_chain # Import your FastAPI app and dependency

# --- Mocking LangChain for Tests ---
# We need to "fake" the LangChain part so our tests don't actually call OpenAI
# This is called "mocking"
class MockLLMChain:
    """A fake LangChain LLMChain for testing."""
    def __init__(self, llm, prompt):
        self.llm = llm
        self.prompt = prompt

    async def arun(self, question: str):
        if "capital of France" in question:
            return "Paris"
        elif "your name" in question:
            return "I am a test AI."
        else:
            return f"Mock answer for: {question}"

@pytest.fixture(name="mock_qa_chain")
def override_get_qa_chain():
    """Fixture to provide a mocked LangChain QA chain."""
    return MockLLMChain(None, None) # LLM and prompt aren't used in our mock

# --- Tests ---
@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

@pytest.mark.asyncio
async def test_create_greeting():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/greet", json={"message": "Testing!", "user_name": "Tester"})
    assert response.status_code == 200
    assert response.json() == {
        "greeting": "Hello, Tester! You said: 'Testing!'",
        "length_of_message": 8
    }

@pytest.mark.asyncio
async def test_ask_ai_with_mock(mock_qa_chain):
    # Override the dependency for this test
    app.dependency_overrides[get_qa_chain] = lambda: mock_qa_chain

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/ask_ai", json={"question": "What is the capital of France?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Paris"

    response = await ac.post("/ask_ai", json={"question": "What is your name?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "I am a test AI."

    # Clear the dependency override after the test
    app.dependency_overrides = {}
```

Let's break down this example of `testing FastAPI apps`:

*   **Imports**: We import `pytest`, `AsyncClient` from `httpx` (for making asynchronous HTTP requests), and our `app` and `get_qa_chain` from `main.py`.
*   **Mocking LangChain**:
    *   `MockLLMChain`: This is a fake version of our `LLMChain`. Its `arun` method doesn't call OpenAI but instead returns predefined answers for specific questions or a generic one otherwise. This saves money and makes tests fast and reliable.
    *   `@pytest.fixture(name="mock_qa_chain")`: This tells pytest that `override_get_qa_chain` is a "fixture." A fixture provides resources for tests. Here, it provides our `MockLLMChain`.
*   **`@pytest.mark.asyncio`**: This decorator (you'll need to install `pytest-asyncio` via `pip install pytest-asyncio` if you haven't already) allows us to write `async` test functions.
*   **`async with AsyncClient(app=app, base_url="http://test") as ac:`**: This is how we interact with our FastAPI app in tests. `AsyncClient` simulates requests to your app without actually starting a network server.
    *   `app=app`: Tells the client which FastAPI app to test.
    *   `base_url="http://test"`: A dummy base URL.
*   **`response = await ac.get("/")`**: We make a simulated GET request to the root endpoint.
*   **`assert response.status_code == 200`**: We check if the HTTP status code is 200 (OK).
*   **`assert response.json() == {"message": "Hello, FastAPI!"}`**: We check if the JSON response is what we expect.
*   **`test_ask_ai_with_mock(mock_qa_chain)`**:
    *   `app.dependency_overrides[get_qa_chain] = lambda: mock_qa_chain`: This is crucial for `dependency injection` in testing. We temporarily replace our *real* `get_qa_chain` function with one that returns our `MockLLMChain`. This ensures our test uses the fake AI.
    *   After making the requests, `app.dependency_overrides = {}` clears the override, so other tests aren't affected.

#### Running Your Tests

To run these tests, make sure your virtual environment is active, then simply type in your terminal:

```bash
pytest
```

You should see output indicating that all your tests passed:

```
============================= test session starts ==============================
platform linux -- Python 3.9.7, pytest-6.2.5, pluggy-1.0.0
rootdir: /path/to/your/langchain_fastapi_app
plugins: asyncio-0.17.2
collected 3 items

test_main.py ...                                                         [100%]

============================== 3 passed in 0.XXXs ==============================
```

This comprehensive example of `testing FastAPI apps` with `pytest` and `httpx`, especially with mocking external dependencies like LangChain, is a best practice. It ensures your API functions correctly and is robust, making your `deploy langchain api fastapi tutorial` project reliable.

### Deployment Considerations for Your LangChain API

You've built an amazing FastAPI application with LangChain integration! Now, you might be thinking about how to `deploy LangChain API` so others can use it. While this tutorial focuses on building the API, let's briefly touch on what deployment means.

Deployment is like opening your digital restaurant to the public, making it accessible on the internet. You take your code and put it on a server somewhere, so people can send requests to it.

Here are some common ways to deploy FastAPI apps:

1.  **Using a Cloud Provider**: Services like Heroku, Vercel, AWS (EC2, Lambda), Google Cloud (App Engine, Cloud Run), or Azure (App Service) are popular. They handle the server infrastructure for you.
    *   **Heroku/Vercel**: Very easy for small projects, quick to get started.
    *   **Cloud Run (Google Cloud) / AWS Fargate**: Great for containerized apps, scales well, you pay for what you use.
    *   **EC2/App Service**: More control, but also more to manage.

2.  **Containerization with Docker**: This is a very common and recommended approach.
    *   You package your application and all its dependencies (like Python, FastAPI, LangChain) into a single, self-contained unit called a "Docker image."
    *   This image can then run consistently on any server that has Docker installed, making deployment predictable and reproducible.
    *   You would typically create a `Dockerfile` in your project that lists the steps to build this image.

3.  **Reverse Proxy (Nginx/Traefik)**: In a production environment, you usually put a web server like Nginx or Traefik in front of your Uvicorn server.
    *   This "reverse proxy" handles things like SSL (HTTPS), caching, load balancing, and serving static files, leaving Uvicorn to focus solely on running your FastAPI application.

#### Key Steps for Deployment:

1.  **Dockerize Your Application (Recommended)**:
    *   Create a `Dockerfile`.
    *   Build your Docker image.
    *   Push your image to a container registry (like Docker Hub or your cloud provider's registry).

2.  **Choose a Hosting Platform**: Pick a cloud provider or your own server.

3.  **Set Environment Variables**: Crucially, ensure your `OPENAI_API_KEY` (and any other sensitive information) is set as an environment variable on your deployed server. Never hardcode sensitive keys in your code that goes to production.

4.  **Run with a Production-Ready Server**: While `uvicorn main:app --reload` is great for development, for production, you'd use a more robust command, often with multiple worker processes, like:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 80 --workers 4
    ```
    (Note: `0.0.0.0` makes the app accessible from outside the container/server).

5.  **Monitor Your API**: Once deployed, keep an eye on your API's performance, errors, and usage.

Deployment can be a complex topic on its own. For a deep dive into specific deployment strategies, you might want to look for tutorials like "[Deploying FastAPI with Docker and Nginx](/blog/fastapi-docker-nginx-deployment)" or "[FastAPI on Google Cloud Run](/blog/fastapi-google-cloud-run)". The key takeaway is to prepare your application for a production environment, especially around security and performance, once you're ready to deploy LangChain API to the world.

### Conclusion: You've Built and Integrated a Smart AI API!

Wow, you've come a long way! From setting up your basic FastAPI environment to integrating a powerful AI like LangChain, you've learned how to `deploy LangChain API` using a comprehensive FastAPI tutorial. You now have a solid foundation for building interactive AI-powered web services.

We covered essential topics like FastAPI setup, creating endpoints, using async route handlers, and defining clear request/response models. You saw how seamless LangChain integration can be, making your API smart and responsive. We also enhanced our understanding of API documentation, secured our API with CORS configuration, made it more robust with middleware setup, and structured it cleanly using dependency injection. Finally, we learned about the importance of testing FastAPI apps to ensure reliability.

This knowledge opens up a world of possibilities for you. You can expand on this example to create more complex LangChain chains, integrate different AI models, or build entire applications around your AI API. Keep experimenting, keep building, and unleash the power of AI with FastAPI!