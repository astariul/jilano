import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os

from functions import DbFunc, LANG_EN, LANG_FR
from db import define_db
from layout import base_index_string, dash_layout
from translations import get_content, get_dropdown_content

MAX_POEM_PER_PAGE = 50
URL_LANG_FR = "?lang=fr"

print(dcc.__version__)  # 0.6.0 or above is required

app = dash.Dash(__name__)

# Use in-mem database if we are in debug mode
db, tables = define_db(app.server, in_mem=__debug__)
db_func = DbFunc(db, tables)

app.index_string = base_index_string

app.layout = dash_layout


@app.callback(
    [Output('validateSubmitHaikuMsg', 'children'),
     Output('submissionHaiku', 'value'),
     Output('submissionAuthor', 'value'),
     Output('submissionKeywords', 'value')],
    [Input('submitHaikuButton', 'n_clicks')],
    [State('submissionHaiku', 'value'),
     State('submissionAuthor', 'value'),
     State('submissionKeywords', 'value'),
     State('lang-dropdown', 'value')]
)
def validate_submit(n1, haiku, author, keywords, lang):
    """
    Method ran when the user submit a haiku by clicking the submit button.
    It checks the inputs and add it to database if no error is found.
    Fields are updated (not changed if there was an error, reinitialized if
    submission was successful), and displayed message is set.
    """
    if n1 is None:
        # Site loading
        return "", "", "", ""

    # Here, put the submission code that verify if the poem can be submitted
    is_valid, msg = db_func.submit_poem(haiku, author, keywords, lang or LANG_EN)

    if is_valid:
        # reset the input form
        haiku = ""
        author = ""
        keywords = ""

    return msg, haiku, author, keywords


@app.callback(
    Output('placeForSearchedHaiku', 'children'),
    [Input('searchHaikuButton', 'n_clicks')],
    [State('searchByDrop', 'value'),
     State('searchHaiku', 'value'),
     State('searchAuthor', 'value'),
     State('searchKeywords', 'value'),
     State('lang-dropdown', 'value')]
)
def search_submit(n1, search_by, content, author, keywords, lang):
    """
    Method ran when the user search by clicking the search button.
    It search haikus based on the search fields, and return formatted haikus
    found (corresponding to the search fields).
    """
    if n1 is None:
        # Site loading
        return []

    def haiku(poem, author="Unknown", keywords=None, stars=0):
        if keywords is None:
            keywords = []
        clean_keywords = []
        for k in keywords:
            if k.strip() != "":
                clean_keywords.append(k)
        poem_lines = poem.split("\n")
        return html.Div(className="text-left", children=[
            html.Div(className="portfolio-item mx-auto", children=[
                *[html.P(p, className="text-haiku") for p in poem_lines],
                html.P("― " + author, className="author-name"),
                html.Button("{} ⭐".format(stars), type="button", disabled=True, className="btn btn-tertiary mr-2"),
                *[html.Button(k, type="button", disabled=True, className="btn btn-primary mr-2") for k in clean_keywords]
            ])
        ])
        return html.Div(className="align-items-center", children=[
            html.Div(className="mx-auto", children=[
                *[html.P(p, className="text-haiku") for p in poem_lines],
                html.P("― " + author, className="author-name"),
                html.Button("{} ⭐".format(stars), type="button", disabled=True, className="btn btn-tertiary mr-2"),
                *[html.Button(k, type="button", disabled=True, className="btn btn-primary mr-2") for k in clean_keywords]
            ])
        ])
    divider = html.Div(className="divider-custom divider-primary mb-4 mt-5", children=[
                html.Div(className="divider-custom-line"),
                html.Div(className="divider-custom-icon divider-light", children=[
                    html.I(className="fas fa-star")
                ]),
                html.Div(className="divider-custom-line divider-light"),
            ])
    info_more_poem = html.P("Only the first {} haikus are displayed. Please precise your search if you couldn't find what you "
                            "want.".format(MAX_POEM_PER_PAGE))

    # Search
    all_poems = db_func.search(search_by, content, author, keywords, lang or LANG_EN)

    # No pagination yet
    poems = all_poems[:MAX_POEM_PER_PAGE]

    # Create the display of haikus
    childrens = []
    for p in poems:
        childrens.append(haiku(p.poem, p.author or "Unknown", p.keywords.split(','), p.stars))

    divided_children = []
    for c in childrens:
        divided_children.append(c)
        divided_children.append(divider)
    if len(all_poems) > MAX_POEM_PER_PAGE:
        divided_children.append(info_more_poem)
    elif len(divided_children) != 0:
        del divided_children[-1]    # Remove last divider
    return divided_children


