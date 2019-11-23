from flask_sqlalchemy import SQLAlchemy

DB_URL = "sqlite:///:memory:"

def define_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
    db = SQLAlchemy(app)

    class Poem(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        poem = db.Column(db.String, unique=True, nullable=False)
        author = db.Column(db.String)
        _keywords = db.Column(db.String, default="")
        stars = db.Column(db.Integer, default=0)
        flags = db.Column(db.Integer, default=0)

        @property
        def keywords(self):
            return [x for x in self._keywords.split()]

        @keywords.setter
        def keywords(self, keyword):
            if self._keywords is None:
                self._keywords = keyword
            else:
                self._keywords += " {}".format(keyword)

        def __repr__(self):
            return "<Poem(id={}, poem={}, author={}, keywords={})>".format(self.id, \
                                                self.poem, self.author, self.keywords)

    db.create_all()

    return db, Poem