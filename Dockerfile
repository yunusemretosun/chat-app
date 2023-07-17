FROM python:3.9

WORKDIR /

COPY ./chatapp /chatapp
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port on which the Django app will run
EXPOSE 8000

# Set environment variables (if necessary)
ENV SECRET_KEY=${SECRET_KEY}
ENV DEBUG=${DEBUG}

# Run the Django app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]