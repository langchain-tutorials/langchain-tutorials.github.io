---
title: "LangChain with Next.js: How to Build a Production-Ready AI App with App Router and API Routes"
description: "Build a production-ready AI app using LangChain with Next.js, App Router, and API Routes. Master scalable development for your next big project today!"
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain with Next.js]
featured: false
image: '/assets/images/langchain-nextjs-production-ai-app-app-router-api-routes.webp'
---

## LangChain with Next.js: Building a Smart AI App from Start to Finish

Imagine building an app that can talk, answer questions, and even help you create things, just like magic! This guide shows you how to combine two powerful tools: LangChain and Next.js. We will learn how to make an AI application that's ready for everyone to use.

You will see how to use the latest features like the Next.js App Router and API routes to make your app super fast and reliable. We'll also cover how to make sure your AI brain (the LangChain backend) works smoothly. This combination means you can build amazing AI experiences.

### Why Combine LangChain with Next.js for AI Apps?

Using LangChain with Next.js is like having a superhero team for building AI apps. LangChain helps your app understand language and do smart things. It connects to big AI models and manages complex conversations.

Next.js is perfect for building the website part of your app. It makes websites fast and easy to update. Together, they let you create interactive and powerful AI tools. You get the best of both worlds: smart AI and a great user experience. If you are curious about other options, you can explore some [top LangChain alternatives]({% post_url 2026-02-14-top-langchain-alternatives-2026-10-frameworks-compared-ranked %}).

### Getting Started: Setting Up Your Next.js Project

First, you need to create a new Next.js project. Think of this as setting up the foundation for your house. We will use a special command to get everything ready. This command will ask you a few questions about your project.

Make sure to say "yes" to using the App Router. The App Router is a new and better way to organize your Next.js app. It makes building complex apps much simpler.

To start, open your computer's command line and type:

{% raw %}
```bash
npx create-next-app@latest my-ai-app
```
{% endraw %}

When it asks about the App Router, choose "Yes". For other options, you can usually pick the defaults. After that, go into your new project folder:

{% raw %}
```bash
cd my-ai-app
```
{% endraw %}

Now you have a fresh Next.js project ready for your LangChain with Next.js adventure. Next, we need to add LangChain itself. This is like adding the "brain" to your app.

### Adding LangChain to Your Project

LangChain is a toolkit that helps you talk to AI models. It makes it easy to build chatbots, summarizers, and more. You need to install it into your Next.js project. This command adds LangChain and its parts to your app.

We will also install the tools needed for the AI models we want to use, like OpenAI or Google Gemini. These are like connecting your brain to different knowledge sources.

Run these commands in your project folder:

{% raw %}
```bash
npm install langchain @langchain/openai
# or using yarn
yarn add langchain @langchain/openai
```
{% endraw %}

You've now set up both your Next.js frontend and the LangChain backend tools. You're ready to start building the AI features.

### Understanding the Next.js App Router

The Next.js App Router is a powerful way to structure your application. It uses a special folder called `app` to manage all your pages and data. This makes it easier to know where everything is. You can create different parts of your website, like `/dashboard` or `/settings`, by just making new folders inside `app`.

Each folder in `app` can have a `page.tsx` file, which is what users see. It can also have `layout.tsx` for shared designs or `loading.tsx` for showing a spinner. The App Router handles how your app fetches data and runs code. This makes your LangChain with Next.js app very efficient.

### API Routes vs. Server Actions: Choosing Your LangChain Backend

When building your LangChain backend, you have two main choices in Next.js: API Routes or Server Actions. Both let you run code on the server, which is important for talking to AI models safely. You don't want to expose your secret AI keys to everyone. Let's look at each one.

#### Using API Routes for Your LangChain Backend

API routes are like special web addresses your app can "call" to get information or send data. They live in your `app/api` folder. When you send a message to an API route, it runs some code on the server. This code can then talk to LangChain and send back the AI's answer.

