import streamlit as st
from st_utils import SessionState

LANGUAGES = ["FR", "EN"]
MENU_HOME =     "⠀⠀⠀⠀⠀⠀⠀⠀Home⠀⠀⠀⠀⠀⠀⠀⠀"
MENU_EXPLORE =  "⠀⠀⠀⠀⠀⠀⠀⠀Explore⠀⠀⠀⠀⠀⠀⠀"
MENU_JUDGE =    "⠀⠀⠀⠀⠀⠀⠀⠀Judge⠀⠀⠀⠀⠀⠀⠀⠀"
MENU_SUBMIT =   "⠀⠀⠀⠀⠀⠀⠀⠀Submit⠀⠀⠀⠀⠀⠀⠀"
MENU = [MENU_HOME, MENU_SUBMIT, MENU_JUDGE, MENU_EXPLORE]

def navigation_menu():
    lang = st.sidebar.selectbox("Language", LANGUAGES)
    st.sidebar.markdown("")
    buttons = []
    for m in MENU:
        buttons.append(st.sidebar.button(m))
    choice = [i for i, b in enumerate(buttons) if b]
    assert len(choice) <= 1
    if len(choice) == 0:
        return lang, None
    else:
        return lang, MENU[choice[0]]

def welcome():
    st.markdown("Welcome to **Jilano** !")
    st.markdown("The goal of this web app is to reference shorts poems, known as _haiku_.")
    st.markdown("A haiku is usually a **17-syllables poem**, divided in **3 lines** and following the **5-7-5 pattern** : 5 syllables for the first line, 7 for the second and 5 for the last one.")
    st.markdown("Haiku traditionally focus on **nature / seasons**, with a **contemplative tone**, with **non-rhyming lines**.")
    st.markdown("---")
    st.markdown("However, the goal of this site is not to limit your creativity. Even if your haiku does not exactly respect those rules, submit it ! We'd love to hear about your poem.")
    st.markdown("---")
    st.markdown("Content of this website :")
    st.markdown("* **Home** : This page.")
    st.markdown("* **Submit** : Where you can submit your own poem. Your poem will be saved in the database and other users will be able to see it.")
    st.markdown("* **Judge** : Where you can help us finding the best poems ! 2 poems will be displayed to you, and you can choose the one you prefer.")
    st.markdown("* **Explore** : Read the best poems, or search poems by keyword(s).")

def submit():
    poem = st.text_area("Enter your poem here :")
    author = st.text_input("Author's name :")
    keywords = st.text_input("Keywords (separated by space) :")

    if st.button("Submit"):
        st.markdown(poem)
        st.markdown("_By {}_".format(author))
        st.write(keywords.split())

def explore():
    # TODO : add possibility to star peom here ?
    exploration_method = st.selectbox("What do you want to explore :", ["Best", "Search by keywords", "Search by author"])
    if exploration_method == "Best":
        # Retrieve bests
        poems = ["poem 1", "poem 2", "poem 3"]
    elif exploration_method == "Search by keywords":
        keywords = st.text_input("Search keywords (separated by space) :")
        # Retrieve poems
        poems = ["kpoem 1 : {}".format(keywords), "kpoem 2", "kpoem 3"]
    elif exploration_method == "Search by author":
        author = st.text_input("Author :")
        # Retrieve poems
        poems = ["kpoem 1 : {}".format(author), "kpoem 2", "kpoem 3"]

    # Display poems TODO : pagination
    for poem in poems:
        st.markdown("---")
        st.markdown(poem)

def judge():
    # TODO : add possibility to compare certain type of poem : newest, best, etc..
    # Retrieve 2 random poem
    poem1 = "poem 1"
    poem2 = "poem 2"

    st.markdown("Compare these 2 poems and choose the one you prefer :")
    skip = st.button("Skip")
    st.markdown("---")
    st.markdown(poem1)
    p1 = st.button("I prefer this one")
    r1 = st.button("Report")
    st.markdown("---")
    st.markdown(poem2)
    p2 = st.button("I prefer this one", key="2")
    r2 = st.button("Report", key="2")

    if skip:
        st.write("Skipped")
    elif p1:
        st.write("You prefered the first one")
    elif p2:
        st.write("You prefered the second one")
    elif r1:
        st.write("You reported the first one")
    elif r2:
        st.write("You reported the second one")

def main():
    state = SessionState.get(page=MENU_HOME)

    lang, page = navigation_menu()
    if page:
        state.page = page

    if state.page == MENU_HOME:
        welcome()
    elif state.page == MENU_SUBMIT:
        submit()
    elif state.page == MENU_EXPLORE:
        explore()
    elif state.page == MENU_JUDGE:
        judge()

if __name__ == "__main__":
    main()