---
title: "LangChain with Kubernetes Deployment Using Docker & Helm (Full Practical Guide)"
description: "Master LangChain with Kubernetes deployment. This practical guide shows you how to deploy LangChain apps using Docker & Helm. Start building your AI now."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [LangChain with Kubernetes deployment]
featured: false
image: '/assets/images/langchain-kubernetes-docker-helm-guide.webp'
---

# LangChain with Kubernetes Deployment Using Docker & Helm (Full Practical Guide)

Hello there! Have you ever built a cool LangChain app and wondered how to share it with many friends or make it work all the time? Well, you're in the right place! We're going to learn how to put your smart LangChain app into a powerful system using some amazing tools.

This guide will show you how to get your LangChain application ready, put it in special boxes called Docker containers, and then use Kubernetes to make sure it runs smoothly. We'll also use Helm charts, which are like instruction manuals, to make deploying your LangChain with Kubernetes deployment super easy. Get ready for a fun journey into making your AI projects bigger and better!

## Understanding the Key Tools for Your LangChain Journey

Before we start building, let's get to know our main tools. Think of them as the LEGO bricks we'll use to create our amazing structure. Each tool plays a special part in making your LangChain application strong and always available.

### What is LangChain?

LangChain is like a magic toolkit for building apps that understand and create language. It helps you connect different powerful AI models, like the ones that write stories or answer questions, into one smart program. You can create intelligent agents, chatbots, or even systems that can read huge amounts of information and tell you exactly what you need to know.

If you're curious about how LangChain stacks up against other tools, you might find this interesting: [Top LangChain Alternatives in 2026]({% post_url 2026-02-14-top-langchain-alternatives-2026-10-frameworks-compared-ranked %}). LangChain helps you build smart applications that can talk, think, and even make decisions using AI. It lets you link different AI brains together, making them even smarter.

### What are Docker Containers?

Imagine you have a toy car that needs very specific batteries and a special track to run. Docker containers are like a small, self-contained box that holds your entire toy car, its special batteries, and even a small piece of the track. This means your toy car will always work the same way, no matter where you take it.

For your LangChain app, a Docker container bundles all its code, libraries, and everything it needs to run perfectly. This way, your app behaves the same on your computer, your friend's computer, or a big server in the cloud. Docker containers make sure there are no "it works on my machine!" problems.

### What is Kubernetes?

If Docker containers are like individual toy cars, then Kubernetes is like a giant, super-smart garage manager for all your toy cars. It makes sure all your cars are running, replaces them if they break, and even adds more cars if many people want to play. Kubernetes automatically handles where your Docker containers run and makes sure they are always available.

When you're doing a LangChain with Kubernetes deployment, Kubernetes ensures your AI application is always online and can handle many users at once. It's fantastic for making sure your smart apps are reliable and can grow. Kubernetes is the brain behind keeping your application up and running smoothly, no matter how popular it gets.

### What are Helm Charts?

Now, imagine you have a lot of different toy cars, and each needs a specific setup. Helm charts are like detailed instruction manuals or blueprints for deploying your applications on Kubernetes. They tell Kubernetes exactly how to set up your LangChain application, including how many copies to run and what resources it needs.

Helm charts simplify the process of Kubernetes packaging. Instead of writing many complex commands, you just use one Helm command, and it sets everything up for your LangChain with Kubernetes deployment. It's like having a universal remote control for your Kubernetes garage, making complex setups feel simple and manageable.

## Preparing Your LangChain Application for Deployment

Before we can put our LangChain application into Docker containers and on Kubernetes, we need to make sure it's ready. This means writing your application code and then packaging it up correctly. We'll start with a simple LangChain application example.

### Creating a Simple LangChain Application

Let's imagine we have a small LangChain app that takes a question and answers it using a language model. This could be a basic agent or a simple RAG (Retrieval Augmented Generation) setup. If you want to dive deeper into RAG, check out this guide: [Build RAG Applications with LangChain]({% post_url 2026-02-05-build-rag-applications-langchain-vector-store-2026 %}).

