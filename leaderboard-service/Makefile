.PHONY: run

# Define the default target
run:
	uvicorn app.main:app --reload

run-prod:
	uvicorn app.main:app --workers 4

# Install dependencies
install:
	pip install -r requirements.txt

# Lint the code
lint:
	flake8 .

# Run tests
test:
	pytest