API routes are great when you need to do things like fetching data from a database or running a complex AI process. They are also good for making your app talk to other services on the internet. You can use them to build a robust LangChain backend that your frontend can easily interact with.

Here's an example of a simple API route that uses LangChain to get a response from an AI model. This file would be in `app/api/chat/route.ts`:

{% raw %}
```typescript
// app/api/chat/route.ts
import { OpenAI } from "@langchain/openai";
import { HumanMessage, AIMessage } from "@langchain/core/messages";
import { NextRequest, NextResponse } from "next/server";

export const runtime = 'edge'; // Use Edge runtime for faster responses

export async function POST(req: NextRequest) {
  try {
    const { message } = await req.json();

    if (!message) {
      return NextResponse.json({ error: "No message provided" }, { status: 400 });
    }

    // Initialize the OpenAI model
    // Make sure to set your OPENAI_API_KEY as an environment variable
    const model = new OpenAI({
      modelName: "gpt-3.5-turbo",
      temperature: 0.7,
      openAIApiKey: process.env.OPENAI_API_KEY,
    });

    // You can also use a more complex chain here
    // For simplicity, we're just directly calling the model
    const response = await model.invoke([new HumanMessage(message)]);

    return NextResponse.json({ reply: response.content });
  } catch (error) {
    console.error("Error in chat API route:", error);
    return NextResponse.json({ error: "Failed to get AI response" }, { status: 500 });
  }
}
```
{% endraw %}

In this example, we've set `runtime = 'edge'`. This tells Next.js to run this API route in a very fast, serverless environment close to your users. This is perfect for quick AI interactions and a production-ready LangChain with Next.js app.

#### Embracing Server Actions for Simpler Interactions

Server Actions are a newer feature in Next.js App Router that makes sending data from your website directly to the server much easier. Instead of building a full API route, you can write a special function right inside your component or a separate file. This function runs on the server.

Think of it like directly asking the server to do something without needing a separate "phone number" (API endpoint). Server actions are great for things like submitting forms, updating settings, or triggering small AI tasks. They simplify how your frontend talks to your LangChain backend.

Here's how a Server Action might look in a React component file (`page.tsx` or a separate file `actions.ts`):

{% raw %}
{% raw %}
``` typescript
// app/chat/page.tsx or app/actions.ts
'use client'; // This component runs on the client

import { useState } from 'react';
import { HumanMessage, AIMessage } from "@langchain/core/messages";
import { ChatOpenAI } from "@langchain/openai"; // Using ChatOpenAI for chat models

// This is the server action. It runs ONLY on the server.
async function getAIReply(message: string): Promise<string> {
  "use server"; // Important: Mark this function as a Server Action

  try {
    const model = new ChatOpenAI({
      modelName: "gpt-3.5-turbo",
      temperature: 0.7,
      openAIApiKey: process.env.OPENAI_API_KEY, // Ensure this is set securely
    });

    // Invoke the model with the user's message
    const response = await model.invoke([new HumanMessage(message)]);

    return response.content as string;
  } catch (error) {
    console.error("Error in Server Action:", error);
    return "Sorry, I couldn't get a response right now.";
  }
}

export default function ChatPage() {
  const [input, setInput] = useState('');
  const [chatHistory, setChatHistory] = useState<{ type: 'user' | 'ai'; text: string }[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setChatHistory((prev) => [...prev, { type: 'user', text: userMessage }]);
    setInput('');
    setIsLoading(true);

    try {
      const aiReply = await getAIReply(userMessage); // Call the server action directly
      setChatHistory((prev) => [...prev, { type: 'ai', text: aiReply }]);
    } catch (error) {
      console.error("Failed to get AI reply:", error);
      setChatHistory((prev) => [...prev, { type: 'ai', text: "Error: Could not get a response." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '20px auto', fontFamily: 'sans-serif' }}>
      <h1>AI Chat with LangChain and Next.js</h1>
      <div style={{ border: '1px solid #ccc', padding: '10px', minHeight: '300px', overflowY: 'auto', marginBottom: '10px' }}>
        {chatHistory.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.type === 'user' ? 'right' : 'left', marginBottom: '5px' }}>
            <span style={{
              display: 'inline-block',
              padding: '8px 12px',
              borderRadius: '15px',
              backgroundColor: msg.type === 'user' ? '#007bff' : '#f0f0f0',
              color: msg.type === 'user' ? 'white' : 'black'
            }}>
              {msg.type === 'user' ? 'You: ' : 'AI: '}
              {msg.text}
            </span>
          </div>
        ))}
        {isLoading && (
          <div style={{ textAlign: 'left', marginBottom: '5px' }}>
            <span style={{
              display: 'inline-block',
              padding: '8px 12px',
              borderRadius: '15px',
              backgroundColor: '#f0f0f0',
              color: 'black'
            }}>
              AI: Thinking...
            </span>
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} style={{ display: 'flex' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          disabled={isLoading}
          style={{ flexGrow: 1, padding: '10px', border: '1px solid #ccc', borderRadius: '5px', marginRight: '10px' }}
        />
        <button type="submit" disabled={isLoading} style={{ padding: '10px 15px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
          Send
        </button>
      </form>
    </div>
  );
}
```
{% endraw %}
{% endraw %}

