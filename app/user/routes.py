from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Subject, Quiz, QuizAttempt, Question, UserAnswer, Chapter
from app.user.forms import ProfileForm, QuizAnswerForm
from app.utils import calculate_score
from datetime import datetime, timedelta
from . import user
# Add this import at the top of the file
from sqlalchemy import func

@user.before_request
@login_required
def require_user():
    if current_user.is_admin:
        abort(403)


@user.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    search_query = ''
    if request.method == 'POST':
        search_query = request.form.get('q', '')
    elif request.method == 'GET':
        search_query = request.args.get('q', '')
    
    if search_query:
        subjects = Subject.query.filter(Subject.name.ilike(f'%{search_query}%')).all()
    else:
        subjects = Subject.query.all()
    return render_template('user/dashboard.html', subjects=subjects, search_query=search_query)

@user.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.age = form.age.data
        current_user.interests = form.interests.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.age.data = current_user.age
        form.interests.data = current_user.interests
    return render_template('user/profile.html', form=form)

@user.route('/subject/<int:subject_id>/quizzes')
def view_quizzes(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    # Prepare quiz access information for each quiz
    quiz_access_info = []
    for quiz in sorted(subject.quizzes, key=lambda q: q.sequence_number):
        is_unlocked = quiz.is_unlocked_for_user(current_user)
        attempts_remaining = quiz.attempts_remaining_for_user(current_user)
        is_past_deadline = quiz.is_past_deadline()

        quiz_access_info.append({
            'quiz': quiz,
            'is_unlocked': is_unlocked,
            'attempts_remaining': attempts_remaining,
            'is_past_deadline': is_past_deadline,
            'can_attempt': is_unlocked and attempts_remaining > 0 and not is_past_deadline
        })

    return render_template('user/view_quizzes.html', subject=subject, quiz_access_info=quiz_access_info)
@user.route('/quiz/<int:quiz_id>/attempt', methods=['GET', 'POST'])
def attempt_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    # Access control checks
    if not quiz.is_unlocked_for_user(current_user):
        flash('This quiz is locked. Complete the prerequisite quiz first.', 'warning')
        return redirect(url_for('user.view_quizzes', subject_id=quiz.subject_id))

    if quiz.is_past_deadline():
        flash('The deadline for this quiz has passed.', 'danger')
        return redirect(url_for('user.view_quizzes', subject_id=quiz.subject_id))

    attempts_remaining = quiz.attempts_remaining_for_user(current_user)
    if attempts_remaining <= 0:
        flash('You have used all attempts for this quiz.', 'danger')
        return redirect(url_for('user.view_quizzes', subject_id=quiz.subject_id))

    # Check for existing incomplete attempt
    existing_attempt = QuizAttempt.query.filter_by(
        user_id=current_user.id,
        quiz_id=quiz.id,
        completed=False
    ).first()
    
    if existing_attempt:
        attempt = existing_attempt
        # Check if time has expired
        time_elapsed = datetime.utcnow() - attempt.started_at
        if time_elapsed.total_seconds() > quiz.time_limit * 60:
            attempt.completed = True
            attempt.completed_at = datetime.utcnow()
            db.session.commit()
            flash('Time for this attempt has expired!', 'danger')
            return redirect(url_for('user.quiz_result', attempt_id=attempt.id))
    else:
        # Create new attempt
        attempt = QuizAttempt(
            user_id=current_user.id,
            quiz_id=quiz.id,
            started_at=datetime.utcnow()
        )
        db.session.add(attempt)
        db.session.commit()
    
    # Get unanswered questions
    answered_question_ids = [answer.question_id for answer in attempt.answers]
    current_question = Question.query.filter(
        Question.quiz_id == quiz.id,
        ~Question.id.in_(answered_question_ids)
    ).first()
    
    if not current_question:
        # All questions answered, complete the attempt
        attempt.completed = True
        attempt.completed_at = datetime.utcnow()
        attempt.score = calculate_score(attempt)
        db.session.commit()
        return redirect(url_for('user.quiz_result', attempt_id=attempt.id))
    
    # Calculate remaining time
    time_elapsed = datetime.utcnow() - attempt.started_at
    remaining_time = max(0, quiz.time_limit * 60 - time_elapsed.total_seconds())
    
    # Create form with options for current question
    form = QuizAnswerForm()
    if form.validate_on_submit():
        selected_option = int(request.form.get('option'))
        is_correct = (selected_option == current_question.correct_option)
        
        answer = UserAnswer(
            attempt_id=attempt.id,
            question_id=current_question.id,
            selected_option=selected_option,
            is_correct=is_correct
        )
        db.session.add(answer)
        db.session.commit()
        
        return redirect(url_for('user.attempt_quiz', quiz_id=quiz.id))
    
    return render_template('user/attempt_quiz.html',
                         quiz=quiz,
                         question=current_question,
                         form=form,
                         remaining_time=remaining_time,
                         attempt=attempt)  # Add this line to pass the attempt variable
    
@user.route('/attempt/<int:attempt_id>/result')
def quiz_result(attempt_id):
    # Correct way to eager load answers and their related questions
    attempt = QuizAttempt.query.options(
        db.joinedload(QuizAttempt.answers).joinedload(UserAnswer.question)
    ).get_or_404(attempt_id)
    
    if attempt.user_id != current_user.id:
        abort(403)
    
    # Ensure score is calculated
    if attempt.score is None:
        attempt.score = calculate_score(attempt)
        attempt.completed = True
        attempt.completed_at = datetime.utcnow()
        db.session.commit()
    
    return render_template('user/quiz_result.html', attempt=attempt)


# Then update the performance route
@user.route('/performance')
def performance():
    # User's performance by subject (only completed attempts)
    subject_stats = db.session.query(
        Subject.name,
        func.avg(QuizAttempt.score).label('average_score')
    ).join(Quiz, Quiz.subject_id == Subject.id
    ).join(QuizAttempt, QuizAttempt.quiz_id == Quiz.id
    ).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.completed == True,
        QuizAttempt.completed_at.isnot(None)
    ).group_by(Subject.name).all()
    
    # User's completed quiz attempts
    quiz_attempts = db.session.query(
        Quiz.name,
        Subject.name.label('subject_name'),
        QuizAttempt.score,
        QuizAttempt.completed_at
    ).join(Quiz, QuizAttempt.quiz_id == Quiz.id
    ).join(Subject, Quiz.subject_id == Subject.id
    ).filter(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.completed == True,
        QuizAttempt.completed_at.isnot(None)
    ).order_by(QuizAttempt.completed_at.desc()).all()
    
    # Prepare data for charts
    subject_names = [stat.name for stat in subject_stats]
    subject_scores = [float(stat.average_score or 0) for stat in subject_stats]  # Ensure float
    
    return render_template('user/performance.html',
                         subject_stats=subject_stats,
                         quiz_attempts=quiz_attempts,
                         subject_names=subject_names,
                         subject_scores=subject_scores)
    
    
@user.route('/subject/<int:subject_id>')
def view_subject(subject_id):
    subject = Subject.query.options(
        db.joinedload(Subject.chapters).joinedload(Chapter.quizzes),
        db.joinedload(Subject.quizzes)
    ).get_or_404(subject_id)
    return render_template('user/view_subject.html', subject=subject)

@user.route('/chapter/<int:chapter_id>')
def view_chapter(chapter_id):
    chapter = Chapter.query.options(
        db.joinedload(Chapter.quizzes)
    ).get_or_404(chapter_id)
    return render_template('user/view_chapter.html', chapter=chapter)