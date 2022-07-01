# Quick start

Create a virtual environment and activate it.
```bash
$ python -m venv ./venv
$ source ./venv/bin/activate
```

Install the prerequisites.
```bash
(venv) $ pip install -r requirements.txt
```

Apply the migrations.
```bash
(venv) $ python manage.py migrate
```

Start the development server.
```bash
(venv) $ python manage.py runserver
```

Navigate to http://localhost:8000/ to see the Supernaut app in action.
