# Clean Air Marketing Crew

A specialized AI crew for creating environmental marketing content, focusing on clean air products and solutions.

## Features

- Market research on air quality issues and solutions
- Marketing strategy development for clean air products
- Content creation for environmentally conscious consumers

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   ```

## Usage

Run the crew from the src directory:
```bash
cd src
python main.py
```

## Configuration

- `config/agents.yaml`: Defines the roles and characteristics of each AI agent
- `config/tasks.yaml`: Defines the tasks each agent will perform

## Environment Variables

Required environment variables in `.env`:
- `OPENAI_API_KEY`: Your OpenAI API key
- `SERPER_API_KEY`: Your Serper API key for web search
- `AGENTOPS_API_KEY`: (Optional) Your AgentOps API key for monitoring

## Output

The crew will generate:
1. Market research insights
2. Marketing strategy recommendations
3. Marketing content tailored to your target audience 