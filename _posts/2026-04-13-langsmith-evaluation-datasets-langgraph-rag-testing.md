---
title: "How to Set Up LangSmith Evaluation Datasets for LangGraph RAG Testing"
description: "Master setting up LangSmith evaluation datasets for LangGraph RAG testing. Efficiently optimize your AI applications by accurately measuring RAG performance."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangSmith evaluation datasets LangGraph RAG]
featured: false
image: '/assets/images/langsmith-evaluation-datasets-langgraph-rag-testing.webp'
---

## How to Set Up LangSmith Evaluation Datasets for LangGraph RAG Testing

Imagine you have a super smart robot helper built with LangGraph RAG. This robot can answer questions by looking up information, just like you might use a book. But how do you know if your robot helper is actually giving good answers all the time?

This is where LangSmith evaluation datasets come in handy. They help you check your robot's work. We will learn how to create these special datasets so you can test your LangGraph RAG system properly.

### What is a LangGraph RAG System and Why Test It?

First, let's talk about what a LangGraph RAG system is. "RAG" stands for Retrieval Augmented Generation. It means your AI model can retrieve information from a special knowledge base before generating an answer. This makes its answers much more accurate and up-to-date than a regular chatbot.

LangGraph helps you build these systems step-by-step, like creating a complex recipe for your robot. You can make your robot do multiple things, like search, think, and then answer. If you want to dive deeper into how LangGraph works, check out this guide on [building multi-step AI agents with LangGraph]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

Now, why do we need to test it? Even the smartest robots can make mistakes or give incomplete answers. You want to be sure your LangGraph RAG system understands your questions and finds the right information. Testing helps you find problems and make your robot helper even better.

### Why Use LangSmith for RAG Benchmarking?

LangSmith is like a special lab for your AI projects. It helps you see what your AI is doing behind the scenes. You can track every step your LangGraph RAG system takes to answer a question.

This tracking is super important for RAG benchmarking. Benchmarking means comparing how well your system performs against a standard. LangSmith lets you set up these comparisons easily, using what we call LangSmith experiments.

With LangSmith, you can run many test cases and see exactly where your system succeeds or fails. This helps you understand what parts of your LangGraph RAG need fixing. It's a powerful tool for improving your AI's reliability and accuracy.

### Understanding Evaluation Datasets: Your Golden Standards

An evaluation dataset is like a special list of questions and their perfect answers. We also call this a golden dataset because it holds the "gold standard" for what a correct answer should look like. It's how you tell your robot if it got things right or wrong.

Each item in this dataset is a "test case." A test case usually has a question (the input) and the correct answer (the ground truth). Sometimes it also includes the correct information source that the robot *should* have used.

Imagine you're taking a test; the evaluation dataset is like the answer key for that test. Without an answer key, you wouldn't know if your answers were correct, right? That's why these evaluation datasets are so vital for good RAG benchmarking.

### Types of LangSmith Evaluation Datasets for LangGraph RAG

There are different kinds of evaluation dataset examples you might use for your LangGraph RAG system. The most common one is a simple Question-Answer (Q&A) pair. You ask a question, and you expect a specific answer.

Another type might involve not just the answer, but also the context or document that answer should come from. This is very useful for RAG systems because you can check if your robot retrieved the *correct* information. For instance, if you're building a RAG system that uses a vector store, you'll want to ensure it fetches the right chunks of information. You can learn more about building RAG applications with vector stores in this article: [Build RAG Applications with LangChain Vector Store in 2026]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).

Sometimes, you might even have test cases that check if your robot can follow specific instructions or perform certain actions. These structured data examples help you test more complex LangGraph RAG behaviors.

### Step-by-Step: Creating Your First LangSmith Evaluation Dataset

Creating a LangSmith evaluation dataset might sound tricky, but it's like gathering good examples for your robot to learn from. Let's break it down into easy steps. You'll need to think about what questions your LangGraph RAG system should answer well.

The first step is to clearly define what your LangGraph RAG system is supposed to do. Is it answering questions about your company's policies? Or helping users find product information? Knowing its purpose helps you create relevant test cases.

Once you know your system's goal, you can start collecting the questions and their perfect answers. This is like making flashcards for your robot.

#### 1. Defining Your LangGraph RAG System's Purpose

Before you build any test cases, you must know what your LangGraph RAG system is designed for. Is it a customer service agent? A research assistant? For example, if your system helps people with travel plans, your questions should be about travel.

Understanding its purpose helps you create questions that it should genuinely be able to answer. If your system is meant to summarize long documents, your test cases should involve documents and expected summaries. This focus ensures your evaluation dataset is truly helpful.

