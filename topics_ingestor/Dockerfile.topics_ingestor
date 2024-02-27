# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/twitter-app/topics_ingestor_job

# Copy the current directory contents into the container at /usr/src/app
COPY ./topics_ingestor .
COPY ./topic_repository_module .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r topic-repo-requirements.txt
RUN python -m spacy download en_core_web_sm

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "topic_ingestor.py"]