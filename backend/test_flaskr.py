import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name)
        
        setup_db(self.app, self.database_path)
        
        self.new_question = {"question": "Combien de continent compte le monde", "Answer": "5", "deficulty": 1, "category": 1}

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
    def test_get_available_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        
        if len(data["categories"])==0:
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["categories"], [])
        else:
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data["categories"])
        
    def test_get_paginate_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])
        
    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/questions?page=1000", json={"id": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_get_paginate_questions_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["current_category"])
    
    def test_404_sent_request_question_by_category_beyond_valid_page(self):
        res = self.client().get("/categories/1000/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
    def test_delete_question(self):
        res = self.client().delete("/questions/10")
        data = json.loads(res.data)

        book = Question.query.filter(Question.id ==10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["deleted"], 10)

    def test_404_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
        
    def test_create_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        pass
    
    def test_get_question_search_whith_result(self):
        res = self.client().post('/questions', json={"searchTerm" : "movie"})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertEqual(data["current_category"], "Science")
        self.assertEqual(len(data["questions"]), 1)
        
    def test_get_question_search_whithout_result (self):
        res = self.client().post('/questions', json={"searchTerm" : "thhhshs"})
        data = json.loads(res.data)
        
        self.assertEqual(data["questions"], [])
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(data["current_category"], "Science")
    

    def test_422_if_question_creation_fails(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        pass
    
    def test_get_quizze(self):
        res = self.client().post('/quizzes', json={"previous_questions":[1,3], "quiz_category" : {"type": "Science", "id": "3" }})
        data = json.loads(res.data)
        
        self.assertTrue(data["question"])
    
    def test_get_404_quizz_not_found_if_category_not_exit(self):
        res = self.client().post("/quizzes", json={"previous_questions":[1,3], "quiz_category" : {"type": "Science", "id": "30" }})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()