---
title: "Fine-Tune LangChain Agents: Boost Tool-Calling Accuracy with SFT/DPO"
description: "Master LangChain Tool-Calling Fine-tuning and learn SFT/DPO techniques to boost agent accuracy and reliability for your Python AI projects."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: ["LangChain", "AI Agents", "Fine-Tuning", "Python", "Tool Calling"]
featured: false
image: '/assets/images/langchain-tool-calling-fine-tuning.webp'
---
## Fine-Tune LangChain Agents: Boost Tool-Calling Accuracy with SFT/DPO

Optimize agent tool performance and transform your LangChain agents from merely functional to exceptionally reliable. While prompt engineering offers a good starting point, achieving consistent and accurate tool utilization often requires a deeper intervention. This guide will show you how to leverage Supervised Fine-Tuning (SFT) and Direct Preference Optimization (DPO) to dramatically improve your LangChain agent's tool-calling accuracy, giving them a sharper understanding of when and how to invoke specific functions.

### The Challenge of Agent Tool Use in LangChain

LangChain agents empower Large Language Models (LLMs) to interact with external tools, enabling them to perform actions beyond their core knowledge base. This capability is crucial for building powerful applications like customer service bots, data analysis assistants, or automated research agents. However, out-of-the-box LLMs can sometimes struggle with precise tool invocation.

They might hallucinate non-existent tools, fail to call a tool when necessary, or extract incorrect arguments from user prompts. These inconsistencies lead to unreliable agent behavior, frustrating user experiences, and broken workflows. Relying solely on system prompts or few-shot examples often hits a ceiling when dealing with complex, nuanced, or domain-specific tool-calling scenarios.

### Why Fine-Tune for LangChain Tool-Calling Accuracy?

While sophisticated prompt engineering can guide an LLM, it essentially tries to "trick" the model into generating the desired output. This approach often falls short for highly specific or robust tool-calling requirements. Fine-tuning, on the other hand, fundamentally changes the model's internal representations and biases, teaching it new patterns for tool invocation.

LLM fine-tuning trains the model directly on examples of correct tool usage, enabling it to better understand the semantics of your tools and the appropriate conditions for their activation. This process significantly boosts the precision and recall of tool selection and argument extraction. By directly embedding the desired behavior into the model weights, you create agents that are more robust and less prone to errors in diverse real-world scenarios.

### Understanding LangChain Agents and Tool Interaction

Before diving into fine-tuning, let's briefly recap how LangChain agents utilize tools. In LangChain, an agent typically consists of an LLM, a set of tools, and an agent executor that orchestrates their interaction. The LLM's role is to decide which tool to call (if any) and with what arguments, based on the user's input and its internal reasoning.

The LLM receives a prompt containing the user's query, descriptions of available tools, and possibly a conversation history. It then generates a response that often includes a `tool_code` or `function_call` structure, which the LangChain framework parses and executes. For a deeper dive into LangChain fundamentals, check out our [LangChain Python Complete Guide]({% post_url 2026-11-15-langchain-python-complete-guide %}).

When an agent misinterprets the user's intent or incorrectly structures the tool call, it leads to errors. This is where specialized LangChain Tool-Calling Fine-tuning comes in, directly addressing these decision-making shortcomings.

### Supervised Fine-Tuning (SFT) for Precise Tool Calls

Supervised Fine-Tuning (SFT) is a straightforward yet powerful technique for improving tool-calling accuracy. You provide the model with explicit input-output pairs, where the input is a user query and tool descriptions, and the output is the *exact* desired tool call in the model's native function-calling format. This direct instruction helps the LLM learn to map specific user intents to precise tool invocations.

#### Data Preparation for SFT

The core of SFT is a high-quality dataset. For tool calling, each data point should ideally consist of:

