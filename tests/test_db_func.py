import pytest
import datetime

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
    assert poem.stars == stars
    assert poem.flags == flags

    # Since keywords order can be modified, it's not trivial to check it
    db_kw = poem.keywords.split(',')
    kw = keywords.split(',')
    for k in db_kw:
        assert k in kw
    for k in kw:
        assert k in db_kw

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

        assert len(poems) == 0
        
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

    def test_submit_too_small_poem(self, db_func):
        poem_content = "x"
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

class TestSearch:
    def test_search_best(self, db_func):
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

        poems = db_func.search()

        assert len(poems) == 10
        assert poems[0].poem == "5" and poems[0].stars == 12
        assert poems[1].poem == "7" and poems[1].stars == 5
        assert poems[2].poem == "3" and poems[2].stars == 1
        for p in poems[3:]:
            assert p.stars == 0

    def test_search_latest(self, db_func):
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords", time_created=datetime.datetime.now() - datetime.timedelta(seconds=10 - i)))
            db_func.session.commit()      # Need to commit everytime to be sure we have different dates

        poems = db_func.search('Latest')

        assert len(poems) == 10
        for i, p in enumerate(poems):
            assert p.poem == "{}".format(10 - 1 - i)

    def test_retrieve_2_random(self, db_func):
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poem1, poem2 = db_func.get_2_rand_poems()

        assert poem1.poem in ["{}".format(j) for j in range(10)]
        assert poem2.poem in ["{}".format(j) for j in range(10)]
        assert poem1.poem != poem2.poem

    def test_retrieve_2_random_not_enough(self, db_func):
        db_func.session.add(db_func.Poem(poem="test", author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poem1, poem2 = db_func.get_2_rand_poems()

        assert poem1 is None
        assert poem2 is None

    def test_search_content_exact_match(self, db_func):
        content = "Test Exact Match"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem=content, author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(content=content)

        assert len(poems) == 1
        assert poems[0].poem == content

    def test_search_content_exact_match_caps(self, db_func):
        content = "TEST Exact MATCH"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem=content, author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(content=content.lower())

        assert len(poems) == 1
        assert poems[0].poem == content

    def test_search_2content(self, db_func):
        content = "Test Exact Match"
        content2 = "Test Exact Match Double"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem=content, author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem=content2, author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(content=content)

        assert len(poems) == 2
        assert poems[0].poem == content
        assert poems[1].poem == content2

    def test_search_content_start_with(self, db_func):
        content = "Test Exact Match"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem=content, author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(content=content.split()[0])

        assert len(poems) == 1
        assert poems[0].poem == content

    def test_search_content_end_with(self, db_func):
        content = "Test Exact Match"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem=content, author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(content=content.split()[-1])

        assert len(poems) == 1
        assert poems[0].poem == content

    def test_search_content_middle(self, db_func):
        content = "Test Exact Match"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem=content, author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(content=content.split()[1])

        assert len(poems) == 1
        assert poems[0].poem == content

    def test_search_content_separated(self, db_func):
        content = "Test Exact Match"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem=content, author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(content=content.split()[0] + " " + content.split()[-1])

        assert len(poems) == 1
        assert poems[0].poem == content

    def test_search_author_exact_match(self, db_func):
        author = "Test Exact Match"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author=author, keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(author=author)

        assert len(poems) == 1
        assert poems[0].author == author

    def test_search_author_exact_match_caps(self, db_func):
        author = "TEST Exact MATCH"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author=author, keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(author=author.lower())

        assert len(poems) == 1
        assert poems[0].poem == content

    def test_search_2author(self, db_func):
        author = "Test Exact Match"
        author2 = "Test Exact Match Double"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author=author, keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content2", author=author2, keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(author=author)

        assert len(poems) == 2
        assert poems[0].author == author
        assert poems[1].author == author2

    def test_search_author_start_with(self, db_func):
        author = "Test Exact Match"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author=author, keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(author=author.split()[0])

        assert len(poems) == 1
        assert poems[0].author == author

    def test_search_author_end_with(self, db_func):
        author = "Test Exact Match"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author=author, keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(author=author.split()[-1])

        assert len(poems) == 1
        assert poems[0].author == author

    def test_search_author_middle(self, db_func):
        author = "Test Exact Match"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author=author, keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(author=author.split()[1])

        assert len(poems) == 1
        assert poems[0].author == author

    def test_search_author_separated(self, db_func):
        author = "Test Exact Match"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author=author, keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(author=author.split()[0] + " " + author.split()[-1])

        assert len(poems) == 1
        assert poems[0].author == author

    def test_search_keyword_exact_match(self, db_func):
        keyword = "Test"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords=keyword))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(keywords=keyword)

        assert len(poems) == 1
        assert poems[0].poem == "content"

    def test_search_keyword_exact_match(self, db_func):
        keyword = "TeST"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords=keyword))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(keywords=keyword.lower())

        assert len(poems) == 1
        assert poems[0].poem == "content"

    def test_search_keyword_among_several(self, db_func):
        keyword = "Test,Exact,Lol"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords=keyword))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(keywords=keyword.split(',')[0])

        assert len(poems) == 1
        assert poems[0].poem == "content"

    def test_search_2keyword(self, db_func):
        keyword = "Test,Exact,Lol"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords=keyword))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(keywords=keyword.split(',')[0] + ',' + keyword.split(',')[-1])

        assert len(poems) == 1
        assert poems[0].poem == "content"

    def test_search_2keyword_no_single(self, db_func):
        keyword = "Test,Exact,Lol"
        keyword_part1 = "Test,Exact"
        keyword_part2 = "Exact,Lol"
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords=keyword))
        db_func.session.add(db_func.Poem(poem="content1", author="author", keywords=keyword_part1))
        db_func.session.add(db_func.Poem(poem="content2", author="author", keywords=keyword_part2))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(keywords=keyword.split(',')[0] + ',' + keyword.split(',')[-1])

        assert len(poems) == 1
        assert poems[0].poem == "content"

    def test_search_2keywords_double(self, db_func):
        keyword = "Test,Exact,Lol"
        keyword2 = "Test,Exact,Lol,Double"
        for i in range(10):
            db_func.session.add(db_func.Poem(poem="{}".format(i), author="author", keywords="keywords"))
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords=keyword))
        db_func.session.add(db_func.Poem(poem="content2", author="author", keywords=keyword2))
        db_func.session.commit()        # Populate DB

        poems = db_func.search(keywords=keyword)

        assert len(poems) == 2
        assert poems[0].poem == "content"
        assert poems[1].poem == "content2"

class TestUpdate:
    def test_star_update(self, db_func):
        db_func.session.add(db_func.Poem(poem="content", author="author", keywords="keywords"))
        db_func.session.commit()        # Populate DB

        poem = db_func.session.query(db_func.Poem).all()[0]
        assert poem.stars == 0

        db_func.star(1)

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
            db_func.star(1)

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

        db_func.report(1)

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
            db_func.report(1)

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