# Django Cheat Sheet

## Installation & Setup

```bash
# Install Django
pip install django

# Create new project
django-admin startproject projectname

# Create new app
python manage.py startapp appname

# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080
```

## Project Structure

```
projectname/
├── manage.py
├── projectname/
│   ├── __init__.py
│   ├── settings.py      # Project settings
│   ├── urls.py          # URL routing
│   ├── wsgi.py
│   └── asgi.py
└── appname/
    ├── migrations/
    ├── __init__.py
    ├── admin.py         # Admin interface config
    ├── apps.py
    ├── models.py        # Database models
    ├── tests.py
    └── views.py         # View functions/classes
```

## Models

```python
from django.db import models

class ModelName(models.Model):
    # Field types
    title = models.CharField(max_length=200)
    description = models.TextField()
    email = models.EmailField()
    url = models.URLField()
    number = models.IntegerField()
    decimal = models.DecimalField(max_digits=5, decimal_places=2)
    boolean = models.BooleanField(default=False)
    date = models.DateField()
    datetime = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Relationships
    foreign_key = models.ForeignKey('OtherModel', on_delete=models.CASCADE)
    many_to_many = models.ManyToManyField('OtherModel')
    one_to_one = models.OneToOneField('OtherModel', on_delete=models.CASCADE)

    # Meta options
    class Meta:
        ordering = ['-created']
        verbose_name_plural = "ModelNames"

    # String representation
    def __str__(self):
        return self.title
```

## Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# SQL for migration
python manage.py sqlmigrate appname 0001
```

## Views

### Function-Based Views
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

def my_view(request):
    context = {'key': 'value'}
    return render(request, 'template.html', context)

def detail_view(request, pk):
    item = get_object_or_404(ModelName, pk=pk)
    return render(request, 'detail.html', {'item': item})
```

### Class-Based Views
```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class MyListView(ListView):
    model = ModelName
    template_name = 'list.html'
    context_object_name = 'items'

class MyCreateView(CreateView):
    model = ModelName
    fields = ['field1', 'field2']
    success_url = reverse_lazy('list-view')
```

## URLs

```python
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
]
```

## Templates

### Template Syntax
```django
{# Comments #}

{{ variable }}
{{ object.attribute }}
{{ dictionary.key }}

{% if condition %}
    ...
{% elif other_condition %}
    ...
{% else %}
    ...
{% endif %}

{% for item in items %}
    {{ item }}
{% empty %}
    No items
{% endfor %}

{% url 'view-name' %}
{% url 'view-name' arg1 arg2 %}

{% extends 'base.html' %}
{% block content %}{% endblock %}

{% include 'partial.html' %}

{% load static %}
{% static 'css/style.css' %}
```

### Template Filters
```django
{{ value|lower }}
{{ value|upper }}
{{ value|title }}
{{ value|truncatewords:30 }}
{{ value|date:"Y-m-d" }}
{{ value|default:"N/A" }}
{{ list|length }}
{{ list|join:", " }}
```

## Forms

```python
from django import forms
from .models import ModelName

class MyForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class MyModelForm(forms.ModelForm):
    class Meta:
        model = ModelName
        fields = ['field1', 'field2']
        # or exclude = ['field3']
        widgets = {
            'field1': forms.Textarea(attrs={'rows': 4}),
        }
```

## Admin

```python
from django.contrib import admin
from .models import ModelName

@admin.register(ModelName)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['field1', 'field2', 'created']
    list_filter = ['status', 'created']
    search_fields = ['title', 'description']
    ordering = ['-created']

# Or simple registration
admin.site.register(ModelName)
```

## QuerySet API

```python
# Retrieve
Model.objects.all()
Model.objects.get(pk=1)
Model.objects.filter(field=value)
Model.objects.exclude(field=value)
Model.objects.first()
Model.objects.last()

# Create
Model.objects.create(field1=value1, field2=value2)
obj = Model(field1=value1)
obj.save()

# Update
obj = Model.objects.get(pk=1)
obj.field = new_value
obj.save()

Model.objects.filter(pk=1).update(field=value)

# Delete
obj.delete()
Model.objects.filter(pk=1).delete()

# Filtering
Model.objects.filter(field__exact=value)
Model.objects.filter(field__iexact=value)  # case-insensitive
Model.objects.filter(field__contains='text')
Model.objects.filter(field__icontains='text')
Model.objects.filter(field__gt=value)  # greater than
Model.objects.filter(field__gte=value)  # greater than or equal
Model.objects.filter(field__lt=value)  # less than
Model.objects.filter(field__lte=value)  # less than or equal
Model.objects.filter(field__in=[1, 2, 3])
Model.objects.filter(field__isnull=True)

# Ordering
Model.objects.order_by('field')
Model.objects.order_by('-field')  # descending

# Chaining
Model.objects.filter(field1=value1).exclude(field2=value2).order_by('-created')
```

## Static Files

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Collect static files
python manage.py collectstatic
```

## Settings (settings.py)

```python
# Add app to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appname',  # Your app
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        ...
    },
]
```

## Common Commands

```bash
# Create superuser
python manage.py createsuperuser

# Shell
python manage.py shell

# Database shell
python manage.py dbshell

# Check for issues
python manage.py check

# Show project settings
python manage.py diffsettings
```

## Messages Framework

```python
from django.contrib import messages

messages.success(request, 'Success message')
messages.info(request, 'Info message')
messages.warning(request, 'Warning message')
messages.error(request, 'Error message')

# In template
{% if messages %}
    {% for message in messages %}
        {{ message }}
    {% endfor %}
{% endif %}
```

## Redirects

```python
from django.shortcuts import redirect
from django.urls import reverse

return redirect('view-name')
return redirect('view-name', pk=object.pk)
return redirect(reverse('view-name'))
return redirect('/absolute/url/')
```
