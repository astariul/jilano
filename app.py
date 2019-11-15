import dash
import dash_core_components as dcc
import dash_html_components as html

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

  <title>Freelancer - Start Bootstrap Theme</title>

  <!-- Custom fonts for this theme -->
  <link href="assets/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css">
  <link href="https://fonts.googleapis.com/css?family=Lato:400,700,400italic,700italic" rel="stylesheet" type="text/css">

  <!-- Theme CSS -->
  <link href="assets/css/freelancer.css" rel="stylesheet">

</head>

<body id="page-top">

  <!-- Navigation -->
  <nav class="navbar navbar-expand-lg bg-secondary text-uppercase fixed-top" id="mainNav">
    <div class="container">
      <a class="navbar-brand js-scroll-trigger" href="#welcome">Start Bootstrap</a>
      <button class="navbar-toggler navbar-toggler-right text-uppercase font-weight-bold bg-primary text-white rounded" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
        Menu
        <i class="fas fa-bars"></i>
      </button>
      <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item mx-0 mx-lg-1">
            <a class="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger my-menu" href="#portfolio">Portfolio</a>
          </li>
          <li class="nav-item mx-0 mx-lg-1">
            <a class="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger my-menu" href="#about">About</a>
          </li>
          <li class="nav-item mx-0 mx-lg-1">
            <a class="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger my-menu" href="#contact">Contact</a>
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

# nav_bar = html.Nav(className="navbar navbar-expand-lg bg-secondary text-uppercase fixed-top", id="mainNav", children=[
#         html.Div(className="container", children=[
#             html.A("Start Bootstrap", className="navbar-brand js-scroll-trigger", href="/"),
#             html.Button(className="navbar-toggler navbar-toggler-right text-uppercase font-weight-bold bg-primary text-white rounded", type="button", **{"data-toggle": "collapse", "data-target": "#navbarResponsive", "aria-controls": "navbarResponsive", "aria-expanded": "false", "aria-label": "Toggle navigation"}, children=[
#                 "Menu",
#                 html.I(className="fas fa-bars")
#             ]),
#             html.Div(className="collapse navbar-collapse", id="navbarResponsive", children=[
#                 html.Ul(className="navbar-nav ml-auto", children=[
#                     html.Li(className="nav-item mx-0 mx-lg-1", children=[
#                         html.A("Portfolio", className="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger", href="#portfolio")
#                     ]),
#                     html.Li(className="nav-item mx-0 mx-lg-1", children=[
#                         html.A("About", className="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger", href="#about")
#                     ]),
#                     html.Li(className="nav-item mx-0 mx-lg-1", children=[
#                         html.A("Contact", className="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger", href="#contact")
#                     ]),
#                 ])
#             ])
#         ])
#     ])

# nav_bar = html.Nav(className="navbar navbar-expand-lg bg-secondary text-uppercase fixed-top", id="mainNav", children=[
#         html.Div(className="container", children=[
#             html.A("Start Bootstrap", className="navbar-brand js-scroll-trigger", href="/"),
#             html.Button(className="navbar-toggler navbar-toggler-right text-uppercase font-weight-bold bg-primary text-white rounded", type="button", **{"data-toggle": "collapse", "data-target": "#navbarResponsive", "aria-controls": "navbarResponsive", "aria-expanded": "false", "aria-label": "Toggle navigation"}, children=[
#                 "Menu",
#                 html.I(className="fas fa-bars")
#             ]),
#             html.Div(className="collapse navbar-collapse", id="navbarResponsive", children=[
#                 html.Ul(className="navbar-nav ml-auto", children=[
#                     html.Li(className="nav-item mx-0 mx-lg-1", children=[
#                         html.A("Page 1", className="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger", href="/page-1")
#                     ]),
#                     html.Li(className="nav-item mx-0 mx-lg-1", children=[
#                         html.A("Page 2", className="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger", href="/page-1")
#                     ]),
#                     html.Li(className="nav-item mx-0 mx-lg-1", children=[
#                         html.A("Contact", className="nav-link py-3 px-0 px-lg-3 rounded js-scroll-trigger", href="#contact")
#                     ]),
#                 ])
#             ])
#         ])
#     ])

nav_bar = html.Div()

