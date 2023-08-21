from home import app, db
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run('0.0.0.0', 4568)

