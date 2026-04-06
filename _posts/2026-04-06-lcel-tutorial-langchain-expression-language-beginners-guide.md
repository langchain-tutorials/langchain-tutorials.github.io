---
title: "LCEL Tutorial: A Complete Beginner's Guide to LangChain Expression Language"
description: "Unlock the power of LangChain Expression Language (LCEL) with this beginner's LCEL tutorial. Build robust LLM applications efficiently from scratch. Start ma..."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LCEL tutorial LangChain Expression Language]
featured: false
image: '/assets/images/lcel-tutorial-langchain-expression-language-beginners-guide.webp'
---

## LCEL Tutorial: A Complete Beginner's Guide to LangChain Expression Language

Welcome to this comprehensive LCEL tutorial! If you're looking to build amazing applications with large language models, you've come to the right place. We're going to explore the LangChain Expression Language (LCEL) step by step. This guide will help you understand how to create powerful and flexible LLM chains.

Imagine you want to talk to a smart computer program, like ChatGPT, but you want to give it specific instructions first. LangChain helps you do this easily. LCEL is a special way inside LangChain to connect different parts of your smart program together. It's like building with LEGO bricks, where each brick does something specific.

By the end of this LCEL tutorial, you will be able to compose complex LangChain applications with ease. You'll understand the core concepts of LangChain Expression Language. This will unlock new possibilities for your AI projects.

### What is LangChain Expression Language (LCEL)?

LangChain Expression Language, or LCEL, is a super cool way to build complex chains in LangChain. Think of it as a special language for creating sequences of actions for your AI. It makes building LangChain applications much easier and more organized.

LCEL helps you connect different components like prompts, language models, and tools. You can link them together like beads on a string. This allows you to define how information flows through your application. It’s perfect for making your LLM chains do exactly what you want.

It focuses on something called "runnables," which are like small, self-contained tasks. These runnables can be strung together using a simple pipe operator. This makes the LangChain Expression Language very powerful and easy to read. You'll soon see how simple it is to use.

#### Why Should You Care About LCEL?

LCEL brings many benefits to building your LangChain applications. First, it makes your code much clearer and easier to understand. You can see how each part of your system connects and works together. This is a huge help when your projects start to grow.

Second, LCEL helps your applications run faster and more efficiently. It can do multiple things at the same time when possible. This means your smart programs respond quicker. This optimization is built right into the LangChain Expression Language.

Third, LCEL makes your chains more reliable. It provides built-in tools for things like retries and fallbacks. This means if one part of your chain has a problem, your whole application won't break. This robustness is a key advantage of using LCEL.

Fourth, you get better insights into how your chains are working. LCEL allows for great observability. You can easily track inputs, outputs, and intermediate steps of your LangChain Expression Language chains. This helps you debug and improve your applications.

### Getting Started: Setting Up Your Environment

Before we dive into the LCEL tutorial, let's make sure your computer is ready. You'll need Python installed, which is a popular programming language. We will also need to install the LangChain library. This is where all the magic happens.

If you haven't already, you should also have an API key for a language model, like OpenAI or Google Gemini. These keys let your code talk to the powerful AI models. You can get one from their official websites. This LCEL tutorial will use OpenAI for most examples.

#### Installing LangChain

Open your terminal or command prompt. This is where you type commands to your computer. We will use a command called `pip` to install the necessary packages. It's like telling your computer to get a new app.

Type the following command and press Enter:

```bash
pip install langchain langchain-openai
```

This command installs the core LangChain library and a specific part for OpenAI models. The `langchain-openai` package lets you easily connect to OpenAI's large language models. This is crucial for building many LLM chains.

#### Setting Your API Key

Your API key acts like a secret password to use the AI services. You should never share it with anyone. It's best to store it in a special place called an environment variable. This keeps it safe from being accidentally put into your code.

You can set it temporarily in your terminal like this (replace `YOUR_API_KEY` with your actual key):

**For macOS/Linux:**

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

**For Windows (Command Prompt):**

```cmd
set OPENAI_API_KEY="YOUR_API_KEY"
```

**For Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY="YOUR_API_KEY"
```

It's even better to put this key in a `.env` file for your project. Then, you can use a library like `python-dotenv` to load it. This keeps your key out of your code files. This is a common and secure practice for LangChain applications.

```bash
pip install python-dotenv
```

Then, create a file named `.env` in your project folder and add your key:

```
OPENAI_API_KEY="YOUR_API_KEY"
```

And in your Python script, you can load it:

```python
from dotenv import load_dotenv
import os

