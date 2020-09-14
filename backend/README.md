# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks [Done]

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. [x] Use Flask-CORS to enable cross-domain requests and set response headers. 
2. [x] Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. [x] Create an endpoint to handle GET requests for all available categories. 
4. [x] Create an endpoint to DELETE question using a question ID. 
5. [x] Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. [x] Create a POST endpoint to get questions based on category. 
7. [x] Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. [x] Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. [x] Create error handlers for all expected errors including 400, 404, 422 and 500. 

## Error Handling
Errors are returned as JSON objects in the following format:
```
 {
    "success": False, 
    "error": 400,
     "message": "Bad request"
 }
```

The API will return four error types when requests fail:
- 400: Bad request
- 404: Not found
- 422: Unprecessable entity
- 500: Internal server error

## Endpoints

### GET /api/categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{
    "success": True,
    "categories":[
        {"id": 1, "type": "Science"},
        {"id": 2, "type": "Art"},
        {"id": 3, "type": "Geography"},
        {"id": 4, "type": "History"},
        {"id": 5, "type": "Entertainment"},
        {"id": 6, "type": "Sports"}
        ]
}
```

### GET /api/questions
- Fetches a list of questions, number of total questions, current category and categories.
- Request Arguments: page, default = 1
- Returns: A list of questions objects, total number of questions, categories and current category which equals to categories. Results are paginated in groups of 10. 
```
{
"categories":[
 {"id": 1, "type": "Science"},
        {"id": 2, "type": "Art"},
        {"id": 3, "type": "Geography"},
        {"id": 4, "type": "History"},
        {"id": 5, "type": "Entertainment"},
        {"id": 6, "type": "Sports"}
],
"current_category":[
        {"id": 1, "type": "Science"},
        {"id": 2, "type": "Art"},
        {"id": 3, "type": "Geography"},
        {"id": 4, "type": "History"},
        {"id": 5, "type": "Entertainment"},
        {"id": 6, "type": "Sports"}
],
"questions":[
{"answer": "test passed", "category": "History", "difficulty": 4, "id": 25,…},
{"answer": "Scarab", "category": "History", "difficulty": 4, "id": 23,…},
{"answer": "Blood", "category": "Science", "difficulty": 4, "id": 22,…},
{"answer": "Alexander Fleming", "category": "Science", "difficulty": 3, "id": 21,…},
{"answer": "The Liver", "category": "Science", "difficulty": 4, "id": 20,…},
{"answer": "Jackson Pollock", "category": "Art", "difficulty": 2, "id": 19,…},
{"answer": "One", "category": "Art", "difficulty": 4, "id": 18,…},
{"answer": "Mona Lisa", "category": "Art", "difficulty": 3, "id": 17,…},
{"answer": "Escher", "category": "Art", "difficulty": 1, "id": 16,…},
{"answer": "Agra", "category": "Geography", "difficulty": 2, "id": 15,…}
],
"success": true,
"total_questions": 20
}
```

### POST /api/questions
- create a new question using the submitted question, answer, category and difficulty.
- Request Arguments: "question", "answer", "catogry", "difficulty"
```
{
            "question": "What's your name?",
            "answer": "Test Bot",
            "category": 1,
            "difficulty": 4,
        }
```
- Returns: The created question object, total number of questions, and current category 
```
{
    'question': {
        'answer': 'Test Bot', 
        'category': 'Science', 
        'difficulty': 4, 'id': 24, 
        'question': "What's your name?"
        }, 
    'success': True
}
```

### DELETE /api/questions/{question_id}
- Deletes the question of the given ID if it exists
- Request Arguments: question id
- Returns: success value
```
{"success": True}
```

### POST /api/questions/searches
- Search questions of the given search term if they exist
- Request Arguments: search term
- Returns: The question object, total questions
```
{
"current_category": null,
"questions":[
        {
        "answer": "Lake Victoria",
        "category": "Geography",
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
        }
    ],
"success": true,
"total_questions": 1
}
```

### GET  /api/categories/{category_id}/questions
- Fetch the questions of given category ID 
- Request Arguments: category id
- Returns: The list of question objects, total questions and current_category
```
{
"current_category":{
    "id": 1,
    "type": "Science"
},
"questions":[
    {"answer": "The Liver", "category": "Science", "difficulty": 4, "id": 20,…},
    {"answer": "Alexander Fleming", "category": "Science", "difficulty": 3, "id": 21,…},
    {"answer": "Blood", "category": "Science", "difficulty": 4, "id": 22,…},
    {"answer": "test passed", "category": "Science", "difficulty": 1, "id": 26,…},
    {"answer": "test passed", "category": "Science", "difficulty": 2, "id": 27,…}
    ],
"success": true,
"total_questions": 5
}
```

### POST /api/quizzes
- Fetch the questions to play quiz
- Request Arguments: category id, previous question ids
```
{
    "previous_questions": [20, 21, 22, 24],
    "quiz_category": {
        "type": {
            "id": 1, "type": "Science"
        } / {"type": "click} # include all categories
    }
}
```
- Returns: Random question object of the given category
```
{
    'question': {
        'answer': 'Test Bot', 
        'category': 'Science', 
        'difficulty': 4, 
        'id': 24, 
        'question': "What's your name?"
        }, 
    'success': True
}
```
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```