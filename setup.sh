#!/bin/bash

# Check if pipenv is installed, if not, install it
if ! command -v pipenv &> /dev/null
then
    echo "pipenv could not be found, installing..."
    pip install pipenv
else
    echo "pipenv is installed"
fi

# Install dependencies using pipenv
echo "Installing dependencies..."
pipenv install

# Activate the virtual environment
echo "Activating the virtual environment..."

# Now run your setup function within your Python application
# Assuming setup is a package
echo "Running setup..."
pipenv run python -c 'import setup.setup; setup.setup.setup()'
echo "Setup is complete!"
