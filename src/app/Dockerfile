FROM streamlit/streamlit:latest

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy application code
COPY . /app

# Set the command to run when the container starts
CMD ["streamlit", "run", "app.py"]