load_dotenv() # This loads variables from .env
# Now os.environ.get("OPENAI_API_KEY") will work
```

Now you are fully set up for our LCEL tutorial. We can start building our first LangChain Expression Language chains. You have all the tools needed to begin.

### The Core Building Blocks: Runnables

At the heart of LangChain Expression Language are "Runnables." Think of a runnable as a single step or a piece of a task in your larger AI application. Each runnable can take some input and produce some output. It's like a small machine that does one specific job.

Runnables are super important because they are the foundation for chain composition. You can connect these small machines together to build bigger, more complex machines. This modularity makes building LangChain applications very flexible. Everything in LCEL is a runnable, from simple prompts to complex models and tools.

#### Common Types of Runnables

Let's look at some common runnables you'll use all the time in the LangChain Expression Language. Understanding these will help you build your LLM chains effectively. These are the basic LEGO bricks we talked about earlier.

##### H3: Prompt Templates (ChatPromptTemplate)

A `ChatPromptTemplate` is a runnable that helps you create clear instructions for the AI. It allows you to mix fixed text with information you provide. This ensures the AI understands exactly what you want it to do. It’s like filling in the blanks on a form before giving it to someone.

For example, you can tell the AI to act as a helpful assistant. Then, you can provide the specific question you want it to answer. This makes your interactions with the AI very structured. It's a key part of effective LangChain Expression Language prompts.

```python
from langchain_core.prompts import ChatPromptTemplate

# Create a prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer all questions honestly and accurately."),
        ("user", "What is the capital of {country}?"),
    ]
)
```

In this snippet, `prompt` is now a runnable. It expects an input called `country`. When you give it a country, it will create a full set of instructions for the AI. This is a fundamental part of building dynamic LLM chains.

##### H3: Language Models (ChatOpenAI)

A `ChatOpenAI` runnable is how your application talks to powerful AI models like GPT-4. You send it a message, and it sends back a response. It's the brain of your LangChain application.

You can choose different models and settings, like how creative the AI should be. This gives you control over the AI's behavior. It’s a crucial component in any LangChain Expression Language setup.

```python
from langchain_openai import ChatOpenAI

# Create a language model instance
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
```

Here, `llm` is a runnable that takes messages (like the ones from our prompt) and returns AI-generated responses. The `temperature` setting controls randomness. A higher temperature means more creative answers, while a lower one makes answers more focused. This is essential for fine-tuning your LLM chains.

##### H3: Output Parsers (StrOutputParser)

An `StrOutputParser` is a runnable that helps you clean up the AI's answer. Sometimes, the AI gives back text that needs to be simplified or converted. This parser turns the AI's complex response into a simple string of text.

It's useful when you just need the core message from the AI. This makes it easier for other parts of your application to use the answer. It’s a common step in many LangChain Expression Language applications.

```python
from langchain_core.output_parsers import StrOutputParser

# Create an output parser
parser = StrOutputParser()
```

The `parser` runnable takes any input and tries to turn it into a simple string. For example, if the LLM returns a `HumanMessage` object, the parser extracts just the text content. This is great for making the output of your LLM chains more predictable.

### Connecting Runnables: The Pipe Operator (`|`)

Now that you know about individual runnables, let's learn how to connect them. The most common and powerful way to do this in LangChain Expression Language is using the pipe operator, `|`. This operator is super easy to understand and use.

The pipe operator `|` means "take the output from this runnable and send it as input to the next runnable." It's like connecting pipes in a plumbing system. Water flows from one pipe to the next. In LCEL, information flows from one runnable to the next.

#### Building Your First LCEL Chain

Let's combine our prompt, LLM, and parser using the pipe operator. This will create a simple but complete LangChain Expression Language chain. This chain will take a country, ask the AI about its capital, and then give us a plain text answer.

```python
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# 1. Define the Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Answer all questions concisely."),
        ("user", "What is the capital of {country}?"),
    ]
)

# 2. Define the Language Model
llm = ChatOpenAI(model="gpt-4o", temperature=0) # Use temperature=0 for consistent answers

# 3. Define the Output Parser
parser = StrOutputParser()

# 4. Chain them together using the pipe operator
chain = prompt | llm | parser

# 5. Invoke the chain
result = chain.invoke({"country": "France"})