Here's a very basic Python example of a LangChain application that uses a simple chain. We'll put this into a file named `app.py`.

```python
# app.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import OpenAI
import os

# Set your OpenAI API key
# You should get this from an environment variable in a real deployment
# For this example, we'll assume it's set in the environment
# os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY" # Do not hardcode this!

def get_llm_chain():
    """
    Creates and returns a simple LangChain LLM chain.
    """
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Answer the user's questions concisely."),
        ("user", "{question}")
    ])
    llm = OpenAI(temperature=0.7) # Using OpenAI as an example, replace with your preferred LLM
    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    return chain

if __name__ == "__main_main__":
    my_chain = get_llm_chain()
    print("LangChain App Ready! To use, run `chain.invoke({'question': 'Your question here'})`")
    # Example usage (for testing locally before deployment)
    # response = my_chain.invoke({"question": "What is the capital of France?"})
    # print(f"Response: {response}")

```

This `app.py` script defines a function `get_llm_chain()` that sets up our LangChain. It uses a simple prompt, an OpenAI model, and a string output parser. We will run this application as a web service. For that, we need a web framework like Flask or FastAPI. Let's add a simple FastAPI server to expose our LangChain chain.

```python
# app.py (updated with FastAPI)
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import OpenAI
import os
import uvicorn

app = FastAPI()

# Make sure to set your OpenAI API key as an environment variable
# e.g., export OPENAI_API_KEY="sk-..."

@app.post("/ask")
async def ask_question(question: str):
    try:
        if "OPENAI_API_KEY" not in os.environ:
            return {"error": "OPENAI_API_KEY environment variable not set"}, 500

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Answer the user's questions concisely."),
            ("user", "{question}")
        ])
        llm = OpenAI(temperature=0.7) # Using OpenAI as an example
        output_parser = StrOutputParser()

        chain = prompt | llm | output_parser
        response = chain.invoke({"question": question})
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}, 500

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

Next, we need a file that lists all the Python libraries our app needs. This is called `requirements.txt`.

```
# requirements.txt
langchain-core==0.1.33
langchain-community==0.0.29
openai==1.14.0
fastapi==0.110.0
uvicorn==0.29.0
```

### Dockerizing Your LangChain Application

Now, let's put our LangChain app into a Docker container. This means creating a special file called a `Dockerfile`. This file has instructions for Docker on how to build our container. It tells Docker which base operating system to use, how to add our app code, and what commands to run.

Here's what our `Dockerfile` will look like:

```dockerfile
# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app.py .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the uvicorn server when the container launches
# We're using the gunicorn recommended way to run uvicorn in production
# For simplicity, we'll start with a basic uvicorn command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Building the Docker Image

With your `Dockerfile` and `app.py` (and `requirements.txt`) in the same folder, open your computer's terminal.
First, make sure you have Docker Desktop running or Docker installed on your machine.
Then, you can build your Docker image using this command:

```bash
docker build -t my-langchain-app:latest .
```

*   `docker build`: This command tells Docker to build an image.
*   `-t my-langchain-app:latest`: This gives your image a name (`my-langchain-app`) and a tag (`latest`). You can choose any name you like!
*   `.`: This tells Docker to look for the `Dockerfile` in the current folder.

This command will take a moment to download things and build your image. Once it's done, you'll have a Docker image of your LangChain app!

#### Testing Your Docker Image (Optional but Recommended)

You can run your Docker image on your own computer to see if it works before sending it to Kubernetes.

```bash
docker run -p 8000:8000 --env OPENAI_API_KEY="YOUR_ACTUAL_OPENAI_KEY" my-langchain-app:latest
```

*   `-p 8000:8000`: This links port 8000 on your computer to port 8000 inside the Docker container.
*   `--env OPENAI_API_KEY="YOUR_ACTUAL_OPENAI_KEY"`: **IMPORTANT!** You need to provide your actual OpenAI API key here. In a real scenario, you'd use Kubernetes Secrets for this.
*   `my-langchain-app:latest`: This is the name of the image you just built.

