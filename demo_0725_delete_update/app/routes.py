""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/delete/<int:PostID>", methods=['POST'])
def delete(PostID):
    """ recieved post requests for entry delete """
    print('get before helper')
    try:
        db_helper.remove_post_by_id(PostID)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:PostID>", methods=['POST'])
def update(PostID):
    """ recieved post requests for entry updates """

    data = request.get_json()
    print('get again!')
    try:
        # if "status" in data:
        #     db_helper.update_task_entry(PostID, data["status"])
        #     result = {'success': True, 'response': 'Status Updated'}
        if "description" in data:
            db_helper.update_comment_entry(PostID, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_task(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_Review()
    return render_template("index.html", items=items)
