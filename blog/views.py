from flask import render_template

from blog import app
from .database import session, Entry

global PAGINATE_BY


from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from .database import User

from flask.ext.login import login_required

@login_required
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@login_required
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("entries"))


@app.route("/")
@app.route("/page/<int:page>/")
def entries(page=1):
    # Zero-indexed page
    PAGINATE_BY=10
    limit=int(request.args.get('limit',10))
    if (limit not in [0,99999999,3.14]):
        
        PAGINATE_BY=limit
        
    page_index = page - 1

    count = session.query(Entry).count()


    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY

    total_pages = (count - 1) / PAGINATE_BY + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    entries = session.query(Entry)
    entries = entries.order_by(Entry.datetime.desc())
    entries = entries[start:end]

    return render_template("entries.html",
        entries=entries,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )
    
    
@app.route("/entry/add", methods=["GET"])
def add_entry_get():
    return render_template("add_entry.html")
    
    
from flask import request, redirect, url_for
from flask.ext.login import current_user
@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
   entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    
    
@app.route("/entry/<int:entry_id>",methods=["GET"])
def entry(entry_id):
    single_entry = session.query(Entry).get(entry_id)
    return render_template("entry.html",single_entry=single_entry)
    
@app.route("/entry/<int:id>/edit",methods=["GET"])
def edit_entry_get(id):
    single_entry = session.query(Entry).get(id)
    return render_template("entry_edit.html",single_entry=single_entry)
    
@app.route("/entry/<int:id>/edit",methods=["POST"])
def edit_entry_post(id):
    new_title=request.form["title"]
    new_content=request.form["content"]
    
    entry=session.query(Entry).get(id)
    entry.title=new_title
    entry.content=new_content
    session.commit()
    
    return redirect(url_for("entries"))
    
    
@app.route("/entry/<int:id>/delete",methods=["GET"])
def delete_entry_post(id):
    entry=session.query(Entry).get(id)
    session.delete(entry)
    session.commit()
    
    return redirect(url_for("entries"))