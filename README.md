# AI Job Hunter System

AI Job Hunter System is an AI-assisted workspace for making the job search process more focused, organized, and practical.

The project helps a candidate prepare for applications by reading their profile and CV, extracting useful information, and building a structured workflow that can later support job matching, document preparation, and application tracking.

The goal is not to create a spam auto-apply bot. The goal is to build a careful assistant that helps the user understand opportunities, prepare better material, and stay in control.

## What The Project Does

At the current stage, the system focuses on the first part of the workflow:

- Cleans and normalizes the user profile.
- Reads CV files from supported document formats.
- Extracts raw CV text and document metadata.
- Sends the CV text to an LLM for structured parsing.
- Produces a CV summary and structured CV data.
- Stores workflow results in a shared agent state.
- Uses LangGraph to connect the first workflow nodes.

The workflow map is documented in [nodes.md](nodes.md).

## Current Workflow

The implemented flow currently connects:

```text
profile_loader_node
  ↓
cv_parsing_node
```

The profile loader prepares user data.  
The CV parsing node validates the CV file, extracts text, asks the LLM to summarize and structure the CV, then writes the result back into the workflow state.

## Tech Stack

- Python
- LangGraph
- LangChain
- Ollama
- OpenAI-compatible model support
- PyMuPDF for PDF extraction
- python-docx for DOCX extraction
- Pydantic for schema validation
- python-dotenv for environment configuration

## Project Structure

```text
src/
  agents/
    graphs/
    nodes/
    prompts/
    schemas/
    states/
    tools/
  models/
  utils/
```

The project separates workflow nodes, reusable tools, prompts, schemas, model configuration, and general utilities. This keeps the agent workflow easier to extend as the system grows.

## Environment

Create a virtual environment and install the requirements:

```bash
pip install -r requirements.txt
```

The project expects model settings to be configured through environment variables. See `.env.example` for the expected values.

## Status

This project is in active development.

The first workflow foundation is in place, and the next work focuses on expanding the job-search pipeline while keeping the system reviewable and user-controlled.

## Design Principle

The system should assist the user, not replace their judgment.

Every generated result should be understandable, editable, and safe to review before it is used in a real application.
