pip install -r requirements.txt
cd .\project\
set FLASK_APP=__init__.py
$env:FLASK_APP="__init__.py"
set FLASK_ENV=development
$env FLASK_ENV="development"
flask run
pause
