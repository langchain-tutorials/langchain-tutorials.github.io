---
title: "Deploy LangChain API: Security, Authentication, and Rate Limiting Guide"
description: "Learn to securely deploy LangChain API. This essential guide covers security, authentication, and rate limiting best practices to protect your services effec..."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [deploy langchain api security authentication]
featured: false
image: '/assets/images/deploy-langchain-api-security-authentication-rate-limiting.webp'
---

## Secure Your AI Powerhouse: A Guide to Deploying LangChain API with Top-Tier Security

You're ready to deploy your amazing LangChain API, which uses smart AI to do cool things. That's super exciting! But before you launch it for everyone to use, it's super important to make sure it's safe and sound.

Imagine building a fantastic house, but forgetting to put locks on the doors. This guide will show you how to add strong locks, security cameras, and even a friendly bouncer to your LangChain API. We'll talk about how to deploy LangChain API security authentication, and make sure it can handle lots of visitors without crashing.

We'll cover everything from who can use your API to how to protect it from bad guys. By the end, you'll know exactly how to deploy your LangChain API safely and effectively. Let's make your AI project a secure success!

## Why Security is a Must for Your LangChain API

When you build and deploy a LangChain API, you're giving others access to your clever AI tools. This is great, but it also opens doors to potential problems if not handled carefully. You wouldn't want just anyone messing with your hard work or the data it uses.

Unauthorized access could mean someone uses your API without permission, maybe even costing you money or accessing sensitive information. Bad actors might try to steal data, disrupt your service, or even make your API do things it shouldn't. That's why strong API security best practices are non-negotiable.

Protecting your LangChain API is like putting a helmet on your head before riding a bike; it's a basic safety measure. It keeps your service running smoothly, protects user data, and maintains trust. Let's dive into how you can make your LangChain API deployment super secure.

## Authentication: Knowing Who's at Your API's Door

Authentication is simply checking if someone is who they say they are. When you deploy a LangChain API, you need to make sure only approved people or applications can use it. This prevents strangers from just walking in and using your services.

There are different ways to authenticate users for your LangChain API, each with its own strengths. Choosing the right method depends on how your API will be used and how much security you need. We'll look at the most common and effective ways to secure access to your API.

Having a good authentication system is the first and most crucial step in any API security strategy. It lays the groundwork for all other protective measures.

### API Key Management: Your Simple Front Door Key

API keys are like special passwords that applications use to identify themselves to your LangChain API. When you give someone an API key, it's their unique token to access your service. They send this key with every request they make.

It's important to treat API keys like any other secret. You should generate them securely, store them in a safe place, and never put them directly in your code that others can see. Good API key management also means you can easily create new keys and revoke old ones if they get lost or stolen.

Here's how you might check for an API key in a Python web framework like FastAPI, which you could use to deploy a LangChain API:

```python
# main.py
from fastapi import FastAPI, Header, HTTPException, Depends
import os

app = FastAPI()

# Get your API key from an environment variable (best practice!)
# You would set this environment variable in your deployment environment
API_KEY = os.getenv("LANGCHAIN_API_KEY", "your_super_secret_default_key_dont_use_in_prod")

def verify_api_key(x_api_key: str = Header(...)):
    """
    Checks if the API key provided in the request header is valid.
    """
    if not API_KEY or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

@app.get("/secure-langchain-endpoint")
async def read_secure_data(api_key: str = Depends(verify_api_key)):
    """
    An example endpoint protected by an API key.
    Here you would integrate your LangChain logic.
    """
    # Example LangChain interaction
    # from langchain.llms import OpenAI
    # llm = OpenAI(api_key="your_openai_key")
    # response = llm.invoke("Tell me a simple joke.")
    return {"message": "Access granted to secure LangChain endpoint!", "api_key_used": api_key}

# To run this example:
# 1. Save as main.py
# 2. Install FastAPI and Uvicorn: pip install fastapi uvicorn python-dotenv
# 3. Set the environment variable: export LANGCHAIN_API_KEY="my_secret_key_123"
# 4. Run the server: uvicorn main:app --reload
# 5. Test with curl: curl -X GET "http://127.0.0.1:8000/secure-langchain-endpoint" -H "X-API-Key: my_secret_key_123"
#    Test with wrong key: curl -X GET "http://127.0.0.1:8000/secure-langchain-endpoint" -H "X-API-Key: wrong_key"
```

