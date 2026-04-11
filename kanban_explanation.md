# Kanban Board Explanation and Our Custom Implementation

## What is a Kanban Board?

A **Kanban board** is a visual workflow management tool that uses columns (representing stages of work) and cards (representing individual tasks or issues) to show the progress of work through a process.

### Core Principles of Kanban
1. **Visualize Workflow** - Make work visible to all team members
2. **Limit Work-In-Progress (WIP)** - Prevent bottlenecks and reduce multitasking
3. **Manage Flow** - Smooth progression of work through stages
4. **Make Policies Explicit** - Clear rules for moving cards
5. **Implement Feedback Loops** - Continuous improvement through metrics

## Our Custom Kanban Board Structure

### Column Workflow
To Do → In Progress → Testing → In Review → Blocked → Done

### Column Descriptions

| Column | Purpose | WIP Limit | Description |
|--------|---------|-----------|-------------|
| To Do | Backlog of items | Unlimited | New issues to be worked on |
| In Progress | Currently being developed | 5 items | Developer actively working |
| Testing | QA validation phase | 3 items | Development complete, testing |
| In Review | Code review process | 4 items | Ready for peer review |
| Blocked | Waiting on dependencies | 2 items | Blocker discovered |
| Done | Completed and merged | Unlimited | Successfully merged to main |

## How WIP Limits Prevent Bottlenecks

When Testing column has 3 items (limit reached), developers cannot move new items there until something moves to "In Review". This prevents QA overload and encourages team collaboration.

## Agile Principles Supported

✅ **Continuous Delivery** - Smooth flow from To Do to Done  
✅ **Transparency** - Real-time status visibility  
✅ **Adaptability** - Columns can be adjusted as needed  
✅ **Collaboration** - Clear task ownership via assignments  
✅ **Efficiency** - WIP limits reduce multitasking  
✅ **Feedback** - Board metrics reveal process improvements
