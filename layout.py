import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from functions import SEARCH_BY_BEST, SEARCH_BY_LATEST, LANG_EN, LANG_FR

base_index_string = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Jilano</title>

    <!-- Custom fonts for this theme -->
    <link href="assets/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Lato:400,700,400italic,700italic" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Caveat&display=swap" rel="stylesheet" type="text/css">

    <!-- Theme CSS -->
    <link href="assets/css/freelancer.css" rel="stylesheet">

    <!-- Favicon -->
    <link rel="shortcut icon" href="assets/img/logo.png" type="image/x-icon">
    <link rel="icon" href="assets/img/logo.png" type="image/x-icon">

</head>

<body id="page-top">

    {%app_entry%}

    <!-- Bootstrap core JavaScript -->
    <script src="assets/vendor/jquery/jquery.min.js"></script>
    <script src="assets/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Plugin JavaScript -->
    <script src="assets/vendor/jquery-easing/jquery.easing.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/jquery-tagsinput/1.3.6/jquery.tagsinput.min.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-tagsinput/1.3.6/jquery.tagsinput.min.js"></script>

    <script type="text/javascript">
        $('#input-tags').tagsInput();
    </script>

    <!-- Contact Form JavaScript -->
    <script src="assets/js/jqBootstrapValidation.js"></script>

    <!-- Custom scripts for this template -->
    <footer>
        <script src="assets/js/freelancer.js"></script>
    </footer>

    <!-- Footer -->
    <footer class="bg-black small text-c enter text-white-50">
        <div class="container">
            {%config%}
            {%scripts%}
            {%renderer%}
        </div>
    </footer>
</body>

