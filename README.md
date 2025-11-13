# CS 3200 Intro to Docker Compose and Streamlit

This repository is a quick introduction to running [Streamlit](https://streamlit.io) apps using Docker Compose.

## How to Run

1. **Clone this repository.**
2. **Start the app with Docker Compose:**
   ```bash
   docker compose up
   ```
3. **Open your browser and visit** [http://localhost:8080](http://localhost:8080).

## Project Structure

- `app/first-streamlit.py`: Example Streamlit app with lots of basic features.
- `app/requirements.txt`: Python dependencies for the app.
- `app/Dockerfile`: Docker config for the Streamlit container.
- `docker-compose.yaml`: Orchestrates running the Streamlit app in Docker.

## Requirements

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

Have fun learning Streamlit and Docker!