In this example, your LangChain API requires a special header called `X-API-Key` with the correct secret. If the key doesn't match, access is denied. Remember, API keys are often sent in plain text (though over HTTPS!), so they are best for machine-to-machine communication where the key isn't exposed to end-users. For more details on environment variables, check out our guide on [Secure Configuration Management](/blog/secure-configuration-management).

### JWT Authentication: The Stamped Passport

JWT stands for JSON Web Token. It's like a special stamped passport that proves who you are and for how long you're allowed in. When a user logs in, your server gives them a JWT. This token contains information about the user and is signed by your server to prevent tampering.

The user then sends this JWT with every request to your LangChain API. Your API just needs to check the signature to know if the token is valid and hasn't been changed. This is a very popular method for securing APIs because it's stateless, meaning your server doesn't have to remember who is logged in after giving out the token.

Implementing JWT authentication involves two main parts: issuing the token when a user authenticates, and verifying the token on subsequent requests. This is especially good when you deploy a LangChain API that needs user-specific access.

#### Steps to Implement JWT Authentication

1.  **Login/Issue Token:** When a user successfully logs in (e.g., with a username and password), your server creates a JWT. This token includes things like the user's ID and an expiration time. It's then signed with a secret key that only your server knows.
2.  **Send Token:** Your server sends this JWT back to the user's browser or application.
3.  **Access Protected Resources:** For every protected request, the user's application sends the JWT in the `Authorization` header, usually like `Bearer <your_jwt_token>`.
4.  **Verify Token:** Your LangChain API receives the request, takes the JWT, and verifies its signature using the same secret key. If the signature is valid and the token hasn't expired, the user is authenticated.

Here's a simplified example of how you might verify a JWT in a FastAPI application for your LangChain API:

```python
# main.py (continued from previous example)
import jwt
from datetime import datetime, timedelta
from typing import Optional

# Super secret key for signing JWTs - keep this REALLY secret and in environment variables!
# For production, generate a strong, random key.
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_super_secret_jwt_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a new JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str = Header(..., alias="Authorization")):
    """
    Verifies a JWT token from the Authorization header.
    Expects Authorization: Bearer <token>
    """
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    token = token.split(" ")[1] # Extract the actual token

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid JWT payload")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid JWT token")

@app.post("/login")
async def login_for_access_token():
    """
    Example login endpoint (simplified for demonstration).
    In a real app, you'd check username/password here.
    """
    # In a real app, validate user credentials
    user_id = "test_user_123"
    access_token = create_access_token(data={"sub": user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/secure-langchain-endpoint-jwt")
async def read_secure_data_jwt(current_user: str = Depends(verify_jwt_token)):
    """
    An example endpoint protected by JWT.
    Here you would integrate your LangChain logic, possibly tailored by current_user.
    """
    # Example LangChain interaction
    # from langchain.llms import OpenAI
    # llm = OpenAI(api_key="your_openai_key")
    # response = llm.invoke(f"Tell user {current_user} a secret.")
    return {"message": f"Hello, {current_user}! Access granted to secure LangChain endpoint!", "user": current_user}

# To run this example:
# 1. Install PyJWT: pip install PyJWT
# 2. Set JWT_SECRET_KEY: export JWT_SECRET_KEY="a_very_secret_key_for_jwt"
# 3. Log in: curl -X POST "http://127.0.0.1:8000/login"
#    You'll get an access_token.
# 4. Use the token: curl -X GET "http://127.0.0.1:8000/secure-langchain-endpoint-jwt" -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>"
```