Notice the `"use server";` at the top of the `getAIReply` function. This is what makes it a Server Action. This powerful feature simplifies your LangChain with Next.js development.

#### Which one to choose?

*   **API Routes:** Use them when you need more control, streaming responses (like a chatbot typing out text letter by letter), or when you want other services to be able to talk to your AI backend. They are very flexible for a production-ready LangChain with Next.js application.
*   **Server Actions:** Use them for simpler, direct interactions from your forms or buttons. They often make your code cleaner and easier to manage when the frontend and backend actions are closely related.

Both are great choices for different situations. You can even use both in the same Next.js app!

### Building Your LangChain Backend: Practical Examples

Now let's dive into more detailed LangChain examples for your Next.js app. The core idea is that your LangChain backend will handle all the smart AI parts. It will connect to big language models and process your requests. You can build simple question-answering tools or more complex AI agents.

#### Simple Question Answering with LangChain

A basic LangChain application might just take a question and return an answer. This is like asking a very smart assistant a single question. Your Next.js backend (either API route or Server Action) will get the question. Then, LangChain will do the hard work.

Here’s how you might set up a basic chain within your backend code:

{% raw %}
```typescript
// Inside your API route or Server Action function
import { ChatOpenAI } from "@langchain/openai";
import { HumanMessage, SystemMessage } from "@langchain/core/messages";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";

async function runSimpleQA(question: string): Promise<string> {
  const chatModel = new ChatOpenAI({
    temperature: 0.7,
    modelName: "gpt-3.5-turbo",
    openAIApiKey: process.env.OPENAI_API_KEY,
  });

  const prompt = ChatPromptTemplate.fromMessages([
    new SystemMessage("You are a helpful assistant. Answer the user's question clearly and concisely."),
    new HumanMessage("{input}"),
  ]);

  const outputParser = new StringOutputParser();

  // Create a simple chain
  const chain = prompt.pipe(chatModel).pipe(outputParser);

  const result = await chain.invoke({ input: question });
  return result;
}

// How you'd call this in an API route or Server Action:
// const answer = await runSimpleQA(message);
```
{% endraw %}

This example uses a `ChatPromptTemplate` to tell the AI its role. It then pipes the prompt, the AI model, and an output parser together. This chain is a fundamental concept in LangChain. For more about tailoring AI responses, you can check out [how to create a custom output parser]({% post_url 2026-03-31-langchain-custom-output-parser-tutorial %}).

#### Building a RAG Application

RAG stands for Retrieval Augmented Generation. It means your AI doesn't just rely on what it already knows. Instead, it looks up information from your own documents first. This is super useful for building AI apps that answer questions based on your company's data, specific articles, or private knowledge bases.

