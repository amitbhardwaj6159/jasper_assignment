# jasper_assignment
Task for technical assignment
fast api project

# Start server
Please follow below steps to start serverf

1 Take checkout and go to jasper_assigment folder

2 Run -> pip install -r requirements.txt

3 Do -> cd backend and run > uvicorn main:app --reload

4 Try http://127.0.0.1:8000/secure-endpoint from postman

5 Generate the access token from keycloak by running local instance of docker keycloak. Steps to run docker instance are mentioned below.

6 Edit .env file to edit keycloak url, realm and client id



# pull docker image
docker pull quay.io/keycloak/keycloak:latest

docker run -d --name keycloak \
-p 8080:8080 \
-e KEYCLOAK_ADMIN=admin \
-e KEYCLOAK_ADMIN_PASSWORD=admin \
quay.io/keycloak/keycloak:latest start-dev