JWT authentication offers a secure and scalable way to manage user sessions for your deployed LangChain API. It's great for applications where individual users interact with your service through a frontend. For further reading on user authentication, you might find our article on [Building User Portals with FastAPI](/blog/building-user-portals-fastapi) helpful.

### OAuth2 Implementation: The Delegated Authority

OAuth2 is a bit more complex, but it's super powerful for specific situations. Think of it as giving a trusted friend permission to pick up a package for you, without giving them your house keys. You delegate permission for a specific task. When you deploy a LangChain API that needs to be accessed by third-party applications (like "Log in with Google"), OAuth2 is the way to go.

It allows a user to grant an application limited access to their resources on another server, without giving their password to the application. For example, a user might grant a note-taking app access to their Google Drive.

While full OAuth2 implementation is beyond a simple snippet, understanding its purpose is key. It involves multiple steps, including authorization requests, consent screens, and token exchanges. It's often used when your LangChain API serves as a backend for multiple client applications or when you want to allow users to sign in using their existing accounts from other big services like Google or Facebook.

For your LangChain API, OAuth2 would primarily be used to authenticate the *user* of a client application, allowing that application to make requests on the user's behalf. It adds another layer of security and trust for complex ecosystems.

## Authorization: What Can They Do?

Once someone is authenticated (you know who they are), authorization decides what actions they are allowed to perform. Authentication is about identity, authorization is about permissions. For example, a "guest" might be authenticated but only authorized to view public information, while an "admin" might be authorized to change settings.

When you deploy a LangChain API, you might have different types of users or applications. Some might only be allowed to ask simple questions, while others can perform more complex operations or access sensitive data. Your authorization system ensures that each authenticated entity only does what it's supposed to do.

You can implement authorization by checking the user's role or permissions after they've been authenticated. For instance, if your JWT token included a 'role' field, your LangChain API could check if that role is 'admin' before allowing access to an administrative endpoint.

## Rate Limiting Strategies: Protecting Your LangChain API from Overload

Imagine a popular store where everyone rushes in at once, causing a huge jam. Rate limiting is like having a bouncer at the door, making sure too many people don't enter at the same time. This is crucial for your LangChain API, especially when dealing with AI models which can be resource-intensive.

Rate limiting helps protect your service from being overwhelmed by too many requests, which could slow it down or even crash it. It also acts as a first line of defense against malicious attacks like Distributed Denial of Service (DDoS) attempts, where attackers try to flood your service with requests. By limiting how many requests a user or IP address can make in a certain time period, you ensure fair usage and system stability.

There are a few popular rate limiting strategies you can use when you deploy a LangChain API:

*   **Fixed Window:** You set a limit (e.g., 100 requests per minute) for a fixed time window. If someone exceeds it, they're blocked until the next window starts. This is simple but can lead to "bursts" of requests at the start of a new window.
*   **Sliding Window:** This is a smoother version of the fixed window. It still has a limit over a time period, but it constantly "slides," so it's less prone to bursts at the edge of the window.
*   **Token Bucket:** Imagine a bucket that constantly refills with "tokens." Each request takes a token. If the bucket is empty, no more requests are allowed until more tokens appear. This allows for some burstiness but caps the overall rate.

Let's look at a simple example of rate limiting in FastAPI using a library:

```python
# main.py (continued)
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

# Initialize the rate limiter
# This uses the client's IP address to limit requests.
# In a production environment behind a proxy, you might need a different strategy for get_remote_address.
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/limited-endpoint", dependencies=[Depends(verify_api_key)])
@limiter.limit("5/minute") # Allows 5 requests per minute for this endpoint
async def limited_endpoint(request: Request):
    """
    An example endpoint with rate limiting.
    It's also protected by the API key.
    """
    # This is where your LangChain API logic would go.
    # from langchain.agents import load_tools, initialize_agent
    # agent = initialize_agent(...)
    return {"message": "You accessed the limited endpoint!"}

@app.get("/another-limited-endpoint")
@limiter.limit("10/minute") # A different limit for another endpoint
async def another_limited_endpoint(request: Request):
    """
    Another endpoint with a different rate limit.
    """
    return {"message": "This endpoint has a different limit."}

# To run this example:
# 1. Install slowapi: pip install slowapi
# 2. Test: make more than 5 requests to /limited-endpoint within a minute using your API key.
#    You'll get a 429 Too Many Requests response.
```

