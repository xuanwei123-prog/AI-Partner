# 🤖 AI Intelligent Companion (AI智能伴侣)

A highly customizable, interactive AI companion web application powered by **Streamlit** and the **Anthropic API**. This application allows users to define the AI's personality and maintains persistent local chat sessions for a continuous conversational experience.

## ✨ Key Features

* **Customizable Persona:** Dynamically adjust the AI's nickname and personality traits (e.g., "A gentle and cute Malaysian girl") through the sidebar control panel.
* **Real-time Streaming:** Utilizes Anthropic's message streaming functionality for a fast, typewriter-like response experience.
* **Session Management:** Automatically saves chat histories locally as JSON files. Users can easily create new sessions, load previous conversations, or delete old histories.
* **Roleplay Enforcement:** The system prompt strictly enforces the AI to adopt the assigned persona, use appropriate emojis, and respond concisely like a real messaging app.

## 🛠️ Tech Stack

* **Frontend & Backend UI:** Python (Streamlit)
* **LLM Provider:** Anthropic Claude API
* **Data Storage:** Local JSON file system

## 🚀 Getting Started

### Prerequisites
* Python 3.8 or higher
* An active Anthropic API Key

### Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
