
## install the dependecies
```angular2html
pip install -r requirements.txt
```

## set up the virtual env
```angular2html
python3 -m venv env //or python -m venv env
source env/bin/activate 
```

## run
```angular2html
uvicorn app.main:app --reload
```