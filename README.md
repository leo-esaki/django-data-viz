# Django Bokeh Visualization Project
This Django project showcases my skills and experience in Python/Django development, particularly focusing on data visualization using the Bokeh library.

## Overview
This project is a web application built with Django, a high-level Python web framework. It incorporates Bokeh, a powerful library for creating interactive visualizations in web browsers using Python. The application allows users to visualize data in various forms, leveraging the capabilities of Bokeh to create rich and interactive plots.

## Features
- Data Visualization: Utilizes Bokeh to generate interactive plots and charts.
- Django Framework: Built on top of Django, providing a robust web development environment.
- Modular Design: Follows a modular structure for easy scalability and maintenance.
- User Authentication: Implements user authentication and authorization for secure access.

## Installation
To run this project locally, follow these steps:
1. Clone the repository:
    ```sh
    git clone https://github.com/leo-esaki/django-data-viz.git
    ```
2. Install Python(3.10.x or higher is preferred) with [peynv](https://pypi.org/project/pyenv/):
    ```sh
    pyenv install 3.12
    ```
3. Make a virtual environment for this project.
    ```sh
    pyenv virtualenv 3.12 <virtualenv-name>(ex: django-data-viz-env)
    ```
4. Activate the virtual environment:
    ```sh
    pyenv activate django-data-viz-env
    ```
5. Navigate to the project directory:
    ```sh
    cd django-data-viz
    ```
6. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
## Run
1. Activate the virtual environment:
    ```sh
    pyenv activate django-data-viz-env
    ```
2. Run the server:
    ```sh
    python manage.py runserver
    ```
3. Access the application in your web browser at <tt>http://localhost:8000/viz/users</tt>.

## Usage
Upon running the application, users can navigate to the visualization section to interact with the Bokeh plots. They can explore different datasets, customize the visualization parameters, and gain insights from the displayed data.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the <tt>MIT License</tt>.

## Acknowledgments
Special thanks to the Django and Bokeh communities for their excellent documentation and support resources.
