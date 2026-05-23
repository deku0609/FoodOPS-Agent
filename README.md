# FoodOPS Agent

FoodOPS Agent is an AI-powered restaurant operations assistant built with Python, Streamlit, Pandas, and OpenRouter-compatible LLM APIs.

The project started as an offline chatbot prototype and evolved into a more grounded restaurant assistant that can answer business questions using structured CSV data, dashboard metrics, and evaluation workflows.

## Project Overview

This project simulates a restaurant operations environment and includes:

- A restaurant analytics dashboard
- An offline chatbot prototype
- An online chatbot assistant
- Offline and online evaluation scripts
- Synthetic restaurant data generated using Python
- A red-team benchmark to test factual, policy-based, unsupported, and adversarial prompts

The goal of the project was not just to build a chatbot UI, but to explore how grounded business context, evaluation logic, and safer response behavior improve the usefulness of an AI assistant.

## Features

- Interactive restaurant dashboard built in Streamlit
- Chatbot support for restaurant operations queries
- Synthetic restaurant dataset generation
- Data cleaning and analysis workflow
- Offline assistant prototype for initial experimentation
- Online assistant for grounded responses using API-based LLM access
- Red-team evaluation pipeline for testing chatbot performance
- CSV-based benchmark prompts and saved result outputs

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- OpenRouter / OpenAI-compatible API
- Python Dotenv

## Project Structure

```text
foodops-agent/
│
├── data/
├── docs/
├── notebooks/
├── generate_data.py
├── clean_analyse.py
├── dashboard.py
├── offline_assistant.py
├── eval_offline.py
├── online_assistant.py
├── eval_online.py
├── redteam_questions.csv
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## File Descriptions

- `generate_data.py`  
  Generates the synthetic restaurant operations dataset used in the project.

- `clean_analyse.py`  
  Cleans and analyses the generated data before dashboard or assistant use.

- `dashboard.py`  
  Streamlit dashboard showing business metrics such as revenue, orders, bookings, and top-selling items.

- `offline_assistant.py`  
  Initial offline chatbot prototype built as the first version of the assistant.

- `eval_offline.py`  
  Evaluation script for testing the offline chatbot behavior.

- `online_assistant.py`  
  Online AI assistant connected through an API and grounded using business context.

- `eval_online.py`  
  Red-team evaluation script for the online assistant.

- `redteam_questions.csv`  
  Benchmark prompt set covering factual, policy, unsupported, and adversarial questions.

## Synthetic Data Note

This project uses synthetically generated restaurant operations data created for demo, experimentation, and evaluation purposes.

It does not contain real customer, restaurant, or production business records.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/deku0609/foodops-agent.git
cd foodops-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows
```bash
.venv\Scripts\activate
```

#### macOS / Linux
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create a `.env` file

Create a file named `.env` in the project root and add your API key:

```env
OPENROUTER_API_KEY=your_openrouter_key_here
```

Do not upload your real `.env` file to GitHub.

## Running the Project

### Generate synthetic data
```bash
python generate_data.py
```

### Clean and analyse data
```bash
python clean_analyse.py
```

### Run the dashboard
```bash
streamlit run dashboard.py
```

### Run the offline assistant
```bash
streamlit run offline_assistant.py
```

### Evaluate the offline assistant
```bash
python eval_offline.py
```

### Run the online assistant
```bash
streamlit run online_assistant.py
```

### Evaluate the online assistant
```bash
python eval_online.py
```

## Evaluation

The project includes a red-team benchmark designed to test the assistant across multiple prompt categories:

- Factual questions
- Policy-based questions
- Unsupported questions
- Adversarial questions

The online evaluation workflow was used to test whether the assistant remained grounded, refused unsupported requests appropriately, and handled restaurant operations questions more reliably.

## Results

The final online assistant achieved strong benchmark performance on the structured red-team test set after improving evaluation logic and grounding behavior.

You can include screenshots of:
- the dashboard
- the chatbot interface
- the evaluation summary
- benchmark outputs

inside the `docs/` folder and reference them here later.

## Why This Project Matters

This project reflects an end-to-end AI application workflow:

- synthetic data generation
- data cleaning and analysis
- dashboard building
- assistant development
- evaluation and red-team testing
- iterative improvement from prototype to stronger system design

It also highlights an important practical lesson: building an AI assistant is not only about generating responses, but about grounding, reliability, evaluation, and usability in a realistic setting.

## Future Improvements

- Improve retrieval and grounding logic further
- Add conversation memory and better prompt orchestration
- Expand benchmark coverage
- Deploy the project publicly
- Improve UI and documentation

## Screenshots

Add your screenshots inside the `docs/` folder and display them here later, for example:

```md



```

## Author

Built by [Om Vishwakarma](https://github.com/deku0609)

## License

This project is available under the MIT License.