Without a clear purpose, your test cases might not actually test the important features of your LangGraph RAG. So take a moment to write down what your AI helper is supposed to achieve.

#### 2. Gathering Questions and Prompts

This is where you collect the actual questions, or "prompts," you will feed to your LangGraph RAG system. Think about what real users might ask. Try to include a variety of questions: simple ones, complex ones, and even tricky ones.

You can get these questions from several places. Maybe from user chat logs, frequently asked questions (FAQs) on a website, or by brainstorming with your team. The more realistic your questions are, the better your LangSmith experiments will be.

It's also a good idea to include questions that might be slightly out of scope for your system. This helps you test how your LangGraph RAG handles situations where it doesn't have an answer. This robust approach helps in comprehensive RAG benchmarking.

#### 3. Collecting Ground Truth Answers and Contexts

For each question you gathered, you now need to find the *perfect* answer. This is your "ground truth." This answer should be accurate, complete, and directly address the question. It's the answer you want your LangGraph RAG to produce.

If your RAG system uses specific documents, you should also note down which part of the document contains the answer. This is called the "ground truth context." For example, if you have a RAG system that uses a Weaviate vector store for hybrid search, knowing the exact document part that contains the correct answer is invaluable for debugging. You can learn more about such setups here: [LangChain Weaviate Hybrid Search for Scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}).

Having both the ground truth answer and context helps you evaluate two things. First, if your LangGraph RAG generated the correct answer. Second, if it used the correct information to generate that answer.

#### 4. Structuring Your Dataset for LangSmith

LangSmith expects your evaluation dataset to be organized in a specific way. Usually, it's a list of examples, and each example is a small bundle of information. This bundle will contain your input question and the ground truth output.

Here’s a simple structure you might use for a Q&A dataset:

*   **Input:** The question you ask your RAG system.
*   **Output:** The perfect answer that your RAG system should provide (ground truth).
*   **Reference Contexts (Optional):** The specific pieces of information your RAG system should retrieve to answer the question.

You can store this information in a list of dictionaries, a CSV file, or even directly in LangSmith. The clearer your structure, the easier it is to use.

#### 5. Programmatic Creation of LangSmith Evaluation Datasets

You can create these evaluation datasets right inside your Python code and upload them to LangSmith. This is very handy, especially if you have many test cases or if your golden dataset changes often. You'll need the `langchain` and `langsmith` libraries for this.

First, make sure you have LangSmith set up. You need an API key and to tell your Python program where to find LangSmith. Then you can create a list of your examples.

Here’s how you might set up your environment and create some basic examples for your LangGraph RAG.

```python
{% raw %}
import os
from langsmith import Client

# Set up your LangSmith API key
# You would usually get this from an environment variable or a secure config file
os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_API_KEY"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "LangGraph RAG Testing" # Your project name

client = Client()

# Define your evaluation examples
# Each example has an 'input' (the question) and an 'output' (the perfect answer)
evaluation_examples = [
    {
        "input": "What is the capital of France?",
        "output": "Paris",
        "reference_contexts": ["Paris is the largest city and capital of France, located on the Seine River."]
    },
    {
        "input": "Who painted the Mona Lisa?",
        "output": "Leonardo da Vinci",
        "reference_contexts": ["The Mona Lisa is a half-length portrait painting by Italian artist Leonardo da Vinci."]
    },
    {
        "input": "What is the primary function of a LangGraph StateGraph?",
        "output": "A LangGraph StateGraph allows you to define a sequence of steps and conditional logic for complex AI agent behavior.",
        "reference_contexts": ["LangGraph provides a StateGraph for orchestrating multi-step AI agent workflows, allowing agents to perform various actions based on the current state."]
    }
]

# Create a dataset in LangSmith
dataset_name = "LangGraph RAG Core Questions"
dataset = client.create_dataset(
    dataset_name=dataset_name,
    description="Fundamental questions for evaluating a LangGraph RAG system."
)

# Add the examples to the created dataset
for example in evaluation_examples:
    client.create_example(
        dataset_id=dataset.id,
        inputs={"question": example["input"]}, # LangSmith expects inputs as a dictionary
        outputs={"answer": example["output"]}, # LangSmith expects outputs as a dictionary
        reference_contexts=example.get("reference_contexts") # Optional, but good for RAG
    )

print(f"Dataset '{dataset_name}' created with {len(evaluation_examples)} examples.")
print(f"You can view it at: https://smith.langchain.com/datasets/{dataset.id}/")
```
{% endraw %}

In this snippet, we first set up the LangSmith client. Then, we prepare a list of `evaluation_examples`. Each example includes an `input` (the question) and an `output` (the correct answer). We also added `reference_contexts` which are super helpful for RAG evaluation.

