@echo off
echo Starting test generation pipeline...

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
if not exist data\raw mkdir data\raw
if not exist data\processed mkdir data\processed

REM Fix Swagger specification
echo Fixing Swagger specification...
python fix_swagger_spec.py

REM Fine-tune CodeT5 model
echo Fine-tuning CodeT5 model...
python ai_model/fine_tune_codet5.py

REM Generate English test cases
echo Generating English test cases...
python generate_english_tests.py --swagger data/raw/swagger_fixed.json --output data/processed/english_test_cases.json --num-cases 3

echo Pipeline complete! Check data/processed/english_test_cases.json for the generated test cases.
pause 