To build a RAG app, you need a way to store and search your documents, often called a vector store. LangChain works great with these. You can then retrieve relevant document pieces and give them to the AI model along with the user's question. If you are building a [RAG application]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}), this is a crucial step.

Here’s a simplified idea of a RAG pipeline in your LangChain backend:

{% raw %}
```typescript
// Inside your API route or Server Action function
import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { RunnableSequence } from "@langchain/core/runnables";
import { PromptTemplate } from "@langchain/core/prompts";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitters";
import { Document } from "@langchain/core/documents";

// Assume you have some documents
const documents = [
  new Document({ pageContent: "The capital of France is Paris." }),
  new Document({ pageContent: "Eiffel Tower is in Paris." }),
  new Document({ pageContent: "Germany's capital is Berlin." }),
];

async function runRAG(question: string): Promise<string> {
  const embeddings = new OpenAIEmbeddings({ openAIApiKey: process.env.OPENAI_API_KEY });
  const model = new ChatOpenAI({ openAIApiKey: process.env.OPENAI_API_KEY, temperature: 0 });

  // 1. Create a vector store from your documents (in a real app, this would be pre-built and persistent)
  const vectorStore = await MemoryVectorStore.fromDocuments(documents, embeddings);
  const retriever = vectorStore.asRetriever();

  // 2. Define the prompt for the AI model
  const prompt = PromptTemplate.fromTemplate(`
    Answer the question based only on the following context:
    {context}
    
    Question: {question}
    `);

  // 3. Build the RAG chain
  const ragChain = RunnableSequence.from([
    {
      context: retriever, // Retrieve relevant documents
      question: (input: string) => input, // Pass the original question
    },
    prompt, // Format with the prompt
    model, // Send to the AI model
    new StringOutputParser(), // Get the string answer
  ]);

  const result = await ragChain.invoke(question);
  return result;
}
```
{% endraw %}

This example shows a basic RAG flow. First, it finds relevant pieces of information (context). Then, it combines this context with your question and sends it to the AI. This way, the AI can give accurate answers based on your specific data. For advanced RAG solutions, consider topics like [hybrid search with Weaviate]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}) or using [semantic text splitters]({% post_url 2026-04-03-langchain-semantic-text-splitter-chunk-by-meaning %}) to improve your data processing.

### Connecting Your Frontend to the LangChain Backend

Now that your LangChain backend is ready, you need to make your Next.js frontend talk to it. This is how users will interact with your AI app. If you used API Routes, your frontend will `fetch` data from those routes. If you used Server Actions, you will call those functions directly from your client-side components.

#### Frontend with API Routes

If you chose API Routes for your LangChain backend, your frontend code will use the standard `fetch` API. This sends a request to your API route and waits for a response.

Here's a simple React component that sends a message to the `/api/chat` route we created earlier:

{% raw %}
{% raw %}
``` typescript
// app/chat-api/page.tsx
'use client';

import { useState } from 'react';

export default function ChatApiPage() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setIsLoading(true);
    setResponse('Thinking...'); // Provide immediate feedback

    try {
      const res = await fetch('/api/chat', { // Calls your API route
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data.reply);
    } catch (error) {
      console.error('Failed to fetch AI response:', error);
      setResponse('Error: Could not get a response from the AI.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '20px auto', fontFamily: 'sans-serif' }}>
      <h1>Chat with AI (using API Route)</h1>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask the AI a question..."
        disabled={isLoading}
        style={{ width: '100%', padding: '10px', marginBottom: '10px', borderRadius: '5px', border: '1px solid #ccc' }}
      />
      <button onClick={sendMessage} disabled={isLoading} style={{ padding: '10px 15px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
        {isLoading ? 'Sending...' : 'Send Question'}
      </button>
      {response && (
        <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f9f9f9', border: '1px solid #eee', borderRadius: '5px' }}>
          <strong>AI Response:</strong> {response}
        </div>
      )}
    </div>
  );
}
```
{% endraw %}
{% endraw %}