print(result)
```

Let's break down this example step by step:

*   **`prompt | llm`**: This part takes the output of the `prompt` (which is a formatted message for the AI) and sends it directly to the `llm` (our OpenAI model). The LLM then processes this message.
*   **`llm | parser`**: The output from the `llm` (the AI's raw response) is then sent to the `parser`. The parser extracts just the text part of the AI's response. This gives us a clean, readable answer.
*   **`chain.invoke({"country": "France"})`**: This line runs the entire chain. We provide the input `{"country": "France"}` to the `prompt`. The prompt uses this to create the full message, which then flows through the `llm` and `parser`.
*   **Output**: You should see something like "Paris." This is the clean answer extracted by the parser.

This simple example demonstrates the power of the pipe operator for chain composition. You can easily see the flow of information. It creates a robust and readable LangChain Expression Language application.

#### A More Complex LCEL Chain Example

Let's create a slightly more complex chain. This chain will take a product name and generate a short, catchy slogan for it. We'll use a prompt, an LLM, and an output parser again. This is a common pattern for LLM chains.

```python
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Define the Prompt Template for slogan generation
slogan_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a creative marketing assistant. Generate short, catchy slogans."),
        ("user", "Create a slogan for a new product: {product_name}."),
    ]
)

# Define the Language Model (still OpenAI)
slogan_llm = ChatOpenAI(model="gpt-4o", temperature=0.9) # Higher temperature for creativity

# Define the Output Parser
slogan_parser = StrOutputParser()

# Chain them together
slogan_chain = slogan_prompt | slogan_llm | slogan_parser

# Invoke the chain with a product
product_name = "Eco-Friendly Water Bottle"
slogan_result = slogan_chain.invoke({"product_name": product_name})

print(f"Product: {product_name}")
print(f"Slogan: {slogan_result}")
```

In this example, we adjusted the system prompt to make the AI act as a marketing assistant. We also increased the `temperature` of the LLM to `0.9`. This encourages more creative and varied slogans. The structure of the LangChain Expression Language chain remains clean and easy to follow.

### Advanced Chain Composition with LCEL

LCEL isn't just for simple linear chains. It allows for much more complex and flexible chain composition. You can combine runnables in parallel, make choices, and pass information through. This makes building advanced LangChain applications much easier.

#### RunnablePassthrough: Passing Information Along

Sometimes you need to send some input data through a part of your chain without changing it. This is where `RunnablePassthrough` comes in handy. It literally just passes the input it receives directly to the next step. It's like a transparent section of pipe.

This is super useful when you have multiple inputs or want to preserve context. For example, you might want to send a user's question to the LLM. You might also want to send the original question along to an output formatter, even if the LLM only uses part of it. This is a powerful feature of LangChain Expression Language.

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

# Define prompt for summarization
summary_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert summarizer. Provide a brief summary of the text."),
        ("user", "Summarize the following text: {text}"),
    ]
)

# Define LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Define parser
parser = StrOutputParser()

# Define a chain that summarizes a text
summarize_chain = summary_prompt | llm | parser

# Now, let's create a chain that takes 'original_text' and 'question'
# It will summarize the text and also return the original question.

# We need a way to pass the original 'question' through while 'summarize_chain' only gets 'text'.
# We can use RunnablePassthrough and combine with other runnables.

combined_chain = (
    {
        "summary": summarize_chain, # This part gets the 'text' input implicitly from the full input
        "original_question": RunnablePassthrough(), # This passes the entire input through
        "original_text": RunnablePassthrough(), # Also passes the original text
    }
    |
    ChatPromptTemplate.from_template(
        "Here's the summary: {summary}\n"
        "And your original question was: {original_question}\n"
        "The text summarized was: {original_text}"
    )
    | llm
    | parser
)

# Invoke the combined chain
input_data = {
    "text": "The quick brown fox jumps over the lazy dog. This is a classic pangram. Pangrams are sentences that contain every letter of the alphabet at least once.",
    "original_question": "What was the initial question about this text?"
}
result = combined_chain.invoke(input_data)

print(result)
```

Let's break this down:

*   The `summarize_chain` expects an input named `text`.
*   The `combined_chain` starts with a dictionary `{}`, where keys are the names of outputs.
*   `"summary": summarize_chain`: This tells LCEL to run `summarize_chain`. By default, if `summarize_chain` expects `text`, LCEL will try to find a `text` key in the overall input (`input_data`).
*   `"original_question": RunnablePassthrough()`: This takes the entire input dictionary (`input_data`) and passes it through. Because it's assigned to `original_question`, only the `original_question` *key's value* from the input will be passed through to the next step.
*   `"original_text": RunnablePassthrough()`: Similarly, this will pass the `original_text` key's value from the initial input.
*   The output of this first dictionary block is a new dictionary: `{"summary": "...", "original_question": "...", "original_text": "..."}`.
*   This new dictionary is then passed to the final `ChatPromptTemplate`. The template uses the keys `summary`, `original_question`, and `original_text` to format the final output. This demonstrates how LangChain Expression Language handles complex input routing.

#### RunnableParallel: Doing Things at the Same Time

