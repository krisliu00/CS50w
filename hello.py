from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def bash_command():
    GeneralContent = ["cd xxdir 前往某个目录下", "cd .. 返回上级目录", "ls 列出目录里的文件", "cat xxfile 显示xxfile里的内容" ]
    RepositoryContent = ["git clone xxURL 从GitHub上copy需要clone的url下载到本地"]
    BranchContent = ["git checkout xxbranch 转到xxbranch上"]
    FlaskContent = ["flask --app hello run 在python里运行flask app hello.py", "flask --app hello run --debug"]

    return render_template("flask_test.html", GeneralContent=GeneralContent, RepositoryContent=RepositoryContent, BranchContent=BranchContent, FlaskContent=FlaskContent)