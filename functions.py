import random

def submit_poem(sess, Poem, poem, author=None, keywords=None):
    # Ensure poem is not an empty string
    if poem == "":
        return "Poem cannot be empty !"

    # TODO : Also have to check if poem is already submitted
    author = author or "Unknown"      # TODO : to translate
    keywords = keywords or " "      # TODO : remove duplicata

    print(poem, author, keywords)
    sess.add(Poem(poem=poem, author=author, keywords=keywords))
    sess.commit()
    return "Poem successfully submitted ! Thank you for sharing :)"

def get_poems_by_best(sess, Poem):
    return sess.query(Poem).order_by(Poem.stars).all()

def get_2_rand_poems(sess, Poem):
    poems = random.choices(sess.query(Poem).all(), k=2)
    return poems[0], poems[1]

def best_of_2(sess, Poem, poem):
    poem.stars += 1
    sess.add(poem)
    sess.commit()

def report(sess, Poem, poem):
    poem.flags += 1     # Later : add automatically remove of poem after X report ?
    sess.add(poem)
    sess.commit()
