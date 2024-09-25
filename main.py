from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuring SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'questions.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model for Questions
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    pdf_filename = db.Column(db.String(150), nullable=False)
    answer_sequence = db.Column(db.String(50), nullable=False)

    def __init__(self, title, pdf_filename, answer_sequence):
        self.title = title
        self.pdf_filename = pdf_filename
        self.answer_sequence = answer_sequence

# Initialize database
with app.app_context():
    db.create_all()

# Route to upload question details
@app.route('/upload', methods=['POST'])
def upload_question():
    if 'pdf' not in request.files:
        return jsonify({'message': 'No PDF file part'}), 400
    
    pdf_file = request.files['pdf']
    title = request.form['title']
    answer_sequence = request.form['answer_sequence']

    if pdf_file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Save the PDF file
    pdf_path = os.path.join('uploads', pdf_file.filename)
    pdf_file.save(pdf_path)

    # Create a new question
    new_question = Question(title=title, pdf_filename=pdf_file.filename, answer_sequence=answer_sequence)
    db.session.add(new_question)
    db.session.commit()

    return jsonify({'message': 'Question uploaded successfully!'})

# Route to retrieve all questions
@app.route('/questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    output = []

    for question in questions:
        question_data = {
            'id': question.id,
            'title': question.title,
            'pdf_filename': question.pdf_filename,
            'answer_sequence': question.answer_sequence
        }
        output.append(question_data)

    return jsonify(output)

# Route to retrieve a single question by ID
@app.route('/questions/<int:id>', methods=['GET'])
def get_question(id):
    question = Question.query.get(id)
    if not question:
        return jsonify({'message': 'Question not found'}), 404
    
    question_data = {
        'id': question.id,
        'title': question.title,
        'pdf_filename': question.pdf_filename,
        'answer_sequence': question.answer_sequence
    }
    return jsonify(question_data)


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
