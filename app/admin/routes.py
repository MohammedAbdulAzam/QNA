from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from app import db
from app.models import Subject, Quiz, Question, User, QuizAttempt, UserAnswer, Chapter
from app.admin.forms import SubjectForm, QuizForm, QuestionForm, ChapterForm
from app.utils import calculate_score
from sqlalchemy import func
from datetime import datetime
from . import admin

@admin.before_request
@login_required
def require_admin():
    if not current_user.is_admin:
        abort(403)


@admin.route('/dashboard', methods=['GET', 'POST'])
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
    return render_template('admin/dashboard.html', subjects=subjects, search_query=search_query)

@admin.route('/subject/add', methods=['GET', 'POST'])
def add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data, description=form.description.data)
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('admin/add_subject.html', form=form)

@admin.route('/subject/<int:subject_id>/edit', methods=['GET', 'POST'])
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = SubjectForm()
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    elif request.method == 'GET':
        form.name.data = subject.name
        form.description.data = subject.description
    return render_template('admin/edit_subject.html', form=form, subject=subject)

@admin.route('/subject/<int:subject_id>')
def view_subject(subject_id):
    subject = Subject.query.options(
        db.joinedload(Subject.chapters),
        db.joinedload(Subject.quizzes)
    ).get_or_404(subject_id)
    return render_template('admin/view_subject.html', subject=subject)

@admin.route('/subject/<int:subject_id>/delete', methods=['POST'])
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/quiz/<int:subject_id>/add', methods=['GET', 'POST'])
def add_quiz(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = QuizForm()
    form.chapter_id.choices = [(c.id, c.name) for c in subject.chapters]
    
    # Pre-select chapter if coming from chapter page
    if 'chapter_id' in request.args:
        form.chapter_id.data = request.args.get('chapter_id')
    
    if form.validate_on_submit():
        quiz = Quiz(
            name=form.name.data,
            description=form.description.data,
            time_limit=form.time_limit.data,
            subject_id=subject.id,
            chapter_id=form.chapter_id.data
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz added successfully!', 'success')
        return redirect(url_for('admin.view_subject', subject_id=subject.id))
    return render_template('admin/add_quiz.html', form=form, subject=subject)

@admin.route('/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizForm()
    if form.validate_on_submit():
        quiz.name = form.name.data
        quiz.description = form.description.data
        quiz.time_limit = form.time_limit.data
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('admin.view_subject', subject_id=quiz.subject_id))
    elif request.method == 'GET':
        form.name.data = quiz.name
        form.description.data = quiz.description
        form.time_limit.data = quiz.time_limit
    return render_template('admin/edit_quiz.html', form=form, quiz=quiz)

@admin.route('/quiz/<int:quiz_id>/view')
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('admin/view_quiz.html', quiz=quiz)

@admin.route('/quiz/<int:quiz_id>/delete', methods=['POST'])
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    subject_id = quiz.subject_id
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('admin.view_subject', subject_id=subject_id))

@admin.route('/question/<int:quiz_id>/add', methods=['GET', 'POST'])
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            text=form.text.data,
            marks=form.marks.data,
            option1=form.option1.data,
            option2=form.option2.data,
            option3=form.option3.data,
            option4=form.option4.data,
            correct_option=form.correct_option.data,
            quiz_id=quiz.id
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully!', 'success')
        return redirect(url_for('admin.view_quiz', quiz_id=quiz.id))
    return render_template('admin/add_question.html', form=form, quiz=quiz)

@admin.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    form = QuestionForm()
    if form.validate_on_submit():
        question.text = form.text.data
        question.marks = form.marks.data
        question.option1 = form.option1.data
        question.option2 = form.option2.data
        question.option3 = form.option3.data
        question.option4 = form.option4.data
        question.correct_option = form.correct_option.data
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('admin.view_quiz', quiz_id=question.quiz_id))
    elif request.method == 'GET':
        form.text.data = question.text
        form.marks.data = question.marks
        form.option1.data = question.option1
        form.option2.data = question.option2
        form.option3.data = question.option3
        form.option4.data = question.option4
        form.correct_option.data = question.correct_option
    return render_template('admin/edit_question.html', form=form, question=question)

@admin.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('admin.view_quiz', quiz_id=quiz_id))

from sqlalchemy import func

