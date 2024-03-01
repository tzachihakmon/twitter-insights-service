# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/twitter-app/tweets-public-api

# Copy the current directory contents into the container at /usr/src/app
COPY ./tweets_public_api_service .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "tweets_public_api.py"]