Finally, we use `client.create_dataset` to make a new dataset in LangSmith. Then, we loop through our examples and add each one using `client.create_example`. This automatically uploads your test cases to your LangSmith project.

#### 6. Adding More Complex Examples for LangGraph RAG

For a LangGraph RAG system, your inputs might be more than just a simple question. You might want to test how it handles follow-up questions or specific instructions. For instance, if you're building a function-calling agent with LangChain and Google Gemini, you might test if it correctly identifies which tool to use. For more on that, see [LangChain Google Gemini Function Calling Agent with Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}).

Let's consider an example where you want to test if your RAG system can handle multi-turn conversations or specific tool invocations. Your `input` might become a history of messages, not just a single question.

```python
{% raw %}
import os
from langsmith import Client

os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_API_KEY"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "LangGraph RAG Testing"

client = Client()

complex_evaluation_examples = [
    {
        "input": {
            "chat_history": [
                {"role": "user", "content": "Tell me about large language models."},
                {"role": "assistant", "content": "Large language models (LLMs) are deep learning models with many parameters, trained on vast amounts of text data."},
                {"role": "user", "content": "What are some of their common applications?"}
            ],
            "current_question": "What are some of their common applications?"
        },
        "output": "LLMs are used for text generation, translation, summarization, and question answering.",
        "reference_contexts": ["Common applications of LLMs include natural language generation, machine translation, text summarization, and question-answering systems."]
    },
    {
        "input": {
            "query": "Find the policy regarding vacation days for new employees.",
            "policy_type": "HR"
        },
        "output": "New employees are eligible for 10 vacation days after their 6-month probation period.",
        "reference_contexts": ["HR Policy 3.1: Vacation days are accrued at a rate of 1.66 days per month, with eligibility beginning after 6 months of employment, totaling 10 days in the first year."]
    }
]

dataset_name_complex = "LangGraph RAG Advanced Scenarios"
dataset_complex = client.create_dataset(
    dataset_name=dataset_name_complex,
    description="Advanced test cases for multi-turn and structured queries in LangGraph RAG."
)

for example in complex_evaluation_examples:
    client.create_example(
        dataset_id=dataset_complex.id,
        inputs=example["input"], # Input is already a dictionary
        outputs={"answer": example["output"]},
        reference_contexts=example.get("reference_contexts")
    )

print(f"Dataset '{dataset_name_complex}' created with {len(complex_evaluation_examples)} examples.")
print(f"You can view it at: https://smith.langchain.com/datasets/{dataset_complex.id}/")
```
{% endraw %}

Notice how the `input` for `complex_evaluation_examples` can be a dictionary itself. This allows you to provide structured inputs that your LangGraph agent might expect. This is especially useful for agents that handle conversation history or need specific parameters.

### Connecting Your Dataset to LangGraph RAG Runs

Once your evaluation dataset is ready in LangSmith, the next step is to use it. You want your LangGraph RAG system to process each input from the dataset. Then, LangSmith will record its outputs and compare them to your golden dataset.

To do this, you typically run your LangGraph RAG system in "evaluation mode." You tell your system to take an input from the dataset, run its usual process, and then submit the results back to LangSmith.

This connection allows LangSmith to automatically track how well your system performs on each test case. It's like giving your robot a list of homework problems and then checking its answers against your answer key.

#### 1. Preparing Your LangGraph RAG for Evaluation

Your LangGraph RAG system needs to be callable, meaning you can easily send it a question and get an answer. If you've built your LangGraph using the LangChain Expression Language (LCEL), this is usually straightforward. You might have a runnable object that takes an input (e.g., a dictionary with a "question" key) and returns an output.

Make sure your LangGraph agent can receive the same type of input that you defined in your LangSmith evaluation dataset. For example, if your dataset has inputs like `{"question": "..."}`, your LangGraph should be able to process that. If your inputs include `{"chat_history": "...", "current_question": "..."}`, your graph should handle that too.

This preparation ensures that when LangSmith feeds an input from your evaluation dataset, your LangGraph RAG knows exactly what to do with it.

#### 2. Running LangSmith Experiments with Your LangGraph RAG

LangSmith experiments are where the magic happens. You link your LangGraph RAG model to your evaluation dataset and tell LangSmith to run them together. LangSmith will then iterate through every example in your dataset.

For each example, LangSmith will:
1.  Take the `input` from your test case.
2.  Send that input to your LangGraph RAG system.
3.  Record what your LangGraph RAG outputs.
4.  Compare your system's output to the `ground truth` in your dataset.

