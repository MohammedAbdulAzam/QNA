from flask import render_template

def page_not_found(e):
    return render_template('errors/404.html'), 404

def forbidden(e):
    return render_template('errors/403.html'), 403

def server_error(e):
    return render_template('errors/500.html'), 500

def calculate_score(attempt):
    if not attempt.answers:
        return 0.0
    
    total_questions = len(attempt.answers)
    correct_answers = sum(1 for answer in attempt.answers if answer.is_correct)
    return (correct_answers / total_questions) * 100