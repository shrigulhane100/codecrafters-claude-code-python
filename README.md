[![progress-banner](https://backend.codecrafters.io/progress/claude-code/60c979a0-a088-46a4-b5bf-0e4e643c9e81)](https://app.codecrafters.io/users/shrigulhane100?r=2qF)



# Terminal AI Coding Assistant (Claude Code Clone)

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![LLM](https://img.shields.io/badge/LLM-REST_API-orange.svg)
![Architecture](https://img.shields.io/badge/Architecture-Agentic-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue)

A powerful, terminal-based AI coding assistant built from scratch to understand code, execute commands, edit files, and autonomously iterate until programming tasks are completed. 

The industry is rapidly shifting from simple chatbots to **autonomous AI agents**. If you've ever wondered how tools like GitHub Copilot, Cursor, or Claude Code actually read your codebase and apply changes, this project reveals the magic under the hood. 


## Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [How It Works (The Agent Loop)](#-how-it-works-the-agent-loop)
- [Development Roadmap](#-development-roadmap)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [Why Build This?](#-why-build-this)

---


## Overview

This project is a custom implementation of an AI-powered CLI assistant (similar to Claude Code). It connects to Large Language Models (LLMs) via REST APIs and uses **tool calling** to interact directly with your local environment. 

Instead of just returning text, this assistant feels alive. You can give it an instruction like, *"Refactor main.py to use a class,"* and watch it autonomously read the file, generate a new version, apply the edits, and verify the changes.


## Key Features

### Core Capabilities
* **Autonomous Task Execution:** The AI can edit files, run system commands, and iterate on its own until a task is fully resolved.
* **LLM Tool Calling:** Translates JSON schemas into executable local actions.
* **Safe Execution Environment:** Controlled guardrails for executing system commands and applying file edits.
* **Context Management:** Efficiently handles conversation history and manages context windows to maintain long-running sessions.

### Advanced Capabilities 
* **Interactive TUI:** A rich Terminal User Interface for an interactive conversational mode.
* **MCP Integration:** Full support for the Model Context Protocol (MCP) to seamlessly connect with external tools and datasets.
* **LSP Server Connection:** Integrates with Language Server Protocols (LSP) for deep, semantic code understanding.
* **Web Search:** Allows the agent to look up real-time documentation or solutions on the web.

---


## How It Works (The Agent Loop)

At the heart of this assistant is the **Agent Loop**. Instead of a simple request/response cycle, the application uses a continuous loop that mimics human reasoning:

1. **Think:** The LLM analyzes the user prompt and the current state of the codebase.
2. **Act:** The LLM decides to use a specific tool (e.g., `read_file`, `execute_bash`, `write_file`).
3. **Observe:** The system executes the tool, captures the output (or error), and feeds it back to the LLM.
4. **Iterate:** The LLM evaluates the new information and repeats the process until the original goal is achieved.

---


## Development Roadmap

This project is built progressively, starting from core API connections up to a complex, extensible architecture.

### Stages 1-7: The Core Agent
- [x] Connect to an LLM via REST APIs.
- [x] Define and register tools (translating JSON schemas into Python actions).
- [x] Implement the core Agent Loop (Think, Act, Observe).
- [x] Safely execute local file edits and system commands.
- [x] Manage context windows and persistent conversation history.

---

## Getting Started

### Prerequisites
* Python 3.9+
* An active API key for your chosen LLM (e.g., Anthropic Claude API, OpenAI API).

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/claude-code-clone.git
   cd claude-code-clone
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your environment variables:**
   Create a `.env` file in the root directory and add your API key:
   ```env
   LLM_API_KEY=your_api_key_here
   ```

---

## Usage

Run the assistant directly from your terminal:

```bash
python main.py
```

### Example Commands
Once the interactive prompt is running, you can ask it to perform complex, multi-step tasks:

```text
> Refactor main.py to use a class structure and add docstrings.
```
**What happens next:**
1. The agent reads `main.py`.
2. It processes the code and generates a refactored version.
3. It overwrites the file.
4. It runs a linter or tests (if instructed) to verify the code works.
5. It reports back to you that the task is complete.


2. Run `./your_program.sh` to run your program, which is implemented in
   `app/main.py`.
3. Run `codecrafters submit` to submit your solution to CodeCrafters. Test
   output will be streamed to your terminal.
