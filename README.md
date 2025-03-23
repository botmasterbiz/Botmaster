# Masterclass Projects

This repository contains various projects developed during the masterclass sessions.

## Projects

### 1. Clean Air Marketing Crew

A project that uses AI agents to create marketing strategies and content for clean air products. The project uses the CrewAI framework to orchestrate multiple AI agents working together:

- Research Analyst: Conducts market research and competitor analysis
- Marketing Strategist: Develops marketing strategies based on research insights
- Content Creator: Creates engaging marketing content

#### Setup

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the project:
```bash
cd "Botmaster/01 - CleanAirMarketingCrew/src"
python main.py
```

#### Project Structure

```
Botmaster/
└── 01 - CleanAirMarketingCrew/
    └── src/
        ├── main.py          # Main entry point
        └── crew.py          # AI crew configuration
```

## Requirements

- Python 3.8+
- CrewAI
- LangChain
- Other dependencies listed in requirements.txt 