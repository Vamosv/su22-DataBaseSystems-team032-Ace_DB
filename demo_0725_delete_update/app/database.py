"""Defines all the functions related to the database"""
from app import db

# def fetch_todo() -> dict:
#     """Reads all tasks listed in the todo table
#
#     Returns:
#         A list of dictionaries
#     """
#
#     conn = db.connect()
#     query_results = conn.execute("Select * from tasks;").fetchall()
#     conn.close()
#     todo_list = []
#     for result in query_results:
#         item = {
#             "id": result[0],
#             "task": result[1],
#             "status": result[2]
#         }
#         todo_list.append(item)
#
#     return todo_list

def fetch_Review() -> dict:
    """Reads all tasks listed in the Review table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from Review LIMIT 50;").fetchall()
    conn.close()
    Review_list = []
    for result in query_results:
        item = {
            "PostID": result[0],
            "GameID": result[1],
            "Rating": result[2],
            "Comment": result[3],
            "UserID": result[4]
        }
        Review_list.append(item)

    return Review_list

def update_comment_entry(PostID: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'UPDATE Review set Comment = "{}" where PostID = {};'.format(text, PostID)
    conn.execute(query)
    conn.close()


def update_status_entry(PostID: int, text: str) -> None:
    """Updates task status based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    conn = db.connect()
    query = 'UPDATE tasks set status = "{}" where id = {};'.format(text, PostID)
    conn.execute(query)
    conn.close()


def insert_new_task(text: str) ->  int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into Review (PostID, GameID, Rating,Comment,UserID) VALUES ("{}", "{}");'.format(
        text, "Todo")
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_post_by_id(PostID: int) -> None:
    """ remove entries based on PostID """
    conn = db.connect()
    query = 'Delete From Review WHERE PostID={};'.format(PostID)
    print('delete function')
    conn.execute(query)
    conn.close()