`RunnableParallel` allows you to run multiple runnables simultaneously. This is fantastic for speed! Imagine you want to ask two different questions to your AI at once. `RunnableParallel` makes it easy to do this.

It takes a dictionary where each key is a name for an output. Each value is a runnable that will run in parallel. The results are then combined into a dictionary. This is a very efficient way to build LLM chains.

```python
from langchain_core.runnables import RunnableParallel
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)
parser = StrOutputParser()

# Define two separate prompt templates
joke_prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}.")
fact_prompt = ChatPromptTemplate.from_template("Give me an interesting fact about {topic}.")

# Create two independent chains
joke_chain = joke_prompt | llm | parser
fact_chain = fact_prompt | llm | parser

# Combine them using RunnableParallel
# The input to this parallel runnable will be expected to have a 'topic' key.
combined_output_chain = RunnableParallel(
    joke=joke_chain,
    fact=fact_chain,
)

# Invoke the parallel chain
result = combined_output_chain.invoke({"topic": "cats"})

print(f"Joke about cats: {result['joke']}")
print(f"Fact about cats: {result['fact']}")
```

Here's how this works:

*   `joke_chain` and `fact_chain` are two independent LangChain Expression Language chains. Both expect a `topic` as input.
*   `RunnableParallel(joke=joke_chain, fact=fact_chain)` creates a new runnable.
*   When `combined_output_chain.invoke({"topic": "cats"})` is called, both `joke_chain` and `fact_chain` receive `{"topic": "cats"}` as input. They run at the same time.
*   The final `result` is a dictionary: `{'joke': '...', 'fact': '...'}`. This shows the power of parallel chain composition. This dramatically speeds up applications that require multiple independent queries.

#### RunnableSequence: Ensuring Order

While the pipe operator `|` inherently creates a sequence, `RunnableSequence` can sometimes be explicitly used. It's often used when you need to enforce a specific order of operations. It is particularly useful when you're passing a list of runnables.

For most cases, the pipe operator is cleaner for simple sequences. However, `RunnableSequence` provides another way to define ordered LLM chains. This is especially true if you are dynamically building the list of runnables.

```python
from langchain_core.runnables import RunnableSequence
# (Other imports as before)
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)
parser = StrOutputParser()

# Define a prompt template
greeting_prompt = ChatPromptTemplate.from_template("Say hello to {name} in a friendly way.")

# Create a RunnableSequence explicitly
explicit_sequence_chain = RunnableSequence(
    [
        greeting_prompt,
        llm,
        parser
    ]
)

# Invoke the chain
result = explicit_sequence_chain.invoke({"name": "Alice"})

print(result)
```

In this case, `explicit_sequence_chain` behaves exactly like `greeting_prompt | llm | parser`. The `RunnableSequence` constructor simply takes a list of runnables to execute in order. This is another way to express chain composition in LangChain Expression Language.

#### RunnableBranch: Making Decisions

`RunnableBranch` allows your chain to make decisions based on certain conditions. It's like an "if-else" statement for your LangChain Expression Language flow. You can specify a condition and then choose which runnable to execute if the condition is true, and which if it's false. This adds powerful logic to your LLM chains.

This is invaluable for creating dynamic and adaptive applications. For example, you might send an email to a support team if a user's query is marked as urgent. This flexibility is a core strength of LCEL.

```python
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)
parser = StrOutputParser()

# Define a runnable to check if the input contains "urgent"
# RunnableLambda allows you to wrap any Python function into a runnable
check_urgent = RunnableLambda(lambda x: "urgent" in x.lower())

# Define runnables for true and false branches
urgent_response = ChatPromptTemplate.from_template("Respond with 'URGENT: I will get back to you immediately regarding: {text}'.") | llm | parser
standard_response = ChatPromptTemplate.from_template("Respond with 'Thanks for your message: {text}'.") | llm | parser

# Create the RunnableBranch
# It takes a list of (condition, runnable) tuples, and a final fallback runnable.
branch_chain = RunnableBranch(
    (check_urgent, urgent_response), # If check_urgent is True, run urgent_response
    standard_response # Otherwise, run standard_response
)

# Invoke with an urgent message
result_urgent = branch_chain.invoke({"text": "I have an urgent question about my order."})
print(f"Urgent message response: {result_urgent}")

# Invoke with a standard message
result_standard = branch_chain.invoke({"text": "What are your operating hours?"})
print(f"Standard message response: {result_standard}")
```

Here's how `RunnableBranch` works:

