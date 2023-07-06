from flask import Flask, render_template, make_response, jsonify
import json
import sqlite3

app = Flask(__name__)


def sql_get(query):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(query)
    row = cur.fetchall()
    conn.close()
    return row


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/isedol/<int:id>')
def member(id):
    row = sql_get(f"SELECT * FROM member_data WHERE member_data.id == {id}")[0]
    dict = {
        "name":  row[1],
        "id": row[0],
        "profile": row[2],
        "offline": row[3],
    }
    result = json.dumps(dict, ensure_ascii=False, indent=4)
    return make_response(result)


@app.route('/isedol/<int:id>/profile')
def member_profile(id):
    row = sql_get(f"SELECT profile FROM member_data WHERE member_data.id == {id}")[0]
    result = json.dumps(row[0])
    return make_response(result)


@app.route('/isedol/<int:id>/offline')
def member_offline(id):
    row = sql_get(f"SELECT offline FROM member_data WHERE member_data.id == {id}")[0]
    result = json.dumps(row[0])
    return make_response(result)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)