from flask import render_template, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms import RegisterForm, PostForm, LoginForm, ContactForm, CommentForm
from datetime import datetime as date
from os import path
from models import Post, User, Comment, Like
from ext import app, db


@app.route('/')
def home():
    post_base = Post.query.all()
    return render_template('Home.html', post_base=post_base, like=Like)


@app.route('/log_in', methods=['GET', 'POST'])
def log_in():
    form = LoginForm()
    if current_user.is_authenticated:
        flash('You are logged in already')
        return redirect('/')

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.uname.data).first()
        if user and user.check_pass(form.password.data):
            login_user(user)
            return redirect('/')
        else:
            flash("Either Username or Password is incorrect")
    return render_template('log_in.html', form=form)


@app.route('/logout')
def log_out():
    logout_user()
    return redirect('/')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    
    if current_user.is_authenticated:
        flash('You are logged in already')
        return redirect('/')

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.uname.data).all()
        mail = User.query.filter(User.gmail == form.email.data).all()
        if user:
            flash('Username is taken')
            return redirect('/sign_up')
        elif mail:
            flash('This email is registered')
            return redirect('/sign_up')
        else:
            new_user = User(
            fname =  form.fname.data,
            lname = form.lname.data,
            gmail = form.email.data,
            username = form.uname.data,
            password = form.password.data,
            )
            db.session.add(new_user)
            db.session.commit()

            if form.check == True:
               login_user(new_user, remember=True)
            else:
               login_user(new_user)
            return redirect('/')
        
    return render_template('Sign_up.html', form=form)


@app.route('/post/<num>', methods=["GET", 'POST'])
def ind(num):
    form = CommentForm()
    post = Post.query.get(num)
    comments = Comment.query.filter(Comment.post_id == num).all()
    likes = Like.query.filter(Like.post_id == num).all()
    asd = []
    for like in likes:
        asd.append(like.u_id)


    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
            post_id = num,
            usern = current_user.username,
            content = form.content.data
            )
            db.session.add(new_comment)
            db.session.commit()
        else:
            flash('Log in to comment')
                

        return redirect(f'/post/{num}')

    return render_template(f'post.html', post=post, form=form, comments=comments, likes = likes, asd = asd)


@app.route("/contact")
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('contact.html', form=form)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/upload', methods=["GET", 'POST'])
@login_required
def upload():
    delete = False
    post_form = PostForm()
    if post_form.validate_on_submit():
        x = date.today().strftime("%B %d, %Y")
        new_post = Post(
            title=post_form.title.data,
            subtitle=post_form.s_title.data,
            content=post_form.content.data,
            author=current_user.username,
            date=x,
            user_id = current_user.id,
            likes = 0
            )
        
        print(post_form.background_img)
    
        if post_form.background_img.data:
            image = post_form.background_img.data
            directory = path.join(app.root_path, "static", "images", image.filename)
            image.save(directory)
            new_post.img = image.filename
       
        db.session.add(new_post)
        db.session.commit()

        return redirect('/') 
    return render_template('upload.html', pform=post_form, delete=delete)


@app.route('/delete_post/<int:post>')
def delete(post):
    postt = Post.query.get(post)
    coments = Comment.query.filter(Comment.post_id == post).all()
    
    if current_user.id == postt.user_id:
        for coment in coments:
            db.session.delete(coment)
        db.session.delete(postt)
        db.session.commit()
    else:
        flash('You cannot delete this post')

    
    return redirect('/')

@app.route('/edit/<int:post>', methods=['GET', 'POST'])
def edit(post):
    delete = True
    pst = Post.query.get(post)

    if current_user.id == pst.user_id:
        edit_form = PostForm(title=pst.title, s_title=pst.subtitle, content=pst.content, author=pst.author)

        if edit_form.validate_on_submit():
            pst.title = edit_form.title.data
            pst.subtitle = edit_form.s_title.data
            pst.content = edit_form.content.data
            
            if edit_form.background_img.data != None:
                image = edit_form.background_img.data
                directory = path.join(app.root_path, "static", "images", image.filename)
                image.save(directory)

                pst.img = image.filename

            db.session.commit()
            return redirect('/')
        return render_template('upload.html', pform=edit_form, post=pst, delete=delete)
    else:
        flash('You cannot edit this post')
        return redirect('/')
    
    
@app.route('/user/<username>')
def userpage(username):
    user = User.query.filter(User.username == username).first()

    return render_template('userpage.html', user=user)

@app.route('/delete_user/<username>')
def delette(username):
    user = User.query.filter(User.username == username).first()
    post = Post.query.filter(Post.author == username).all()   
    if current_user.id == user.id:
        # User Info delete
        upvotes = Like.query.filter(Like.u_id == current_user.id).all() 
        for u in upvotes:
            ptt = Post.query.filter(Post.id == u.post_id).first()
            if ptt:
                ptt.likes -= 1
            db.session.delete(u)
        # Post info delete
        if post:
            for p in post:
                coments = Comment.query.filter(Comment.post_id == p.id).all()
                likes = Like.query.filter(Like.post_id == p.id).all()
                for like in likes:
                    db.session.delete(like)
                for coment in coments:
                    db.session.delete(coment)
                db.session.delete(p)
        logout_user()
        db.session.delete(user)
        db.session.commit()
    else:
        flash('Unable')
    
    return redirect('/')

@app.route('/like/<p_id>')
@login_required
def like(p_id):
    post = Post.query.get(p_id)
    likes = Like.query.filter(Like.post_id == p_id).all()


    if likes != []:
        for like in likes:
            asd = []
            asd.append(like.u_id)
            
        if current_user.id in asd:
                post.likes -= 1
                db.session.delete(like)
                db.session.commit()
        else:
            post.likes +=1
            nl = Like(
                post_id = p_id,
                u_id = current_user.id
            )
            db.session.add(nl)
            db.session.commit()
    else:
        post.likes +=1
        nl = Like(
            post_id = p_id,
            u_id = current_user.id
        )
        db.session.add(nl)
        db.session.commit()

        
    
    return redirect('/')
    
