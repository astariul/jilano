import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import argparse

print(dcc.__version__) # 0.6.0 or above is required

app = dash.Dash(__name__)

app.index_string = """
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

</head>

<body id="page-top">

  <!-- Navigation -->
  <nav class="navbar navbar-expand-lg bg-secondary text-uppercase fixed-top" id="mainNav">
    <div class="container">
      <a class="navbar-brand js-scroll-trigger" href="#welcome">Jilano</a>
      <button class="navbar-toggler navbar-toggler-right text-uppercase font-weight-bold bg-primary text-white rounded" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
        Menu
        <i class="fas fa-bars"></i>
      </button>
      <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item mx-0 mx-lg-1">
            <a class="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger my-menu" href="#explore">Explore</a>
          </li>
          <li class="nav-item mx-0 mx-lg-1">
            <a class="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger my-menu" href="#submit">Submit</a>
          </li>
          <li class="nav-item mx-0 mx-lg-1">
            <a class="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger my-menu" href="#judge">Judge</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  {%app_entry%}

  <!-- Footer -->
  <footer class="bg-black small text-c enter text-white-50">
    <div class="container">
      {%config%}
      {%scripts%}
      {%renderer%}
    </div>
  </footer>

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
  <script src="assets/js/contact_me.js"></script>

  <!-- Custom scripts for this template -->
  <footer>
    <script src="assets/js/freelancer.js"></script>
  </footer>
</body>

</html>
"""

divider = html.Div(className="divider-custom divider-light", children=[
                html.Div(className="divider-custom-line"),
                html.Div(className="divider-custom-icon", children=[
                    html.I(className="fas fa-star")
                ]),
                html.Div(className="divider-custom-line"),
            ])

def haiku(poem, author="Unknown", keywords=None):
    if keywords is None:
        keywords = []
    poem_lines = poem.split("\n")
    return html.Div(className="col-md-6 col-lg-4", children=[
        html.Div(className="portfolio-item mx-auto", children=[
            *[html.P(p, className="text-haiku") for p in poem_lines],
            html.P("― " + author, className="author-name"),
            *[html.P(k, className="Lead") for k in keywords],
        ])
    ])


portfolio = html.Div(className="col-md-6 col-lg-4", children=[
        html.Div(className="portfolio-item mx-auto", children=[
            html.Div(className="portfolio-item-caption d-flex align-items-center justify-content-center h-100 w-100", children=[
                html.Div(className="portfolio-item-caption-content text-center text-white", children=[
                    html.I(className="fas fa-plus fa-3x")
                ])
            ]),
            html.Img(className="img-fluid", src="assets/img/portfolio/cabin.png")
        ])
    ])

