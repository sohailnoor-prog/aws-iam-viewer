# AWS IAM Viewer

A Python web application for viewing AWS IAM users, roles, and permissions with AWS Cognito authentication.

## Features

- 🔐 AWS Cognito authentication
- 🔒 Encrypted AWS credential storage
- 👥 View IAM users with pagination
- 🎭 View IAM roles with pagination
- ⚡ 5-minute caching for performance
- 🎨 Clean, professional UI
- 🐳 Docker support

## Prerequisites

- Python 3.12
- AWS Account with Cognito User Pool configured
- AWS credentials with IAM read permissions

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/sohailnoor-prog/aws-iam-viewer.git
cd aws-iam-viewer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Required variables:
# - FLASK_SECRET_KEY
# - COGNITO_USER_POOL_ID
# - COGNITO_CLIENT_ID
# - COGNITO_CLIENT_SECRET (optional)
# - COGNITO_REGION (default: us-west-2)
# - AWS_DEFAULT_REGION (default: us-west-2)
```

### 3. Set Up AWS Cognito

Run the setup script to create a Cognito User Pool:

```bash
python setup_cognito.py
```

Or manually create:
- Cognito User Pool in us-west-2
- App Client with USER_PASSWORD_AUTH enabled
- Test user with email and password

### 4. Run the Application

```bash
# Development mode
python app.py

# Production mode with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

Visit http://localhost:5000

## Docker Deployment

### Using Docker Compose

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker

```bash
# Build image
docker build -t aws-iam-viewer .

# Run container
docker run -p 5000:5000 \
  -e FLASK_SECRET_KEY=your-secret \
  -e COGNITO_USER_POOL_ID=your-pool-id \
  -e COGNITO_CLIENT_ID=your-client-id \
  -e COGNITO_REGION=us-west-2 \
  aws-iam-viewer
```

## Project Structure

```
.
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── models/              # Data models (User, IAMUser, IAMRole, etc.)
│   ├── routes/              # Route handlers (auth, aws, iam)
│   ├── services/            # Business logic (Cognito, AWS, IAM)
│   └── utils/               # Utilities (pagination)
├── static/
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript files
├── templates/               # Jinja2 templates
├── tests/                   # Test suite
├── app.py                   # Development entry point
├── wsgi.py                  # Production entry point
├── config.py                # Configuration management
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
└── requirements.txt         # Python dependencies
```

## Usage

1. **Login**: Use your Cognito credentials
2. **Connect to AWS**: Provide AWS Access Key, Secret Key, and Region
3. **View IAM Resources**:
   - Click "View Users" to see all IAM users
   - Click "View Roles" to see all IAM roles
   - Use pagination for large lists (50 items per page)

## AWS IAM Permissions Required

The AWS credentials you provide need these IAM permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "iam:ListUsers",
        "iam:GetUser",
        "iam:ListRoles",
        "iam:GetRole"
      ],
      "Resource": "*"
    }
  ]
}
```

## Testing

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
python test_pagination.py
```

## Security Notes

- AWS credentials are encrypted using Fernet before session storage
- Cognito handles password hashing and authentication
- Session cookies are HTTPOnly and Secure (in production)
- All secrets should be stored in environment variables
- Never commit `.env` file to version control

## Troubleshooting

**Issue**: Cannot connect to AWS
- Verify AWS credentials are valid
- Check IAM permissions
- Ensure region is correct (us-west-2)

**Issue**: Cognito authentication fails
- Verify User Pool ID and Client ID
- Check user exists in Cognito
- Ensure USER_PASSWORD_AUTH is enabled

**Issue**: No users/roles displayed
- Verify AWS credentials have IAM read permissions
- Check if IAM entities exist in the account
- Review application logs for errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and internal use.
