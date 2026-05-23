# FoodOPS Agent

FoodOPS Agent is an AI-powered restaurant operations assistant built using Python, Streamlit, and OpenRouter/OpenAI-compatible APIs.

## Features
- Restaurant operations dashboard
- AI chatbot for grounded business queries
- Online evaluation pipeline
- Red-team benchmark for factual, policy, unsupported, and adversarial prompts

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly
- OpenRouter / OpenAI API

## Project Files
- `3-dashboard.py` — restaurant analytics dashboard
- `4-ai-assistant.py` — chatbot assistant
- `7-eval-online.py` — online red-team evaluation script

## Setup
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Create a `.env` file with your API key
5. Run the project

## Environment Variables
Create a `.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_key_here
```

## Run
```bash
streamlit run "3-dashboard.py"
streamlit run "4-ai-assistant.py"
python "7-eval-online.py"
```

## Results
The chatbot was evaluated on factual, policy, unsupported, and adversarial prompts using a red-team benchmark.
