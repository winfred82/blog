from flask import render_template

from blog import app
from .database import session, Entry

PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    # Zero-indexed page
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

@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
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