import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, and_
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  """
    cors = CORS(app, resource={r"/api/*": {"origins": "*"}})

    """
  @TODO: Use the after_request decorator to set Access-Control-Allow
  """

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    """
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  """

    def get_formatted_categories():
        categories = Category.query.all()
        if not categories:
            return abort(404)
        formatted_categories = [category.format() for category in categories]
        return formatted_categories

    @app.route("/api/categories", methods=["GET"])
    def get_categories():
        formatted_categories = get_formatted_categories()
        return jsonify({"success": True, "categories": formatted_categories})

    """
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  """

    @app.route("/api/questions", methods=["GET"])
    def get_questions():
        page = request.args.get("page", 1, type=int)
        questions = (
            Question.query.order_by(desc(Question.id))
            .limit(QUESTIONS_PER_PAGE)
            .offset((page - 1) * 10)
            .all()
        )
        if not questions:
            abort(404)
        formatted_questions = [question.format() for question in questions]
        total_questions = Question.query.count()
        categories = get_formatted_categories()

        return jsonify(
            {
                "success": True,
                "questions": formatted_questions,
                "total_questions": total_questions,
                "categories": categories,
                "current_category": categories,
            }
        )

    """
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  """

    @app.route("/api/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if not question:
            abort(422)
        try:
            question.delete()
        except Exception:
            abort(500)
        return jsonify({"success": True}), 200

    """
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  """

    @app.route("/api/questions", methods=["POST"])
    def create_question():
        res_json = request.get_json()
        list_json = list(res_json.keys())
        list_json.sort()
        if list_json != [
            "answer",
            "category",
            "difficulty",
            "question",
        ]:
            abort(400)
        question = res_json["question"]
        answer = res_json["answer"]
        category = res_json["category"]
        difficulty = res_json["difficulty"]

        try:
            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty,
            )
            new_question.insert()
            return (
                jsonify({"success": True, "question": new_question.format()}),
                200,
            )
        except Exception:
            abort(500)

    """
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  """

    @app.route("/api/questions/searches", methods=["POST"])
    def search_questions():
        search_term = request.get_json()["searchTerm"]
        search_term = "%{}%".format(search_term)
        res_questions = (
            Question.query.filter(Question.question.like(search_term))
            .order_by(Question.id)
            .all()
        )
        if not res_questions:
            abort(404)
        formatted_questions = [question.format() for question in res_questions]
        return (
            jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": len(formatted_questions),
                    "current_category": None,
                }
            ),
            200,
        )

    """
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  """

    @app.route("/api/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        current_category = Category.query.get(category_id)
        res_questions = (
            Question.query.filter(Question.category == category_id)
            .order_by(Question.id)
            .all()
        )
        if not res_questions:
            abort(404)
        formatted_questions = [question.format() for question in res_questions]

        return (
            jsonify(
                {
                    "success": True,
                    "questions": formatted_questions,
                    "total_questions": len(formatted_questions),
                    "current_category": current_category.format(),
                }
            ),
            200,
        )

    """
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  """

    @app.route("/api/quizzes", methods=["POST"])
    def get_next_question():
        res_json = request.get_json()
        if list(res_json.keys()) != ["previous_questions", "quiz_category"]:
            abort(400)
        quiz_category = res_json["quiz_category"]
        previous_questions = res_json["previous_questions"]
        if not previous_questions:
            if quiz_category["type"] == "click":
                questions = Question.query.all()
            else:
                questions = Question.query.filter(
                    Question.category == quiz_category["type"]["id"]
                ).all()

        else:
            if quiz_category["type"] == "click":
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)
                ).all()
            else:
                questions = Question.query.filter(
                    and_(
                        Question.category == quiz_category["type"]["id"],
                        Question.id.notin_(previous_questions),
                    )
                ).all()
        if not questions:
            return jsonify({"success": True, "question": ""}), 200
        formatted_questions = [question.format() for question in questions]
        return (
            jsonify(
                {
                    "success": True,
                    "question": random.choice(formatted_questions),
                }
            ),
            200,
        )

    """
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  """

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify(
                {"success": False, "error": 400, "message": "Bad request"}
            ),
            400,
        )

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "Unprocessable entity",
                }
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 500,
                    "message": "Internal server error",
                }
            ),
            500,
        )

    return app
