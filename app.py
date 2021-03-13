from datetime import datetime
from flask import Flask, render_template, request ,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30), nullable = False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable = False)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.order_by(Post.due).all()   # 投稿全部を取り出す   (タスクの締め切りの順番に変更)
        return render_template('index.html', posts = posts)
    else:   # requestの方法がPOSTの場合
        title = request.form.get('title')  # formから送られてきたtitleをtitle(変数)に格納
        detail = request.form.get('detail')
        due = request.form.get('due')

        due = datetime.strptime(due, '%Y-%m-%d') #ハイフン繋ぎの日付に変更する
        new_post = Post(title = title, detail = detail, due = due)  # formから来たタスクを新しい投稿(new_post)として作成

        db.session.add(new_post)
        db.session.commit()

        return redirect('/')



@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/detail/<int:id>')   # そのidに属しているタスクを表示させる
def read(id):
    post = Post.query.get(id)  # DBから該当するidをgetする
    return render_template('detail.html',post = post)

@app.route('/update/<int:id>', methods = ['GET', 'POST'])  
def update(id):
    post = Post.query.get(id) 
    if request.method == 'GET':   # updateのページに  
        return render_template('update.html',post = post)  
    else:  # 変更内容を反映し、dbに格納し、トップページに
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')
        
        db.session.commit()
        return redirect('/')     

@app.route('/delete/<int:id>')   # そのidに属しているタスクを削除
def delete(id):
    post = Post.query.get(id)  # DBから該当するidをgetする
    db.session.delete(post)
    db.session.commit()
    return redirect('/')   # トップページに飛ばす


if __name__=='__main__':
    app.run()