@app.callback(
    [Output('placeholderHaiku1', 'children'), Output('placeholderHaiku2', 'children'),
     Output('pid1', 'data'), Output('pid2', 'data')],
    [Input('skipButton', 'n_clicks'),
     Input('pid1', 'clear_data'), Input('pid2', 'clear_data'),
     Input('closeValidateSubmitHaiku', 'n_clicks')],
    [State('lang-dropdown', 'value')]
)
def skip(n, n1, n2, n3, lang):
    """
    Method ran to update the 2 haikus displayed in the judge page.
    When 2 haikus are displayed in the judge page, it should be updated with
    new haikus when :
    * The skip button is pressed
    * One of the judged haiku was selected
    * User submitted a new haiku
    """
    # Randomly choose 2 haikus
    poem1, poem2 = db_func.get_2_rand_poems(lang or LANG_EN)

    if poem1 is None or poem2 is None:
        return "", "", {}, {}

    def haiku(poem, author="Unknown"):
        poem_lines = poem.split("\n")
        return html.Div(className="", children=[
            html.Div(className="mx-auto", children=[
                *[html.P(p, className="text-haiku") for p in poem_lines],
                html.P("― " + author, className="author-name"),
            ])
        ])
    data1 = {'pid': poem1.id}    # Set PID for the first and second haiku
    data2 = {'pid': poem2.id}
    return haiku(poem1.poem, poem1.author or "Unknown"), haiku(poem2.poem, poem2.author or "Unknown"), data1, data2


@app.callback(
    Output('pid1', 'clear_data'),
    [Input('choose1Button', 'n_clicks')],
    [State('pid1', 'data')]
)
def choose1(n, data):
    """
    Method ran to choose the haiku #1 of the judge page. Haiku #1 is chosen
    when button #1 is pressed.
    """
    if n is not None and data is not None:
        db_func.star(data['pid'])
    return False


@app.callback(
    Output('pid2', 'clear_data'),
    [Input('choose2Button', 'n_clicks')],
    [State('pid2', 'data')]
)
def choose2(n, data):
    """
    Method ran to choose the haiku #2 of the judge page. Haiku #2 is chosen
    when button #2 is pressed.
    """
    if n is not None and data is not None:
        db_func.star(data['pid'])
    return False


@app.callback(
    Output('reportPid', 'data'),
    [Input('report1Button', 'n_clicks_timestamp'), Input('report2Button', 'n_clicks_timestamp')],
    [State('pid1', 'data'), State('pid2', 'data')]
)
def report(n1, n2, data1, data2):
    """
    Method ran when one haiku is reported (in the judge page).
    It will save the PID of the haiku being reported, either PID of haiku #1 or
    PID of haiku #2.
    """
    if n1 is None and n2 is None:
        return None
    elif n2 is None:
        return data1
    elif n1 is None:
        return data2
    elif n1 > n2:
        return data1
    else:
        return data2


@app.callback(
    Output('reportPid', 'clear_data'),
    [Input('yesReportHaiku', 'n_clicks')],
    [State('reportPid', 'data')]
)
def reportsure(n, data):
    """
    Method ran when haiku is indeed reported. The haiku is then flagged in
    database.
    """
    if data is not None:
        db_func.report(data['pid'])
    return True


@app.callback(
    Output('url', 'search'),
    [Input('lang-dropdown', 'value')],
    [State('url', 'search')]
)
def update_lang(lang, search):
    """
    Language dropdown update the search bar to add the language in the URL.
    """
    if lang is None:
        return search
    if lang == LANG_FR:
        return URL_LANG_FR
    else:
        return ""


@app.callback(
    Output('lang-dropdown', 'placeholder'),
    [Input('url', 'search')]
)
def update_dropdown(search):
    """
    If the search bar contain language information, the language dropdown is
    updated with this information.
    """
    if search == URL_LANG_FR:
        return LANG_FR
    else:
        return LANG_EN