*   `check_urgent` is a `RunnableLambda` that takes the input and returns `True` if "urgent" is found, `False` otherwise.
*   `urgent_response` is a chain for urgent messages.
*   `standard_response` is a chain for regular messages.
*   `RunnableBranch((check_urgent, urgent_response), standard_response)` means:
    *   First, run `check_urgent` on the input.
    *   If `check_urgent` returns `True`, then run `urgent_response` with the original input.
    *   If `check_urgent` returns `False`, then run `standard_response` with the original input.

This shows how you can build intelligent, conditional logic into your LangChain Expression Language applications. It's a powerful tool for complex LLM chains.

#### Using `bind`, `partial`, and `pick` for Flexibility

LCEL offers even more ways to modify and control your runnables. These functions allow you to tailor runnables without rewriting them. They provide fine-grained control over how information flows through your LLM chains.

##### H4: `.bind()`: Attaching Parameters

The `.bind()` method allows you to attach parameters to a runnable for all its invocations. Think of it as pre-setting some options for your runnable. For example, you can `bind` specific `stop` sequences or `functions` to your LLM.

This is useful when you want certain configurations to always apply to a specific runnable within a chain. It simplifies the definition of your LangChain Expression Language components.

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

# Original LLM
llm_original = ChatOpenAI(model="gpt-4o", temperature=0.7)

# LLM with 'stop' sequence bound
# The LLM will stop generating text if it encounters "Human:"
llm_with_stop = llm_original.bind(stop=["Human:"])

# Invoke original LLM (might generate more than desired)
message = HumanMessage(content="Write a short story about a brave knight.")
print("Original LLM Output:")
print(llm_original.invoke([message]).content)

# Invoke LLM with stop sequence
print("\nLLM with Stop Sequence Output:")
print(llm_with_stop.invoke([message]).content)
```

In this example:

*   `llm_original` is a standard `ChatOpenAI` instance.
*   `llm_with_stop` is a *new runnable* created by binding the `stop=["Human:"]` parameter to `llm_original`.
*   Now, whenever `llm_with_stop` is invoked, it will automatically use that `stop` parameter. This is a concise way to configure LLM chains.

##### H4: `.partial()`: Filling in Template Variables

The `.partial()` method is excellent for prompt templates. It lets you fill in some of the template variables in advance. This creates a "partially filled" template that only needs the remaining variables.

It's like having a form where some fields are already filled out. You only need to provide the rest of the information. This makes your prompts more reusable and flexible in LangChain Expression Language.

```python
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# Original prompt template
full_prompt = ChatPromptTemplate.from_template("Act as a {role}. Explain {topic} to a {level} audience.")

# Partially filled prompt for an "expert" role
expert_prompt = full_prompt.partial(role="expert")

# Now, expert_prompt only needs 'topic' and 'level'
result_prompt = expert_prompt.invoke({"topic": "quantum physics", "level": "beginner"})
print("Partially filled prompt output:")
print(result_prompt.messages[0].content)

# You can even partially fill more
beginner_expert_prompt = expert_prompt.partial(level="beginner")
final_result_prompt = beginner_expert_prompt.invoke({"topic": "AI"})
print("\nFurther partially filled prompt output:")
print(final_result_prompt.messages[0].content)
```

Here:

*   `full_prompt` requires `role`, `topic`, and `level`.
*   `expert_prompt` is created by calling `.partial(role="expert")` on `full_prompt`. Now, `expert_prompt` only needs `topic` and `level`.
*   This makes it easier to create specialized versions of your prompts without copying and pasting. This enhances chain composition.

##### H4: `.pick()`: Extracting Keys from Input/Output

The `.pick()` method allows you to select specific keys from a dictionary input or output. This is very useful when a runnable produces more information than you need for the next step. Or when you need to select a specific input from a larger dictionary.

It helps to streamline the data flow in your LangChain Expression Language chains. It ensures that each runnable receives only the information it requires.

```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)
parser = StrOutputParser()

# Let's say we have an input dictionary with user info and a question
# We only want to pass the 'question' to the LLM chain.

full_input_data = {
    "user_name": "Alice",
    "user_id": "123",
    "question": "What is the capital of Canada?"
}

# Define a simple Q&A chain
qa_chain = (
    ChatPromptTemplate.from_template("Answer the following question: {question}")
    | llm
    | parser
)

# Use .pick("question") to select only the 'question' key from the input
# And pass it to the qa_chain
final_chain = {"question": RunnablePassthrough()} | qa_chain

print("Output from chain with .pick('question'):")
result = final_chain.invoke(full_input_data)
print(result)

# Example: Picking from output (less common but possible)
# Imagine an LLM that outputs a dictionary (e.g., using PydanticOutputParser)
# For simplicity, let's simulate that here.
from langchain_core.runnables import RunnableLambda

