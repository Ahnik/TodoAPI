<h2>Requirements</h2>
<p>
1. User registration to create a new user<br>
2. Login endpoint to authenticate the user and generate a token<br>
3. CRUD operations for managing the to-do list<br>
4. Implement user authentication to allow only authorized users to access the to-do list<br>
5. Implement error handling and security measures<br>
6. Use a database to store the user and to-do list data<br>
7. Implement proper data validation<br>
8. Implement pagination and filtering for the to-do list<br>
</p>

<h2>User Registration</h2>
<p>
Register a new user using the following request:<br>
<br>
POST /register<br>
{<br>
    "name": "John Doe",<br>
    "email": "john@doe.com",<br>
    "password": "password"<br>
}<br>
<br>
This will validate the given details, make sure the email is unique and store the user details in the database. Make sure to 
hash the password before storing it in the database. Respond with a token that can be used for authentication if the registration is successful.<br>
{<br>
    "token": "GY30MsR31QSCwMGW5vkPBKmaaXvd5mK42uxDMkzjtsT8qFpRcFYfHoljBWTxZdq3"<br>
}<br>
This token can either be a JWT or a random string that can be used for authentication.<br>
</p>

<h2>User Login</h2>
<p>
Authenticate the user using the following request:<br>
<br>
POST /login<br>
{<br>
    "email": "john@doe.com",<br>
    "password": "password"<br>
}<br>
<br>
This will validate the given email and password, and respond with a token if the authentication is successful.<br><br>
{<br>
    "token": "GY30MsR31QSCwMGW5vkPBKmaaXvd5mK42uxDMkzjtsT8qFpRcFYfHoljBWTxZdq3"<br>
}<br><br>
</p>

<h2>Create a To-Do Item</h2>
<p>
Create a new to-do item using the following request:<br><br>
POST /todos<br>
{<br>
    "title": "Buy groceries",<br>
    "description": "Buy milk, eggs, and bread"<br>
}<br><br>
User must send the token received from the login endpoint in the header to authenticate the request. The Authorization header 
can be used with the token as the value. In case the token is invalid or missing, respond with an error and status code 401.
<br><br>
{<br>
    "message": "Unauthorized"<br>
}<br><br>
Upon successful creation of the to-do item, respond with the details of the created item.<br><br>
{<br>
    "id": 1,<br>
    "title": "Buy groceries",<br>
    "description": "Buy milk, eggs, and bread"<br>
}<br><br>
</p>

<h2>Update a To-Do Item</h2>
<p>
Update an existing to-do item using the following request:<br><br>
PUT /todos/1<br>
{<br>
    "title": "Buy groceries",<br>
    "description": "Buy milk, eggs, bread and cheese"<br>
}<br><br>
Just like the create todo endpoint, user must send the token received. Also make sure to validate the user has the permission to update the to-do item, i.e. the user is the creator of the todo item that they are updating. Respond with an error and status code 403 if the user is not authorized to update the item.<br><br>
{<br>
    "message": "Forbidden"<br>
}<br><br>
Upon successful update of the to-do item, respond with the updated details of the item.<br><br>
{<br>
    "id": 1,<br>
    "title": "Buy groceries",<br>
    "description": "Buy milk, eggs, bread and cheese"<br>
}<br><br>
</p>

<h2>Delete a To-Do Item</h2>
<p>
Delete an existing to-do item using the following request:<br><br>
DELETE /todos/1<br><br>
User must be authenticated and authorized to delete the to-do item. Upon successful deletion, respond with status code 204.<br>
</p>

<h2>Get To-Do Items</h2>
<p>
Get the list of to-do items using the following request:<br><br>
GET /todos?page=1&limit=10<br><br>
User must be authenticated to access the tasks and the response should be paginated. Respond with the list of to-do items along with pagination details.<br><br>
{<br>
    "data":[<br>
        {<br>
            "id": 1,<br>
            "title": "Buy groceries",<br>
            "description": "Buy milk, eggs, bread and cheese"<br>
        },<br>
        {<br>
            "id": 2,<br>
            "title": "Pay bills",<br>
            "description": "Pay electricity and water bills"<br>
        }<br>
    ],<br>
    "page": 1,<br>
    "limit": 10,<br>
    "total": 2<br>
}<br><br>
</p>

<h2>Bonus</h2>
<p>
1. Implement filtering and sorting for the to-do list<br>
2. Implement unit tests for the API<br>
3. Implement rate limiting and throttling for the API<br>
4. Implement refresh token mechanism for authentication<br>
</p>

<h2>Guide</h2>
<a href="https://roadmap.sh/projects/todo-list-api">https://roadmap.sh/projects/todo-list-api</a>