@admin.route('/statistics')
def statistics():
    # Basic counts
    user_count = User.query.filter_by(is_admin=False).count()
    subject_count = Subject.query.count()
    quiz_count = Quiz.query.count()
    question_count = Question.query.count()
    
    # Subject-wise average scores
    subject_stats = db.session.query(
        Subject.name,
        func.avg(QuizAttempt.score).label('average_score')
    ).join(Quiz, Quiz.subject_id == Subject.id
    ).join(QuizAttempt, QuizAttempt.quiz_id == Quiz.id
    ).group_by(Subject.name).all()
    
    # Prepare chart data
    subject_names = [stat.name for stat in subject_stats]
    subject_scores = [float(stat.average_score or 0) for stat in subject_stats]
    
    # Top 10 quizzes by attempts
    popular_quizzes = db.session.query(
        Quiz.name,
        func.count(QuizAttempt.id).label('attempt_count'),
        func.avg(QuizAttempt.score).label('average_score')
    ).join(QuizAttempt, QuizAttempt.quiz_id == Quiz.id
    ).group_by(Quiz.name
    ).order_by(func.count(QuizAttempt.id).desc()
    ).limit(10).all()
    
    quiz_names = [quiz.name for quiz in popular_quizzes]
    quiz_scores = [float(quiz.average_score or 0) for quiz in popular_quizzes]
    
    return render_template('admin/statistics.html',
                         user_count=user_count,
                         subject_count=subject_count,
                         quiz_count=quiz_count,
                         question_count=question_count,
                         subject_names=subject_names,
                         subject_scores=subject_scores,
                         quiz_names=quiz_names,
                         quiz_scores=quiz_scores)

@admin.route('/user-statistics/<int:user_id>')
def view_user_statistics(user_id):
    user = User.query.get_or_404(user_id)
    
    # User's performance by subject
    subject_stats = db.session.query(
        Subject.name,
        func.avg(QuizAttempt.score).label('average_score')
    ).join(Quiz, Quiz.subject_id == Subject.id
    ).join(QuizAttempt, QuizAttempt.quiz_id == Quiz.id
    ).filter(QuizAttempt.user_id == user.id
    ).group_by(Subject.name).all()
    
    # Prepare chart data
    subject_names = [stat.name for stat in subject_stats]
    subject_scores = [float(stat.average_score or 0) for stat in subject_stats]
    
    # User's quiz attempts
    quiz_attempts = db.session.query(
        Quiz.name,
        Subject.name.label('subject_name'),
        QuizAttempt.score,
        QuizAttempt.completed_at
    ).join(Quiz, QuizAttempt.quiz_id == Quiz.id
    ).join(Subject, Quiz.subject_id == Subject.id
    ).filter(QuizAttempt.user_id == user.id
    ).order_by(QuizAttempt.completed_at.desc()).all()
    
    return render_template('admin/view_user_statistics.html',
                         user=user,
                         subject_stats=subject_stats,
                         quiz_attempts=quiz_attempts,
                         subject_names=subject_names,
                         subject_scores=subject_scores)

@admin.route('/user-statistics')
def user_statistics():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/user_statistics.html', users=users)

@admin.route('/user/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    if current_user.id == user_id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin.user_statistics'))
    
    user = User.query.get_or_404(user_id)
    
    # First delete all dependent records
    # Option 1: Delete all quiz attempts and answers
    attempts = QuizAttempt.query.filter_by(user_id=user.id).all()
    for attempt in attempts:
        # Delete all answers for this attempt
        UserAnswer.query.filter_by(attempt_id=attempt.id).delete()
        # Delete the attempt
        db.session.delete(attempt)
    
    # Option 2: Orphan the attempts (if you want to keep attempt data)
    # QuizAttempt.query.filter_by(user_id=user.id).update({'user_id': None})
    # Note: This requires nullable user_id in the model
    
    # Now delete the user
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.user_statistics'))
# Add these new routes
@admin.route('/subject/<int:subject_id>/add-chapter', methods=['GET', 'POST'])
def add_chapter(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = ChapterForm()
    if form.validate_on_submit():
        chapter = Chapter(name=form.name.data, 
                         description=form.description.data,
                         subject_id=subject.id)
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter added successfully!', 'success')
        return redirect(url_for('admin.view_subject', subject_id=subject.id))
    return render_template('admin/add_chapter.html', form=form, subject=subject)

@admin.route('/chapter/<int:chapter_id>/edit', methods=['GET', 'POST'])
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    form = ChapterForm()
    if form.validate_on_submit():
        chapter.name = form.name.data
        chapter.description = form.description.data
        db.session.commit()
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('admin.view_subject', subject_id=chapter.subject_id))
    elif request.method == 'GET':
        form.name.data = chapter.name
        form.description.data = chapter.description
    return render_template('admin/edit_chapter.html', form=form, chapter=chapter)

@admin.route('/chapter/<int:chapter_id>/view')
def view_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    return render_template('admin/view_chapter.html', chapter=chapter)

@admin.route('/chapter/<int:chapter_id>/delete', methods=['POST'])
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    subject_id = chapter.subject_id
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted successfully!', 'success')
    return redirect(url_for('admin.view_subject', subject_id=subject_id))