This entire process is automated, saving you a lot of time. You can also define custom evaluators in LangSmith to automatically score your RAG system's answers.

Here’s a conceptual example of how you would start an evaluation run in Python, referencing your LangGraph RAG system.

```python
{% raw %}
import os
from langsmith import Client
from langchain_core.runnables import Runnable

# Assume you have your LangGraph RAG chain defined somewhere as `rag_chain`
# For this example, let's create a dummy chain
# In a real scenario, this would be your actual LangGraph RAG pipeline
class DummyRAGChain(Runnable):
    def invoke(self, input_data: dict) -> dict:
        question = input_data.get("question")
        if question:
            if "capital of France" in question:
                return {"answer": "Paris"}
            elif "Mona Lisa" in question:
                return {"answer": "Leonardo da Vinci"}
            elif "LangGraph StateGraph" in question:
                return {"answer": "A LangGraph StateGraph allows you to define a sequence of steps and conditional logic."}
            else:
                return {"answer": "I don't know the answer to that."}
        else:
            return {"answer": "Please provide a question."}
    
    # Required for Runnable interface if you want to support streaming, batch, etc.
    # For a simple invoke, this might be enough.
    # If your LangGraph chain has more complex inputs/outputs, adjust accordingly.
    
rag_chain = DummyRAGChain()

os.environ["LANGCHAIN_API_KEY"] = "YOUR_LANGSMITH_API_KEY"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "LangGraph RAG Testing"

client = Client()

# Retrieve the dataset you created earlier
dataset_name = "LangGraph RAG Core Questions"
# You might need to list datasets and find by name if you don't have the ID
datasets = client.list_datasets(dataset_name=dataset_name)
if not datasets:
    raise ValueError(f"Dataset '{dataset_name}' not found.")
dataset_id = datasets[0].id

# Define the evaluators you want to use
# LangSmith has built-in evaluators for correctness, helpfulness, groundedness, etc.
# You can also write custom evaluators.
# For RAG, 'CriteriaEvaluator' (e.g., "is_correct") and 'ContextRelevance' are common.
from langsmith.evaluation import evaluate

# Let's use a simple 'is_correct' evaluator
# In a real RAG scenario, you'd use more sophisticated evaluators like
# 'ContextRelevance', 'AnswerRelevance', 'Faithfulness', 'Helpfulness'
# Example of a custom evaluator could be:
# evaluator_config = [
#     evaluate.RunEvalConfig.LabeledCriteria("is_correct"),
#     evaluate.RunEvalConfig.LabeledCriteria("is_relevant_to_query", criteria={"is_relevant_to_query": "Is the retrieved context relevant to the query?"}),
#     evaluate.RunEvalConfig.LabeledScoreString(
#         criteria={
#             "faithfulness": "Does the generated answer only contain claims that are supported by the provided context?",
#             "helpfulness": "Is the answer helpful and does it fully answer the query?"
#         }
#     ),
#     evaluate.RunEvalConfig.Metric(
#         name="retrieval_f1",
#         scoring="retrieval_f1" # Example of a retrieval specific metric
#     )
# ]

# For simplicity, let's just use a single 'correctness' evaluator for now.
# In a real RAG setup, you'd define evaluators based on your specific needs.
evaluator_config = [
    evaluate.RunEvalConfig.LabeledCriteria("correctness", criteria={
        "correctness": "Does the assistant's response correctly answer the user's question, based on the provided ground truth?"
    })
]

print(f"Starting evaluation run for dataset '{dataset_name}'...")
run_id = evaluate(
    llm_or_chain_factory=lambda: rag_chain, # Your LangGraph RAG chain
    data=dataset_id, # The dataset ID
    evaluators=evaluator_config, # The evaluators to run
    # You can also pass evaluation_config to specify how outputs map to ground truth etc.
    experiment_prefix="LangGraph RAG Test Run", # A name for your experiment
    num_repetitions=1 # How many times to run each example (usually 1)
)

print(f"Evaluation run started. Check results at: https://smith.langchain.com/o/{client.tenant_id}/projects/{client.project_id}/runs/{run_id}/")
```
{% endraw %}

This code shows you the general idea. You first set up your LangGraph RAG system as a `Runnable`. Then, you retrieve your dataset by its name or ID. You tell LangSmith which `evaluators` to use. Finally, you call `evaluate` with your chain and dataset. This kicks off your LangSmith experiments.

### Analyzing Results for RAG Benchmarking

After your LangSmith experiments complete, it's time to look at the results. LangSmith provides a dashboard where you can see how your LangGraph RAG system performed on all your test cases. This is crucial for RAG benchmarking.

