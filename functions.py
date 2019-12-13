import random

from translations import get_error_msg

MIN_CONTENT_LEN = 3
MAX_CONTENT_LEN = 5000
MAX_AUTHOR_LEN = 500
MAX_KEYWORD_LEN = 500
KEYWORDS_SEPARATOR = ','
MAX_KEYWORDS_NB = 10
SEARCH_BY_BEST = "Best"
SEARCH_BY_LATEST = "Latest"
LANG_EN = "EN"
LANG_FR = "FR"


class DbFunc(object):
    """
    The `DbFunc` class is a class defining the back-end functions. These
    back-end mostly interact with the database. Back-end functions are
    encapsulated in this class for easy access to the database and the tables,
    so there is no need to pass a new session object to every single back-end
    function call.

    Attributes:
        db (SQLAlchemy): Database object.
        session (Session): Session to use, from the Database object.
        Poem (Table): Main (and only) table of the Database, containing all
            poems.
    """

    def __init__(self, db, tables):
        """ Constructor """
        self.db = db
        self.session = db.session
        self.Poem = tables[0]

    def submit_poem(self, poem, author=None, keywords=None, lang=LANG_EN):
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
        Poem is submitted in a certain language.

        Args:
            poem (str): The content of the poem.
            author (str, optional): Name of the author.
            keywords (str, optional): Keywords of the poem.
            lang (str, optional): Language of the poem.

        Return:
            bool: True if the poem was successfully added to the database. False
                otherwise.
            str: Error / Success message to display to the user.
        """
        if lang.upper() not in [LANG_EN, LANG_FR]:
            return False, "Language not supported yet. Please choose language among : {}".format([LANG_EN, LANG_FR])
        error_msg = get_error_msg(lang)
        # Checking length
        if poem == "":
            return False, error_msg[0]
        elif len(poem) < MIN_CONTENT_LEN:
            return False, error_msg[1]
        elif len(poem) > MAX_CONTENT_LEN:
            return False, error_msg[2]

        author = author or ""
        keywords = keywords or ""

        if len(author) > MAX_AUTHOR_LEN:
            return False, error_msg[3]

        keywords_list = keywords.split(KEYWORDS_SEPARATOR)
        if len(keywords_list) > MAX_KEYWORDS_NB:
            return False, error_msg[4]
        for k in keywords_list:
            if len(k) > MAX_KEYWORD_LEN:
                return False, error_msg[5]

        # Remove duplicata of keywords list
        keywords_list = list(set(keywords_list))

        # Check if poem is already in database
        exist_already = self.session.query(self.Poem).filter_by(poem=poem).first()
        if exist_already:
            return False, error_msg[6]

        # Finally submit !
        self.session.add(self.Poem(poem=poem, author=author,
                         keywords=KEYWORDS_SEPARATOR.join(keywords_list),
                         lang=lang.lower()))
        self.session.commit()
        return True, error_msg[7]

    def search(self, search_by=SEARCH_BY_BEST, content="", author="",
               keywords="", lang=LANG_EN):
        """ Search function

        This method allow to search a haiku in the database. The search can be
        done by `best` or `latest`. User can specify a string corresponding to
        the content of the haiku, or a string corresponding to the author name,
        or a string for keywords.

        Args:
            search_by (str, optional): `best` or `latest`. Best retrieve the
                haiku with more stars first, latest retrieve the haiku with the
                latest submit date.
            content (str, optional): String to match the content of the haiku.
            author (str, optional): String to match the author of the haiku.
            keywords (str, optional): String, comma-separated, to match the
                keywords of the haiku. Should match exactly.
            lang (str, optional): Language of the poem to search.

        Return:
            list of Poem: List of poems, based on the search arguments.
        """
        query = self.session.query(self.Poem)

        # Do the search by level, given search queries
        if search_by == SEARCH_BY_BEST:
            query = query.order_by(self.db.desc(self.Poem.stars))
        elif search_by == SEARCH_BY_LATEST:
            query = query.order_by(self.db.desc(self.Poem.time_created))
        else:
            raise ValueError("Unknown way to search the database : {}.".format(search_by))

        if content:
            query = query.filter(self.Poem.poem.contains(content))
        if author:
            query = query.filter(self.Poem.author.contains(author))
        if keywords:
            for k in keywords.split(KEYWORDS_SEPARATOR):
                query = query.filter(self.Poem.keywords.contains(k))
        query = query.filter(self.Poem.lang == lang.lower())

        return query.all()

    def get_2_rand_poems(self, lang=LANG_EN):
        """ Retrieve 2 random poems

        Args:
            lang (str, optional): Language of the poem to search.

        Return:
            Poem: First retrieved poem.
            Poem: Second retrieved poem.
        """
        all_poems = self.session.query(self.Poem).filter(self.Poem.lang == lang.lower()).all()

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
