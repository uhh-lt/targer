# Use an official Python runtime as a parent image
FROM python:3.5

# Add all Data
ADD . /

# Set the working directory to /
WORKDIR /

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN python -m spacy download xx

# Make port 6001 available to the world outside this container
EXPOSE 6001

# Run app.py when the container launches
CMD ["python3", "frontend.py"]









