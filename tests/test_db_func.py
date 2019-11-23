import pytest

@pytest.fixture
def db_func():
    import dash

    from functions import DbFunc
    from db import define_db

    app = dash.Dash(__name__)   # Mocking dash app
    db, tables = define_db(app.server, in_mem=True)
    return DbFunc(db, tables)

@pytest.fixture(autouse=True)
def empty_db(db_func):
    meta = db_func.db.metadata
    for table in reversed(meta.sorted_tables):
        db_func.session.execute(table.delete())
    db_func.session.commit()

def assert_poem_is(poem, content, author, keywords, stars, flags):
    assert poem.poem == content
    assert poem.author == author
    assert poem.keywords == keywords
    assert poem.stars == stars
    assert poem.flags == flags

class TestSubmit:
    def test_basic_submit(self, db_func):
        poem_content = "This is a test poem"
        poem_author = "test author"
        poem_keywords = "test keyword 1,test keyword 2"

        db_func.submit_poem(poem_content, poem_author, poem_keywords)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 1
        assert_poem_is(poems[0], poem_content, poem_author, poem_keywords, 0, 0)

    def test_submit_no_keywords(self, db_func):
        poem_content = "This is a test poem"
        poem_author = "test author"

        db_func.submit_poem(poem_content, poem_author)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 1
        assert_poem_is(poems[0], poem_content, poem_author, "", 0, 0)

    def test_submit_no_author(self, db_func):
        poem_content = "This is a test poem"
        poem_keywords = "test keyword 1,test keyword 2"

        db_func.submit_poem(poem_content, keywords=poem_keywords)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 1
        assert_poem_is(poems[0], poem_content, "", poem_keywords, 0, 0)
    
    def test_submit_only_poem(self, db_func):
        poem_content = "This is a test poem"

        db_func.submit_poem(poem_content)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 1
        assert_poem_is(poems[0], poem_content, "", "", 0, 0)

    def test_submit_2_poems(self, db_func):
        poem_content1 = "This is a first test poem"
        poem_content2 = "This is a second test poem"

        db_func.submit_poem(poem_content1)
        db_func.submit_poem(poem_content2)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 2
        assert_poem_is(poems[0], poem_content1, "", "", 0, 0)
        assert_poem_is(poems[1], poem_content2, "", "", 0, 0)

    def test_submit_duplicata(self, db_func):
        poem_content1 = "This is a test poem"
        poem_content2 = "This is a test poem"

        db_func.submit_poem(poem_content1)
        db_func.submit_poem(poem_content2)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 1
        assert_poem_is(poems[0], poem_content1, "", "", 0, 0)

    def test_submit_empty(self, db_func):
        poem_content = ""

        db_func.submit_poem(poem_content)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 0

    def test_submit_duplicate_keywords(self, db_func):
        poem_content = "This is a test poem"
        poem_author = "test author"
        poem_keywords = "test,test"

        db_func.submit_poem(poem_content, poem_author, poem_keywords)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 1
        assert_poem_is(poems[0], poem_content, poem_author, "test", 0, 0)

    def test_submit_more_than_10_keywords(self, db_func):
        poem_content = "This is a test poem"
        poem_author = "test author"
        poem_keywords = "test1,test2,test3,test4,test5,test6,test7,test8,test9,test10,test11"

        db_func.submit_poem(poem_content, poem_author, poem_keywords)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 1
        assert_poem_is(poems[0], poem_content, poem_author, "test1,test2,test3,test4,test5,test6,test7,test8,test9,test10", 0, 0)

    def test_submit_too_big_author(self, db_func):
        poem_content = "This is a test poem"
        poem_author = "x" * 501
        poem_keywords = "test keyword 1,test keyword 2"

        db_func.submit_poem(poem_content, poem_author, poem_keywords)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 0

    def test_submit_too_big_poem(self, db_func):
        poem_content = "x" * 5001
        poem_author = "test author"
        poem_keywords = "test keyword 1,test keyword 2"

        db_func.submit_poem(poem_content, poem_author, poem_keywords)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 0
    
    def test_submit_too_big_keyword(self, db_func):
        poem_content = "This is a test poem"
        poem_author = "test author"
        poem_keywords = "x" * 501

        db_func.submit_poem(poem_content, poem_author, poem_keywords)
        poems = db_func.session.query(db_func.Poem).all()

        assert len(poems) == 0

