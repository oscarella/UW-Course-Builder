from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Term, Course
from .filters import htmlfy

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Term Creation
        if 'name_term' in request.form:
            name = request.form.get('name_term')
            if not name:
                flash('The title cannot be empty.', category='error')
            elif len(name) > 20:
                flash('The term\'s title should be maximum 20 characters.', category='error')
            else:
                flash('Term has been successfully created.', category='success')
                new_term = Term(name=name)
                current_user.terms.append(new_term)
                db.session.commit()
        # Term title modification
        elif 'rename_term' in request.form:
            id = request.form.get('rename_term')
            title = request.form.get('new_title')
            if not title or len(title) > 20:
                flash('Length requirements are not met.', 'error')
            else:
                term = Term.query.filter_by(id=id, user_id=current_user.id).first()
                if term:
                    term.name = title
                    db.session.commit()
                    flash('Request successful.', 'success')
                else:
                    flash('Request unsuccessful.', 'error')
        # Term deletion
        elif 'delete_term' in request.form:
            id = request.form.get('delete_term')
            term = Term.query.filter_by(id=id, user_id=current_user.id).first()
            if term:
                db.session.delete(term)
                db.session.commit()
                flash('Deletion successful.', 'success')
            else:
                flash('Request unsuccessful.', 'error')
        elif 'remove_course' in request.form:
            course_id = request.form.get('remove_course')
            term_id = request.form.get('from_term')
            term = Term.query.filter_by(id=term_id, user_id=current_user.id).first()
            if term:
                term.courses.remove(Course.query.get(course_id))
                db.session.commit()
                flash('Course was successfully removed.', 'success')
            else:
                flash('Request unsuccessful.', 'error')
        return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)

@views.route('/add-courses', methods=['POST'])
@login_required
def add_courses():
    data = request.get_json()
    courses = data.get("courses")
    termId = data.get("term")
    print(courses)
    if len(courses) == 0:
        flash('No courses were added to cart.', 'error')
    else:
        term = Term.query.get(termId)
        if term is None or term.user_id != current_user.id:
            flash('Request unsuccessful.', 'error')
        else:
            for cdict in courses:
                course = Course.query.get(cdict['id'])
                if course:
                    term.courses.append(course)
            db.session.commit()
            flash('Successfully added.', 'success')
    return jsonify({})

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():

    return render_template("search.html", user=current_user)

@views.route('/star-course', methods=['POST'])
@login_required
def star_course():
    data = request.get_json()
    courseId  = data.get("courseId")
    course = Course.query.get(courseId)
    if course:
        if course in current_user.courses:
            current_user.courses.remove(course)
            db.session.commit()
            flash('Starred course removed.', 'success')
        else:
            current_user.courses.append(course)
            db.session.commit()
            flash('Course successfully starred.', 'success')
    return jsonify({})

@views.route('/star-course-search', methods=['POST'])
@login_required
def star_course_search():
    data = request.get_json()
    courseId  = data.get("courseId")
    course = Course.query.get(courseId)
    if course:
        if course in current_user.courses:
            current_user.courses.remove(course)
            db.session.commit()
        else:
            current_user.courses.append(course)
            db.session.commit()
    return fetch_starred()

@views.route('/fetch-starred')
@login_required
def fetch_starred():
    starred = current_user.courses
    return jsonify([c.to_dict() for c in starred])

@views.route('/fetch-terms')
@login_required
def fetch_terms():
    terms = current_user.terms
    return jsonify([t.to_dict() for t in terms])

@views.route('/check-status', methods = ['POST'])
@login_required
def check_status():
    courseId = request.get_json().get("courseId")
    contains = False
    for term in current_user.terms:
        for course in term.courses:
            if courseId == course.id:
                contains = True
    return jsonify(contains)

@views.route('/search-keyword', methods=['POST'])
@login_required
def search_keyword():
    query = request.get_json().get("query")
    results = Course.query.whooshee_search(query, order_by_relevance=-1).limit(250).all()
    return jsonify([c.to_dict() for c in results])

@views.route('/search-course-id', methods=['POST'])
@login_required
def search_course_id():
    data = request.get_json()
    courseId  = data.get("courseId")
    course = Course.query.get(courseId)
    return jsonify(course.to_dict())

@views.route('/prettify-desc', methods=['POST'])
@login_required
def prettify_desc():
    body = request.get_json().get('courseBody')
    body = htmlfy(body)
    return jsonify(body)