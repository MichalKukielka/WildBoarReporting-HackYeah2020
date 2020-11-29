import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from pages import dashboard, login, admin_panel


content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.layout = content_div

app.validation_layout = html.Div([
    content_div,
    login.index_layout,
    dashboard.main_layout
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return login.index_layout
    elif pathname == '/dashboard':
        return dashboard.main_layout
    elif pathname == '/admin':
        return admin_panel.panel_layout
    else:
        return login.index_layout


if __name__ == "__main__":
    app.run_server(debug=True)