1.  **User Input (Prompt):** The user's natural language query.
2.  **Tool Definitions:** The JSON schema or Pydantic definitions of the tools available to the agent.
3.  **Expected Tool Call:** The correct tool name and its arguments, formatted as the LLM would generate it (e.g., in OpenAI's function calling format).

Let's illustrate with an example of how you might structure this data.

**Example Tool Definition:**

```python
{% raw %}
from langchain_core.tools import tool

@tool
def get_weather(city: str, unit: str = "celsius") -> dict:
    """
    Retrieves the current weather for a specified city.
    Args:
        city (str): The name of the city.
        unit (str, optional): The unit of temperature (celsius or fahrenheit). Defaults to "celsius".
    """
    if city.lower() == "london":
        return {"city": city, "temperature": 15, "unit": unit, "conditions": "cloudy"}
    elif city.lower() == "new york":
        return {"city": city, "temperature": 20, "unit": unit, "conditions": "sunny"}
    else:
        return {"city": city, "temperature": 18, "unit": unit, "conditions": "partly cloudy"}

@tool
def search_database(query: str) -> list[dict]:
    """
    Searches a product database for items matching the query.
    Args:
        query (str): The search query for products.
    """
    if "laptop" in query.lower():
        return [{"name": "Laptop Pro X", "price": 1200}, {"name": "Laptop Lite", "price": 800}]
    return [{"name": "Generic Item", "price": 50}]
{% endraw %}
```

**SFT Training Example Format (simplified for illustration, actual format depends on model):**

Many models, especially those fine-tuned for function calling, expect a specific chat-like format for training. For example, an OpenAI-compatible format might look like this:

```json
{% raw %}
[
  {
    "messages": [
      {"role": "user", "content": "What's the weather like in London?"},
      {
        "role": "assistant",
        "tool_calls": [
          {
            "id": "call_123",
            "function": {
              "name": "get_weather",
              "arguments": "{\"city\": \"London\"}"
            },
            "type": "function"
          }
        ]
      }
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "Find me some laptops, please."},
      {
        "role": "assistant",
        "tool_calls": [
          {
            "id": "call_456",
            "function": {
              "name": "search_database",
              "arguments": "{\"query\": \"laptops\"}"
            },
            "type": "function"
          }
        ]
      }
    ]
  },
  {
    "messages": [
      {"role": "user", "content": "Tell me a joke."},
      {
        "role": "assistant",
        "content": "Why don't scientists trust atoms? Because they make up everything!"
      }
    ]
  }
]
{% endraw %}
```

Notice the third example where no tool is called. It's crucial to include examples where the model should *not* call a tool, teaching it when to respond directly. Tools are usually passed to the model as part of the system prompt or tool descriptions within the prompt context.

#### Model Selection and Training Process

You can start with a base LLM that has some initial function-calling capabilities, or even a general-purpose model. Models like Llama-2, Mistral, or even smaller specialized models are excellent candidates. For efficient fine-tuning, especially on consumer-grade GPUs, techniques like LoRA (Low-Rank Adaptation) or QLoRA (Quantized LoRA) are highly recommended.

The training process involves feeding your prepared dataset to a SFT trainer, often using libraries like Hugging Face `transformers` and `trl` (Transformer Reinforcement Learning). The model learns to predict the correct tool call given the input.

**Conceptual SFT Code Snippet (using `trl` for Llama-2-like models):**

This example provides a high-level overview. For a complete training script, you would typically use `accelerate` for distributed training and ensure proper tokenizer configuration.

```python
{% raw %}
# pip install transformers trl peft bitsandbytes accelerate
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer
import json


<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2784742237479601"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-2784742237479601"
     data-ad-slot="7340313511"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>


# 1. Load a base model and tokenizer
model_id = "NousResearch/Llama-2-7b-chat-hf" # Example model
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token # Essential for Llama models

# Quantization config for QLoRA
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=False,
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    use_cache=False # Important for training
)
model.config.pretraining_tp = 1 # Important for Llama 2

# LoRA config
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"], # Common target for Llama-2, adjust as needed
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# 2. Prepare your SFT dataset
# For simplicity, let's use the JSON structure defined above.
# In a real scenario, you'd load from a file or generate.
sft_data_raw = [
    {
        "messages": [
            {"role": "user", "content": "What's the weather like in London?"},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_123",
                        "function": {
                            "name": "get_weather",
                            "arguments": "{\"city\": \"London\"}"
                        },
                        "type": "function"
                    }
                ]
            }
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Find me some laptops, please."},
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_456",
                        "function": {
                            "name": "search_database",
                            "arguments": "{\"query\": \"laptops\"}"
                        },
                        "type": "function"
                    }
                ]
            }
        ]
    },
    {
        "messages": [
            {"role": "user", "content": "Tell me a joke."},
            {
                "role": "assistant",
                "content": "Why don't scientists trust atoms? Because they make up everything!"
            }
        ]
    }
]

# Convert messages to chat format expected by tokenizer
# This function formats messages similar to OpenAI's chat completion API.
def format_chat_template(example):
    # This is a simplified example. Real-world would involve converting tool_calls to text
    # that the model expects for function calling. For Llama-2, this might be
    # <tool_code>...<call:tool_name>...<args>...</args></call:tool_name>... </tool_code>
    # or similar.
    # For now, let's just make a very basic text representation.
    formatted_messages = []
    for msg in example["messages"]:
        if "tool_calls" in msg:
            tool_calls_text = ""
            for tc in msg["tool_calls"]:
                tool_calls_text += f"<tool_code><call: {tc['function']['name']}>{tc['function']['arguments']}</call: {tc['function']['name']}></tool_code>"
            formatted_messages.append({"role": "assistant", "content": tool_calls_text})
        elif msg["role"] == "assistant" and "content" in msg and msg["content"] is not None:
             formatted_messages.append({"role": "assistant", "content": msg["content"]})
        else:
             formatted_messages.append(msg) # Assume user messages are fine

    # Use the tokenizer's chat template for proper formatting
    # IMPORTANT: You need a tokenizer with a chat template that supports tool calls.
    # Llama-2's default template might not directly support OpenAI-style tool_calls.
    # You might need to adjust the template or pre-process tool calls into a textual format
    # that the model understands, e.g., via a prompt template.
    try:
        # This will convert a list of dicts like [{"role": "user", "content": "..."}]
        # into a single string formatted for the model, e.g., "<s>[INST]...[/INST]..."
        return {"text": tokenizer.apply_chat_template(formatted_messages, tokenize=False, add_generation_prompt=False)}
    except Exception as e:
        print(f"Error applying chat template: {e}")
        print(f"Messages causing error: {formatted_messages}")
        return {"text": ""}

# Create a Hugging Face Dataset
dataset = Dataset.from_list(sft_data_raw)
dataset = dataset.map(format_chat_template, remove_columns=["messages"])
dataset = dataset.filter(lambda x: x["text"] != "") # Filter out empty examples

# 3. Setup SFTTrainer
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=1,
    gradient_checkpointing=True,
    logging_steps=10,
    save_strategy="epoch",
    learning_rate=2e-4,
    fp16=True, # Use FP16 for faster training if supported
    max_grad_norm=0.3,
    warmup_ratio=0.03,
    lr_scheduler_type="constant",
    report_to="tensorboard", # Or "wandb" for tracking (Internal Link: {% post_url 2026-11-12-langchain-langsmith-wandb-tutorial %})
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=lora_config,
    max_seq_length=512, # Adjust based on your data
    tokenizer=tokenizer,
    args=training_args,
    packing=False, # Set to True for packing multiple short examples into one sequence
    formatting_func=None, # We already formatted using .map()
)

# 4. Train the model
trainer.train()

# 5. Save the fine-tuned adapter
trainer.model.save_pretrained("./fine_tuned_llama_agent")
tokenizer.save_pretrained("./fine_tuned_llama_agent")

print("SFT Training complete! Model saved to ./fine_tuned_llama_agent")
{% endraw %}
```

**Important Note on Chat Templates and Tool Calling:** The `tokenizer.apply_chat_template` is crucial. For function calling, your tokenizer's template (or a custom `formatting_func` in `SFTTrainer`) needs to correctly convert the tool call JSON into a text format that the model was originally trained to understand as a function call. Many open-source models (like Llama-2) do not inherently have OpenAI-style `tool_calls` in their chat templates. You might need to:
1.  Use a model specifically pre-trained for function calling (e.g., certain fine-tunes of Mistral or Llama).
2.  Manually convert the `tool_calls` JSON into a specific textual format (e.g., `<tool_code>...</tool_code>`) that you then train the model to generate, and then write a custom parser in LangChain.
3.  Use `transformers` `FunctionCallingTokenizer` if available for your model.

### Direct Preference Optimization (DPO) for Refined Tool Usage

While SFT is excellent for teaching the *how*, Direct Preference Optimization (DPO) excels at teaching the *what's better*. DPO is a form of Reinforcement Learning from Human Feedback (RLHF) that doesn't require a separate reward model. Instead, it directly optimizes the LLM based on pairwise preferences between a "chosen" (good) response and a "rejected" (bad) response for a given prompt. This is especially powerful for refining nuanced behaviors like handling ambiguous queries or avoiding hallucinated tool calls.

#### Data Preparation for DPO

For DPO, your dataset should consist of triplets:

1.  **Prompt:** The user's query and available tool descriptions.
2.  **Chosen Response:** The preferred, correct tool call (or a direct answer if no tool is needed).
3.  **Rejected Response:** An undesirable response, such as:
    *   Calling the wrong tool.
    *   Calling the correct tool with incorrect arguments.
    *   Hallucinating a non-existent tool.
    *   Failing to call a tool when one was needed.
    *   Calling a tool when a direct answer was appropriate.

**DPO Training Example Format (simplified for illustration):**

```json
{% raw %}
[
  {
    "prompt": "What's the weather in London today?",
    "chosen": "<tool_code><call:get_weather>{\"city\": \"London\"}</call:get_weather></tool_code>",
    "rejected": "<tool_code><call:get_weather>{\"city\": \"Lonon\"}</call:get_weather></tool_code>"
  },
  {
    "prompt": "Tell me about cars.",
    "chosen": "Cars are a common mode of transport...",
    "rejected": "<tool_code><call:search_database>{\"query\": \"cars\"}</call:search_database></tool_code>"
  },
  {
    "prompt": "What's the price of a Tesla?",
    "chosen": "<tool_code><call:search_database>{\"query\": \"Tesla\"}</call:search_database></tool_code>",
    "rejected": "I cannot provide real-time stock prices."
  }
]
{% endraw %}
```

Again, the `chosen` and `rejected` responses would need to be in the specific text format your model expects for tool calls.

#### Training Process with DPO

DPO builds upon a pre-trained or SFT-tuned model. The `DPO_Trainer` from `trl` simplifies this process significantly. It computes a loss based on the preference pairs, effectively pushing the model to generate responses similar to the `chosen` ones and dissimilar to the `rejected` ones. This process fine-tunes the LLM to align better with desired agent behavior, leading to a substantial boost in tool-calling accuracy and robustness.

**Conceptual DPO Code Snippet (using `trl`):**

```python
{% raw %}
# Assuming you have a base model or an SFT-tuned model loaded
# and a tokenizer.
# Model and tokenizer setup is similar to SFT example.
# Let's assume `model` and `tokenizer` are loaded from the SFT step.

from trl import DPOTrainer

# 1. Prepare your DPO dataset
dpo_data_raw = [
    {
        "prompt": "What's the weather in London today?",
        "chosen": "<tool_code><call:get_weather>{\"city\": \"London\"}</call:get_weather></tool_code>",
        "rejected": "<tool_code><call:get_weather>{\"city\": \"Lonon\"}</call:get_weather></tool_code>"
    },
    {
        "prompt": "Tell me about cars.",
        "chosen": "Cars are a common mode of transport...",
        "rejected": "<tool_code><call:search_database>{\"query\": \"cars\"}</call:search_database></tool_code>"
    },
    {
        "prompt": "What's the price of a Tesla?",
        "chosen": "<tool_code><call:search_database>{\"query\": \"Tesla\"}</call:search_database></tool_code>",
        "rejected": "I cannot provide real-time stock prices."
    }
]

# Convert raw data to Hugging Face Dataset format, tokenizing the prompt, chosen, and rejected responses.
# IMPORTANT: The prompt and response format here must match what your base/SFT model expects.
# For chat models, it typically means formatting with the tokenizer's chat template.
def format_dpo_example(example):
    # This is simplified. In reality, you'd apply the tokenizer's chat template
    # to format the 'prompt', 'chosen', and 'rejected' strings.
    # The 'prompt' needs to include the system message and tool definitions.
    # For instance:
    # prompt_text = tokenizer.apply_chat_template([{"role": "user", "content": example["prompt"]}], tokenize=False)
    # chosen_text = tokenizer.apply_chat_template([{"role": "assistant", "content": example["chosen"]}], tokenize=False, add_generation_prompt=False)
    # rejected_text = tokenizer.apply_chat_template([{"role": "assistant", "content": example["rejected"]}], tokenize=False, add_generation_prompt=False)
    # The actual content of `chosen` and `rejected` should be the model's direct output (e.g., tool_code tags).

    # For this example, let's assume the prompt and responses are already in the final textual format.
    return {
        "prompt": example["prompt"],
        "chosen": example["chosen"],
        "rejected": example["rejected"]
    }

dpo_dataset = Dataset.from_list(dpo_data_raw).map(format_dpo_example)

# 2. Setup DPOTrainer
dpo_training_args = TrainingArguments(
    output_dir="./dpo_results",
    num_train_epochs=1,
    per_device_train_batch_size=2, # DPO often uses smaller batches
    gradient_accumulation_steps=1,
    gradient_checkpointing=True,
    logging_steps=10,
    save_strategy="epoch",
    learning_rate=5e-5, # DPO learning rate is often smaller
    fp16=True,
    report_to="tensorboard",
)


<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2784742237479601"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-2784742237479601"
     data-ad-slot="7340313511"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>


dpo_trainer = DPOTrainer(
    model=model, # Use the SFT-tuned model or the base model
    ref_model=None, # If None, `model` is cloned to be the reference model
    args=dpo_training_args,
    train_dataset=dpo_dataset,
    tokenizer=tokenizer,
    peft_config=lora_config, # If using LoRA
    max_length=512,
    max_prompt_length=256, # Max length for the prompt part
)

# 3. Train the DPO model
dpo_trainer.train()

# 4. Save the DPO fine-tuned adapter
dpo_trainer.model.save_pretrained("./dpo_fine_tuned_llama_agent")
tokenizer.save_pretrained("./dpo_fine_tuned_llama_agent") # Save tokenizer again just in case

print("DPO Training complete! Model saved to ./dpo_fine_tuned_llama_agent")
{% endraw %}
```

### Architecture for Fine-Tuned LangChain Agents

The architectural shift with fine-tuning is minimal but impactful. Instead of using a generic, pre-trained LLM as the brain of your agent, you simply swap it out with your custom fine-tuned model. The LangChain agent framework handles the integration seamlessly.

Consider the flow:

| Component                 | Description                                                                     | Role in Fine-tuning                                          |
| :------------------------ | :------------------------------------------------------------------------------ | :----------------------------------------------------------- |
| **User Input**            | Natural language query from the end-user.                                       | Input for generating training examples.                      |
| **LangChain Agent Executor** | Orchestrates the agent's reasoning loop (plan, act, observe).                   | Remains the same; manages flow regardless of LLM.            |
| **Fine-Tuned LLM (SFT/DPO)** | Your custom model, trained to understand and generate specific tool calls.      | **Replaces the base LLM**, providing superior tool-calling logic. |
| **Tool Definitions**      | Schemas and descriptions of available functions (e.g., `get_weather`, `search_database`). | Provided to the LLM as context during inference and training. |
| **Tool Execution**        | Actual execution of the chosen tool, returning results to the agent.            | Remains the same; external tools are unchanged.              |
| **Observation**           | Results from tool execution, fed back into the agent's context.                 | Informs subsequent LLM reasoning steps.                      |
| **Agent Response**        | Final answer or action provided to the user.                                    | Improved accuracy due to better tool calls.                  |

This architecture ensures that the boosted tool-calling accuracy from your LLM fine-tuning directly translates into more reliable and effective agent behavior.

### Integrating Fine-Tuned Models with LangChain

Once you've fine-tuned and saved your model (e.g., in a local directory or uploaded to Hugging Face Hub), integrating it into LangChain is straightforward. You'll load your custom model and tokenizer, wrap it in a LangChain-compatible LLM interface, and then use it to construct your agent.

**Example: Loading and Using a Fine-Tuned Model with LangChain:**

This example assumes your fine-tuned model understands a text-based function calling format (e.g., using `<tool_code>` tags) and that you have a custom parser for it. For models natively supporting OpenAI-style function calling, the integration might be simpler using `ChatOpenAI(model=...)` with a local server or a compatible client.

```python
{% raw %}
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.llms import HuggingFacePipeline
from transformers import pipeline

# --- 1. Define Tools (same as before) ---
@tool
def get_weather(city: str, unit: str = "celsius") -> dict:
    """
    Retrieves the current weather for a specified city.
    Args:
        city (str): The name of the city.
        unit (str, optional): The unit of temperature (celsius or fahrenheit). Defaults to "celsius".
    """
    if city.lower() == "london":
        return {"city": city, "temperature": 15, "unit": unit, "conditions": "cloudy"}
    elif city.lower() == "new york":
        return {"city": city, "temperature": 20, "unit": unit, "conditions": "sunny"}
    else:
        return {"city": city, "temperature": 18, "unit": unit, "conditions": "partly cloudy"}

@tool
def search_database(query: str) -> list[dict]:
    """
    Searches a product database for items matching the query.
    Args:
        query (str): The search query for products.
    """
    if "laptop" in query.lower():
        return [{"name": "Laptop Pro X", "price": 1200}, {"name": "Laptop Lite", "price": 800}]
    return [{"name": "Generic Item", "price": 50}]

tools = [get_weather, search_database]

# --- 2. Load Fine-Tuned Model ---
# Assuming you saved your model in './dpo_fine_tuned_llama_agent'
fine_tuned_model_path = "./dpo_fine_tuned_llama_agent"

# Reload the base model and then load the LoRA adapter
model_id = "NousResearch/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(fine_tuned_model_path) # Load fine-tuned tokenizer
tokenizer.pad_token = tokenizer.eos_token

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=False,
)

base_model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Load the fine-tuned adapter weights
from peft import PeftModel
model = PeftModel.from_pretrained(base_model, fine_tuned_model_path)
model = model.merge_and_unload() # Merge LoRA weights into the base model for inference

# Create a HuggingFace pipeline for the model
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.7,
    do_sample=True,
    top_p=0.95,
    repetition_penalty=1.1,
    pad_token_id=tokenizer.eos_token_id, # Important for consistent generation
)

# Wrap the pipeline in LangChain's HuggingFacePipeline LLM
llm = HuggingFacePipeline(pipeline=pipe)

# --- 3. Define the Prompt Template ---
# This is a simplified example. A real-world prompt would convert tools to a structured format
# that the LLM expects for function calling, potentially using the agent's format_tools helper.
# For Llama-2-chat, it often uses specific INST/<<SYS>> tags.
# You need to ensure your prompt format matches how you fine-tuned your model.

# This is a generic React-style prompt for illustration.
# The tool descriptions would be injected into the `input` by `create_react_agent`.
prompt_template_str = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

{input}
{agent_scratchpad}
"""

# LangChain's create_react_agent automatically formats tools and tool names.
# For a custom fine-tuned model, you might need a custom parser or prompt construction.
# The following prompt is a basic example. You would adapt it to your model's exact finetuning format.
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI assistant. You have access to the following tools: {tools}
            You should always think about what to do.
            Use the following format for your responses:
            Thought: I need to use a tool to answer this question.
            Action: tool_name
            Action Input: {{arg_name: arg_value}}
            Observation: tool_output
            ...
            Thought: I now know the final answer.
            Final Answer: final_answer
            """
        ),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

# --- 4. Create the Agent ---
# For custom models, you might need to implement a custom output parser
# if your model's function calling format isn't directly compatible with LangChain's default parsers.
# For simplicity, let's assume `create_react_agent` can work with a model that directly
# emits `Action:` and `Action Input:` for our fine-tuned output.
# If your model was fine-tuned to emit `tool_code` XML-like tags, you'd need a custom `AgentOutputParser`.


<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2784742237479601"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block; text-align:center;"
     data-ad-layout="in-article"
     data-ad-format="fluid"
     data-ad-client="ca-pub-2784742237479601"
     data-ad-slot="7340313511"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>


# The `create_react_agent` function handles formatting tools into the prompt for you.
agent = create_react_agent(llm, tools, prompt)

# Create an AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- 5. Run the Agent ---
print("\n--- Running Agent (Weather Query) ---")
try:
    result_weather = agent_executor.invoke({"input": "What's the weather in New York?"})
    print(f"Agent Weather Result: {result_weather['output']}")
except Exception as e:
    print(f"Error running agent for weather: {e}")

print("\n--- Running Agent (Product Search Query) ---")
try:
    result_product = agent_executor.invoke({"input": "Find me a cheap laptop."})
    print(f"Agent Product Result: {result_product['output']}")
except Exception as e:
    print(f"Error running agent for product: {e}")

print("\n--- Running Agent (No Tool Query) ---")
try:
    result_no_tool = agent_executor.invoke({"input": "Tell me a fun fact."})
    print(f"Agent No Tool Result: {result_no_tool['output']}")
except Exception as e:
    print(f"Error running agent for no tool: {e}")
{% endraw %}
```

The success of the above code depends heavily on:
1.  **Tokenizer Chat Template:** Ensure your tokenizer (from your fine-tuned model) correctly formats `ChatPromptTemplate` messages for your model.
2.  **Model Output Format:** Your fine-tuned model *must* generate outputs that can be parsed by LangChain's `AgentOutputParser`. If your model generates a custom `tool_code` XML-like format, you'll need to implement a custom parser and provide it to the agent.
3.  **`create_react_agent` Compatibility:** `create_react_agent` relies on specific prompt structures and output parsing. If your fine-tuning deviates significantly, you might need to build a custom `RunnableAgent` or integrate with a tool-calling specific library.

For more complex agent orchestration and state management, consider using LangGraph, which allows you to build robust, scalable agents. You can learn more about it in [LangGraph Scalable Agents]({% post_url 2026-11-15-langgraph-scalable-agents %}).

### Dataset Creation Strategies for LangChain Tool-Calling Fine-tuning

Creating a high-quality dataset is arguably the most critical step for successful fine-tuning. Here are several strategies:

*   **Manual Annotation:** This is the most precise but labor-intensive method. Human annotators examine user queries and hand-craft the ideal tool call (or direct response). This is best for small, high-stakes datasets or for bootstrapping.
*   **Synthetic Data Generation:** Leverage a powerful, off-the-shelf LLM (e.g., GPT-4, Claude) to generate a diverse set of user queries and corresponding tool calls. You can prompt it with your tool definitions and ask it to imagine various user intents. This can quickly scale your dataset.
*   **Logging and Feedback:** Instrument your existing LangChain agents to log their interactions. Collect user queries, agent decisions, and tool outputs. When an agent fails or acts incorrectly, manually correct the `chosen` and `rejected` responses. Tools like LangSmith are invaluable for this, providing rich observability into agent traces and facilitating data collection for fine-tuning. Learn more about it in [LangChain Observability LangSmith Tutorial]({% post_url 2026-11-13-langchain-observability-langsmith-tutorial %}) and [LangChain LangSmith W&B Tutorial]({% post_url 2026-11-12-langchain-langsmith-wandb-tutorial %}).
*   **Error Analysis:** Systematically review agent failures (e.g., incorrect tool calls, argument extraction errors, unnecessary tool calls). This process helps you identify patterns in the agent's weaknesses and prioritize which types of examples to add to your fine-tuning dataset. Our [Debug LangChain Tool Agents]({% post_url 2026-11-12-debug-langchain-tool-agents %}) tutorial can guide you here.

When collecting data, aim for diversity in user phrasing, intent, and edge cases. Include examples where tools should *not* be called, where multiple tools *could* be called (and which one is preferred), and variations in argument values.

### Evaluation Metrics for Tool-Calling Accuracy

To objectively measure the impact of your LangChain Tool-Calling Fine-tuning, establish clear evaluation metrics:

*   **Tool Selection Accuracy (Precision/Recall/F1-score):**
    *   **Precision:** Of all the tool calls made by the agent, how many were correct? (True Positives / (True Positives + False Positives)).
    *   **Recall:** Of all the times a tool *should* have been called, how many did the agent correctly identify? (True Positives / (True Positives + False Negatives)).
    *   **F1-score:** The harmonic mean of precision and recall, providing a balanced measure.
*   **Argument Extraction Accuracy:** For correctly selected tools, how often were the arguments (e.g., `city="London"`) exactly as expected? This can be measured as an exact match percentage.
*   **No-Tool Accuracy:** How accurately does the agent decide *not* to call a tool when a direct response is sufficient?
*   **End-to-End Task Success Rate:** The ultimate metric – does the agent successfully complete the user's task from start to finish? This is crucial for real-world impact.
*   **Latency and Cost:** Fine-tuned smaller models can significantly reduce inference latency and cost compared to larger, general-purpose LLMs, while delivering superior domain-specific performance.

Automated evaluation frameworks can compare agent outputs against a golden dataset, while human evaluation is often necessary for nuanced judgments.

### When to Choose SFT vs. DPO

Both SFT and DPO are powerful LLM fine-tuning techniques, but they shine in different scenarios for agent tool use:

| Feature/Metric      | Supervised Fine-Tuning (SFT)                                  | Direct Preference Optimization (DPO)                                |
| :------------------ | :------------------------------------------------------------ | :------------------------------------------------------------------ |
| **Data Format**     | Input-output pairs (prompt -> desired tool call/response)     | Prompt, preferred response, rejected response (triplets)            |
| **Primary Goal**    | Teach the *how*; establish fundamental tool-calling patterns | Teach the *what's better*; refine behavior, improve safety/robustness |
| **Ideal Use Case**  | Bootstrapping initial tool-calling capability, learning specific API schemas, precise instruction following. | Improving agent reliability, reducing hallucinations, handling ambiguity, aligning with complex preferences. |
| **Strengths**       | Direct, explicit learning; good for new skills.               | Qualitatively better outputs, less prone to "catastrophic forgetting," more stable. |
| **Weaknesses**      | Can be brittle if data lacks diversity, doesn't inherently optimize for "goodness" over "correctness." | Requires preference data (chosen vs. rejected), which can be harder to collect. |
| **Computational Cost** | Generally lower than DPO.                                     | Slightly higher than SFT due to reference model computations.     |
| **Recommended Path**| Start with SFT to establish baseline tool-calling behavior, then use DPO to refine and address edge cases. | Often applied after SFT to further polish agent performance and user experience. |

### Advanced Considerations & Best Practices

*   **LoRA/QLoRA:** Always consider using LoRA (Low-Rank Adaptation) or QLoRA for fine-tuning. These techniques drastically reduce memory usage and training time, making LLM fine-tuning accessible on more modest hardware.
*   **Iterative Improvement:** Fine-tuning is rarely a one-shot process. Start with a small, high-quality dataset, fine-tune, evaluate, collect more challenging examples (especially failures), and repeat the process. This iterative approach leads to continuous improvement.
*   **Version Control:** Treat your fine-tuning datasets and model checkpoints like code. Use tools like DVC (Data Version Control) or MLflow to manage different versions, ensuring reproducibility.
*   **Safety and Bias:** Fine-tuning can amplify biases present in your training data. Carefully curate your datasets and evaluate your fine-tuned models for unintended biases or safety issues.
*   **Prompt Engineering Synergy:** Fine-tuning doesn't replace good prompt engineering; it enhances it. Use your fine-tuned model with well-structured prompts that provide clear instructions and context.
*   **Agent Framework Choice:** While this guide focuses on LangChain agents, the principles of LLM fine-tuning for function calling apply universally. Whether you use `RunnableAgent` or more advanced frameworks like LangGraph, the core fine-tuned model remains the intelligent core. Explore [LangGraph Scalable Agents]({% post_url 2026-11-15-langgraph-scalable-agents %}) for stateful and more complex agent architectures.

### Conclusion

Fine-tuning your LLMs with SFT and DPO for specific LangChain Tool-Calling scenarios is a game-changer for building truly robust and reliable agents. By moving beyond generic models and training on your domain-specific interactions, you empower your agents to make more accurate decisions about when and how to use their tools. This leads to higher success rates, better user experiences, and more powerful applications. Embrace these advanced techniques to unlock the full potential of your LangChain agents and achieve unparalleled tool-calling accuracy.

### Frequently Asked Questions (FAQs)

**Q1: What exactly is LangChain Tool-Calling Fine-tuning?**
A1: LangChain Tool-Calling Fine-tuning refers to the process of training a Large Language Model (LLM) on a custom dataset specifically designed to teach it to accurately identify and invoke external tools (functions) within the LangChain framework. This improves the model's ability to select the correct tool and extract the right arguments from a user's query.

**Q2: Why can't I just use prompt engineering for better tool use?**
A2: While prompt engineering (system prompts, few-shot examples) can guide an LLM, it often reaches a limit for complex or domain-specific tool-calling tasks. Fine-tuning fundamentally alters the model's internal weights, making the desired tool-calling behavior an inherent part of the model, rather than just an instruction it tries to follow. This results in much higher consistency, robustness, and overall LangChain Tool-Calling accuracy.

**Q3: What's the difference between SFT and DPO for fine-tuning?**
A3: SFT (Supervised Fine-Tuning) teaches the model by showing it explicit input-output pairs (e.g., user query -> correct tool call). It's great for teaching initial capabilities. DPO (Direct Preference Optimization) refines the model's behavior by comparing a preferred response against a rejected one for the same prompt. DPO helps the model learn what "good" behavior looks like, reducing errors like hallucinations and improving alignment with desired outcomes, often yielding qualitatively better agent tool use.

**Q4: Do I need a super powerful GPU for LLM fine-tuning?**
A4: Not necessarily. Techniques like LoRA (Low-Rank Adaptation) and QLoRA (Quantized LoRA) significantly reduce the memory and computational requirements for fine-tuning, allowing you to fine-tune 7B-13B parameter models on consumer-grade GPUs (e.g., 12GB-24GB VRAM).

**Q5: How do I get the data for fine-tuning tool calls?**
A5: You can gather data through several methods:
    1.  **Manual Annotation:** Humans label user queries with the correct tool calls.
    2.  **Synthetic Data Generation:** Use a powerful, existing LLM to create diverse question-answer pairs involving your tools.
    3.  **Logging and Feedback:** Record interactions from live agents, identify failures, and create preferred/rejected examples for DPO. Tools like LangSmith are excellent for this.

**Q6: Can I fine-tune only a part of the model for tool calling?**
A6: Yes, techniques like LoRA allow you to fine-tune only a small set of "adapter" layers, which are then added to the pre-trained model. This is much more efficient than fine-tuning the entire model and is the recommended approach for most use cases.

**Q7: Will fine-tuning my LLM break its general knowledge or other abilities?**
A7: This is a concern known as "catastrophic forgetting." While SFT can sometimes lead to this if not carefully managed, DPO is generally more resistant to it. Using LoRA and keeping your learning rate appropriate can also help mitigate this risk by preventing large updates to the base model weights. It's crucial to evaluate your model on both tool-calling and general benchmarks.

**Q8: What kind of models are suitable for fine-tuning for function calling?**
A8: Many open-source models like Llama-2, Mistral, and their derivatives are excellent candidates. Some models might even have initial function-calling capabilities, which you can then enhance. Ensure the model's tokenizer supports chat templates or that you can convert your tool calls into a format the model understands during training.