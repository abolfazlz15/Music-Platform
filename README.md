# ⚠️ This project has not been updated.
# Music-Platform
A web application powered by Django framework and DRF

# Some features:
- Authentication (JWT and OTP)
- Documented by Swagger
- Dockerized
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
## Run project with docker
make sure you`ve installed docker
- In terminal: `git clone https://github.com/abolfazlz15/Music-Platform.git`
- cd `/Music-Platform` Where the docker-compose.yaml is
- In terminal: `docker-compose up -d`
- Visit http://0.0.0.0:8000/ 
