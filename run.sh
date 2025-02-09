#!/bin/bash

python3 -m venv venv

source venv/bin/activate

pip install flask flask-cors

pip freeze >  requirements.txt

echo  "We are live! Virtual environment is activated"
echo  "To deactivate , run: deactivate "

