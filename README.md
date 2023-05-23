# Music-Platform
A web application powered by Django framework and DRF

# Some features:
- Write testing for APIs, models, URLs
- Authentication (JWT and OTP code)
- Documented by Swagger
- Use reids for caching (coming soon)
- Dockerized (coming soon)
- Useing the nginx (coming soon)

# How to run project
```
git clone https://github.com/abolfazlz15/Music-Platform.git
```

- `cd /Music-Platform` Where the manage.py is
- In terminal: `python -m venv venv`
- Activate your venv: in windows `cd venv\scripts\activate` in linux: `venv/bin/activate`
- And then back to the main directory `cd ..\..`
- Run `pip install requirements.txt`
- Run `python manage.py runserve`
- Visit `http://127.0.0.1:8000/swagger` to see the api documentation
