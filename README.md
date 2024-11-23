## Modules

### 1. Code Execution Module

This module demonstrates how to use CrewAI for code execution and analysis tasks. It includes:

- Custom code interpretation capabilities
- Data analysis using County Health Rankings dataset
- Configurable agents and tasks through YAML files
- Environment configuration for secure credential management

### 2. Meeting Minutes Module

This module showcases integration with Gmail for processing meeting minutes, featuring:

- Gmail integration tools
- Automated email processing
- Custom crew configurations for handling meeting-related tasks

## Setup

1. Clone the repository:

bash
git clone [repository-url]
cd master-crewai-course


2. Create and activate a Python virtual environment:

bash
conda create -n crewai python=3.11
conda activate crewai


3. Install dependencies:

bash
pip install -r requirements.txt


4. Configure environment variables:
- Copy `.env.example` to `.env` in each module directory
- Fill in required credentials and API keys

## Environment Variables

Each module has its own `.env` file for configuration. Ensure you set up the following:

### Code Execution Module


### Meeting Minutes Module

python
cd meeting_minutes
python src/meeting_minutes/main.py


## Configuration

### Agents Configuration
Agents are configured in `config/agents.yaml` files within each module. This allows for easy modification of agent properties and roles.

### Tasks Configuration
Tasks are defined in `config/tasks.yaml` files, specifying the workflow and requirements for each automated process.

## Tools

The project utilizes several custom tools:

- Code Interpreter Tool: For executing and analyzing code
- Gmail Tool: For email processing and communication
- Additional CrewAI tools for specific tasks

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request