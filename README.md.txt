# AI Agent Workflow Automation Engine

## Overview
This project implements a reusable, metadata-driven AI agent workflow automation engine. Instead of building 10 hard-coded chatbots, workflows are dynamically ingested from an Excel specification file (`data/AI_Agent_Workflow_Assessment (1).xlsx`).

## Architecture
The system consists of:
1. **Dynamic Workflow Registry (`openpyxl` & Pydantic):** Parses workflow metadata (triggers, steps, decision logic, tools, and outputs) directly from the Excel file at runtime.
2. **Intent Router:** Evaluates natural language user queries and routes them to the appropriate workflow.
3. **Execution Engine & Simulated Tools:** Executes discrete workflow steps sequentially, enforces business thresholds/rules, and handles error states.
4. **Standardized Tracing:** Emits structured output showing the Selected Workflow, numbered Steps Executed, and the Final Result.

## Scalability: Adding an 11th Workflow
Adding an 11th workflow requires **zero changes to the core orchestration engine**:
1. Add a new row to the Excel sheet (`Workflow_ID`, `Workflow_Name`, `Trigger`, `Steps`, `Decision_Logic`, `Tools_Required`).
2. Add any new tool functions needed to the tool registry.
The engine automatically ingests the definition on the next execution.

## Setup & Running
1. Activate environment:
   ```bash
   venv\Scripts\activate