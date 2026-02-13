# Django PWA with Clean Architecture

This project is a Django Progressive Web Application (PWA) refactored to follow Clean Architecture principles.

## Project Structure

The project is structured into the following layers:

- **Domain**: Contains pure business logic and entities. No Django imports allowed here.
- **Application**: Implements use cases and orchestrates interactions between the domain and infrastructure.
- **Infrastructure**: Handles external concerns like Django ORM, database interactions, and external services.
- **Interface**: Consists of Django views, API endpoints, and PWA-specific logic (e.g., service workers).

## Getting Started

### Prerequisites

- Python 3.8+
- Django
- npm (for frontend PWA assets)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd mySite
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt # (You may need to create this file first)
    ```
4.  **Run database migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5.  **Create a superuser (optional):**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## Development

### Running Tests

To run the unit tests for the domain and application layers:

```bash
python manage.py test app.tests
```

### Frontend (PWA)

The frontend assets and service worker logic are handled in the `app/interfaces/` directory.

## Clean Architecture Principles

This project adheres to the following Clean Architecture principles:

-   **Dependency Rule**: Outer layers depend on inner layers. The Domain layer has no dependencies on Django.
-   **Separation of Concerns**: Each layer has a specific responsibility.
-   **Testability**: Business logic (Domain and Application layers) is independent of frameworks and easily testable.

## Contributing

Please refer to `CONTRIBUTING.md` (if available) for guidelines on contributing to this project.
