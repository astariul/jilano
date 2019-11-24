import random

MIN_CONTENT_LEN = 3
MAX_CONTENT_LEN = 5000
MAX_AUTHOR_LEN = 500
MAX_KEYWORD_LEN = 500
KEYWORDS_SEPARATOR = ','
MAX_KEYWORDS_NB = 10

class DbFunc(object):
    def __init__(self, db, tables):
        self.db = db
        self.session = db.session
        self.Poem = tables[0]

    def submit_poem(self, poem, author=None, keywords=None):
        """ Function to submit a poem to the database.

        A poem should have a content, can have an author, and can have keywords.

        Content is not limited to 3 lines. It can be anything as long as :
        * There is at least 3 characters
        * There is at maximum 5000 characters
        * Should be unique !

        Author name can be anything, as long as it smaller than 500 characters.

        Keywords can be anything, as long as each keyword is smaller than 500
        characters. Maximum of 10 keywords per poem. Keywords are separated by 
        comma.

        Args:
            poem (str): The content of the poem.
            author (str, optional): Name of the author.
            keywords (str, optional): Keywords of the poem.

        Return:
            bool: True if the poem was successfully added to the database. False
                otherwise.
            str: Error / Success message to display to the user.
        """
        # Checking length
        if poem == "":
            return False, "Poem cannot be empty."
        elif len(poem) < MIN_CONTENT_LEN:
            return False, "Poem is too short : it should be at least 3 characters."
        elif len(poem) > MAX_CONTENT_LEN:
            return False, "Poem is too long : it should be at maximum 5000 characters."

        author = author or ""
        keywords = keywords or ""

        if len(author) > MAX_AUTHOR_LEN:
            return False, "Author name is too long : it should be at maximum 500 characters."

        keywords_list = keywords.split(KEYWORDS_SEPARATOR)
        if len(keywords_list) > MAX_KEYWORDS_NB:
            return False, "Too much keywords : please specify maximum 10 keywords."
        for k in keywords_list:
            if len(k) > MAX_KEYWORD_LEN:
                return False, "Keyword is too long : it should be at maximum 500 characters."

        # Remove duplicata of keywords list
        keywords_list = list(set(keywords_list))

        # Check if poem is already in database
        exist_already = self.session.query(self.Poem).filter_by(poem=poem).first()
        if exist_already:
            return False, "This poem already exists in the database."

        # Finally submit !
        self.session.add(self.Poem(poem=poem, author=author, \
                         keywords=KEYWORDS_SEPARATOR.join(keywords_list)))
        self.session.commit()
        return True, "Poem successfully submitted ! Thank you for sharing :)"

    def get_poems_by_best(self):
        """ Function to retrieve Poems classified by stars.

        Return:
            list of Poem: List of poems, ordered based on their stars
        """
        return self.session.query(self.Poem).order_by(self.db.desc(self.Poem.stars)).all()

    def get_poems_by_latest(self):
        """ Function to retrieve Poems classified by their creating date.

        Return:
            list of Poem: List of poems, ordered based on their creating date.
        """
        return self.session.query(self.Poem).order_by(self.db.desc(self.Poem.time_created)).all()

    def get_2_rand_poems(self):
        """ Retrieve 2 random poems
        
        Return:
            Poem: First retrieved poem.
            Poem: Second retrieved poem.
        """
        all_poems = self.session.query(self.Poem).all()

        if len(all_poems) < 2:
            return None, None

        poems = random.sample(all_poems, 2)
        return poems[0], poems[1]

    def star(self, poem_id):
        """ Star a poem

        This function add +1 star to the designated poem.

        Args:
            poem_id (int): ID of the poem to star.
        """
        p = self.session.query(self.Poem).filter_by(id=poem_id).first()
        p.stars += 1
        self.session.add(p)
        self.session.commit()

    def report(self, poem_id):
        """ Report a poem

        This function add +1 flag to the designated poem.

        Args:
            poem_id (int): ID of the poem to report.
        """
        p = self.session.query(self.Poem).filter_by(id=poem_id).first()
        p.flags += 1
        self.session.add(p)
        self.session.commit()