class TestRetrieve:
    def test_order_retrieve_best(self, db_func):
        for i in range(10):
            stars = 0
            if i == 3:
                stars = 1
            elif i == 5:
                stars = 12
            elif i == 7:
                stars = 5
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords", stars=stars))
        db_func.session.commit()        # Populate DB

        poems = db_func.get_poems_by_best()

        assert len(poems) == 10
        assert poems[0].poem == "5" and poems[0].stars == 12
        assert poems[1].poem == "7" and poems[1].stars == 5
        assert poems[2].poem == "3" and poems[2].stars == 1
        for p in poems[3:]:
            assert p.stars == 0

    def test_retrieve_latest(self, db_func):
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
            db_func.session.commit()      # Need to commit everytime to be sure we have different dates

        poems = db_func.get_poems_by_latest()

        assert len(poems) == 10
        for i, p in enumerate(poems):
            assert p.poem == "{}".format(10 - i)

    def test_retrieve_2_random(self, db_func):
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poem1, poem2 = db_func.get_2_rand_poems()

        assert poem1.poem in ["{}".format(j) for j in range(10)]
        assert poem2.poem in ["{}".format(j) for j in range(10)]
        assert poem1.poem != poem2.poem

class TestUpdate:
    def test_star_update(self, db_func):
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poem = db_func.session.query(db_func.Poem).all()[0]
        assert poem.stars == 0

        db_func.star(0)

        poem = db_func.session.query(db_func.Poem).all()[0]
        assert poem.stars == 1

    def test_star_update_among_others(self, db_func):
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            assert p.stars == 0

        db_func.star(5)

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            if p.id == 5:
                assert p.stars == 1
            else:
                assert p.stars == 0

    def test_star_10update(self, db_func):
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poem = db_func.session.query(db_func.Poem).all()[0]
        assert poem.stars == 0

        for _ in range(10):
            db_func.star(0)

        poem = db_func.session.query(db_func.Poem).all()[0]
        assert poem.stars == 10

    def test_star_10update_among_others(self, db_func):
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            assert p.stars == 0

        for _ in range(10):
            db_func.star(5)

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            if p.id == 5:
                assert p.stars == 10
            else:
                assert p.stars == 0

    def test_star_update_several(self, db_func):
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            assert p.stars == 0

        for _ in range(5):
            db_func.star(4)
        for _ in range(3):
            db_func.star(2)
        for _ in range(5):
            db_func.star(4)
        db_func.star(9)

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            if p.id == 4:
                assert p.stars == 10
            elif p.id == 2:
                assert p.stars == 3
            elif p.id == 9:
                assert p.stars == 1
            else:
                assert p.stars == 0

    def test_report_update(self, db_func):
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poem = db_func.session.query(db_func.Poem).all()[0]
        assert poem.flags == 0

        db_func.report(0)

        poem = db_func.session.query(db_func.Poem).all()[0]
        assert poem.flags == 1

    def test_report_update_among_others(self, db_func):
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            assert p.flags == 0

        db_func.report(5)

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            if p.id == 5:
                assert p.flags == 1
            else:
                assert p.flags == 0

    def test_report_10update(self, db_func):
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poem = db_func.session.query(db_func.Poem).all()[0]
        assert poem.flags == 0

        for _ in range(10):
            db_func.report(0)

        poem = db_func.session.query(db_func.Poem).all()[0]
        assert poem.flags == 10

    def test_report_10update_among_others(self, db_func):
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            assert p.flags == 0

        for _ in range(10):
            db_func.report(5)

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            if p.id == 5:
                assert p.flags == 10
            else:
                assert p.flags == 0

    def test_report_update_several(self, db_func):
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            assert p.flags == 0

        for _ in range(5):
            db_func.report(4)
        for _ in range(3):
            db_func.report(2)
        for _ in range(5):
            db_func.report(4)
        db_func.report(9)

        poems = db_func.session.query(db_func.Poem).all()
        for p in poems:
            if p.id == 4:
                assert p.flags == 10
            elif p.id == 2:
                assert p.flags == 3
            elif p.id == 9:
                assert p.flags == 1
            else:
                assert p.flags == 0