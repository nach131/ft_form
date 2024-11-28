**FT_Form para 42 Barcelona**

**FT_Form** es un sistema integral diseñado para la gestión y creación de formularios, especialmente desarrollado para satisfacer las necesidades de la comunidad de 42 Barcelona. Este sistema permite a los staff crear, personalizar y gestionar formularios de manera intuitiva y eficiente. Además, cuenta con un módulo de análisis de datos, que genera gráficos y estadísticas detalladas a partir de las respuestas recopiladas.

Con FT_Form, los staff pueden:
- Crear formularios personalizados con una interfaz intuitiva y opciones de diseño flexibles.
- Gestionar formularios en tiempo real, con opciones de edición y actualización de preguntas y campos.
- Visualizar estadísticas en gráficos dinámicos para un análisis rápido y claro de los datos, optimizado para el seguimiento y la toma de decisiones.
- Exportar los datos en varios formatos y personalizar la presentación de los gráficos para incluir en reportes o presentaciones.

Este sistema facilita la recolección y el análisis de datos de manera ágil, contribuyendo a mejorar la toma de decisiones en proyectos, eventos y actividades clave de 42 Barcelona.


# ft-form Project

## Setup Instructions

1. **Clone the Repository:**  
   `git clone <repository-url>`

2. **Install Python:**  
   Ensure you have Python 3 installed:  
   `apt install python3`

3. **Set Up a Virtual Environment:**  
   Create and activate a Python virtual environment:  
   `python3 -m venv .venv`  
   `source .venv/bin/activate`  

   You should see the environment path in your terminal, something like:  
   `(env) /home/ft-form`

## Makefile Commands

- **Build the Project:**  
  Run the following command to build the Docker containers and install necessary dependencies:  
  `make`

- **Apply Django Migrations:**  
  After the build, apply Django migrations to update the database according to the models:  
  `make mi`

- **Start the Project:**  
  Launch the project on [localhost:8000](http://localhost:8000):  
  `make up`

- **Code Quality Check:**  
  Run `flake8` (similar to Norminette) to check for style issues:  
  `make control`

- **Create a Superuser:**  
  Set up a superuser for the Django admin panel:  
  `make super`

- **Clean Up:**  
  Remove volumes and images:  
  `make fclean`

## Project Overview

This project uses Django for the backend, with Docker for containerization. Follow the commands above for setup, development, and maintenance. For issues, ensure Docker is running and dependencies are installed.