def simulate_llm_output(input_dict):
    # This simulates an LLM returning a dict, maybe from a tool call or structured output.
    return {
        "answer": f"The capital of {input_dict['country']} is Ottawa.",
        "confidence": "high",
        "model_id": "gpt-4o"
    }

simulated_llm_chain = RunnableLambda(simulate_llm_output)

# Now, chain it and pick only the 'answer' from its output
answer_picker_chain = {"country": RunnablePassthrough()} | simulated_llm_chain.pick("answer")

print("\nOutput from chain picking 'answer' from simulated LLM output:")
result_pick_output = answer_picker_chain.invoke({"country": "Canada"})
print(result_pick_output)

```

In the first part of the example:

*   `{"question": RunnablePassthrough()}` takes the entire input `full_input_data`. It then creates an output dictionary `{"question": "What is the capital of Canada?"}`. This effectively `picks` the question.
*   This simplified dictionary is then passed to `qa_chain`, which only needs `question`. This makes sure `qa_chain` only gets relevant information.

In the second part, we use `.pick("answer")` directly on the `simulated_llm_chain`. This means that even if `simulated_llm_chain` produces a dictionary with `answer`, `confidence`, and `model_id`, only the value of the `answer` key is passed to the next stage. This cleans up the data flow in your LangChain Expression Language applications.

### LCEL in Action: Building Practical LLM Chains

Let's put everything we've learned into more practical, real-world scenarios. We'll build a few common types of LLM chains using LangChain Expression Language. These examples will show you how powerful and flexible LCEL can be.

#### Example 1: Basic Question Answering with LCEL

This is a fundamental use case. You provide a question, and the AI gives an answer. We'll use a `ChatPromptTemplate`, `ChatOpenAI`, and `StrOutputParser`. This is the basic pattern for many LLM chains.

```python
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Define the prompt template
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a highly knowledgeable AI assistant. Answer the user's question accurately and concisely."),
        ("user", "{question}"),
    ]
)

# Define the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Define the parser
parser = StrOutputParser()

# Create the QA chain
qa_chain = qa_prompt | llm | parser

# Invoke the chain with a question
question = "What is photosynthesis?"
answer = qa_chain.invoke({"question": question})

print(f"Question: {question}")
print(f"Answer: {answer}")
```

This LCEL tutorial example shows the simplest form of a LangChain Expression Language chain. The input dictionary `{"question": question}` flows into the `qa_prompt`. The prompt prepares the message, sends it to the `llm`, and the `parser` cleans the output. It's clean, efficient, and easy to read.

#### Example 2: Content Generation with Specific Tone

Sometimes you need the AI to generate text with a specific style or tone. LCEL makes it easy to incorporate this into your LangChain applications. We'll ask for a short story with a "whimsical" tone.

```python
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Define the prompt template with tone parameter
story_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a creative storyteller. Write a very short story with a {tone} tone."),
        ("user", "The story should be about: {topic}."),
    ]
)

# Define the LLM (higher temperature for creativity)
llm = ChatOpenAI(model="gpt-4o", temperature=0.8)

# Define the parser
parser = StrOutputParser()

# Create the story generation chain
story_chain = story_prompt | llm | parser

# Invoke the chain with topic and tone
topic = "a talking squirrel"
tone = "whimsical"
story_output = story_chain.invoke({"topic": topic, "tone": tone})

print(f"Story about: {topic} (Tone: {tone})")
print(story_output)
```

In this example, the `story_prompt` expects both a `topic` and a `tone`. The LCEL chain composition remains straightforward. You just pass both pieces of information in your input dictionary. The AI then generates the story according to your specifications. This highlights the flexibility of LangChain Expression Language prompts.

#### Example 3: Simple Retrieval Augmented Generation (RAG) Chain

RAG is a powerful technique where you give the AI extra information to help it answer questions. Imagine you have a document and want the AI to answer questions *only* based on that document. This is where a RAG system shines.

For this LCEL tutorial example, we'll simplify it by using a fixed "document" for now. In a real RAG system, you would retrieve relevant document snippets from a database (like a vector store). You can learn more about RAG systems in our blog post on [Building a Basic RAG System with LangChain](/blog/building-a-basic-rag-system-with-langchain-tutorial).

```python
import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# Simulate a "retriever" that provides context (for a real RAG, this would query a vector DB)
def get_context(question):
    # In a real app, this would query a database for relevant docs
    return {
        "context": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower. Constructed from 1887 to 1889, it was originally built as the entrance arch to the 1889 World's Fair. It is the most-visited paid monument in the world."
    }

# Convert get_context into a runnable
context_retriever = RunnablePassthrough.assign(context=get_context)

