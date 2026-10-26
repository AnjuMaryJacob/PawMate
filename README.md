# PawMate 🐾

**An AI-powered pet adoption and care platform built with Django and Ollama.**

## Overview

PawMate aims to connect pets with potential adopters while providing a convenient platform for pet listing and care-related information.

## Features

* User accounts and pet-owner or shelter profiles
* Pet listings with photos and detailed information
* Search and filtering for pet listings
* Add, edit, and delete pet listings
* Favorite pets
* AI-generated pet adoption descriptions using Ollama
* Pet-care chatbot (planned or in development)

## Technology Stack

* Python
* Django
* HTML and CSS
* JavaScript
* SQLite for local development
* Ollama with the Llama 3.2 1B model for local AI generation

## Local Setup

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install the project's dependencies from `requirements.txt`.
4. Configure environment variables if required.
5. Run database migrations.
6. Create a Django superuser if needed.
7. Start the development server.

```bash
python manage.py migrate
python manage.py runserver
```

## AI Integration

PawMate uses a locally running Ollama model to generate pet adoption descriptions. Ollama must be installed and the required model downloaded for this feature to work.

## Project Status

Under development.

## Security

Never commit `.env` files, API tokens, production secret keys, passwords, or private user data.