You'll see scores from the evaluators you chose. For example, if you used a "correctness" evaluator, you'll see a percentage of how many answers were correct. You can also dive into individual test cases to see where your system went wrong.

Analyzing these results helps you pinpoint weaknesses in your LangGraph RAG. Maybe it struggles with complex questions, or perhaps it retrieves irrelevant information. This analysis guides you on how to improve your system.

#### 1. Understanding Evaluation Metrics

When you run your LangSmith experiments, you'll get various scores. These are your evaluation metrics. For RAG systems, common metrics include:

*   **Correctness:** How often the generated answer matches the ground truth.
*   **Helpfulness:** Whether the answer fully addresses the user's need.
*   **Groundedness/Faithfulness:** If the answer is truly based on the retrieved documents and doesn't "hallucinate" information.
*   **Context Relevance:** How relevant the retrieved documents are to the original question.
*   **Answer Relevance:** How relevant the generated answer is to the original question.

LangSmith offers built-in evaluators for many of these, or you can create custom evaluators if you have specific needs. For more details on custom logic, you might find this guide helpful: [LangChain Custom Output Parser Tutorial]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}).

By looking at these metrics, you get a clear picture of your LangGraph RAG's strengths and weaknesses.

#### 2. Debugging Failed Test Cases

The real power of LangSmith is in debugging. For every failed test case, you can click into the "trace" of that run. This trace shows you every step your LangGraph RAG system took to answer the question.

You can see what chunks of information it retrieved, what thoughts it had, and how it generated the final answer. If your RAG system uses semantic text splitting, you can even check if the initial chunking was effective. Find out more about that here: [LangChain Semantic Text Splitter: Chunk by Meaning]({% post_url 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning %}).

By reviewing these traces, you can often figure out exactly *why* your system failed. Did it retrieve the wrong document? Did the language model misunderstand the question? This insight is invaluable for fixing your system.

#### 3. Iterating and Improving Your LangGraph RAG

RAG benchmarking is not a one-time thing. It's a cycle of test, analyze, improve, and re-test. Once you identify problems from your LangSmith experiments, you make changes to your LangGraph RAG.

Maybe you adjust your retrieval strategy, refine your prompts, or fine-tune your language model. After making changes, you run the evaluation again using the same dataset. This helps you see if your changes actually made things better.

This iterative process of testing with LangSmith evaluation datasets helps you continuously improve your LangGraph RAG system. It's how you make your AI helper truly smart and reliable.

### Tips for Building Effective LangSmith Evaluation Datasets

Building a good evaluation dataset is an art. Here are some tips to make sure your golden dataset truly helps you test your LangGraph RAG. These tips ensure your test cases are high quality.

*   **Diversity is Key:** Don't just include easy questions. Add hard ones, ambiguous ones, and questions with no direct answer in your knowledge base. This tests your LangGraph RAG's robustness.
*   **Realistic Questions:** Use questions that real users would actually ask. This makes your RAG benchmarking more meaningful.
*   **Clear Ground Truth:** Ensure your expected answers are unambiguous and correct. If your ground truth is flawed, your evaluation will be flawed too.
*   **Include Edge Cases:** Test how your system handles unusual requests, misspellings, or out-of-scope questions. A good evaluation dataset covers these scenarios.
*   **Regular Updates:** As your LangGraph RAG system and its knowledge base evolve, your evaluation dataset should too. Keep it current.

By following these tips, you'll create a powerful set of test cases that gives you accurate insights into your LangGraph RAG's performance.

### Beyond Basics: Advanced Evaluation Strategies

Once you're comfortable with basic LangSmith evaluation datasets, you can explore more advanced strategies. This helps you conduct even more detailed RAG benchmarking for your LangGraph RAG.

One advanced technique is to use different golden datasets for different aspects of your system. For example, one dataset could focus on retrieval accuracy, and another on summarization quality.

You can also leverage human evaluators in LangSmith. After your automated evaluators run, you can have real people review a subset of the results. Human feedback provides invaluable insights that automated metrics might miss. This combined approach makes your LangSmith experiments very powerful.

### Conclusion

Setting up LangSmith evaluation datasets for your LangGraph RAG testing is a vital step in building reliable and accurate AI systems. You've learned what evaluation datasets are, why they're important for RAG benchmarking, and how to create them.

By using a golden dataset of test cases, running LangSmith experiments, and analyzing the results, you can continuously improve your LangGraph RAG system. Remember to keep your questions diverse, your ground truth clear, and your evaluations regular.

With LangSmith as your trusted lab, you're well-equipped to make your LangGraph RAG system the smartest and most helpful robot assistant it can be. Keep testing, keep learning, and keep building!