---
title: "LangGraph Human in the Loop: Multi-Step Approval Workflows with Checkpoints"
description: "Discover how to implement robust langgraph multi-step approval checkpoints, creating human-in-the-loop workflows with resumable processes for enhanced AI apps."
author_profile: true
read_time: true
comments: true
share: true
related: true
toc: true 
toc_sticky: true 
toc_icon: "list-ul"
tags: [langgraph multi-step approval checkpoints]
featured: false
image: '/assets/images/langgraph-human-loop-multi-step-approval-checkpoints.webp'
---

## Unlock Powerful Workflows: LangGraph Human in the Loop for Multi-Step Approvals with Checkpoints

Imagine you have an important task at work. This task needs many people to say "yes" before it can move forward. For example, getting a new idea approved, requesting a big purchase, or signing off on a new project plan. This is where `langgraph multi-step approval checkpoints` become super helpful.

It's like playing a game where you need to clear several levels, and at each level, a different person needs to give their permission. If someone says "no," you might need to go back a few steps or try a different path. Sounds complicated, right?

Not with LangGraph! We are going to explore how LangGraph makes these `complex approval patterns` easy to manage. You will learn how to build robust systems where humans and AI work together, making sure every step is just right.

### What are Approval Workflows and Why Do They Matter?

Think about how things get done in a big company. Many decisions are not made by just one person. They often need several people to review and agree. This series of steps is called an approval workflow.

These workflows ensure that decisions are fair, compliant, and well-thought-out. Without them, chaos might happen, leading to mistakes or bad decisions. That's why having clear `multi-stage approval design` is super important for smooth operations.

When you need different people to approve at different times, it's a `sequential approvals` process. Sometimes, many people need to approve at the same time, which we call `parallel approval paths`. Both are vital for different types of tasks.

### The Challenge of Complex Approvals

Building these approval systems can be tricky. What happens if someone approves, but then the next person rejects it? Do you lose all the progress? Or what if the system crashes in the middle of an approval?

Traditional systems might make you start all over again. This can be very frustrating and waste a lot of time. It makes `progress tracking` difficult and recovery even harder.

Imagine building a house, and every time someone changes their mind about a wall, you have to tear down the whole house. That's how some old approval systems feel! We need a smarter way to handle these changes and pauses.

### Introducing LangGraph: Your Workflow Maestro

LangGraph is like a smart manager for your workflow. It helps you draw a map of all the steps your task needs to go through. Each step can be a human action, an AI decision, or an automated task.

LangGraph is built on LangChain, which helps you create AI agents. But LangGraph adds the ability to create more powerful, stateful, and cyclic workflows. It helps define the `workflow orchestration` needed for complex processes.

