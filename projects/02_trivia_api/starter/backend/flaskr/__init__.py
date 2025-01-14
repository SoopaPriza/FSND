import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config=True)
  setup_db(app, 'postgresql://alex:th!ng5c%5En1ie@localhost:5432/trivia')
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [category.type for category in categories]
    print("le formatted categories:",formatted_categories)
    return jsonify({
      'success':True,
      'categories': formatted_categories
    })

  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def get_category_questions(id):
    print("id:",id)
    questions = Question.query.filter_by(category = (id+1)).all()
    formatted_questions = [question.format() for question in questions]

    # categories = Category.query.all()
    # formatted_categories = [category.format() for category in categories]
    # print("de formattedformatted_categories)

    return jsonify({
      'success':True,
      'questions': formatted_questions,
      # 'total_questions': len(questions),
      # 'categories': formatted_categories
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions', methods=['GET'])
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    current_questions = formatted_questions[start:end]

    categories = Category.query.all()
    formatted_categories = [category.type for category in categories]
    print("formatted categories:",formatted_categories)
    print("formatted questions:",formatted_questions)

    return jsonify({
      'success':True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': formatted_categories,
      'current_category': ""
    })

  # @app.route('/')
  # def daendpoint():
  #   return 
  # return app

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_questions(question_id):
    question=Question.query.get(question_id)
    question.delete()
    return jsonify({
      'success':True
    })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route('/questions', methods=['POST'])
  def create_questions():
    request_data = request.get_json()
    result = {}
    if 'searchTerm' in request_data.keys():
      questions = Question.query.filter(Question.question.ilike('%' + request_data['searchTerm'] + '%')).all()
      formatted_questions = [question.format() for question in questions]
      result = {
        'success':True,
        'questions': formatted_questions,
      }
    else:
      inquiry=Question(
        question=request_data['question'],
        answer=request_data['answer'],
        difficulty=request_data['difficulty'],
        category=int(request_data['category']) + 1
      )
      print("inquiry.category:",inquiry.category)
      inquiry.insert()
      result = {'success':True}
    return jsonify(result)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start.
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def get_questions_for_quiz():
    request_data = request.get_json()
    previous_questions=request_data['previous_questions']

    # questions = None
    if 'quiz_category' in request_data.keys():
      cat=request_data['quiz_category']
      id = int(cat['id'])
      questions = Question.query.filter_by(category = (id+1)).all()
    else:
      questions = Question.query.all()
    formatted_questions = [question.format() for question in questions]
    if len(formatted_questions)>len(previous_questions):
      numbor=random.randrange(0,len(questions))
      question_id=questions[numbor].id
      while question_id in previous_questions:
        numbor=random.randrange(0,len(questions))
        question_id=questions[numbor].id
      previous_questions.append(question_id)
      result={
        'success':True,
        'question': formatted_questions[numbor],
        'previousQuestions': previous_questions
      }
    else:
      result={'forceEnd':True}

    return jsonify(result)
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify ({
      'success': False,
      'error': 404,
      'message': 'not found'
    }), 404

  @app.errorhandler(422)
  def not_found(error):
    return jsonify ({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422
  
  return app

    