After running this, you should see messages from Uvicorn in your terminal. Open another terminal and try to send a request:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the capital of Japan?"}' http://localhost:8000/ask
```

You should get a response like `{"answer": "The capital of Japan is Tokyo."}`. If it works, great! Your Docker container is ready.

#### Pushing to a Docker Registry

For Kubernetes to find your Docker image, it needs to be stored in a place that Kubernetes can access. This place is called a Docker Registry. Docker Hub is a popular public registry, or you can use private registries like AWS ECR, Google Container Registry (GCR), or Azure Container Registry (ACR).

First, log in to Docker Hub (or your chosen registry):

```bash
docker login
```

Then, tag your image with your Docker Hub username (or registry path):

```bash
docker tag my-langchain-app:latest yourusername/my-langchain-app:latest
```

Finally, push your image to the registry:

```bash
docker push yourusername/my-langchain-app:latest
```

Replace `yourusername` with your actual Docker Hub username. Now your Docker container is ready for Kubernetes!

## Setting Up Your Kubernetes Environment

To deploy your LangChain application, you'll need a Kubernetes cluster. Don't worry, setting one up can be quite simple for testing purposes.

### Choosing a Kubernetes Cluster

*   **For Learning and Local Testing:**
    *   **Minikube:** This is a great tool that runs a single-node Kubernetes cluster on your own computer. It's perfect for trying things out without needing a cloud account.
    *   **Kind (Kubernetes in Docker):** Another excellent option for local development, Kind runs Kubernetes nodes as Docker containers.
*   **For Real Applications (Cloud):**
    *   **Amazon Elastic Kubernetes Service (EKS):** Amazon's managed Kubernetes service.
    *   **Google Kubernetes Engine (GKE):** Google's managed Kubernetes service.
    *   **Azure Kubernetes Service (AKS):** Microsoft's managed Kubernetes service.

For this guide, we'll assume you have a Kubernetes cluster running, whether it's Minikube on your laptop or a cloud cluster.

### Installing `kubectl` and `helm`

You'll need two command-line tools on your computer to talk to Kubernetes and use Helm.

*   **`kubectl`:** This is the official tool to control your Kubernetes cluster. You use it to send commands like "show me what's running" or "delete this app." You can find installation instructions on the official Kubernetes website.
    *   [Install `kubectl` documentation](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
*   **`helm`:** This is the tool we use to manage Helm charts, which help us package and deploy applications easily on Kubernetes. You can find installation instructions on the official Helm website.
    *   [Install `helm` documentation](https://helm.sh/docs/intro/install/)

Once installed, make sure they are working by typing `kubectl version` and `helm version` in your terminal. You should see information about their versions.

## Deploying LangChain with Kubernetes Using Helm

This is where the magic happens! We'll use Helm to take our Dockerized LangChain app and deploy it onto our Kubernetes cluster. This is the core of our LangChain with Kubernetes deployment.

### Why Helm for LangChain with Kubernetes Deployment?

Helm charts are super helpful for several reasons when deploying complex applications like LangChain.
They let you define your application's setup once and then deploy it many times with small changes. This is part of what makes Kubernetes packaging so powerful. Helm helps you manage updates, rollbacks, and even share your application's setup with others easily.

Imagine you have a complex multi-step AI agent built with LangGraph; deploying such a system manually on Kubernetes could be tricky. Helm makes it manageable. You can learn more about building such agents here: [LangGraph StateGraph for Multi-Step AI Agents]({% post_url 2026-04-05-langgraph-stategraph-multi-step-ai-agent %}).

### Creating a Helm Chart

First, let's create a basic Helm chart. Open your terminal and run this command:

```bash
helm create langchain-app-chart
```

This command creates a new folder called `langchain-app-chart`. Inside, you'll find a basic structure of a Helm chart.

Let's look at the important files and folders within `langchain-app-chart`:

*   `Chart.yaml`: This file holds information about your chart, like its name, version, and a small description.
*   `values.yaml`: This is a very important file! It's where you put all the customizable settings for your application, like the Docker image name, the number of copies (replicas), and any special environment variables.
*   `templates/`: This folder contains the actual Kubernetes configuration files, but with placeholders. Helm fills in these placeholders using the values from `values.yaml`. You'll find `deployment.yaml` (how to run your app) and `service.yaml` (how to access your app) here.

### Customizing the Helm Chart for LangChain

Now, we need to tell our Helm chart about our specific LangChain application.

#### Modifying `values.yaml`

Open `langchain-app-chart/values.yaml` and make some changes. We need to tell it about our Docker image and our OpenAI API key.

```yaml
# langchain-app-chart/values.yaml
# Default values for langchain-app-chart.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