You can think of it as building a story where different characters (humans or AI) take turns to move the story forward. You define the rules for who does what and when. To learn more about the basics of LangChain, you can check out this [Beginner's Guide to LangChain](https://python.langchain.com/docs/get_started/introduction).

### Human in the Loop: When People and AI Work Together

"Human in the Loop" (HITL) means that people are part of the automated process. An AI might do some work, but then a human reviews it, makes a decision, or adds their special touch. This blend makes systems both efficient and smart.

For approval workflows, HITL is essential. AI can pre-fill forms or suggest actions, but a human must give the final "go" or "no go." This ensures accuracy and handles situations where only human judgment truly counts.

You get the best of both worlds: the speed and consistency of AI, combined with the wisdom and flexibility of human decision-making. This is crucial for sensitive tasks that require careful review.

### Checkpoints: Saving Your Progress Along the Way

What if you're building that house, and you finish the first floor? You'd want to save that progress, right? You wouldn't want to rebuild it if a problem came up later on. This is exactly what `checkpoint strategies` do for your workflow.

A checkpoint is a saved state of your workflow at a specific point. If something goes wrong, or if you need to pause and resume later, you can start right from that saved point. You don't lose all your hard work!

This feature is incredibly powerful for `langgraph multi-step approval checkpoints`. It means you can have long, complex approval processes, and no matter what happens, you can always pick up where you left off. It ensures resilience and a smoother experience for everyone involved.

### Why LangGraph's Checkpoints are a Game Changer

Without checkpoints, a rejection in a multi-step approval process often means restarting from the very beginning. This is inefficient and frustrating. LangGraph changes that by letting you define points where the workflow's state is saved.

This means if an approval fails at step 3 of 5, you might only need to revisit steps 2 and 3, not 1, 2, 3, 4, and 5 again. It simplifies `stage transition handling` and makes your workflows much more robust.

The ability to save and restore state is fundamental for building reliable systems, especially for enterprise-level `workflow orchestration`. For more advanced options, you might consider dedicated [checkpoint management systems](https://docs.python.org/3/library/pickle.html).

### Building a Simple Multi-Step Approval Workflow with LangGraph

Let's imagine a simple "Expense Report Approval" workflow.

1.  **Employee submits report.** (Automated initial step)
2.  **Manager approves.** (Human step)
3.  **Finance reviews.** (Human step)
4.  **Final approval.** (Human step)

If the manager rejects it, the employee needs to fix it and resubmit, but we don't want to lose the initial submission details.

#### H3: Basic Setup for Your LangGraph Workflow

First, you'd set up your LangGraph environment. You'll need to install the necessary libraries.

```python
# Assuming you have Python installed
# pip install langchain_core langchain_community langgraph
```

Next, you define the "nodes" in your graph. Each node is a step in your workflow.

#### H3: Defining Nodes: Human Approval and Automated Steps

In LangGraph, nodes are like functions that do a specific job.

```python
from langgraph.graph import StateGraph, START, END

# Define your workflow state
# This dictionary will hold all the information passed between steps
class WorkflowState(TypedDict):
    report_id: str
    amount: float
    status: str
    manager_feedback: Optional[str]
    finance_feedback: Optional[str]
    history: List[str] # To track progress

def submit_expense(state: WorkflowState):
    # This is an automated step where the employee's submission is processed
    print(f"Employee submitted report {state['report_id']} for ${state['amount']}.")
    return {"status": "Submitted", "history": state["history"] + ["Submitted"]}

def manager_approval_node(state: WorkflowState):
    # This is where a human manager would interact.
    # In a real system, this would trigger an email or a UI task for the manager.
    # For this example, we simulate a decision.
    print(f"Manager needs to approve report {state['report_id']}.")
    # Simulate manager decision
    manager_decision = input("Manager: Approve or Reject? (A/R): ").upper()
    feedback = input("Manager feedback (optional): ")
    if manager_decision == "A":
        return {"status": "Manager Approved", "manager_feedback": feedback, "history": state["history"] + ["Manager Approved"]}
    else:
        return {"status": "Manager Rejected", "manager_feedback": feedback, "history": state["history"] + ["Manager Rejected"]}

def finance_review_node(state: WorkflowState):
    # Similar to manager approval, but for finance
    print(f"Finance needs to review report {state['report_id']}.")
    # Simulate finance decision
    finance_decision = input("Finance: Approve or Reject? (A/R): ").upper()
    feedback = input("Finance feedback (optional): ")
    if finance_decision == "A":
        return {"status": "Finance Approved", "finance_feedback": feedback, "history": state["history"] + ["Finance Approved"]}
    else:
        return {"status": "Finance Rejected", "finance_feedback": feedback, "history": state["history"] + ["Finance Rejected"]}

def final_approval_node(state: WorkflowState):
    # The last human approval step
    print(f"Senior approver needs to give final approval for report {state['report_id']}.")
    final_decision = input("Final Approver: Approve or Reject? (A/R): ").upper()
    if final_decision == "A":
        return {"status": "Fully Approved", "history": state["history"] + ["Fully Approved"]}
    else:
        return {"status": "Final Rejected", "history": state["history"] + ["Final Rejected"]}

def notify_employee(state: WorkflowState):
    # Automated notification
    print(f"Employee notified: Report {state['report_id']} status is {state['status']}.")
    if state.get("manager_feedback"):
        print(f"Manager feedback: {state['manager_feedback']}")
    if state.get("finance_feedback"):
        print(f"Finance feedback: {state['finance_feedback']}")
    return {"history": state["history"] + ["Employee Notified"]}
```

In this setup, each function `submit_expense`, `manager_approval_node`, etc., is a node. When you use `langgraph multi-step approval checkpoints`, you can save the state after any of these nodes.

#### H3: Edges and Conditional Routing

Edges tell LangGraph how to move from one node to another. You can have simple "go to next" edges or "conditional" edges. Conditional edges are smart; they look at the state and decide where to go next. This is key for `approval routing logic`.

```python
# Define the graph
workflow = StateGraph(WorkflowState)

# Add the nodes
workflow.add_node("submit_expense", submit_expense)
workflow.add_node("manager_approval", manager_approval_node)
workflow.add_node("finance_review", finance_review_node)
workflow.add_node("final_approval", final_approval_node)
workflow.add_node("notify_employee", notify_employee)

# Define the start and end points
workflow.set_entry_point("submit_expense")

# Define edges
# After submission, go to manager approval
workflow.add_edge("submit_expense", "manager_approval")

# Manager approval has two paths: Approved or Rejected
workflow.add_conditional_edges(
    "manager_approval",
    lambda state: "finance_review" if state["status"] == "Manager Approved" else "notify_employee",
    {
        "finance_review": "finance_review",
        "notify_employee": "notify_employee"
    }
)

# Finance review also has two paths
workflow.add_conditional_edges(
    "finance_review",
    lambda state: "final_approval" if state["status"] == "Finance Approved" else "notify_employee",
    {
        "final_approval": "final_approval",
        "notify_employee": "notify_employee"
    }
)

# Final approval also has two paths
workflow.add_conditional_edges(
    "final_approval",
    lambda state: "notify_employee", # Always notify after final decision
    {
        "notify_employee": "notify_employee"
    }
)

workflow.add_edge("notify_employee", END) # Workflow ends after notification

# Compile the graph
app = workflow.compile()
```

This setup shows how `approval routing logic` directs the flow based on the decision made at each human interaction point. If the manager approves, it goes to finance. If not, it informs the employee directly.

#### H3: Implementing Checkpoints for Resilience

To use `langgraph multi-step approval checkpoints`, you simply run your compiled graph with a checkpoint saver. LangGraph can use different kinds of checkpoint savers. For development, a memory-based one is fine, but for production, you'd use a database.

```python
from langgraph.checkpoint import MemorySaver
from uuid import uuid4

# Use MemorySaver for demonstration. For production, use a database.
memory = MemorySaver()

# Example usage:
# Create a unique thread ID for each workflow instance (e.g., each expense report)
thread_id = str(uuid4())
initial_state = {"report_id": "EXP-001", "amount": 150.75, "status": "Draft", "history": []}

print(f"Starting workflow for report {initial_state['report_id']} with thread ID: {thread_id}")

# First run: Employee submits and manager approves
print("\n--- Initial Submission and Manager Approval ---")
for s in app.stream(initial_state, {"configurable": {"thread_id": thread_id}},
                    stream_mode="updates"):
    print(s)
    if "manager_approval" in s and s["manager_approval"]["status"] == "Manager Approved":
        print(f"Checkpoint saved after manager approval for {thread_id}.")
        # LangGraph automatically saves checkpoints after each step.
        # We are just logging here to show where it happens.
        pass

# Now, imagine we stop the process and restart later for finance review
# We can load the state from the checkpoint
print("\n--- Loading from checkpoint for Finance Review ---")
loaded_state = app.get_state({"configurable": {"thread_id": thread_id}})
print(f"Loaded state for {thread_id}: {loaded_state.values}")

# Continue the workflow from the loaded state (Finance Review)
# If the manager rejected, this part wouldn't run, as the workflow would have ended.
if loaded_state.values["status"] == "Manager Approved":
    print("\n--- Continuing to Finance Review ---")
    for s in app.stream(None, {"configurable": {"thread_id": thread_id}},
                        stream_mode="updates"):
        print(s)
        if "finance_review" in s and s["finance_review"]["status"] == "Finance Approved":
            print(f"Checkpoint saved after finance approval for {thread_id}.")
            pass

# Let's check the state again after finance review (or rejection)
loaded_state_after_finance = app.get_state({"configurable": {"thread_id": thread_id}})
print(f"State after finance review: {loaded_state_after_finance.values}")

# Continuing to final approval if finance approved
if loaded_state_after_finance.values["status"] == "Finance Approved":
    print("\n--- Continuing to Final Approval ---")
    for s in app.stream(None, {"configurable": {"thread_id": thread_id}},
                        stream_mode="updates"):
        print(s)
    final_state = app.get_state({"configurable": {"thread_id": thread_id}})
    print(f"Final state: {final_state.values}")

```
The `app.stream()` method with `{"configurable": {"thread_id": thread_id}}` automatically saves the workflow's state after each node runs. If you restart your application or need to pick up a workflow later, you can use `app.get_state()` with the `thread_id` to retrieve the last saved state. This is how `checkpoint strategies` make your application fault-tolerant.

#### H3: Handling Rejections and Retries

If an approval is rejected, LangGraph's conditional edges allow you to route the workflow back to an earlier stage or to a notification step. For instance, if the manager rejects, the system notifies the employee. The employee can then restart the process, potentially with a revised report.

For a true retry, you could have a dedicated node that modifies the state based on feedback.

```python
def revise_and_resubmit_node(state: WorkflowState):
    print(f"Report {state['report_id']} was rejected. Please revise and resubmit.")
    # In a real app, this would trigger a UI for the employee to edit.
    # For simulation, we assume employee revises and resubmits.
    revised_amount = float(input(f"Enter revised amount for {state['report_id']}: "))
    print(f"Employee revised report {state['report_id']} to ${revised_amount} and resubmitted.")
    return {"status": "Resubmitted", "amount": revised_amount, "history": state["history"] + ["Resubmitted"]}

# Modify graph to include a retry path
workflow_retry = StateGraph(WorkflowState)
workflow_retry.add_node("submit_expense", submit_expense)
workflow_retry.add_node("manager_approval", manager_approval_node)
workflow_retry.add_node("finance_review", finance_review_node)
workflow_retry.add_node("final_approval", final_approval_node)
workflow_retry.add_node("notify_employee", notify_employee)
workflow_retry.add_node("revise_and_resubmit", revise_and_resubmit_node)

workflow_retry.set_entry_point("submit_expense")

workflow_retry.add_edge("submit_expense", "manager_approval")

workflow_retry.add_conditional_edges(
    "manager_approval",
    lambda state: "finance_review" if state["status"] == "Manager Approved" else "revise_and_resubmit",
    {
        "finance_review": "finance_review",
        "revise_and_resubmit": "revise_and_resubmit"
    }
)
workflow_retry.add_edge("revise_and_resubmit", "manager_approval") # Loop back to manager approval after revision

# ... (add finance_review and final_approval edges as before,
#      potentially looping back to revise_and_resubmit if they reject)

workflow_retry.add_conditional_edges(
    "finance_review",
    lambda state: "final_approval" if state["status"] == "Finance Approved" else "revise_and_resubmit",
    {
        "final_approval": "final_approval",
        "revise_and_resubmit": "revise_and_resubmit"
    }
)

workflow_retry.add_conditional_edges(
    "final_approval",
    lambda state: "notify_employee" if state["status"] == "Fully Approved" else "revise_and_resubmit", # Only notify on final approval
    {
        "notify_employee": "notify_employee",
        "revise_and_resubmit": "revise_and_resubmit" # If final approver rejects, go back to employee
    }
)

workflow_retry.add_edge("notify_employee", END)

app_retry = workflow_retry.compile()

# Example with retry:
retry_thread_id = str(uuid4())
initial_state_retry = {"report_id": "EXP-002", "amount": 200.00, "status": "Draft", "history": []}

print(f"\n--- Starting workflow with retry path for {initial_state_retry['report_id']} ---")
for s in app_retry.stream(initial_state_retry, {"configurable": {"thread_id": retry_thread_id}},
                          stream_mode="updates"):
    print(s)

# If the manager rejected, you'll see the "revise_and_resubmit" node fire,
# then it loops back to "manager_approval".
```

This example shows how `langgraph multi-step approval checkpoints` combined with conditional routing can handle complex rejections and allow for re-submission and re-approval cycles. It ensures that no progress is truly lost, even if an item needs revision.

### Advanced Approval Patterns with LangGraph

LangGraph's flexible graph structure allows you to model almost any `complex approval patterns`.

#### H3: Sequential Approvals

This is the most common pattern, where approvals happen one after another. Our expense report example is a perfect instance of `sequential approvals`.

```
Step 1 (Submit) -> Step 2 (Manager) -> Step 3 (Finance) -> Step 4 (Final)
```

Each step relies on the previous one finishing successfully. LangGraph handles this naturally by chaining nodes with edges.

#### H3: Parallel Approval Paths

Sometimes, multiple people or departments need to approve something at the same time. For example, a new project might need approval from both the IT department and the Legal department independently.

```
          /-> IT Approval
Step 1 -> -- -- -- --> Final Merge
          \-> Legal Approval
```

LangGraph can model `parallel approval paths` by creating branches in your graph. You would then have a "join" node that waits for all parallel branches to complete before moving on. This is handled using a special `tools_condition` or by custom logic in a node that checks the state of all parallel branches.

#### H3: Conditional Approvals and Approval Dependencies

What if an approval step only happens under certain conditions? For instance, only expense reports over $1000 need a "VP Approval," otherwise, "Finance Approval" is enough. This represents `approval dependencies`.

```python
# Example of a conditional node based on amount
def vp_approval_node(state: WorkflowState):
    print(f"VP needs to approve report {state['report_id']} over $1000.")
    vp_decision = input("VP: Approve or Reject? (A/R): ").upper()
    if vp_decision == "A":
        return {"status": "VP Approved", "history": state["history"] + ["VP Approved"]}
    else:
        return {"status": "VP Rejected", "history": state["history"] + ["VP Rejected"]}

# Modifying the graph for conditional VP approval
workflow_conditional = StateGraph(WorkflowState)
# ... add existing nodes ...
workflow_conditional.add_node("vp_approval", vp_approval_node)
workflow_conditional.set_entry_point("submit_expense")
workflow_conditional.add_edge("submit_expense", "manager_approval")

workflow_conditional.add_conditional_edges(
    "manager_approval",
    # If manager approves, check amount for VP approval
    lambda state: "vp_approval" if state["status"] == "Manager Approved" and state["amount"] > 1000 else \
                  "finance_review" if state["status"] == "Manager Approved" else "notify_employee",
    {
        "vp_approval": "vp_approval",
        "finance_review": "finance_review",
        "notify_employee": "notify_employee"
    }
)
# After VP approval, go to finance review
workflow_conditional.add_edge("vp_approval", "finance_review")

# ... rest of the finance_review and final_approval edges ...
# (ensure all paths eventually lead to notify_employee and END)

app_conditional = workflow_conditional.compile()

# Example run with a large amount
conditional_thread_id = str(uuid4())
initial_state_conditional = {"report_id": "EXP-003", "amount": 1200.00, "status": "Draft", "history": []}

print(f"\n--- Starting workflow with conditional VP approval for {initial_state_conditional['report_id']} ---")
for s in app_conditional.stream(initial_state_conditional, {"configurable": {"thread_id": conditional_thread_id}},
                               stream_mode="updates"):
    print(s)
```

This makes your `approval routing logic` incredibly flexible. You can define intricate rules based on any data in your workflow state.

#### H3: Dynamic Routing

In some very advanced cases, the next approval step might not be known beforehand. It could depend on an AI's analysis or data retrieved at runtime. LangGraph supports this by allowing you to dynamically return the next node to execute.

This is a more advanced topic, often involving AI agents deciding the best next step. It lets your workflows adapt to unforeseen circumstances, making them highly intelligent.

### Best Practices for LangGraph Approval Workflows

To make sure your `langgraph multi-step approval checkpoints` work perfectly, follow these tips.

#### H3: Designing Your Multi-Stage Approval Workflows

*   **Map it out:** Before writing code, use a tool like [Lucidchart](https://www.lucidchart.com/pages/affiliate?partner=YourAffiliateID) or [Miro](https://miro.com/affiliate?partner=YourAffiliateID) to visually draw your workflow. Identify every step, decision point, and approval. This is your `multi-stage approval design`.
*   **Define states clearly:** What information needs to be passed between steps? What does the status mean at each point?
*   **Identify human touchpoints:** Mark exactly where a human needs to intervene. This helps you design your user interfaces or notification systems.
*   **Consider edge cases:** What happens if an approval is rejected? What if a step times out? Plan for these scenarios. For complex workflows, you might find pre-built [multi-stage approval templates](https://www.atlassian.com/templates/workflows) useful.

#### H3: Choosing Checkpoint Strategies

*   **Frequency:** Decide how often to save a checkpoint. After every human decision is a good rule of thumb for `langgraph multi-step approval checkpoints`.
*   **Storage:** For production, use a persistent storage like a database (e.g., PostgreSQL, Redis) for your `checkpoint management systems`, not just in-memory. LangGraph has integrations for this.
*   **Granularity:** What exactly needs to be saved in the state? Only the essential information for continuing the workflow.

#### H3: Error Handling and Recovery

*   **Graceful failures:** Design your nodes to handle unexpected inputs or errors. Don't let a single node crash the entire workflow.
*   **Retry mechanisms:** Implement logic to retry failed automated steps.
*   **Human intervention for errors:** For critical errors, route the workflow to a human administrator. This might be a special "Error Handling" node.

#### H3: Monitoring and Auditing

*   **Track progress:** Use the workflow state and history to implement `progress tracking`. Always know where each approval request stands.
*   **Logging:** Log every decision and state change. This is crucial for auditing and compliance.
*   **Alerts:** Set up alerts for workflows that are stalled or have encountered errors.

#### H3: Security and Access Control

*   **Role-based access:** Ensure only authorized users can perform approval actions.
*   **Data privacy:** Protect sensitive information flowing through your workflow.

### Integrating with Other Systems and Tools

Your LangGraph approval workflow rarely lives in isolation.

#### H3: Workflow Orchestration Platforms

For very large or distributed systems, LangGraph can work alongside dedicated `workflow orchestration` platforms.
*   **Temporal.io:** Offers powerful primitives for long-running, fault-tolerant workflows. You can learn more about its capabilities by visiting [Temporal's website](https://temporal.io/affiliate?partner=YourAffiliateID).
*   **Apache Airflow:** Great for scheduling and monitoring data pipelines, which can include parts of an approval workflow. Explore Airflow at [Apache Airflow's site](https://airflow.apache.org/affiliate?partner=YourAffiliateID).
These platforms provide the backbone for running your LangGraph graphs at scale, ensuring reliability and observability. For deeper insights, consider reading up on [orchestration pattern guides](https://docs.microsoft.com/en-us/azure/architecture/patterns/category/orchestration).

#### H3: User Interface and Notification Systems

You'll need a way for humans to interact with the "Human in the Loop" nodes.
*   **Web applications:** Build a simple web interface where managers or finance can see pending approvals and make decisions.
*   **Email/Slack integration:** Send notifications to approvers and allow them to approve/reject directly from their communication tools.
*   **Task management systems:** Integrate with tools like Jira or Asana to create approval tasks.

#### H3: Data Storage

Your workflow state needs a home.
*   **Databases:** Use relational databases (PostgreSQL, MySQL) or NoSQL databases (MongoDB, DynamoDB) to store workflow states and historical data. LangGraph's checkpointing can integrate with these.

#### H3: AI/ML Services

For smarter approval routing or initial document processing, integrate AI services.
*   **Document understanding:** Use AI to extract key information from expense reports or contracts.
*   **Fraud detection:** AI can flag suspicious requests for human review.

To deepen your knowledge in this area, consider enrolling in a [process automation course](https://www.coursera.org/browse/business/business-process-management). If you're looking for tailored solutions, [enterprise workflow consulting](https://www.gartner.com/en/information-technology/consulting) services can offer expert guidance.

### Conclusion: Empowering Your Approval Processes

You've learned how `langgraph multi-step approval checkpoints` can transform complex, error-prone approval processes into robust, intelligent, and user-friendly workflows. By combining the power of LangGraph's state management and conditional routing with human intelligence, you can build systems that truly work.

Whether it's for `sequential approvals`, `parallel approval paths`, or workflows with intricate `approval dependencies`, LangGraph provides the tools you need. The ability to save `checkpoint strategies` means you never lose progress, making your applications more resilient and reliable.

Start designing your next multi-stage approval system with LangGraph. Embrace the "Human in the Loop" approach, and watch your `workflow orchestration` become smarter and more efficient than ever before. If you need advanced `approval routing frameworks`, explore specialized libraries or consider custom development based on these principles.

### Further Reading

Build advanced approval workflows with LangGraph:

- [LangGraph Tutorial 2026: Complete Beginner's Guide to Building AI Agents](/langgraph-tutorial-2026-beginners-guide/)
- [LangGraph Multi-Agent Systems 2026](/langgraph-multi-agent-systems-2026/)
- [LangGraph Human-in-Loop AI Agents: Approval Workflows](/langgraph-human-in-loop-ai-agents-approval-workflows/)
- [LangGraph vs LangChain 2026: Which Should You Use?](/langgraph-vs-langchain-2026/)
- [Best AI Agent Frameworks 2026: LangChain vs AutoGen vs CrewAI](/best-ai-agent-frameworks-2026/)