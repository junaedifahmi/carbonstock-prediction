# Model Deployment Template with FastAPI and Streamlit

## TLDR;

This template is using fastapi and steramlit to get a fast deployment with fastapi and streamlit. This project will use `uv` as its python package manager

## API with FastAPI

To quick check API only it is advised to use api.

1. ensure to sync the uv `uv sync`
2. run the api with `uv run fastapi run`

## Quick Demo with Streamlit

For quick demo we employ streamlit as its simplicity of presenting the input and output of the model. Running the demo should be simple.

1. ensure that extra package is installed if not run this command `uv sync --extra dev`
2. run the demo with `uv run streamlit run demo/streamlit_app.py`

## Dockerization

run 

```bash
docker build -t app-name:latest .

```
