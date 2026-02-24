# Coffee Logger

A web application for tracking coffee consumption with statistics and customizable coffee types.

## Features

- Log coffee consumption with timestamps and notes
- Create and manage custom coffee types
- View detailed statistics and consumption patterns
- Responsive web interface

## Project Structure

```
app/
├── __init__.py          # Application initialization
├── models.py            # Database models
├── views.py             # Controllers/Views
├── templates/           # HTML templates
├── static/              # Static assets (CSS, JS, images)
└── tests/               # Test files
requirements.txt         # Dependencies
pytest.ini               # Test configuration
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python wsgi.py
   ```

## Development Workflow

- Development happens on the `dev` branch
- Feature branches are created from `dev`
- Pull requests are submitted to `dev` for review
- The `main` branch is protected and only updated via pull requests

## Testing

Run tests with:
```bash
pytest
```

## License

MIT