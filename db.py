from flask_sqlalchemy import SQLAlchemy

INMEM_DB_URL = "sqlite:///:memory:"
DB_URL = "sqlite:///:memory:"

def define_db(app, in_mem=False):
    if in_mem:
        app.config["SQLALCHEMY_DATABASE_URI"] = INMEM_DB_URL
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    class Poem(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        poem = db.Column(db.String, unique=True, nullable=False)
        author = db.Column(db.String)
        keywords = db.Column(db.String, default="")
        stars = db.Column(db.Integer, default=0)
        flags = db.Column(db.Integer, default=0)
        lang = db.Column(db.String, default="en")
        time_created = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

        def __repr__(self):
            return "<Poem(id={}, poem={}, author={}, keywords={}, lang={})>". \
                    format(self.id, self.poem, self.author, self.keywords, self.lang)

    db.create_all()

    return db, [Poem]