In this snippet, we use the `slowapi` library to easily add rate limits. The `@limiter.limit("5/minute")` decorator means that a single client (identified by their IP address) can only make 5 requests to this endpoint every minute. If they try more, they'll get an error message.

You can also use external tools and services for more robust rate limiting, especially when deploying at scale. Cloudflare, AWS API Gateway, and other cloud providers offer built-in rate limiting features that are highly configurable and can protect your LangChain API at the network edge. This takes the burden off your application server and provides stronger DDoS protection.

## Essential API Security Best Practices for LangChain

Beyond authentication and rate limiting, there are many other important practices to keep your LangChain API super secure. Think of these as all the little details that add up to a very strong fortress around your AI. Adopting these API security best practices is crucial for maintaining a reliable and trustworthy service.

### HTTPS Enforcement: Always Use a Secure Channel

HTTPS is like sending your messages in a sealed, encrypted envelope. It makes sure that all communication between your user's application and your LangChain API is encrypted. This means no one can snoop on the data being sent or change it along the way. Without HTTPS, sensitive information (like API keys or personal data) could be intercepted by attackers.

Always make sure your deployed LangChain API uses HTTPS. If you're hosting on a cloud platform like AWS, Google Cloud, or Azure, they typically provide easy ways to enable HTTPS with SSL/TLS certificates. If you're using a web server like Nginx or Caddy, they can also handle HTTPS for you. Your application code itself doesn't always need to explicitly enforce HTTPS if it's behind a good reverse proxy.

### Input Validation and Sanitization: Don't Trust User Input

One of the most common ways attackers try to break into systems is by sending "bad" or unexpected input. Imagine asking your LangChain model for a simple joke, but instead, someone tries to inject malicious code into the request. Input validation and sanitization mean carefully checking and cleaning all data that comes into your API from users.

For your LangChain API, this means validating any text, parameters, or configurations sent by the user before they are passed to your AI models or databases. This helps prevent many common attacks, including SQL injection prevention and cross-site scripting (XSS).

Here’s a simple example for input validation in FastAPI:

```python
# main.py (continued)
from pydantic import BaseModel, Field

class LangChainQuery(BaseModel):
    prompt: str = Field(min_length=10, max_length=500) # Ensure prompt is between 10 and 500 chars
    temperature: float = Field(default=0.7, ge=0.0, le=1.0) # Temperature must be between 0 and 1

@app.post("/query-langchain")
@limiter.limit("10/minute")
async def query_langchain_model(query: LangChainQuery, request: Request, user_id: str = Depends(verify_jwt_token)):
    """
    An example endpoint for LangChain queries with input validation.
    """
    # Here, your LangChain model receives validated input
    # Example LangChain usage:
    # from langchain.chains import LLMChain
    # from langchain.prompts import PromptTemplate
    # prompt_template = PromptTemplate(template="Answer this question: {prompt}", input_variables=["prompt"])
    # llm_chain = LLMChain(llm=llm, prompt=prompt_template)
    # result = llm_chain.invoke({"prompt": query.prompt})

    # Ensure no dangerous characters are passed to external systems
    # For example, if you were using query.prompt in an SQL query,
    # you would ensure it's parameterized.
    clean_prompt = query.prompt.strip() # Basic sanitization
    return {"response": f"Processed prompt: '{clean_prompt}' with temperature {query.temperature} for user {user_id}"}
```

In this example, FastAPI uses Pydantic models to automatically validate the `prompt` length and `temperature` range. If the input doesn't meet these rules, FastAPI will automatically send back an error, protecting your LangChain models from bad data. This is a powerful way to implement input validation.

### SQL Injection Prevention: Protecting Your Databases

