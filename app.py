import streamlit as st
from st_utils import SessionState

LANGUAGES = ["FR", "EN"]
MENU_HOME = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Home⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"
MENU_EXPLORE = "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Explore"
MENU_JUDGE = "Judge"
MENU = [MENU_HOME, MENU_JUDGE, MENU_EXPLORE]

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

def main():
    state = SessionState.get(page=MENU_HOME)

    lang, page = navigation_menu()
    if page:
        state.page = page

    if state.page == MENU_HOME:
        st.write("Yo home")
    elif state.page == MENU_EXPLORE:
        st.write("Exploration de mon cul")
    elif state.page == MENU_JUDGE:
        st.write("Marteau !")

    st.button("Update")

if __name__ == "__main__":
    main()