app.layout = html.Div([
    html.Section(id="welcome", className="page-section welcome my-content", children=[
        html.Div(className="masthead bg-primary text-white text-center", children=[
            html.Div(className="container d-flex align-items-center flex-column", children=[
                html.Img(className="masthead-avatar mb-5", src="assets/img/logo.png"),
                html.H1("Welcome to Jilano", className="masthead-heading text-uppercase mb-0"),
                divider,
                html.P("The goal of this web app is to reference haikus", className="masthead-subheading font-weight-light mb-0")
            ])
        ]),
        html.Div(className="small-masthead container d-flex align-items-center flex-column", children=[
            html.Div(className="container text-left encadre", children=[
                html.P("A Haiku is a short poem, traditionally on 3 lines, following a strict pattern.", className="lead"),
                html.P("For example :", className="lead"),
                html.Br(),
            ]),
            haiku("The west wind whispered\nAnd touched the eyelids of spring\nHer eyes, Primroses", "R. M. Hansard")
        ]),
        html.Div(className="small-masthead bg-primary text-white text-center", children=[
            html.Div(className="container text-left encadre", children=[
                html.P("Haikus are originated from Japan. In Japanese, haikus should follow a 3 lines format with a 5-7-5 pattern (number of syllables per line).", className="lead"),
                html.P("Such constraints force the poet to be creative expressing himself while respecting the rules.", className="lead"),
                html.Br(),
                html.P("Haikus usually focus on the nature, and is divided in 2 asymmetrical sections that juxtaposes 2 subjects, most of the time unexpectedly similar.", className="lead"),
                html.P("There is no need to make the lines rhyme.", className="lead"),
                html.Br(),
                html.P("For other languages than Japanese (like English), it's more difficult to keep the format constraint. Thus, poets are more free.", className="lead")
            ])
        ]),
        html.Div(className="small-masthead container d-flex encadre text-left flex-column", children=[
            html.P("In this website, you can explore haikus submitted by others, and you can submit your own if you wish.", className="lead"),
            html.Br(),
            html.P("We enforce no rules about haiku submission : creativity should have no limit.", className="lead"),
            html.P("However, we would like to keep this website focused on haiku. There is plenty of communities out there for other form of poetry !", className="lead"),
        ])
    ]),
    html.Section(id="explore", style={"display":"none"}, className="page-section portfolio my-content", children=[
        html.Div(className="container", children=[
            html.H2("Portfolio of Page 1", className="page-section-heading text-center text-uppercase text-secondary mb-0"),
            divider,
            # html.Div(className="row", children=[
            #     portfolio,
            #     portfolio,
            #     portfolio,
            #     portfolio,
            #     portfolio,
            #     portfolio
            # ])
        ])
    ]),
    html.Section(id="submit", style={"display":"none"}, className="page-section my-content", children=[
        html.Div(className="small-masthead container d-flex align-items-center flex-column", children=[
            html.H3("Submit your own Haiku", className="masthead-subheading text-uppercase mt-5"), 
        ]),
        html.Div(className="container", children=[
            html.Form(name="submitHaiku", id="submitHaikuForm", children=[
                html.Div(className="control-group", children=[
                    html.Div(className="form-group floating-label-form-group controls mb-0 pb-2", children=[
                        html.Label("Haiku"),
                        dcc.Textarea(placeholder="Enter your haiku...", className="form-group floating-label-form-group controls mb-0 pb-2", id="submissionHaiku", minLength=6, maxLength=2500, rows=3, style={'width': '80%'}),
                        html.P(className="help-block text-danger")
                    ]),
                ]),
                html.Div(className="control-group", children=[
                    html.Div(className="form-group floating-label-form-group controls mb-0 pb-2", children=[
                        html.Label("Author"),
                        dcc.Input(placeholder="Enter author's name...", className="form-group floating-label-form-group controls mb-0 pb-2", id="submissionAuthor", maxLength=250, style={'width': '50%', 'fontSize': '1.2em'}),
                        html.P(className="help-block text-danger")
                    ]),
                ]),
                html.Div(className="control-group", children=[
                    html.Div(className="form-group floating-label-form-group controls mb-0 pb-2", children=[
                        html.Div(style={"display": "inline-block"}, id="validatedKeywords"),
                        html.Form(name="submitHaiku", id="submitKeywordForm", children=[
                            html.Label("Keywords (separated by comma)"),
                            dcc.Input(placeholder="Enter keywords separated by a comma...", className="form-group floating-label-form-group controls mb-0 pb-2", id="submissionKeywords", maxLength=250, debounce=True, style={'width': '50%', 'fontSize': '1.2em'}),
                            html.P(className="help-block text-danger")
                        ])
                    ]),
                ]),
                html.Br(),
                html.Br(),
                html.Div(className="form-group", children=[
                    html.Button("Submit", type="button", className="btn btn-primary btn-xl", id="submitHaikuButton"),
                ]),
            ])
        ]),
        # html.Div(className="container", children=[
        #     html.H2("About", className="page-section-heading text-center text-uppercase text-white"),
        #     divider,
        #     html.Div(className="row", children=[
        #         html.Div(className="col-lg-4 ml-auto", children=[
        #             html.P("Freelancer is a free bootstrap theme created by Start Bootstrap. The download includes the complete source files including HTML, CSS, and JavaScript as well as optional SASS stylesheets for easy customization.", className="lead")
        #         ]),
        #         html.Div(className="col-lg-4 ml-auto", children=[
        #             html.P("You can create your own custom avatar for the masthead, change the icon in the dividers, and add your email address to the contact form to make it fully functional!", className="lead")
        #         ]),
        #     ]),
        #     html.Div(className="text-center mt-4", children=[
        #         html.A(className="btn btn-xl btn-outline-light", href="https://startbootstrap.com/themes/freelancer/", children=[
        #             html.I(className="fas fa-download mr-2"),
        #             "Free Download!"
        #         ])
        #     ])
        # ])
    ]),
    dbc.Modal(id="modal-haiku-submit-success", children=[
        dbc.ModalBody(id="validateSubmitHaikuMsg"),
        dbc.ModalFooter(
            html.Button("Close", type="button", className="btn btn-primary", id="closeValidateSubmitHaiku")
        ),
    ]),
    html.Section(id="judge", style={"display":"none"}, className="page-section my-content", children=[
        html.Div(className="container", children=[
            html.H2("Contact me", className="page-section-heading text-center text-uppercase text-secondary mb-0"),
            divider,
            html.Div(className="row", children=[
                html.Div(className="col-lg-8 mx-auto", children=[
                    html.Form(name="sentMessage", id="contactForm", children=[
                        html.Div(className="control-group", children=[
                            html.Div(className="form-group floating-label-form-group controls mb-0 pb-2", children=[
                                html.Label("Name"),
                                dcc.Input(placeholder="Name", type="text", value="Please enter your name."),
                                html.P(className="help-block text-danger")
                            ])
                        ]),
                        html.Div(className="control-group", children=[
                            html.Div(className="form-group floating-label-form-group controls mb-0 pb-2", children=[
                                html.Label("Email Address"),
                                dcc.Input(placeholder="Email", type="email", value="Please enter your email address."),
                                html.P(className="help-block text-danger")
                            ])
                        ]),
                        html.Div(className="control-group", children=[
                            html.Div(className="form-group floating-label-form-group controls mb-0 pb-2", children=[
                                html.Label("Phone Number"),
                                dcc.Input(placeholder="Phone Number", type="tel", value="Please enter your phone number."),
                                html.P(className="help-block text-danger")
                            ])
                        ]),
                        html.Div(className="control-group", children=[
                            html.Div(className="form-group floating-label-form-group controls mb-0 pb-2", children=[
                                html.Label("Message"),
                                html.Textarea(className="form-control", id="message", rows="5", placeholder="Message", required="required", **{"data-validation-required-message": "Please enter a message."}),
                                html.P(className="help-block text-danger")
                            ])
                        ]),
                        html.Br(),
                        html.Div(id="success"),
                        html.Div(className="form-group", children=[
                            html.Button("Send", type="button", className="btn btn-primary btn-xl", id="sendMessageButton")
                        ])
                    ])
                ])
            ])
        ])
    ]),
    html.Footer(className="footer text-center", children=[
        html.Div(className="container d-flex align-items-center flex-column", children=[
            html.H4("Having Issues or Questions ? ", className="text-uppercase mb-4"),
            html.P(className="lead mb-0", children=[
                "Get in touch on   ",
                html.A("Github", href="https://github.com/astariul/jilano"),
                " !"
            ])
        ])
    ]),
    html.Div(className="scroll-to-top d-lg-none position-fixed ", children=[
        html.A(className="js-scroll-trigger d-block text-center text-white rounded", href="#page-top", children=[
            html.I(className="fa fa-chevron-up")
        ])
    ])
])

