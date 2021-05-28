pip install -r requirements.txt
echo Démmarage...
cd .\project\
set FLASK_APP=__init__.py
$env:FLASK_APP="__init__.py"
flask run
echo Fini
pause