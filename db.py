from flask_sqlalchemy import SQLAlchemy
import os

INMEM_DB_URL = "sqlite:///:memory:"


def define_db(app, in_mem=False):
    """
    Function defining the Database. It defines all tables and return the
    Database object as well as a list of Table used.
    In our current case, only one table is used for simplicity : the table for
    Poems.

    Args:
        app (FlaskApp): Flask application used by Dash. this is necessary
            because we use `flask_sqlalchemy` as ORM.
        in_mem (bool, optional): Bool indicating if we use in-memory database.
            Useful for debug. Defaults to `False`.

    Returns:
        SQLAlchemy: Database object.
        list of Tables: Tables of the Database.
    """
    if in_mem:
        app.config["SQLALCHEMY_DATABASE_URI"] = INMEM_DB_URL
        print("Using in-memory SQLite database...")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
        print("Using database located at {}".format(os.environ["DATABASE_URL"]))
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
