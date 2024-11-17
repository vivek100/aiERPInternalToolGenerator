# AI Code Generator CLI

A powerful command-line tool that generates complete web applications from natural language descriptions using AI. The tool supports both OpenAI's GPT-4 and Anthropic's Claude models.

## Features

- Generate detailed functional requirements
- Create technical specifications
- Generate complete application code
- Support for both OpenAI and Anthropic models
- Three processing modes:
  - Requirements only
  - Code generation
  - Full project setup
- Rich console output with progress tracking
- Modular and extensible architecture


## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Install the package: `pip install -e .`

## Configuration

Create a `.env` file with your API keys: 

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## Usage
Generate requirements only
codegen "Create a todo app" --mode requirements
Generate requirements and code
codegen "Create a todo app" --mode code
Generate full project
codegen "Create a todo app" --mode full
Use Claude instead of GPT-4
codegen "Create a todo app" --mode full --model anthropic


### Options

  - `--mode`: Processing mode
  - `requirements`: Generate only requirements documents
  - `code`: Generate requirements and code (without creating files)
  - `full`: Generate requirements, code, and create project files
  - `--model`: AI model provider
  - `openai`: Use OpenAI's GPT-4 (default)
  - `anthropic`: Use Anthropic's Claude

### Examples

```bash
Generate a simple todo app with OpenAI
codegen "Create a todo app with categories and due dates" --mode full
Generate an inventory system with Claude
codegen "Create an inventory management system" --mode full --model anthropic
Only generate requirements for a CRM
codegen "Create a basic CRM system" --mode requirements
```


## Project Structure

Generated projects follow a consistent structure:

```
generated_projects/
└── project_YYYYMMDD_HHMMSS_uniqueid/
├── docs/
│ ├── functional_requirements.md
│ └── technical_requirements.md
├── backend/
│ ├── models/
│ ├── routes/
│ └── server.js
└── frontend/
├── src/
│ ├── components/
│ ├── pages/
│ └── services/
└── package.json
```


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.