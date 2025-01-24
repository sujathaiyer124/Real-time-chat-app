
#### - Create Virtual Environment
###### # Mac
```
python3 -m venv venv
source venv/bin/activate
```

###### # Windows
```
python3 -m venv venv
.\venv\Scripts\activate.bat
```

<br>

#### - Install dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```

<br>

#### - Migrate to database
```
python manage.py migrate
python manage.py createsuperuser
```

<br>

#### - Run application
```
python manage.py runserver
```

<br>

#### - Generate Secret Key ( ! Important for deployment ! )
```
python manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
exit()
```
#### Real-Time Chat Application
## Overview
A Django-based real-time chat application with user authentication, private messaging, and responsive design.

## Features

- User registration and authentication
- Real-time private messaging
- Responsive left-side user menu
- Dynamic chat interface
- HTMX-powered message updates

# Technologies

- Django
- HTMX
- WebSocket (optional)
- Tailwind CSS
- JavaScript

## Setup
## Prerequisites

- Python 3.9+
- Django
- pip

## Installation
bashCopy# Clone repository
git clone https://github.com/yourusername/chat-app.git

# Create virtual environment
- python -m venv venv
- source venv/bin/activate

# Install dependencies
- pip install -r requirements.txt

# Run migrations
- python manage.py migrate

# Start server
- python manage.py runserver
- Configuration

- Customize settings.py
- Configure authentication
- Set up WebSocket (optional)

## Key Files Explained

- settings.py: Project configuration
- urls.py: URL routing
- models.py: Database models
- views.py: View logic
- forms.py: Form handling
- templates/: HTML templates
- static/: CSS, JavaScript files