def toggle_modal(n1, n2, is_open):
    """
    Generic function used to toggle any given modal.
    """
    if n1 or n2:
        return not is_open
    return is_open


app.callback(
    Output('modal-haiku-submit-success', 'is_open'),
    [Input('submitHaikuButton', 'n_clicks'), Input('closeValidateSubmitHaiku', 'n_clicks')],
    [State('modal-haiku-submit-success', 'is_open')]
)(toggle_modal)


app.callback(
    Output('modal-haiku-report-success', 'is_open'),
    [Input('yesReportHaiku', 'n_clicks'), Input('closeReportSuccessHaiku', 'n_clicks')],
    [State('modal-haiku-report-success', 'is_open')]
)(toggle_modal)


@app.callback(
    Output('modal-haiku-report', 'is_open'),
    [Input('report1Button', 'n_clicks'), Input('report2Button', 'n_clicks'), Input('yesReportHaiku', 'n_clicks'),
     Input('noReportHaiku', 'n_clicks')],
    [State('modal-haiku-report', 'is_open')]
)
def multi_toggle_modal(n1, n2, n3, n4, is_open):
    """
    Similar to `toggle_modal()`, but here several buttons can toggle the modal.
    """
    if n1 or n2 or n3 or n4:
        return not is_open
    return is_open


@app.callback(
    [Output('website-title', 'children'), Output('explore-menu', 'children'),
     Output('submit-menu', 'children'), Output('judge-menu', 'children'),
     Output('welcomessage', 'children'), Output('whatthissite', 'children'),
     Output('whatsahaiku', 'children'), Output('forexample', 'children'),
     Output('exampleline1', 'children'), Output('exampleline2', 'children'),
     Output('exampleline3', 'children'), Output('exampleauthor', 'children'),
     Output('explainhaiku1', 'children'), Output('explainhaiku2', 'children'),
     Output('explainhaiku3', 'children'), Output('explainhaiku4', 'children'),
     Output('explainhaiku5', 'children'), Output('inthiswebsite1', 'children'),
     Output('inthiswebsite2', 'children'), Output('inthiswebsite3', 'children'),
     Output('footerquestion', 'children'), Output('getintouch', 'children'),
     Output('titleexplore', 'children'), Output('explorelabel1', 'children'),
     Output('explorelabel2', 'children'), Output('explorelabel3', 'children'),
     Output('explorelabel4', 'children'), Output('searchHaikuButton', 'children'),
     Output('submittitle', 'children'), Output('submissionHaiku', 'placeholder'),
     Output('submitlabel1', 'children'), Output('submissionAuthor', 'placeholder'),
     Output('submitlabel2', 'children'), Output('submissionKeywords', 'placeholder'),
     Output('submitHaikuButton', 'children'), Output('closeValidateSubmitHaiku', 'children'),
     Output('judgetitle', 'children'), Output('choose1Button', 'children'),
     Output('report1Button', 'children'), Output('choose2Button', 'children'),
     Output('report2Button', 'children'), Output('skipButton', 'children'),
     Output('reportsurebody', 'children'), Output('yesReportHaiku', 'children'),
     Output('noReportHaiku', 'children'), Output('reportvalidbody', 'children'),
     Output('closeReportSuccessHaiku', 'children')],
    [Input('url', 'search')],
)
def translate(search):
    """
    Main translation function. It reads the first X lines of the translation
    file, and associate each of these lines to a component of the page when
    text appear.
    """
    lang = LANG_FR if search == URL_LANG_FR else LANG_EN
    content = get_content(lang)
    return tuple(content)


@app.callback(
    [Output('searchByDrop', 'value'), Output('searchByDrop', 'options')],
    [Input('url', 'search')],
)
def translate_dropdown(search):
    """
    Translation function specific to dropdown. It reads specific lines of the
    translation file, and associate each of these lines to a list of possible
    value for the dropdown component.
    We need to separate the static content of the website and the dropdown into
    2 callbacks because of how the dropdown content is updated.
    """
    lang = LANG_FR if search == URL_LANG_FR else LANG_EN
    content = get_dropdown_content(lang)
    best = content[0]
    latest = content[1]
    return best, [{'label': best, 'value': best}, {'label': latest, 'value': latest}]


if __name__ == '__main__':
    app.run_server(debug=__debug__, port=os.environ["PORT"])
