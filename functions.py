import random

class DbFunc(object):
    def __init__(self, db, tables):
        self.db = db
        self.session = db.session
        self.Poem = tables[0]

    def submit_poem(self, poem, author=None, keywords=None):
        # Ensure poem is not an empty string
        if poem == "":
            return "Poem cannot be empty !"

        # TODO : Also have to check if poem is already submitted
        author = author or "Unknown"      # TODO : to translate
        keywords = keywords or " "      # TODO : remove duplicata

        print(poem, author, keywords)
        self.session.add(self.Poem(poem=poem, author=author, keywords=keywords))
        self.session.commit()
        return "Poem successfully submitted ! Thank you for sharing :)"

    def get_poems_by_best(self):
        return self.session.query(self.Poem).order_by(self.Poem.stars).all()

    def get_poems_by_latest(self):
        return self.session.query(self.Poem).order_by(self.Poem.stars).all()

    def get_2_rand_poems(self):
        poems = random.choices(self.session.query(self.Poem).all(), k=2)
        return poems[0], poems[1]

    def star(self, poem_id):
        poem.stars += 1
        self.session.add(poem)
        self.session.commit()

    def report(self, poem_id):
        poem.flags += 1     # Later : add automatically remove of poem after X report ?
        self.session.add(poem)
        self.session.commit()