</html>
"""

# Layout
dash_layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Nav(className="navbar navbar-expand-lg bg-secondary text-uppercase fixed-top", id="mainNav", children=[
        html.Div(className="container", children=[
            html.A(className="navbar-brand js-scroll-trigger my-menu", href="#welcome", id="website-title", children="Jilano"),
            html.Button(className="navbar-toggler navbar-toggler-right text-uppercase font-weight-bold bg-primary text-white "
                        "rounded", type="button", **{'data-toggle': "collapse", 'data-target': "#navbarResponsive",
                                                     'aria-controls': "navbarResponsive", 'aria-expanded': "false",
                                                     'aria-label': "Toggle navigation"},
                        children=[
                            "Menu  ",
                            html.I(className="fas fa-bars")
                        ]),
            html.Div(className="collapse navbar-collapse", id="navbarResponsive", children=[
                html.Ul(className="navbar-nav ml-auto", children=[
                    html.Li(className="nav-item mx-0 mx-lg-1", children=[
                        html.A(className="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger my-menu", id="explore-menu",
                               href="#explore", children="Explore")
                    ]),
                    html.Li(className="nav-item mx-0 mx-lg-1", children=[
                        html.A(className="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger my-menu", id="submit-menu",
                               href="#submit", children="Submit")
                    ]),
                    html.Li(className="nav-item mx-0 mx-lg-1", children=[
                        html.A(className="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger my-menu", id="judge-menu",
                               href="#judge", children="Judge")
                    ])
                ])
            ])
        ])
    ]),
    html.Div([
        html.Section(id="welcome", className="page-section my-content", children=[
            html.Div(className="masthead bg-primary text-white text-center", children=[
                html.Div(className="container d-flex align-items-center flex-column", children=[
                    html.Img(className="masthead-avatar mb-5", src="assets/img/logo.png"),
                    html.H1("Welcome to Jilano", className="masthead-heading text-uppercase mb-0", id="welcomessage"),
                    html.Div(className="divider-custom divider-light", children=[
                        html.Div(className="divider-custom-line"),
                        html.Div(className="divider-custom-icon", children=[
                            html.I(className="fas fa-star")
                        ]),
                        html.Div(className="divider-custom-line"),
                    ]),
                    html.P("The goal of this web app is to reference haikus", className="masthead-subheading "
                           "mb-0", id="whatthissite")
                ])
            ]),
            html.Div(className="small-masthead container d-flex align-items-center flex-column", children=[
                html.Div(className="container text-left encadre", children=[
                    html.P("A Haiku is a short poem, traditionally on 3 lines, following a strict pattern.",
                           className="lead font-weight-normal", id="whatsahaiku"),
                    html.P("For example :", className="lead font-weight-normal", id="forexample"),
                    html.Br(),
                ]),
                html.Div(className="col-md-6 col-lg-4", children=[
                    html.Div(className="portfolio-item mx-auto", children=[
                        html.P("The west wind whispered", className="text-haiku", id="exampleline1"),
                        html.P("And touched the eyelids of spring", className="text-haiku", id="exampleline2"),
                        html.P("Her eyes, Primroses", className="text-haiku", id="exampleline3"),
                        html.P("― R. M. Hansard", className="author-name", id="exampleauthor"),
                    ])
                ])
            ]),
            html.Div(className="small-masthead bg-primary text-white text-center", children=[
                html.Div(className="container text-left encadre", children=[
                    html.P("Haikus are originated from Japan. In Japanese, haikus should follow a 3 lines format with a 5-7-5 "
                           "pattern (number of syllables per line).", id="explainhaiku1", className="lead font-weight-normal"),
                    html.P("Such constraints force the poet to be creative expressing himself while respecting the rules.",
                           id="explainhaiku2", className="lead font-weight-normal"),
                    html.Br(),
                    html.P("Haikus usually focus on the nature, and is divided in 2 asymmetrical sections that juxtaposes 2 "
                           "subjects, most of the time unexpectedly similar.", id="explainhaiku3",
                           className="lead font-weight-normal"),
                    html.P("There is no need to make the lines rhyme.", id="explainhaiku4",
                           className="lead font-weight-normal"),
                    html.Br(),
                    html.P("For other languages than Japanese (like English), it's more difficult to keep the format "
                           "constraint. Thus, poets are more free.", id="explainhaiku5", className="lead font-weight-normal")
                ])
            ]),
            html.Div(className="small-masthead container d-flex encadre text-left flex-column", children=[
                html.P("In this website, you can explore haikus submitted by others, and you can submit your own if you wish.",
                       id="inthiswebsite1", className="lead font-weight-normal"),
                html.Br(),
                html.P("We enforce no rules about haiku submission : creativity should have no limit.", id="inthiswebsite2",
                       className="lead font-weight-normal"),
                html.P("However, we would like to keep this website focused on haiku. There is plenty of communities out there"
                       " for other form of poetry !", id="inthiswebsite3", className="lead font-weight-normal"),
            ])
        ]),
        html.Section(id="explore", style={"display": "none"}, className="page-section my-content", children=[
            html.Div(className="x-small-masthead bg-primary text-white text-center", children=[
                html.H3("Explore existing Haikus", className="masthead-subheading text-uppercase mt-5 mb-3",
                        id="titleexplore"),
                html.Div(className="container text-left encadre", children=[
                    html.Form(name="searchHaiku", id="searchHaikuForm", children=[
                        html.Div(className="control-group", children=[
                            html.Div(className="form-group floating-label-form-group-primary "
                                     "floating-label-form-group-primary-with-value controls mb-0 pb-2 text-white-75",
                                     children=[
                                        html.Label("Search by", id="explorelabel1"),
                                        html.Div(className="w-25", children=[
                                            dcc.Dropdown(searchable=False, clearable=False, id="searchByDrop",
                                                         value=SEARCH_BY_BEST,
                                                         options=[{'label': SEARCH_BY_BEST, 'value': SEARCH_BY_BEST},
                                                                  {'label': SEARCH_BY_LATEST, 'value': SEARCH_BY_LATEST}],
                                                         className="text-primary dropdown-primary"),
                                        ]),
                                     ]),
                        ]),
                        html.Div(className="control-group", children=[
                            html.Div(className="form-group floating-label-form-group-primary "
                                     "floating-label-form-group-primary-with-value controls mb-0 pb-2 text-white-75",
                                     children=[
                                        html.Label("Search by Haiku content", id="explorelabel2"),
                                        dcc.Textarea(className="form-group floating-label-form-group controls mb-0 pb-2 "
                                                               "text-white",
                                                     id="searchHaiku", minLength=6, maxLength=2500, rows=2,
                                                     style={'width': '100%', 'fontSize': '1.2em'}),
                                     ]),
                        ]),
                        html.Div(className="row ml-0", children=[
                            html.Div(className="control-group", children=[
                                html.Div(className="form-group floating-label-form-group-primary "
                                         "floating-label-form-group-primary-with-value controls mb-0 pb-2 text-white-75",
                                         children=[
                                            html.Label("Search by Author", id="explorelabel3"),
                                            dcc.Input(className="form-group floating-label-form-group controls mb-0 pb-2 "
                                                                "text-white",
                                                      type="text", id="searchAuthor", maxLength=250,
                                                      style={'width': '100%', 'fontSize': '1.2em'}),
                                         ]),
                            ]),
                            html.Div(className="control-group", children=[
                                html.Div(className="form-group floating-label-form-group-primary "
                                         "floating-label-form-group-primary-with-value controls mb-0 pb-2 text-white-75",
                                         children=[
                                            html.Label("Search by Keywords (separated by comma)", id="explorelabel4"),
                                            dcc.Input(className="form-group floating-label-form-group controls mb-0 pb-2 "
                                                                "text-white",
                                                      type="text", id="searchKeywords", maxLength=250, debounce=True,
                                                      style={'width': '100%', 'fontSize': '1.2em'}),
                                         ]),
                            ]),
                        ]),
                        html.Div(className="form-group", children=[
                            html.Button("Search", type="button", className="btn btn-secondary", id="searchHaikuButton"),
                        ]),
                    ])
                ])
            ]),
            html.Div(className="small-masthead container d-flex encadre align-items-center flex-column",
                     id="placeForSearchedHaiku")
        ]),
        html.Section(id="submit", style={"display": "none"}, className="page-section my-content", children=[
            html.Div(className="small-masthead container d-flex align-items-center flex-column", children=[
                html.H3("Submit your own Haiku", className="masthead-subheading text-uppercase mt-5", id="submittitle"),
            ]),
            html.Div(className="container", children=[
                html.Form(name="submitHaiku", id="submitHaikuForm", children=[
                    html.Div(className="control-group", children=[
                        html.Div(className="form-group floating-label-form-group controls mb-0 pb-2", children=[
                            html.Label("Haiku"),
                            dcc.Textarea(placeholder="Enter your haiku...", className="form-group floating-label-form-group "
                                         "controls mb-0 pb-2", id="submissionHaiku", minLength=6, maxLength=2500, rows=3,
                                         style={'width': '100%'}),
                            html.P(className="help-block text-danger")
                        ]),
                    ]),
                    html.Div(className="control-group", children=[
                        html.Div(className="form-group floating-label-form-group controls mb-0 pb-2", children=[
                            html.Label("Author", id="submitlabel1"),
                            dcc.Input(placeholder="Enter author's name...", type="text", className="form-group "
                                      "floating-label-form-group controls mb-0 pb-2", id="submissionAuthor", maxLength=250,
                                      style={'width': '100%', 'fontSize': '1.2em'}),
                            html.P(className="help-block text-danger")
                        ]),
                    ]),
                    html.Div(className="control-group", children=[
                        html.Div(className="form-group floating-label-form-group controls mb-0 pb-2", children=[
                            html.Div(style={"display": "inline-block"}, id="validatedKeywords"),
                            html.Label("Keywords (separated by comma)", id="submitlabel2"),
                            dcc.Input(placeholder="Enter keywords separated by a comma...", type="text", className="form-group"
                                      " floating-label-form-group controls mb-0 pb-2", id="submissionKeywords", maxLength=250,
                                      debounce=True, style={'width': '100%', 'fontSize': '1.2em'}),
                            html.P(className="help-block text-danger")
                        ]),
                    ]),
                    html.Br(),
                    html.Br(),
                    html.Div(className="form-group", children=[
                        html.Button("Submit", type="button", className="btn btn-primary btn-xl", id="submitHaikuButton"),
                    ]),
                ])
            ]),
        ]),
        dbc.Modal(id="modal-haiku-submit-success", children=[
            dbc.ModalBody(id="validateSubmitHaikuMsg"),
            dbc.ModalFooter(
                html.Button("Close", type="button", className="btn btn-primary", id="closeValidateSubmitHaiku")
            ),
        ]),
        html.Section(id="judge", style={"display": "none"}, className="page-section my-content", children=[
            html.Div(className="small-masthead container d-flex align-items-center flex-column mb-5", children=[
                html.H3("Choose the best !", className="masthead-subheading text-uppercase mt-5", id="judgetitle"),
            ]),
            html.Div(className="container", children=[
                html.Div(className="row", children=[
                    html.Div(className="col-lg-4 ml-auto", children=[
                        html.Div(id="placeholderHaiku1"),
                        dcc.Store(id="pid1"),
                        html.Div(className="container text-center mb-5 mt-3", children=[
                            html.Button("Choose", type="button", className="btn btn-primary btn-xl mr-4", id="choose1Button"),
                            html.Button("Report", type="button", className="btn btn-smol-danger", id="report1Button")
                        ])
                    ]),
                    html.Div(className="col-lg-4 ml-auto"),
                    html.Div(className="col-lg-4 ml-auto", children=[
                        html.Div(id="placeholderHaiku2"),
                        dcc.Store(id="pid2"),
                        html.Div(className="container text-center mb-5 mt-3", children=[
                            html.Button("Choose", type="button", className="btn btn-primary btn-xl mr-4", id="choose2Button"),
                            html.Button("Report", type="button", className="btn btn-smol-danger", id="report2Button")
                        ])
                    ]),
                ]),
                html.Div(className="container text-center mb-4", children=[
                    html.Button("Skip", type="button", className="btn btn-tertiary", id="skipButton"),
                ])
            ]),
        ]),
        dbc.Modal(id="modal-haiku-report", children=[
            dbc.ModalBody("Are you sure you want to report this haiku ?", id="reportsurebody"),
            dbc.ModalFooter([
                html.Button("Yes", type="button", className="btn btn-smol-danger mr-4", id="yesReportHaiku"),
                html.Button("No", type="button", className="btn btn-tertiary", id="noReportHaiku"),
            ]),
        ]),
        dcc.Store(id="reportPid"),
        dbc.Modal(id="modal-haiku-report-success", children=[
            dbc.ModalBody("Thank you for helping us keeping this database clean !", id="reportvalidbody"),
            dbc.ModalFooter(
                html.Button("Close", type="button", className="btn btn-primary", id="closeReportSuccessHaiku")
            ),
        ]),
        html.Footer(className="footer text-center", children=[
            html.Div(className="row", children=[
                html.Div(className="col-lg-4 ml-auto", children=[
                    html.Div(className="container d-flex align-items-center flex-column mb-4", children=[
                        dcc.Dropdown(
                            options=[
                                {'label': LANG_EN, 'value': LANG_EN},
                                {'label': LANG_FR, 'value': LANG_FR}
                            ],
                            clearable=False,
                            className="dropdown-primary text-left",
                            style={'width': '6em'},
                            id="lang-dropdown",
                            placeholder=LANG_EN,
                            searchable=False
                        ),
                    ])
                ]),
                html.Div(className="col-lg-4 ml-auto", children=[
                    html.Div(className="container d-flex align-items-center flex-column", children=[
                        html.H4("Having Issues or Questions ? ", className="text-uppercase mb-4", id="footerquestion"),
                        html.P(className="lead font-weight-normal mb-0", children=[
                            html.Div("Get in touch on   ", id="getintouch"),
                            html.A("Github", href="https://github.com/astariul/jilano"),
                            " !"
                        ])
                    ])
                ]),
                html.Div(className="col-lg-4 ml-auto")
            ])
        ]),
        html.Div(className="scroll-to-top d-lg-none position-fixed", id="random-div", children=[
            html.A(className="js-scroll-trigger d-block text-center text-white rounded", href="#page-top", children=[
                html.I(className="fa fa-chevron-up")
            ])
        ])
    ])
])
