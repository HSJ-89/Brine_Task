# Use an official Python runtime as the base image
FROM python:3.9
# Copy the Python program into the container
COPY . /usr/src/app
# switch working directory to app
WORKDIR /usr/src/app
# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt
# switch working directory to orderservice
WORKDIR /usr/src/app/orderservice
# Set the command to run your Python program
CMD ["python", "app.py"]