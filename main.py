from flask import Flask, render_template, request, url_for, redirect
from store import Post, PostStore

app = Flask(__name__)

dummy_posts = [
    Post(id=1,
         photo_url='https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=50&w=50',
         name='Sara',
         body='Lorem ipsum dolor sit amet consectetur adipisicing elit. Inventore repellendus itaque rem vitae,\
                    reprehenderit tempora officia sapiente? Hic, quae qui atque, quaerat, vitae distinctio libero quas\
                    similique facilis iste nostrum?'),
    Post(id=2,
         photo_url='https://images.pexels.com/photos/736716/pexels-photo-736716.jpeg?auto=compress&cs=tinysrgb&dpr=1&h=100&w=100',
         name='John',
         body='Quae qui atque, quaerat, vitae distinctio libero quas similique facilis iste nostrum?'),
]
post_store = PostStore()
post_store.add(dummy_posts[0])
post_store.add(dummy_posts[1])

posts = post_store.get_all()


@app.route('/')
def show_posts():
    return render_template('index.html', posts=posts)


app.current_id = 3


@app.route('/add_post/', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        new_post = Post(id=app.current_id,
                        photo_url=request.form['photo_url'],
                        name=request.form['name'],
                        body=request.form['body'])
        post_store.add(new_post)
        app.current_id += 1
        return redirect(url_for('show_posts'))
    elif request.method == 'GET':
        return render_template('add_post.html')


@app.route('/delete_post/<int:id>')
def delete_post(id):
    post_store.delete(id)
    return redirect(url_for('show_posts'))


@app.route('/update_post/<int:id>', methods=['GET', 'POST'])
def update_post(id):
    if request.method == 'POST':
        update_fields = {
            'photo_url': request.form['photo_url'],
            'name': request.form['name'],
            'body': request.form['body']
        }
        post_store.update(id, update_fields)
        return redirect(url_for('show_posts'))
    elif request.method == 'GET':
        post = post_store.get_by_id(id)
        return render_template('update_post.html', post=post)


app.run()
