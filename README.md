# Django Todo Application

A simple and elegant todo application built with Django that allows you to manage your tasks effectively.

## Features

- Create new todos with title, description, and due date
- Edit existing todos
- Delete todos with confirmation
- Mark todos as resolved/unresolved
- Clean and responsive UI
- Admin interface for advanced management

## Project Structure

```
01-todo/
├── manage.py
├── todo_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── todos/
│   ├── models.py          # Todo model
│   ├── views.py           # CRUD views
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   └── templates/
│       └── todos/
│           ├── base.html
│           ├── todo_list.html
│           ├── todo_form.html
│           └── todo_confirm_delete.html
├── db.sqlite3
├── DJANGO_CHEATSHEET.md   # Django reference guide
└── README.md
```

## Installation & Setup

1. Make sure you have Python installed (Python 3.8 or higher)

2. Install Django if not already installed:
```bash
make install
# or
pip install django
```

3. The database is already set up and migrated

## Quick Start with Makefile

This project includes a Makefile for simplified command execution:

```bash
make help          # Show all available commands
make run           # Start development server
make test          # Run tests
make migrate       # Apply database migrations
make makemigrations # Create new migrations
make createsuperuser # Create admin user
make shell         # Open Django shell
make check         # Check for project issues
make clean         # Remove cache and database
```

## Running the Application

### Using Makefile (Recommended)
```bash
make run
```

### Using manage.py
```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## Using the Application

### Main Features

- **Todo List**: View all your todos on the homepage
- **Create Todo**: Click "New Todo" to create a new task
- **Edit Todo**: Click "Edit" on any todo to modify it
- **Delete Todo**: Click "Delete" to remove a todo (with confirmation)
- **Mark as Resolved**: Toggle the resolved status of any todo

### Admin Interface

To access the admin interface:

1. Create a superuser account:
```bash
make createsuperuser
# or
python manage.py createsuperuser
```

2. Follow the prompts to set username, email, and password

3. Navigate to:
```
http://127.0.0.1:8000/admin/
```

4. Log in with your superuser credentials

In the admin interface, you can:
- Manage todos with advanced filtering
- Search todos by title or description
- Bulk edit resolved status
- View creation and update timestamps

## Todo Model Fields

- **title**: The todo title (required)
- **description**: Detailed description (optional)
- **due_date**: When the todo should be completed (optional)
- **resolved**: Whether the todo is completed (default: False)
- **created_at**: Automatically set when created
- **updated_at**: Automatically updated when modified

## URL Routes

- `/` - Todo list (homepage)
- `/create/` - Create new todo
- `/edit/<id>/` - Edit existing todo
- `/delete/<id>/` - Delete todo
- `/toggle/<id>/` - Toggle resolved status
- `/admin/` - Admin interface

## Technologies Used

- Django 5.2.4
- SQLite (database)
- HTML/CSS (no external CSS frameworks for simplicity)

## Reference

Check out `DJANGO_CHEATSHEET.md` for a comprehensive Django reference guide covering:
- Installation & setup
- Models & migrations
- Views & URLs
- Templates
- Forms
- Admin interface
- QuerySet API
- And more!