divider = html.Div(className="divider-custom divider-light", children=[
                html.Div(className="divider-custom-line"),
                html.Div(className="divider-custom-icon", children=[
                    html.I(className="fas fa-star")
                ]),
                html.Div(className="divider-custom-line"),
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

def social_icon(name):
    name = {"facebook": "facebook-f", "twitter": "twitter", "linkedin": "linkedin-in", "dribble": "dribble"}[name]
    return html.A(className="btn btn-outline-light btn-social mx-1", href="#", children=[
        html.I(className="fab fa-fw fa-{}".format(name))
    ])

app.layout = html.Div([
    html.Section(id="welcome", className="page-section my-content", children=[
        html.Header(className="masthead bg-primary text-white text-center", children=[
            html.Div(className="container d-flex align-items-center flex-column", children=[
                html.Img(className="masthead-avatar mb-5", src="assets/img/avataaars.svg"),
                html.H1("Start Bootstrap", className="masthead-heading text-uppercase mb-0"),
                divider,
                html.P("Graphic Artist - Web Designer - Illustrator", className="masthead-subheading font-weight-light mb-0")
            ])
        ]),
    ]),
    html.Section(id="portfolio", className="page-section portfolio my-content", children=[
        html.Div(className="container", children=[
            html.H2("Portfolio of Page 1", className="page-section-heading text-center text-uppercase text-secondary mb-0"),
            divider,
            html.Div(className="row", children=[
                portfolio,
                portfolio,
                portfolio,
                portfolio,
                portfolio,
                portfolio
            ])
        ])
    ]),
    html.Section(id="about", className="page-section bg-primary text-white mb-0 my-content", children=[
        html.Div(className="container", children=[
            html.H2("About", className="page-section-heading text-center text-uppercase text-white"),
            divider,
            html.Div(className="row", children=[
                html.Div(className="col-lg-4 ml-auto", children=[
                    html.P("Freelancer is a free bootstrap theme created by Start Bootstrap. The download includes the complete source files including HTML, CSS, and JavaScript as well as optional SASS stylesheets for easy customization.", className="lead")
                ]),
                html.Div(className="col-lg-4 ml-auto", children=[
                    html.P("You can create your own custom avatar for the masthead, change the icon in the dividers, and add your email address to the contact form to make it fully functional!", className="lead")
                ]),
            ]),
            html.Div(className="text-center mt-4", children=[
                html.A(className="btn btn-xl btn-outline-light", href="https://startbootstrap.com/themes/freelancer/", children=[
                    html.I(className="fas fa-download mr-2"),
                    "Free Download!"
                ])
            ])
        ])
    ]),
    html.Section(id="contact", className="page-section my-content", children=[
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
                            html.Button("Send", type="submit", className="btn btn-primary btn-xl", id="sendMessageButton")
                        ])
                    ])
                ])
            ]),
            # html.Div(className="text-center mt-4", children=[
            #     html.A(className="btn btn-xl btn-outline-light", href="https://startbootstrap.com/themes/freelancer/", children=[
            #         html.I(className="fas fa-download mr-2"),
            #         "Free Download!"
            #     ])
            # ])
        ])
    ]),
    html.Footer(className="footer text-center", children=[
        html.Div(className="container", children=[
            html.Div(className="row", children=[
                html.Div(className="col-lg-4 mb-5 mb-lg-0", children=[
                    html.H4("Location", className="text-uppercase mb-4"),
                    html.P(className="lead mb-0", children=[
                        "2215 John Daniel Drive",
                        html.Br(),
                        "Clark, MO 65243"
                    ])
                ]),
                html.Div(className="col-lg-4 mb-5 mb-lg-0", children=[
                    html.H4("Around the Web", className="text-uppercase mb-4"),
                    social_icon("facebook"),
                    social_icon("twitter"),
                    social_icon("linkedin"),
                    social_icon("dribble"),
                ]),
                html.Div(className="col-lg-4", children=[
                    html.H4("About Freelancer", className="text-uppercase mb-4"),
                    html.P(className="lead mb-0", children=[
                        "Freelance is a free to use, MIT licensed Bootstrap theme created by",
                        html.A("Start Bootstrap", href="http://startbootstrap.com"),
                        "."
                    ])
                ])
            ])
        ])
    ]),
    html.Section(className="copyright py-4 text-center text-white", children=[
        html.Div(className="container", children=[
            html.Small("Copyright &copy; Your Website 2019")
        ])
    ]),
    html.Div(className="scroll-to-top d-lg-none position-fixed ", children=[
        html.A(className="js-scroll-trigger d-block text-center text-white rounded", href="#page-top", children=[
            html.I(className="fa fa-chevron-up")
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)