# jasper_assignment
Task for technical assignment
fast api project

# Start server
Please follow below steps to start serverf

1 Take checkout and go to jasper_assigment folder

2 Run -> pip install -r requirements.txt

3 Do -> cd backend and run > uvicorn main:app --reload

4 Try http://127.0.0.1:8000/secure-endpoint from postman with header Authorization: Bearer {tokenValue}

5 Generate the access token from keycloak by running local instance of docker keycloak. Steps to run docker instance are mentioned below.

6 Edit .env file to edit keycloak url, realm and client id


# Generate token using postman from keycloak
 Use url {keycloak_server_url}/realms/{your_realm}/protocol/openid-connect/token

1 Create a new POST request in Postman.

2 Set the URL to your token endpoint.

3 Go to the Body tab and select the x-www-form-urlencoded option.
Add the following key-value pairs:
grant_type: password
client_id: {your-client-id}
username: {your-user-name}
password: {your-user-password}
client_secret: {your-client-secret} (only required for confidential clients)

4 Click Send. The response will contain the access_token and refresh_token. 

Postman collection link

https://.postman.co/workspace/My-Workspace~076a8a16-0263-4de0-8752-70b314bcb5e8/request/2777134-729fb3d9-f67d-49ae-a9af-e106bd505645?action=share&creator=2777134&ctx=documentation

https://.postman.co/workspace/My-Workspace~076a8a16-0263-4de0-8752-70b314bcb5e8/request/2777134-254804ab-4cad-4cec-b7d0-e7e7d4897b22?action=share&creator=2777134&ctx=documentation

# pull docker image
docker pull quay.io/keycloak/keycloak:latest

docker run -d --name keycloak \
-p 8080:8080 \
-e KEYCLOAK_ADMIN=admin \
-e KEYCLOAK_ADMIN_PASSWORD=admin \
quay.io/keycloak/keycloak:latest start-dev
