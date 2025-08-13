from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect("documents.db")
cursor = conn.cursor()

#total documents amount
cursor.execute("SELECT count(*) FROM documents")
totalCount = cursor.fetchone()[0]
cursor.close()

perPage = 20
lastPage = int(totalCount / perPage) + (0 if ((totalCount % perPage) == 0) else 1)


@app.route('/')
def index():
    page = request.args.get('page', default=1, type=int)

    conn = sqlite3.connect("documents.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM documents LIMIT {perPage} OFFSET {(page - 1) * perPage}")
    documents = cursor.fetchall()
    cursor.close()

    return render_template('index.html', page=page, lastPage=lastPage, documents=documents)

if __name__ == '__main__':
    app.run(debug=True)