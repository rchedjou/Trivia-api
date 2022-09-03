from crypt import methods
import os
from secrets import choice
from select import select
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from flask_migrate import Migrate

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)
    
    
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    # @app.route("/")
    # def helloWorld():
    #     return "Hello, cross-origin-world!"
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, POST, DELETE"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def retrive_categories():
        selection = Category.query.order_by(Category.id).all()
        if(len(selection)==0):
            return jsonify({
                'categories' : []
            })
        else :    
            formatted_categories_id = [category.format_id() for category in selection]
            formatted_categories_type = [category.format_type() for category in selection]
            formatted_categories = dict(zip(formatted_categories_id,formatted_categories_type))
            return jsonify({
                'categories' : formatted_categories
            })
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
    @app.route("/questions")
    def retrive_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        
        if len(current_questions) == 0:
            abort(404)
            
        else:
            selection_categories = Category.query.order_by(Category.id).all()
            #CHEDJOU ==>cette partie tranforme l'ensembles des categories en un seul dictionnaire
            formatted_categories_id = [category.format_id() for category in selection_categories]
            formatted_categories_type = [category.format_type() for category in selection_categories]
            formatted_categories = dict(zip(formatted_categories_id,formatted_categories_type))

            return jsonify({
                'questions' : current_questions,
                'total_questions': len(Question.query.all()),
                'categories' : formatted_categories,
                'current_category': formatted_categories.get("1")
            }) 
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try : 
            question = Question.query.filter(Question.id==question_id).one_or_none()
            if question is None : 
                abort(404)
            
            question.delete()
        except:
            abort(422)
        return jsonify({
            'deleted' : question_id
        })
    
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=["POST"])
    def create_question():
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)
        searchTerm = body.get("searchTerm", None)
        
        try:
            if searchTerm:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{0}%'.format(searchTerm)))
                current_questions = paginate_questions(request, selection)
                return jsonify({
                    'questions' : current_questions,
                    'total_questions': len(current_questions),
                    'current_category': Category.query.first().type
                }) 
            else:
                question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
                question.insert()
                # print(question.format())
                return jsonify({
                    
                })
                
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    #cette partie sera traité dans le point de terminaison POST /question
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:id_category>/questions")
    def get_question_for_spacific_category(id_category):
        selection = Question.query.order_by(Question.id).filter(Question.category==id_category).all()
        current_questions = paginate_questions(request, selection)
        
        if len(current_questions) == 0:
            abort(404)
            
        else:
            return jsonify({
                'questions' : current_questions,
                'total_questions': len(current_questions),
                'current_category': Category.query.filter(Category.id==id_category).first().type
            }) 
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
    
    @app.route("/quizzes", methods=["POST"])
    def play():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)
        
        # si la question precedente existe on selection les question de la categorie x dont lrs id ne sont pas compris parmis previous_questions
        try:
            if  len(previous_questions)==0:
                selection_question = Question.query.order_by(Question.id).filter(Question.category==quiz_category.get("id")).all()
            else:
                selection_question = Question.query.order_by(Question.id).filter(Question.category==quiz_category.get("id")).filter(~Question.id.in_(previous_questions)).all()
            selection_question_formatted = [question.format() for question in selection_question]
            return jsonify({
                "question" : random.choice(selection_question_formatted),
            })
        except:
            abort(404)
    
    
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )
        
    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )
    return app

