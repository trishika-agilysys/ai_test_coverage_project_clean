#!/bin/bash

# Create and activate virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment (Windows)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/raw data/processed

# Fix Swagger specification
echo "Fixing Swagger specification..."
python fix_swagger_spec.py

# Fine-tune CodeT5 model
echo "Fine-tuning CodeT5 model..."
python ai_model/fine_tune_codet5.py

# Generate English test cases
echo "Generating English test cases..."
python generate_english_tests.py --swagger data/raw/swagger_fixed.json --output data/processed/english_test_cases.json --num-cases 3

echo "Pipeline complete! Check data/processed/english_test_cases.json for the generated test cases." 