replicaCount: 1

image:
  repository: yourusername/my-langchain-app # Replace with your Docker Hub username and image name
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "latest"

imagePullSecrets: []
nameOverride: ""
fullnameOverride: ""

serviceAccount:
  # Specifies whether a service account should be created
  create: true
  # Annotations to add to the service account
  annotations: {}
  # The name of the service account to use.
  # If not set and create is true, a name is generated using the fullname template
  name: ""

podAnnotations: {}
podSecurityContext: {}
  # fsGroup: 2000

securityContext: {}
  # capabilities:
  #   drop:
  #   - ALL
  # readOnlyRootFilesystem: true
  # runAsNonRoot: true
  # runAsUser: 1000

service:
  type: ClusterIP
  port: 8000 # Our FastAPI app runs on port 8000

ingress:
  enabled: false
  className: ""
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: chart-example.local
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls: []
  #  - secretName: chart-example-tls
  #    hosts:
  #      - chart-example.local

resources: {}
  # We usually recommend not to specify default resources and to leave this as a conscious
  # choice for the user. This also increases chances charts run on environments with little
  # resources, such as Minikube. If you do want to specify resources, uncomment the following
  # lines, adjust them as necessary, and remove the curly braces after 'resources:'.
  # limits:
  #   cpu: 100m
  #   memory: 128Mi
  # requests:
  #   cpu: 100m
  #   memory: 128Mi

autoscaling:
  enabled: false
  minReplicas: 1
  maxReplicas: 100
  targetCPUUtilizationPercentage: 80
  # targetMemoryUtilizationPercentage: 80

nodeSelector: {}

tolerations: []

affinity: {}

# Add environment variables for your application here
env:
  # This is how you pass sensitive information like API keys.
  # For production, you should use Kubernetes Secrets.
  # For now, we'll demonstrate using a plain environment variable,
  # but be aware of the security implications.
  OPENAI_API_KEY: "YOUR_OPENAI_API_KEY" # Replace with your actual key (use K8s Secrets for production!)