This component manages the user's input and displays the AI's response. It shows how simple it is to integrate your LangChain with Next.js app's frontend and backend.

### Making Your AI App Production-Ready

Building an app is one thing, but making it ready for lots of people to use is another. A production-ready LangChain with Next.js app needs to be stable, fast, and secure. Here are some key steps.

#### Environment Variables and Security

Never put your secret keys (like `OPENAI_API_KEY`) directly in your code. Hackers could find them. Instead, use environment variables. These are special settings that your server knows about but are not part of your public code.

Next.js makes it easy to use environment variables. Create a file called `.env.local` in the root of your project. Add your key there:

```
OPENAI_API_KEY=sk-your-super-secret-key
```

Then, you can access it in your server-side code (API Routes or Server Actions) using `process.env.OPENAI_API_KEY`. Remember, these keys should *only* be used on the server, never directly in your frontend code.

#### Error Handling and Logging

Things can go wrong, and that's okay! What's important is how your app handles it. Always wrap your AI calls in `try...catch` blocks. This lets you catch errors if the AI model fails or if there's a problem with your LangChain backend.

When an error happens, log it! Use `console.error()` on the server to see what went wrong. For users, provide a friendly message. Don't show them complicated technical errors. Good error handling makes your LangChain with Next.js app more reliable.

#### Using Edge Runtime for Performance

You saw `export const runtime = 'edge';` in our API route example. The Edge runtime is a super-fast way to run server code. It runs your code closer to where your users are, making responses quicker. This is great for AI interactions where every millisecond counts.

For your LangChain backend, using the Edge runtime means your AI calls can be processed almost instantly. This improves the user experience significantly. Not all LangChain features might be compatible with Edge runtime yet, but for basic model calls, it's a fantastic option.

#### Deploying with Vercel

Vercel is a platform that makes deploying Next.js apps incredibly easy. It's built by the same team behind Next.js. You can connect your project to Vercel, and every time you make changes and push them to your code, Vercel will automatically build and deploy your app.

Vercel also handles your environment variables securely. It supports the Edge runtime beautifully. This makes Vercel an ideal choice for getting your production-ready LangChain with Next.js app out to the world. Just link your GitHub, GitLab, or Bitbucket repository, and Vercel takes care of the rest.

### Advanced LangChain Concepts for Your Next.js App

Once you have the basics down, LangChain offers many advanced features to make your AI app even smarter.

#### Agents and Tools

LangChain Agents allow your AI to "think" and decide which tools to use to achieve a goal. Imagine an AI that can not only answer questions but also search the internet, read documents, or use other external services. This is where agents shine.

You can give your LangChain backend "tools" like a web search tool or a calculator. The agent then decides when and how to use these tools to best answer the user's request. This makes your AI app much more dynamic and capable. Learn more about [function calling and custom tools with LangChain]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}).

#### Building Multi-Step AI Workflows with LangGraph

Sometimes, an AI task needs multiple steps. For example, planning a trip might involve asking about destination, dates, preferences, then searching for flights, hotels, and activities. LangGraph, a part of LangChain, helps you build these complex, multi-step AI agents.

LangGraph lets you define "states" and "transitions" for your AI. It's like drawing a flowchart for how your AI should think and act. This is perfect for complex applications where the AI needs to follow a specific process. If you're tackling multi-step AI challenges, [exploring LangGraph and StateGraphs]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}) can be very beneficial.

### Conclusion

You've learned how to combine the power of LangChain with Next.js to build amazing AI applications. We covered setting up your project, understanding the Next.js App Router, and choosing between API routes and server actions for your LangChain backend. You also saw how to create basic AI features and connect them to your frontend.

Finally, we discussed important steps for making your app production-ready, like security, error handling, using the Edge runtime, and deploying with Vercel. With these tools and techniques, you are well-equipped to build smart, fast, and reliable AI applications. The journey of building with LangChain with Next.js is exciting, and you are now ready to create your own intelligent apps!