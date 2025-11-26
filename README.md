# AWS IAM Viewer

A Python web application for viewing AWS IAM users, roles, and permissions with AWS Cognito authentication.

## Setup

### Prerequisites
- Python 3.12

### Installation

1. Create and activate virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your AWS Cognito and configuration values
```

4. Run the application:
```bash
python app.py
```

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── models/              # Data models
│   ├── routes/              # Route handlers
│   └── services/            # Business logic
├── static/
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript files
├── templates/               # Jinja2 templates
├── tests/                   # Test suite
├── app.py                   # Application entry point
├── config.py                # Configuration management
└── requirements.txt         # Python dependencies
```

## Testing

Make sure your virtual environment is activated first:
```bash
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

Run tests with pytest:
```bash
pytest
```

Run property-based tests:
```bash
pytest -v tests/
```