# Define the prompt template for RAG
rag_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI assistant. Use the provided context to answer the question. If the answer is not in the context, say 'I don't know.'\n\nContext:\n{context}"),
        ("user", "Question: {question}"),
    ]
)

# Define the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Define the parser
parser = StrOutputParser()

# Create the RAG chain
# We need to ensure that both 'question' and 'context' are available for the prompt.
rag_chain = (
    # This prepares the input: it takes the original 'question'
    # and adds 'context' to it by running get_context.
    # The output of this step will be {"question": "...", "context": "..."}
    RunnablePassthrough.assign(context=RunnablePassthrough(lambda x: get_context(x["question"])["context"]))
    | rag_prompt
    | llm
    | parser
)

# Invoke the RAG chain
question_eiffel = "Who designed the Eiffel Tower?"
answer_eiffel = rag_chain.invoke({"question": question_eiffel})
print(f"Question: {question_eiffel}")
print(f"Answer: {answer_eiffel}")

question_aliens = "Are there aliens on Mars?"
answer_aliens = rag_chain.invoke({"question": question_aliens})
print(f"\nQuestion: {question_aliens}")
print(f"Answer: {answer_aliens}")
```

Let's break down the `rag_chain` carefully:

*   `RunnablePassthrough.assign(context=RunnablePassthrough(lambda x: get_context(x["question"])["context"]))`: This is where the magic happens for providing context.
    *   The outer `RunnablePassthrough.assign` is for adding new keys to the input dictionary.
    *   `context=` means we're adding a key named `context`.
    *   `RunnablePassthrough(lambda x: get_context(x["question"])["context"])` is the value for `context`. This `RunnablePassthrough` takes the entire input (`x` which is `{"question": "..."}`). It then calls `get_context` with `x["question"]` and extracts the `context` string.
    *   So, if the input is `{"question": "Who designed the Eiffel Tower?"}`, this whole step transforms it into `{"question": "Who designed the Eiffel Tower?", "context": "The Eiffel Tower is..."}`.
*   This modified dictionary is then passed to `rag_prompt`. The prompt uses both `{question}` and `{context}`.
*   The rest of the chain (`llm | parser`) is standard.

This shows how powerful `RunnablePassthrough.assign` is for manipulating data flowing through your LangChain Expression Language applications. It's a cornerstone for building advanced LLM chains like RAG.

#### Example 4: Creating a Sequential Tool-Using Agent with LCEL (Conceptual)

While full agents are complex, LCEL makes the *composition* of agent-like behavior easier. Here, we'll conceptually outline how you might use LCEL to combine an LLM with a simple "tool." A tool could be a calculator, a search engine, or a database query.

Imagine we want to answer questions that require both general knowledge and a specific lookup. For a real agent, you might use a tool that interacts with a specific API. You can read more about tools and agents in LangChain's official documentation for a deeper dive. This LCEL tutorial focuses on how to chain them.

```python
from langchain_core.runnables import RunnableLambda, RunnableBranch, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0)
parser = StrOutputParser()

# --- Define a "tool" (simulated) ---
def lookup_capital(country: str) -> str:
    capitals = {
        "france": "Paris",
        "germany": "Berlin",
        "japan": "Tokyo",
        "canada": "Ottawa"
    }
    return capitals.get(country.lower(), "Unknown. I can only find capitals for a few specific countries.")

# Wrap the tool in a RunnableLambda so it can be part of an LCEL chain
capital_tool = RunnableLambda(lookup_capital)

# --- Define a simple classification chain to decide if a tool is needed ---
classification_prompt = ChatPromptTemplate.from_template(
    "Is the following question about a country's capital? Answer 'yes' or 'no'.\nQuestion: {question}"
)
classifier_chain = classification_prompt | llm | parser

# --- Define a chain for when the tool IS needed ---
tool_use_chain = (
    # Pass the original question through, but extract the country for the tool
    {"country": RunnablePassthrough.assign(country_name=RunnableLambda(lambda x: x["question"].split("of ")[-1].replace("?", "").strip())) | (lambda x: x["country_name"])}
    | capital_tool
)

# Define a chain for when the tool IS NOT needed (general LLM answer)
general_qa_chain = (
    ChatPromptTemplate.from_template("Answer the question: {question}")
    | llm
    | parser
)

# --- Combine with RunnableBranch ---
# This is where the decision-making happens.
full_agent_chain = (
    RunnablePassthrough.assign(
        # First, classify the question
        is_capital_question=classifier_chain
    )
    | RunnableBranch(
        (lambda x: "yes" in x["is_capital_question"].lower(), tool_use_chain),
        general_qa_chain # If not a capital question, use general LLM
    )
)

