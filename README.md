# Django Admin PandasAI

Django Admin PandasAI is a sample project that consists of a Django application integrating PandasAI into the Django admin interface, to provide data analysis capabilities through natural language queries.

## Installation

1. Clone the repository from GitHub:

    ```bash
    git clone https://github.com/runtimerevolution/django-admin-pandasai.git
    ```

2. Navigate to the project directory:

    ```bash
    cd django-admin-pandasai
    ```

3. Install the dependencies using Poetry:

    ```bash
    poetry install
    ```

4. Run migrations:

    ```bash
    python manage.py migrate
    ```

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

## Usage

1. Access the Django Admin interface.
2. Navigate to the Chat model.
3. Create a new chat to interact with the agent.
