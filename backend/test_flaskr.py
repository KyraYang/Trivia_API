import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "What's your name?",
            "answer": "Test Bot",
            "category": "1",
            "difficulty": 4,
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_questions(self):
        # without pagination
        res = self.client().get("/api/questions")
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(len(data["questions"]))
        # with pagination
        res = self.client().get("/api/questions?page=2")
        data_2 = json.loads(res.data)
        self.assertEqual(data_2["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data_2["total_questions"])
        self.assertTrue(data_2["categories"])
        self.assertNotEqual(data_2["questions"], data["questions"])

    def test_404_if_questions_are_not_found(self):
        res = self.client().get("/api/questions?page=10")
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Not found")

    def test_get_categories(self):
        res = self.client().get("/api/categories")
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_delete_question(self):
        res = self.client().delete("/api/questions/4")
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)

        question = Question.query.get(4)
        self.assertEqual(question, None)

    def test_422_if_question_not_exist(self):
        res = self.client().delete("/api/questions/100")
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"], "Unprocessable entity")

    def test_create_question(self):
        res = self.client().post("/api/questions", json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data["question"]))

    def test_400_if_create_question_missed_information(self):
        self.bad_question = {
            "question": "What's your name?",
            "answer": "Test Bot",
            "category": 1,
        }
        res = self.client().post("/api/questions", json=self.bad_question)
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["message"], "Bad request")

    def test_get_questions_by_category(self):
        res = self.client().get("/api/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["current_category"]["id"], 1)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_if_category_not_found(self):
        res = self.client().get("/api/categories/0/questions")
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Not found")

    def test_get_questions_by_search(self):
        search_term = {"searchTerm": "What"}
        res = self.client().post("/api/questions/searches", json=search_term)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_if_question_not_found(self):
        search_term = {"searchTerm": "NotExist"}
        res = self.client().post("/api/questions/searches", json=search_term)
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"], "Not found")

    def test_get_next_question(self):
        # no category and previous question
        quiz_request = {
            "previous_questions": [],
            "quiz_category": {"type": "click"},
        }
        res = self.client().post("/api/quizzes", json=quiz_request)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])
        # with category, without previous question
        quiz_request = {
            "previous_questions": [],
            "quiz_category": {"type": {"id": 1, "type": "Science"},},
        }
        res = self.client().post("/api/quizzes", json=quiz_request)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data["question"]["category"], Category.query.get(1).type
        )
        # without category, with previous question
        quiz_request = {
            "previous_questions": [2],
            "quiz_category": {"type": "click"},
        }
        res = self.client().post("/api/quizzes", json=quiz_request)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(data["question"]["id"], 2)
        # with category and previous questions
        quiz_request = {
            "previous_questions": [21, 22],
            "quiz_category": {"type": {"id": 1, "type": "Science"}},
        }
        res = self.client().post("/api/quizzes", json=quiz_request)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertNotIn(
            data["question"]["id"], quiz_request["previous_questions"]
        )
        self.assertEqual(
            data["question"]["category"], Category.query.get(1).type
        )
        # run out of questions
        quiz_request = {
            "previous_questions": [20, 21, 22, 24],
            "quiz_category": {"type": {"id": 1, "type": "Science"}},
        }
        res = self.client().post("/api/quizzes", json=quiz_request)
        data = json.loads(res.data)
        self.assertEqual(data["success"], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["question"], "")

    def test_400_if_quiz_request_missed_information(self):
        quiz_request = {
            "previous_questions": [20, 21, 22, 24],
        }
        res = self.client().post("/api/questions", json=quiz_request)
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["message"], "Bad request")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
