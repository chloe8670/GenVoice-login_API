#  Mental Health Institute API
This API is designed for clinicians to manage therapy client cases within a mental health institute.

## Endpoints

### User Management

- **POST /register**: Register a new user.
  - Request Body: `{"username": "string", "password": "string"}`
  - Response: `{"message": "User registered successfully"}`

- **POST /login**: Authenticate a user.
  - Request Body: `{"username": "string", "password": "string"}`
  - Response: `{"message": "Login successful, role: [Senior/Junior]"}`

- **POST /promote**: Promote a user to Senior.
  - Request Body: `{"username": "string", "password": "string"}`
  - Response: `{"message": "User promoted to Senior"}` or `{"message": "User is already Senior"}`

- **POST /demote**: Demote a user to Junior.
  - Request Body: `{"username": "string", "password": "string"}`
  - Response: `{"message": "User demoted to Junior"}` or `{"message": "User is already Junior"}`


### Case Management

- **GET /cases**: Fetch all cases.
  - Response: `[{"name": "string", "description": "string"}, ...]`

- **POST /case**: Add a new case.
  - Request Body: `{"name": "string", "description": "string"}`
  - Response: `{"message": "Case added successfully"}`


## Deployment

The API is deployed on Render and can be accessed at : 


## Testing

Use Postman to test the API endpoints.