@app.callback(
    [Output('modal-haiku-submit-success', 'is_open'), 
     Output('validateSubmitHaikuMsg', 'children'),
     Output('submissionHaiku', 'value'),
     Output('submissionAuthor', 'value'),
     Output('submissionKeywords', 'value'),],
    [Input('submitHaikuButton', 'n_clicks'), Input('closeValidateSubmitHaiku', 'n_clicks')],
    [State('modal-haiku-submit-success', 'is_open'),
     State('submissionHaiku', 'value'),
     State('submissionAuthor', 'value'),
     State('submissionKeywords', 'value'),]
)
def validate_submit(n1, n2, is_open, haiku, author, keywords):
    if not (n1 or n2):
        # Site loading
        return is_open, "", haiku, author, keywords
    if n2:
        # On closing the modal, don't submit the haiku again
        return not is_open, "", haiku, author, keywords
    print("DEBUG : Haiku = {}; Author = {}, keywords = {}".format(haiku, author, keywords))

    # Here, put the submission code that verify if the poem can be submitted
    is_valid = False

    if is_valid:
        display_msg = "Haiku successfully submitted."
        # And reset the input form
        haiku = ""
        author = ""
        keywords = ""
    else:
        display_msg = "Not submitted for X reason."

    return not is_open, display_msg, haiku, author, keywords

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--prod", type=bool, nargs='?',const=True,default=False)
    args = parser.parse_args()

    app.run_server(debug=not args.prod)