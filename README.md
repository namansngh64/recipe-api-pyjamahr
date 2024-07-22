#SETUP
1. Create an .env file with the fields provided in the sample
2. Build the docker container using "docker build -t recipe_app ."
3. Run "docker run --env-file .env -p 8000:8000 recipe_app"
4. Use "docker-compose up" to run celery worker, celery beat and redis
5. I have used an online hosted PostgreSQL, so change the env accordingly

#TEST
To test the app, run "pytest" and it will generate a coverage report as well

Emails will the sent at 1st hour of day using celery and redis