# --- Test the agent ---
print("--- Capital Question Test ---")
question_capital = "What is the capital of France?"
result_capital = full_agent_chain.invoke({"question": question_capital})
print(f"Question: {question_capital}")
print(f"Answer: {result_capital}")

print("\n--- General Question Test ---")
question_general = "What is the color of the sky?"
result_general = full_agent_chain.invoke({"question": question_general})
print(f"Question: {question_general}")
print(f"Answer: {result_general}")

print("\n--- Unknown Capital Test ---")
question_unknown_capital = "What is the capital of Mars?"
result_unknown_capital = full_agent_chain.invoke({"question": question_unknown_capital})
print(f"Question: {question_unknown_capital}")
print(f"Answer: {result_unknown_capital}")
```

This is a more advanced example of chain composition, leveraging `RunnableBranch` and `RunnableLambda`.

*   **`capital_tool`**: A simple Python function wrapped as a `RunnableLambda`. It simulates looking up a capital.
*   **`classifier_chain`**: A simple LCEL chain that takes a `question` and outputs "yes" or "no" if it's about a capital.
*   **`tool_use_chain`**: This chain extracts the country name from the question (e.g., "France" from "What is the capital of France?"). It then passes this country name to the `capital_tool`.
    *   `{"country": ...}`: This part ensures the `capital_tool` receives a dictionary with a `country` key.
    *   `RunnablePassthrough.assign(...)`: This extracts the country name from the input question.
    *   `| (lambda x: x["country_name"])`: This is a simple lambda to extract *just* the `country_name` string from the dict created by `assign`, to pass it as a direct string to `capital_tool`.
*   **`general_qa_chain`**: A standard LLM chain for general questions.
*   **`full_agent_chain`**: This is the core decision-making part.
    *   It first uses `RunnablePassthrough.assign` to run `classifier_chain` and store its output as `is_capital_question`.
    *   Then, `RunnableBranch` uses the value of `is_capital_question` to decide whether to run `tool_use_chain` (if it's a capital question) or `general_qa_chain` (otherwise).

This demonstrates how LangChain Expression Language facilitates building complex decision-making into your LLM chains, mimicking agent behavior. You can chain various runnables to create sophisticated logic.

### Benefits of Using LCEL: A Summary

By now, you've seen many examples of LCEL in action. Let's recap why LangChain Expression Language is such a powerful tool for developing your LLM chains and LangChain applications.

#### Performance

LCEL chains are designed for performance right from the start. They can execute steps in parallel whenever possible. This means your applications can run much faster, especially for tasks that have independent parts. For instance, `RunnableParallel` takes advantage of this by firing off multiple API calls simultaneously.

#### Streaming

LCEL supports streaming outputs from your LLMs and other runnables. Instead of waiting for the entire response, you can get parts of it as they are generated. This makes your applications feel much more responsive to users. It's like watching a live stream instead of downloading a whole video first.

#### Asynchronous Support

You can run LCEL chains using `async` and `await` in Python. This means your application can do other things while waiting for an AI model to respond. It makes your LangChain applications more efficient and prevents them from freezing. This is crucial for web applications or complex backend systems.

#### Batching

LCEL can process multiple inputs in a single call, which is called batching. Instead of sending one question at a time, you can send a list of questions. This can be significantly faster and more cost-effective for interacting with AI models. It's like sending a big package instead of many small ones.

#### Fallbacks and Retries

LCEL includes built-in features for handling errors gracefully. You can configure runnables to retry if they fail, or to switch to a "fallback" runnable if the primary one doesn't work. This makes your LangChain Expression Language chains much more robust and reliable. Your application won't crash if an external service temporarily goes down.

#### Observability

Debugging and monitoring complex LLM chains can be tough. LCEL provides excellent observability features, especially when combined with tools like LangSmith. You can easily trace how data flows through your chain, inspect inputs and outputs at each step, and identify bottlenecks or errors. This deep insight is invaluable for developing and optimizing your LangChain applications.

### Conclusion

Congratulations! You've completed this comprehensive LCEL tutorial. You've learned what LangChain Expression Language is, why it's so important, and how to use its core components. You can now build simple to complex LLM chains. You understand runnables, the pipe operator, and advanced chain composition techniques.

LCEL is a cornerstone of modern LangChain development. It provides a flexible, powerful, and observable way to build AI applications. With this knowledge, you are well-equipped to create sophisticated LangChain applications. Start experimenting with LCEL today and unlock the full potential of large language models.

Remember, the best way to learn is by doing. Try creating your own LangChain Expression Language chains for different tasks. Explore the official LangChain documentation for even more advanced features. Happy coding!