# General procedure to start the backend of the webpage

    ## Activate python virtual environment (needed whenever a terminal session is started --> when successful the displayed dir in terminal is preceded by (venv)
    cd backend
    venv\Scripts\activate

    ## Upgrade pip
    pip install --upgrade pip

    ## Install requirements
    pip install -r requirements.txt

    ## Start tje Flask Application
    python app.py

    ## Deactivate python virtual environment
    deactivate