rm -rf htmlcov .coverage
PYTHONPATH=$(pwd) pytest --cov=pomodoro --cov-report=term --cov-report=html tests/
xdg-open htmlcov/index.html