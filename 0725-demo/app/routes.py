""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper
from app import db

# @app.route('/')
# def home():
#     return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search/gets/',methods=['POST'])
def search_result():
    conn = db.connect()
    S = request.form.get('keywords')
    print(S)
    print(type(S))
    sql = "select GameName, Genre, YearPublished, Description, Difficulty from BoardgameProduct where GameName like '%%{}%%';".format(S)
    print(sql)
    #where GameName like '%{}%'
    results = conn.execute(sql).fetchall()
    #print(results)
    conn.close()
    result_list = []
    for result in results:
        item = {
            "GameName": result[0],
            "Genre": result[1],
            "YearPublished": result[2],
            "Description": result[3],
            "Difficulty": result[4]
        }
        result_list.append(item)
    return render_template('search.html',items=result_list)

@app.route('/insert')
def insert():
    return render_template('insert.html')

@app.route('/insert/gets/',methods=['POST'])
def insert_result():
    conn = db.connect()
    GameID = request.form.get('GameID')
    Rating = request.form.get('Rating')
    Comment = request.form.get('Comment')
    UserID = request.form.get('UserID')
    Comment = "{}".format(Comment)
    finalpostID = conn.execute("select PostID from Review order by PostID desc limit 1;").fetchall()
    PostID = finalpostID[0][0] + 1
    sql_1 = 'insert into Review values({}, {}, {}, "{}", {});'.format(PostID, GameID, Rating, Comment, UserID)
    conn.execute(sql_1)
    sql_2 = "select * from Review order by PostID desc limit 5;"
    results = conn.execute(sql_2).fetchall()
    print (results)
    conn.close()
    result_list = []
    for result in results:
        item = {
            "PostID": result[0],
            "GameID": result[1],
            "Rating": result[2],
            "Comment": result[3],
            "UserID": result[4]
        }
        result_list.append(item)
    return render_template('insert.html',items=result_list)

@app.route('/update')
def update_user():
    return render_template('update.html')

@app.route('/update/gets/',methods=['POST'])
def update_user_info():
    conn = db.connect()
    Region = request.form.get('Region')
    Age = request.form.get('Age')
    UserID = request.form.get('UserID')
    # original data for user
    sql = "select UserID, Age, Region from User where UserID = {};".format(UserID)
    results = conn.execute(sql).fetchall()
    result_list = []
    for result in results:
        item = {
            "UserID": result[0],
            "Age": result[1],
            "Region": result[2],
        }
        result_list.append(item)
    #update user info    
    sql_1 = "UPDATE User set Region = '{}', Age = '{}' where UserID = {}".format(Region, Age, UserID)
    #UPDATE Review set Comment = "{}" where PostID = {}
    conn.execute(sql_1)
    #updated info for user
    sql_2 = "select UserID, Age, Region from User where UserID = {};".format(UserID)
    results = conn.execute(sql_2).fetchall()
    print (results)
    conn.close()
    for result in results:
        item = {
            "UserID": result[0],
            "Age": result[1],
            "Region": result[2],
        }
        result_list.append(item)
    return render_template('update.html',items_update=result_list)


@app.route('/advancedSQL1')
def advancedsql1():
    conn = db.connect()
    sql = "SELECT Rev.PostID, Rev.Rating, Rev.Comment, User_.Username FROM Review Rev NATURAL JOIN Upvoted Uv JOIN User User_ ON Uv.UserID=User_.UserID WHERE User_.Level >3 AND PostID IN (SELECT New_table.PostID FROM (SELECT Rev1.PostID, COUNT(User1.UserID) AS no_of_up FROM Review Rev1 JOIN Upvoted Uv1 JOIN User User1 ON Uv1.UserID=User1.UserID GROUP BY Rev1.PostID HAVING COUNT(User1.UserID) >=10) AS New_table);"
    print(sql)
    results = conn.execute(sql).fetchall()
    print(results)
    conn.close()
    result_list = []
    for result in results:
        item = {
            "PostID": result[0],
            "Rating": result[1],
            "Comment": result[2],
            "Username": result[3]
        }
        result_list.append(item)
    return render_template('advanced1.html',items=result_list)

@app.route('/advancedSQL2')
def advancedsql2():
    conn = db.connect()
    sql = "(SELECT Familyname, Avg(g.Difficulty), Avg(g.Duration),PartyFriendly FROM GameFamily f Natural JOIN BelongsTo b JOIN BoardgameProduct g on b.GameID = g.GameID WHERE PartyFriendly = 10 Group By Familyname LIMIT 10 )UNION(SELECT Familyname, Avg(g.Difficulty), Avg(g.Duration), PartyFriendly FROM GameFamily f Natural JOIN BelongsTo b JOIN BoardgameProduct g on b.GameID = g.GameID WHERE PartyFriendly = 1 Group By Familyname LIMIT 10);"
    # print(sql)
    results = conn.execute(sql).fetchall()
    # print(results)
    conn.close()
    result_list = []
    for result in results:
        item = {
            "Familyname": result[0],
            "AvgDifficulty": result[1],
            "AvgDuration": result[2],
            "PartyFriendly": result[3]
            # "Difficulty": result[4]
        }
        result_list.append(item)
    return render_template('advanced2.html',items=result_list)

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



