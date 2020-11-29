import dash_core_components as dcc
import dash_html_components as html
import flask
from flask import request

from app import app


form_q = html.Form(
    id='login-form',
    children=[
        html.Header([html.Img(src='assets/logo_dzikalizator.png', style={'width': '120px', 'height': 'auto'}), html.H2('Zaloguj się')]),
        dcc.Input(type='text', id='input-username', size='20', placeholder='Nazwa użytkownika'),
        dcc.Input(type='password', id='input-password', size='20', placeholder='Hasło'),
        html.Button(children=[dcc.Link('Zaloguj', href='/dashboard')], type='submit'),
    ]
)

index_layout = html.Main(
    children=[html.Section([form_q])]
)

# Login mocked and disabled for purpose of presentation.
# @app.server.route('/', methods=['POST'])
# def route_login():
#     data = flask.request.form
#     username = data.get('username')
#     password = data.get('password')
#     return flask.redirect('dashboard')
