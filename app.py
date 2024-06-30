from ext import app



if __name__ == '__main__':
    from routes import home, log_in, sign_up, ind, contact, about, upload, delete, edit, userpage, like
    app.run(debug=True)
