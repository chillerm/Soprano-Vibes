# Sopranos Flask Application

A Flask web application built as an experiment in vibe coding with Cursor. This project serves as a demonstration of how Cursor's AI capabilities can enhance the development workflow, making it more intuitive and enjoyable.

## Project Purpose

This repository was created to explore and demonstrate the concept of "vibe coding" - a more fluid, conversational approach to software development facilitated by AI tools. Using Cursor's AI capabilities, we're building a Flask application that serves as a reference for Sopranos characters, showcasing how AI can assist in:

- Rapid prototyping
- Code generation
- Test writing
- Documentation
- Best practices implementation

## Features

- RESTful API for Sopranos characters
- Search functionality by first and last name
- Character lookup by ID
- Full test coverage
- Modern Python development practices with Poetry and pyenv

## Prerequisites

- [pyenv](https://github.com/pyenv/pyenv) installed
- [Poetry](https://python-poetry.org/docs/#installation) installed

## Setup

1. Install Python 3.12 using pyenv:
```bash
pyenv install 3.12.2
```

2. Install dependencies using Poetry:
```bash
poetry install
```

## Running the Application

To run the application:

```bash
poetry run python app.py
```

The application will be available at `http://localhost:5000`

## Development

To activate the Poetry shell:
```bash
poetry shell
```

## API Endpoints

- `GET /api/characters/` - List all characters
- `GET /api/characters/?firstName=<name>` - Search by first name
- `GET /api/characters/?lastName=<name>` - Search by last name
- `GET /api/characters/<id>/` - Get character by ID

## Testing

Run the test suite with coverage:
```bash
poetry run pytest
```

## Vibe Coding with Cursor

This project is being developed using Cursor's AI capabilities to demonstrate how AI can enhance the development workflow. The development process focuses on:

1. Natural language communication with the AI
2. Iterative development with AI assistance
3. Learning and applying best practices
4. Maintaining high code quality and test coverage

## Contributing

Feel free to contribute to this project! Since this is an experiment in vibe coding, we welcome suggestions on how to improve the development workflow or enhance the application.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 