If your LangChain agents or tools interact with databases, you must be very careful about SQL injection. This is a type of attack where a malicious user inputs SQL code instead of expected data. If your application isn't careful, it might run this bad code, potentially revealing or deleting your entire database.

To prevent SQL injection when your LangChain API interacts with databases, always use parameterized queries or Object-Relational Mappers (ORMs). These tools ensure that user input is treated as data, not as executable code, making SQL injection attacks virtually impossible. Never build SQL queries by directly combining user input strings!

For example, using an ORM like SQLAlchemy with your LangChain tools:

```python
# Instead of:
# sql_query = f"SELECT * FROM users WHERE name = '{user_input}'" # DANGEROUS!

# Use parameterized query (psycopg2 for PostgreSQL example):
# import psycopg2
# conn = psycopg2.connect(...)
# cur = conn.cursor()
# cur.execute("SELECT * FROM users WHERE name = %s", (user_input,)) # SAFE!

# Or use an ORM (SQLAlchemy example):
# from sqlalchemy import create_engine, text
# engine = create_engine("sqlite:///./test.db")
# with engine.connect() as connection:
#    result = connection.execute(text("SELECT * FROM users WHERE name = :user_name"), {"user_name": user_input}) # SAFE!
```

This ensures that any database interactions driven by your LangChain API are safe from malicious input.

### Security Headers: The Extra Layer of Browser Protection

Security headers are special instructions your server sends to a user's web browser. They tell the browser how to behave when loading your LangChain API's web interface or consuming its responses. These headers can prevent common web attacks like clickjacking, cross-site scripting (XSS), and content injection.

Some important security headers include:

*   **`X-Content-Type-Options: nosniff`**: Prevents browsers from "guessing" the content type, reducing certain attack vectors.
*   **`X-Frame-Options: DENY`**: Prevents your site from being embedded in an iframe on another site, protecting against clickjacking.
*   **`Strict-Transport-Security` (HSTS)**: Tells browsers to always use HTTPS for your site, even if the user types `http://`.
*   **`Content-Security-Policy` (CSP)**: A very powerful header that lets you control which resources (scripts, stylesheets, images) the browser is allowed to load.

Here's how you might add some security headers in FastAPI:

```python
# main.py (continued)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# Middleware to add security headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        # Add other headers as needed, like Content-Security-Policy (CSP)
        # CSP is more complex and depends on your specific front-end needs
        # response.headers["Content-Security-Policy"] = "default-src 'self';"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# ... (rest of your FastAPI app)
```

Adding these headers is a simple yet effective way to boost the security posture of your LangChain API, especially if it interacts with web browsers.

### Logging and Monitoring: Keeping an Eye on Things

You can't protect what you don't know is happening. Logging and monitoring are like having a security guard who records everything and alerts you to suspicious activity. When you deploy a LangChain API, you need to log important events, such as failed login attempts, unusual request patterns, or errors.

Good logging helps you:

*   **Detect attacks:** Spot repeated failed authentication attempts or unusual request spikes.
*   **Troubleshoot issues:** Understand why your API might be behaving unexpectedly.
*   **Audit access:** See who accessed what and when.

You should set up monitoring tools that can collect these logs and, more importantly, alert you when something unusual happens. For example, an alert could be triggered if there are 100 failed login attempts from the same IP address in a minute. This proactive approach is vital for rapid response to security incidents.

### Regular Security Audits and Updates: Staying Ahead of Threats

The world of security changes constantly. New vulnerabilities are discovered, and new attack methods emerge. Just like you update your phone's software, you need to regularly update your LangChain API's underlying libraries, frameworks, and even the operating system it runs on.

Regular security audits involve systematically checking your LangChain API for weaknesses. This could mean using automated security scanners or even hiring experts to try and find flaws. Staying up-to-date and regularly auditing your system ensures that you're always using the latest defenses against known threats.

This also applies to the LangChain library itself. Make sure you are using the most recent stable versions to benefit from security patches and improvements.

### Secrets Management: Guarding Your Most Sensitive Info

