python manage.py schemamigration userprofile --initial 
python manage.py migrate userprofile

python manage.py schemamigration userprofile --auto
python manage.py migrate userprofile
