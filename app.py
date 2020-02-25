from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)



question_number = 0

@app.route('/')
def home():
    surveys_dict = surveys.surveys
    return render_template('choose.html', surveys = surveys_dict)

@app.route('/save-form')
def satisfaction():
    selected_title = request.args.get("survey_title")
    for survey in surveys.surveys.values():
        if survey.title == selected_title:
            # fix
            #session['survey'] = 
            return render_template('start.html', survey = survey)
    return "nope"

@app.route("/set-session", methods=['POST'])
def store_session():
    session["responses"] = []
    return redirect('/questions/0')

@app.route('/questions/<num>')
def questions(num):
    num =int(num)
    if question_number == "done":
        return redirect ('/thank-you')
    if num == question_number:
        curr_question = surveys.satisfaction_survey.questions[num].question
        choices = surveys.satisfaction_survey.questions[num].choices
        
        return render_template('questions.html', choices = choices, question = curr_question)
    else:
        flash("You are trying to access an invalid question")
        return redirect(f'/questions/{question_number}')

@app.route('/answer', methods=["post"])
def answer():

    #save answer in session
    curr_answer = request.form["q"]

    responses = session['responses']
    responses.append(curr_answer) 
    session['responses'] = responses

    #send new question or send to thank you page
    global question_number
    question_number += 1
    if question_number > 3:
        question_number = "done"
        return redirect ('/thank-you')
    else:
        return redirect(f'/questions/{question_number}')

@app.route('/thank-you')
def thank_you():
    return "<h1> Thank you! </h1>"