```

**CRITICAL SECURITY NOTE:** Directly putting your `OPENAI_API_KEY` in `values.yaml` is **NOT secure for production**. For real-world applications, you should use Kubernetes Secrets to store sensitive information. We're doing it this way here for simplicity in this practical guide.

#### Modifying `templates/deployment.yaml`

Next, we'll adjust `langchain-app-chart/templates/deployment.yaml`. This file tells Kubernetes how to run your application's Docker containers. We need to ensure it uses our image and exposes the correct port. We also need to add our environment variable here.

Find the `containers:` section and update it. Pay attention to how the `env` section connects to `values.yaml`.

```yaml
{% raw %}
# langchain-app-chart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "langchain-app-chart.fullname" . }}
  labels:
    {{- include "langchain-app-chart.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "langchain-app-chart.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "langchain-app-chart.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "langchain-app-chart.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      containers:
        - name: {{ .Chart.Name }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: 8000 # Our FastAPI app listens on port 8000
              protocol: TCP
          env: # Added this section for environment variables
            - name: OPENAI_API_KEY
              value: {{ .Values.env.OPENAI_API_KEY | quote }}
          livenessProbe:
            httpGet:
              path: /health # Our FastAPI app has a /health endpoint
              port: http
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health # Our FastAPI app has a /health endpoint
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
{% endraw %}
```

We added the `env` section to pass our `OPENAI_API_KEY` to the container. We also added `livenessProbe` and `readinessProbe` to our `deployment.yaml`. These probes tell Kubernetes how to check if our LangChain application is healthy and ready to receive traffic. Our FastAPI app has a `/health` endpoint for this!

#### Modifying `templates/service.yaml`

Finally, check `langchain-app-chart/templates/service.yaml`. This file tells Kubernetes how to expose your application to other services inside the cluster or to the outside world.

```yaml
{% raw %}
# langchain-app-chart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "langchain-app-chart.fullname" . }}
  labels:
    {{- include "langchain-app-chart.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: http # This maps to the name 'http' in the deployment's containerPort
      protocol: TCP
      name: http
  selector:
    {{- include "langchain-app-chart.selectorLabels" . | nindent 4 }}
{% endraw %}
```

Ensure `targetPort` matches the `containerPort` (8000) we defined in `deployment.yaml`. Also, the `port` in `service.yaml` matches the `service.port` in `values.yaml` (8000).

### Deploying Your LangChain Application

Now that our Helm chart is customized, it's time to deploy! Navigate to the directory *above* `langchain-app-chart` in your terminal.

```bash
cd .. # if you are inside langchain-app-chart, go up one level
```

Then, run the `helm install` command:

```bash
helm install my-langchain-release ./langchain-app-chart
```

*   `helm install`: This command tells Helm to install your application.
*   `my-langchain-release`: This is the name for your specific deployment (called a "release"). You can choose any name.
*   `./langchain-app-chart`: This tells Helm where to find your chart files.

Helm will process your chart, fill in the placeholders from `values.yaml`, and send all the Kubernetes configuration to your cluster.

#### Checking Deployment Status

You can check if your application is running correctly using `kubectl`:

```bash
kubectl get pods
```

You should see a pod (which is your Docker container running) with a name like `my-langchain-release-langchain-app-chart-xxxxxxx-yyyyy` and a status of `Running`.

You can also check the deployment:

```bash
kubectl get deployment
```

And the service:

```bash
kubectl get service
```

This will show you the service Kubernetes created to make your LangChain app accessible.

## Accessing Your Deployed LangChain Application

Your LangChain application is now running inside your Kubernetes cluster! But how do you talk to it?

### Finding the Service IP/Port

If your `service.type` is `ClusterIP` (which is the default), your service is only reachable from *inside* the Kubernetes cluster. This is good for internal services.

To access it from *outside* the cluster (like from your web browser or `curl` command), you typically change the service type or use an Ingress.

**Option 1: Using `kubectl port-forward` (for local testing)**

This is the easiest way to test your `ClusterIP` service from your local machine. It creates a temporary connection.

```bash
kubectl port-forward service/my-langchain-release-langchain-app-chart 8000:8000
```

This command will forward traffic from port 8000 on your local machine to port 8000 on your LangChain service inside the cluster. Keep this terminal window open.

**Option 2: Changing Service Type to `NodePort` (for basic external access)**

You can change `service.type` in your `values.yaml` to `NodePort`. Then, update your Helm release:

```yaml
# In values.yaml
service:
  type: NodePort # Change from ClusterIP to NodePort
  port: 8000
```

Then update your deployment:

```bash
helm upgrade my-langchain-release ./langchain-app-chart
```

After the upgrade, get the service details:

```bash
kubectl get service my-langchain-release-langchain-app-chart
```

Look for the `PORT(S)` column. It will show something like `8000:3xxxx/TCP`. The `3xxxx` is the NodePort. You can then access your app using `http://<YOUR_CLUSTER_NODE_IP>:3xxxx`. If you're using Minikube, you can get the IP with `minikube ip`.

**Option 3: Using an Ingress (for production and domain names)**

For a proper production setup, you would use an Ingress controller and an Ingress resource. An Ingress provides intelligent routing for external HTTP/HTTPS traffic to services within the cluster. You would enable `ingress.enabled: true` in `values.yaml` and configure the host and paths. This is beyond our basic deployment but is crucial for real-world apps.

### Testing the Application

Assuming you're using `kubectl port-forward` from Option 1, open a *new* terminal window.

Now, you can send a request to your LangChain application running in Kubernetes, just like you did with Docker:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the capital of Canada?"}' http://localhost:8000/ask
```

You should see the answer from your LangChain AI! Congratulations, you've successfully completed your LangChain with Kubernetes deployment using Docker containers and Helm charts!

## Managing and Updating Your LangChain Deployment

Deploying is just the beginning! Once your LangChain app is running on Kubernetes, you'll want to manage it, update it, and keep it in tip-top shape. Helm makes these tasks much easier.

### Updating with Helm

Imagine you've made a change to your LangChain application code, or you've updated a dependency. You'll need to:

1.  **Update your `app.py` or `requirements.txt`.**
2.  **Rebuild your Docker image:** `docker build -t yourusername/my-langchain-app:new-tag .` (use a new tag like `v1.1` or `latest` again if you want to overwrite).
3.  **Push the new image to your registry:** `docker push yourusername/my-langchain-app:new-tag`.
4.  **Update your Helm chart's `values.yaml`:** Change `image.tag` to `new-tag`.
5.  **Upgrade your deployment:**

    ```bash
    helm upgrade my-langchain-release ./langchain-app-chart
    ```

Helm will gracefully update your application. It will usually create new pods with the updated image, wait for them to be ready, and then remove the old pods. This ensures your application stays online during the update! This process is smooth due to the Kubernetes packaging provided by Helm.

### Scaling Your LangChain Application

If your LangChain application becomes very popular, you might need more copies (replicas) to handle all the requests.

You can change the `replicaCount` in your `values.yaml` file:

```yaml
# In values.yaml
replicaCount: 3 # Change from 1 to 3
```

Then, run `helm upgrade` again:

```bash
helm upgrade my-langchain-release ./langchain-app-chart
```

Kubernetes will automatically create two more copies of your LangChain app! You can check with `kubectl get pods`.

You can also scale directly using `kubectl` (though Helm is usually preferred for persistent changes):

```bash
kubectl scale deployment my-langchain-release-langchain-app-chart --replicas=5
```

### Rolling Back Your Deployment

Oops! Sometimes, an update doesn't go as planned. Maybe the new version of your LangChain app has a bug. Helm has a fantastic feature for this: rollback. You can go back to a previous, working version of your application with a single command.

First, see the history of your deployments (releases):

```bash
helm history my-langchain-release
```

You'll see a list of revisions. To go back to a specific revision (e.g., revision 1), use:

```bash
helm rollback my-langchain-release 1
```

Helm will undo the changes and bring back the previous stable version of your LangChain with Kubernetes deployment. This is a lifesaver in production environments.

### Monitoring Your LangChain Application

Keeping an eye on your LangChain app in Kubernetes is important. Kubernetes has built-in ways to check if your pods are healthy (our liveness and readiness probes help here). For more advanced monitoring, you might use tools like Prometheus and Grafana to track performance, errors, and resource usage. These tools can give you dashboards to see exactly how your LangChain application is doing.

## Advanced Considerations for LangChain with Kubernetes Deployment

While we've covered the basics, there are often more things to think about for a robust LangChain with Kubernetes deployment in a real-world scenario.

### Persistent Storage

Does your LangChain application need to save information, like a vector store for RAG, or a database? Docker containers are usually "ephemeral," meaning any data saved inside them is lost when the container stops.

For data that needs to stick around, you'll need **Persistent Volumes** in Kubernetes. This connects storage from your cluster (like a cloud disk) to your LangChain pods. If you're building RAG applications that rely on persistent vector stores, you'd definitely need this. For advanced RAG setups, you can explore concepts like hybrid search: [LangChain Weaviate Hybrid Search for Scalable RAG]({% post_url 2026-04-05-langchain-weaviate-hybrid-search-scalable-rag %}).

You would add `PersistentVolumeClaim` and `VolumeMount` configurations to your Helm chart's `deployment.yaml`.

### Secrets Management

We touched on this earlier: putting API keys directly in `values.yaml` is risky. Kubernetes has a special object called **Secrets** to store sensitive data like API keys, database passwords, or private keys.

You would create a Kubernetes Secret first:

```bash
kubectl create secret generic openai-api-key-secret --from-literal=OPENAI_API_KEY="YOUR_ACTUAL_OPENAI_KEY"
```

Then, you would modify your `deployment.yaml` to fetch the API key from this secret, instead of from `values.yaml`.

```yaml
{% raw %}
# Inside containers section in templates/deployment.yaml
          env:
            - name: OPENAI_API_KEY
              valueFrom:
                secretKeyRef:
                  name: openai-api-key-secret # Name of the secret you created
                  key: OPENAI_API_KEY # Key within the secret
{% endraw %}
```

This keeps your sensitive information secure and separate from your main application code or configuration.

### Ingress for External Access

For public-facing LangChain applications, you'll want to set up an **Ingress**. An Ingress acts as a smart router, allowing you to expose your services to the internet using domain names (like `my.langchain.app`) and handle things like SSL/TLS encryption.

You would enable `ingress.enabled: true` in your `values.yaml` and configure the `hosts` and `paths` for your application. This often requires an Ingress controller (like Nginx Ingress or Traefik) to be running in your cluster.

### Resource Management

In `deployment.yaml`, you can specify how much CPU and memory your LangChain application pods need (requests) and how much they are allowed to use (limits).

```yaml
{% raw %}
# In templates/deployment.yaml, within the container spec
          resources:
            limits:
              cpu: 500m   # 0.5 CPU core
              memory: 1Gi # 1 Gigabyte of memory
            requests:
              cpu: 200m   # 0.2 CPU core (minimum needed)
              memory: 512Mi # 512 Megabytes of memory (minimum needed)
{% endraw %}
```

Setting `requests` helps Kubernetes schedule your pods efficiently, and `limits` prevents a runaway LangChain process from consuming all resources on a node.

### CI/CD Integration

For teams, automating the build and deployment process is key. This is where Continuous Integration/Continuous Deployment (CI/CD) pipelines come in.

You can set up systems like GitLab CI, GitHub Actions, Jenkins, or CircleCI to:

1.  Automatically build your Docker image whenever you push new code.
2.  Push the new Docker image to your registry.
3.  Automatically update your LangChain application on Kubernetes using `helm upgrade`.

This ensures that your LangChain with Kubernetes deployment is always up-to-date with your latest code changes without manual steps.

## Conclusion

Wow, you've come a long way! You've learned how to take your fantastic LangChain application, wrap it up neatly in Docker containers, and then use the mighty Kubernetes to keep it running smoothly. We also saw how Helm charts act as easy instruction manuals for Kubernetes packaging, making the whole LangChain with Kubernetes deployment process much simpler.

By using Docker, Kubernetes, and Helm, you're not just deploying an app; you're building a reliable, scalable, and easy-to-manage system for your AI projects. This setup ensures your LangChain application can handle many users and stay online without constant supervision. Keep experimenting, keep building, and keep making those awesome AI tools available to everyone!

If you're looking to explore more advanced LangChain capabilities, don't forget to check out building custom tools for agents: [LangChain Google Gemini Function Calling Agent with Custom Tools]({% post_url 2026-04-06-langchain-google-gemini-function-calling-agent-custom-tools %}). The world of AI and deployment is vast, and you're now equipped with powerful tools to navigate it!