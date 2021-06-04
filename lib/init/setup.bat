pip install -r requirements.txt
cd .\project\
set FLASK_APP=__init__.py
$env:FLASK_APP="__init__.py"
flask run
pause