Your LangChain API might need various "secrets" to do its job, like API keys for external services (OpenAI, Google), database passwords, or your JWT secret key. These pieces of information are super sensitive and must be protected with the utmost care. Never hardcode them directly into your application code.

Instead, use environment variables or dedicated secret management tools. Environment variables are a good starting point for smaller deployments. For larger, more complex systems, consider using tools like HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault. These services are designed to store, manage, and distribute secrets securely without exposing them in your code or configuration files.

## DDoS Protection for Your Deployed LangChain API

A Distributed Denial of Service (DDoS) attack is like a huge crowd trying to get into your store all at once, not to buy anything, but just to block the entrance so real customers can't get in. Attackers flood your LangChain API with tons of fake requests to make it slow down or completely crash. This can be very damaging, making your service unavailable to legitimate users.

Protecting your LangChain API from DDoS attacks usually involves a layered approach. While rate limiting helps, it's often not enough on its own for large-scale attacks.

Consider using specialized DDoS protection services. Providers like Cloudflare, AWS Shield, Google Cloud Armor, and Akamai sit in front of your API. They act as a massive filter, inspecting incoming traffic and blocking known malicious requests before they even reach your servers. These services can absorb huge amounts of attack traffic, ensuring your LangChain API remains accessible to legitimate users. For in-depth information on preventing such attacks, consider reading about [Cloudflare's DDoS protection strategies](https://www.cloudflare.com/learning/ddos/what-is-ddos-protection/).

## Deployment Considerations and Environment Setup

Securing your LangChain API isn't just about the code; it's also about where and how you deploy it. The environment your API runs in needs to be just as secure as the API itself.

If you're using Docker containers, make sure your Dockerfiles are lean and don't include unnecessary tools or sensitive information. If you're orchestrating with Kubernetes, implement network policies to control traffic between your services and ensure pods run with the least necessary privileges.

The principle of "least privilege" is key: give your API and its underlying infrastructure only the permissions they absolutely need to function, and no more. For instance, your API probably doesn't need root access to the server. Following these guidelines helps minimize the damage if an attacker somehow gains access.

## Practical Example: Securing a LangChain API with FastAPI and JWT

Let's put some of these pieces together into a more complete picture. We'll imagine you want to deploy a LangChain API that allows authenticated users to ask questions to an LLM, and we'll protect it with JWT authentication and basic rate limiting.

First, you'll need a `.env` file for your secrets (remember, never hardcode these!):

```text
# .env file
JWT_SECRET_KEY="super_duper_secret_key_for_your_jwt_tokens_change_this"
LANGCHAIN_API_KEY="my_secret_key_for_internal_api_access_if_needed" # Not used in this specific example but good to have
OPENAI_API_KEY="sk-YOUR_OPENAI_API_KEY_HERE" # Replace with your actual OpenAI API key
```

Now, let's create our `main.py` file:

```python
# main.py
import os
import jwt
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, Header, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field

# For rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# For LangChain (make sure to install: pip install langchain openai)
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# --- Configuration ---
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable not set.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Tokens expire after 30 minutes

# --- FastAPI App Setup ---
app = FastAPI(
    title="Secure LangChain API",
    description="A guide to deploying a LangChain API with security, authentication, and rate limiting.",
    version="1.0.0"
)

# --- Rate Limiting Setup ---
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- LangChain Setup ---
# Initialize the OpenAI LLM
llm = OpenAI(api_key=OPENAI_API_KEY, temperature=0.7)

# Define a simple LangChain prompt template
langchain_prompt = PromptTemplate(
    input_variables=["query", "user_id"],
    template="You are a helpful AI assistant. Respond to the following query from user {user_id}: {query}"
)
langchain_chain = LLMChain(llm=llm, prompt=langchain_prompt)

# --- Authentication (JWT) ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # Points to our /token endpoint for getting JWT

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generates a JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Verifies the JWT token and returns the current user ID."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise credentials_exception
    return token_data.username

# --- Input Validation Model ---
class LangChainQueryInput(BaseModel):
    query: str = Field(min_length=5, max_length=1000, description="The query to send to the LangChain LLM.")

# --- API Endpoints ---

@app.post("/token", response_model=Token, summary="Get JWT Access Token (Simulated Login)")
async def login_for_access_token():
    """
    **Simulated Login:** In a real application, you would verify user credentials (username/password) here.
    For this example, we just issue a token for a 'testuser'.
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "testuser"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/langchain/query", summary="Query the LangChain LLM (Protected)",
          dependencies=[Depends(limiter.depends("10/minute"))]) # Apply rate limit here
async def run_langchain_query(
    request: Request, # Required by slowapi
    query_input: LangChainQueryInput,
    current_user: str = Depends(get_current_user)
):
    """
    This endpoint allows authenticated users to send queries to the LangChain LLM.
    It includes input validation and is protected by rate limiting.
    """
    print(f"User '{current_user}' submitted query: '{query_input.query}'")
    try:
        # Use the LangChain chain to process the query
        response = await langchain_chain.arun(query=query_input.query, user_id=current_user) # .arun for async
        return {"user": current_user, "query": query_input.query, "response": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing LangChain query: {str(e)}"
        )

# Example of an unprotected endpoint (for comparison, generally not recommended for LangChain)
@app.get("/unprotected-hello", summary="Unprotected Hello World")
async def unprotected_hello():
    return {"message": "Hello from an unprotected endpoint!"}

# --- Middleware for Security Headers (as shown before) ---
from starlette.middleware.base import BaseHTTPMiddleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        # For a full CSP, you'd need to customize this based on your frontend assets
        # response.headers["Content-Security-Policy"] = "default-src 'self';"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Run instructions:
# 1. pip install fastapi uvicorn python-dotenv PyJWT langchain openai slowapi
# 2. Create a .env file with your JWT_SECRET_KEY and OPENAI_API_KEY
# 3. uvicorn main:app --reload
#
# To test:
# 1. Get a token (simulated login):
#    curl -X POST "http://127.0.0.1:8000/token"
#    Copy the "access_token" from the response.
# 2. Query the LangChain API with the token:
#    curl -X POST "http://127.0.0.1:8000/langchain/query" \
#         -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
#         -H "Content-Type: application/json" \
#         -d '{"query": "What is the capital of France?"}'
# 3. Test rate limiting: Make more than 10 requests within a minute.
# 4. Test input validation: Use a very short or very long query.
#    curl -X POST "http://127.0.0.1:8000/langchain/query" \
#         -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
#         -H "Content-Type: application/json" \
#         -d '{"query": "Hi"}'
```

This example shows how to deploy a LangChain API with multiple security layers:

*   **JWT Authentication:** Users get a token after a "login" (simulated here) and must provide it to access the LangChain endpoint.
*   **Rate Limiting:** The `langchain/query` endpoint is limited to 10 requests per minute per client IP.
*   **Input Validation:** The `LangChainQueryInput` Pydantic model ensures the incoming query meets length requirements.
*   **Environment Variables:** Sensitive keys are loaded from `.env` files, not hardcoded.
*   **Security Headers:** A middleware adds crucial HTTP security headers to all responses.
*   **Error Handling:** Proper HTTP exceptions are raised for authentication failures, expired tokens, and validation errors.

This comprehensive approach makes your LangChain API much more robust and resistant to common attacks.

## Conclusion

Deploying a LangChain API is an exciting step, but ensuring its security, authentication, and proper rate limiting is absolutely critical. We've explored many layers of protection, from knowing who's accessing your API with robust authentication methods like API key management and JWT authentication, to protecting against overload with rate limiting strategies. You've learned about essential API security best practices like HTTPS enforcement, input validation, SQL injection prevention, and the use of security headers.

Remember, security is not a one-time task; it's an ongoing process. Regularly update your software, monitor your API for suspicious activity, and conduct security audits. By adopting these strategies, you can confidently deploy your LangChain API, knowing it's protected against common threats and ready to serve your users reliably.

Start building your secure LangChain API today and unlock the full potential of your AI without compromising safety!