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
        # self.database_name = os.getenv('DBNAME')
        # self.database_uri = os.getenv('DBURI')
        # self.database_path = "postgres://{}/{}".format(self.database_uri, self.database_name)
        # print("this should print right before setup_db")
        # setup_db(self.app, self.database_path)

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     print("this should print right before init_app")
        #     self.db.init_app(self.app)
        #     # create all tables
        #     print("and this should print right before create_all")
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_category_not_found(self):
        res = self.client().get('/categories/<int:id>/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))

    def test_all_questions_not_found(self):
        res = self.client().get('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_search_for_questions(self):
        searchTerm = {"searchTerm":"royal palace"}
        res = self.client().post('/questions', json=searchTerm)
        data = json.loads(res.data)
        print("here is data: ",data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_search_for_questions_no_results(self):
        searchTerm = {"searchTerm":"youshouldntbeabletofindme"}
        res = self.client().post('/questions', json=searchTerm)
        data = json.loads(res.data)
        print("here is data: ",data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
    
    def test_quiz_play(self):
        self.previous_questions = {'previous_questions':[2], 'type':'Geography', 'id' : 2}
        res = self.client().post('/quizzes', json = self.previous_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_quiz_play_not_found(self):
        self.previous_questions = {'previous_questions':[2], 'type':'Geography', 'id' : 2}
        res = self.client().post('/quizzes/', json = self.previous_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        res = self.client().delete('/questions/9')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 9).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    def test_delete_question_not_found(self):
        res = self.client().delete('/question/1000000')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 1000000).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(question, None)
"""
TODO
Write at least one test for each test for successful operation and for expected errors.
"""


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()