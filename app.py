from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


surveys_dict = surveys.surveys
question_number = 0

@app.route('/')
def choose_survey():

    #reset question_number in case someone is taking the survey more than once
    global question_number
    question_number = 0
    return render_template('choose.html', surveys = surveys_dict)

@app.route('/', methods=["POST"])
def start_survey():
    selected_survey = request.form.get("survey_id")
    session["curr_id"] = selected_survey

    return render_template('start.html', survey = surveys_dict[selected_survey])

@app.route("/set-session", methods=['POST'])
def store_session():

    session["responses"] = []
    return redirect('/questions/0')

@app.route('/questions/<num>')
def questions(num):
    num =int(num)

    #send to thank you page
    if question_number == "done":
        return redirect ('/thank-you')
        
    #send next question
    if num == question_number:
        survey = surveys_dict[session["curr_id"]]
        curr_question = survey.questions[num]
        
        return render_template('questions.html', question = curr_question)
    else:
        flash("You are trying to access an invalid question")
        return redirect(f'/questions/{question_number}')

@app.route('/answer', methods=["post"])
def answer():

    #get answer and comment if any 
    curr_answer = request.form["q"]
    curr_comment = request.form.get("comment", "")

    #save answer and comment in session
    responses = session['responses']
    responses.append({"answer": curr_answer, "comment": curr_comment})
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
    survey = surveys_dict[session["curr_id"]]
    responses = session['responses']
    return render_template('thanks.html', response = response, survey = survey)
