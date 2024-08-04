from app import db, app

def create_db():
    with app.app_context():
        db.create_all()
        print("Database and tables created")

if __name__ == "__main__":
    create_db()
