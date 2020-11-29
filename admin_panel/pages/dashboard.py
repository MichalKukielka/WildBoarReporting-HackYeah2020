import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app


def create_markers():
    coords = pd.read_excel('data/coords.xlsx')
    coords = list(zip(coords['lat'].values, coords['lng'].values, coords['desc'].values))
    markers = [dl.Marker(position=(coord[0], coord[1]), children=dl.Tooltip(coord[2])) for coord in coords]
    return markers


def save_coords(click_lat_lng):
    coords = pd.read_excel('data/coords.xlsx')
    coords = coords.append(pd.Series({'lat': click_lat_lng[0], 'lng': click_lat_lng[1], 'desc': 'lalala'}), ignore_index=True)
    coords.to_excel('data/coords.xlsx')


map_container = html.Div(
    className='map-container',
    children=[
        dl.Map(
            children=[
                dl.TileLayer(), 
                dl.LayerGroup(
                    id='click-layer', 
                    children=create_markers()
                )
            ], 
            id='map', 
            center=[51.2167, 22.70], 
            zoom=15, 
            style={'width': '100%', 'height': '100%'})
    ]
)

collapse_container = dbc.Collapse(
    dbc.Card(
        dbc.CardBody(
            children=[
            dbc.ButtonGroup([
                dbc.Button('Dzik', id='report-hole'),
                dbc.Button('Stado', id='report-obstacle'),
                dbc.Button('Inne zwierzę', id='report-other'),
            ],
            ),
            dbc.Row([
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    html.P('1. Zaznacz na mapie miejsce, w którym znalazłeś dziurę.'),
                                    html.P('2. Czy posiadasz zdjęcie przeszkody? Jeśli tak, dołącz je do zgłoszenia:'),
                                    dcc.Upload(
                                        id='upload-image-hole',
                                        children=html.Div([
                                            'Przeciągnij lub ',
                                            html.A('wybierz plik')
                                        ]),
                                        style={
                                            'width': '96%',
                                            'height': '60px',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '5px',
                                            'textAlign': 'center',
                                            'margin': '10px'
                                        },
                                        # Allow multiple files to be uploaded
                                        multiple=False
                                    ),
                                    html.Div(id='output-image-upload-hole'),
                                    dbc.Button('3. Wyślij zgłoszenie!', className='button-send', id='button-send-hole')
                                ]
                            ),
                            className='card-form',
                        ),
                        id='hole-collapse',
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    html.P('1. Zaznacz na mapie miejsce, w którym znalazłeś przeszkodę.'),
                                    html.P('2. Jeśli posiadasz zdjęcie przeszkody, dołącz je do zgłoszenia:'),
                                    dcc.Upload(
                                        id='upload-image-obstacle',
                                        children=html.Div([
                                            'Przeciągnij lub ',
                                            html.A('wybierz plik')
                                        ]),
                                        style={
                                            'width': '96%',
                                            'height': '60px',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '5px',
                                            'textAlign': 'center',
                                            'margin': '10px'
                                        },
                                        # Allow multiple files to be uploaded
                                        multiple=False
                                    ),
                                    html.Div(id='output-image-upload-obstacle'),
                                    dbc.Button('3. Wyślij zgłoszenie!', className='button-send', id='button-send-obstacle')
                                ]
                            ),
                            className='card-form',
                        ),
                        id='obstacle-collapse',
                    ),                                                            
                    dbc.Collapse(
                        dbc.Card(
                            dbc.CardBody(
                                children=[
                                    html.P('1. Zaznacz na mapie miejsce, w którym spotkałeś zwierzę.'),
                                    html.P('2. Czy posiadasz zdjęcie? Jeśli tak, dołącz je do zgłoszenia:'),
                                    dcc.Upload(
                                        id='upload-image-other',
                                        children=html.Div([
                                            'Przeciągnij lub ',
                                            html.A('wybierz plik')
                                        ]),
                                        style={
                                            'width': '96%',
                                            'height': '60px',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '5px',
                                            'textAlign': 'center',
                                            'margin': '10px'
                                        },
                                        # Allow multiple files to be uploaded
                                        multiple=False
                                    ),
                                    html.Div(id='output-image-upload-other'),
                                    html.P('Dodatkowo możesz opisać problem:'),
                                    dbc.Textarea(bs_size='sm', placeholder='Opis problemu'),
                                    dbc.Button('3. Wyślij zgłoszenie!', className='button-send', id='button-send-other')
                                ]
                            ),
                            className='card-form',
                        ),
                        id='other-collapse',
                    ),                                                                                                            
            ])
        ])
    ),
    id='report-collapse'
)

controls_container = html.Div(
    id='controls-container',
    children=[
        dbc.Card(
            dbc.CardBody(
                id='card-body-report',
                children=[
                    dbc.Button('Zgłoś problem', id='report-button'),
                    dbc.Alert(
                        'Dziękujemy za zgłoszenie!',
                        id='alert-thanks',
                        is_open=False,
                        duration=4000,
                        color='success'
                    ),
                    collapse_container,
                ]
            )
        ),
    ]
)

app_container = html.Div(
    className='app-container',
    children=[
        map_container,
        controls_container
    ]
)

main_layout = html.Div(
    id='container',
    children=[
        html.Header(id='app-header', children='Zgłoś dzikusa!'),
        app_container
    ]
)


@app.callback(
    Output('hole-collapse', 'is_open'), 
    Output('obstacle-collapse', 'is_open'),
    Output('other-collapse', 'is_open'),
    Output('report-hole', 'style'),
    Output('report-obstacle', 'style'),
    Output('report-other', 'style'),
    Input('report-hole', 'n_clicks'),
    Input('report-obstacle', 'n_clicks'),
    Input('report-other', 'n_clicks'),
    State('hole-collapse', 'is_open'), 
    State('obstacle-collapse', 'is_open'),
    State('other-collapse', 'is_open'),    
)
def toggle_report_collapses(click_h, click_obs, click_oth,
                            is_open_h, is_open_obs, is_open_oth):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    style_active = {'background-color': '#0065dc'}
    style_not_active = {}
    if trigger_id == 'report-hole':
        return True, False, False, style_active, style_not_active, style_not_active
    elif trigger_id == 'report-obstacle':
        return False, True, False, style_not_active, style_active, style_not_active
    elif trigger_id == 'report-other':
        return False, False, True, style_not_active, style_not_active, style_active
    else:
        # TODO: Fill in
        raise


@app.callback(
    Output('report-collapse', 'is_open'), 
    Output('report-button', 'children'), 
    Output('alert-thanks', 'is_open'),
    Output('click-layer', 'children'),
    Input('report-button', 'n_clicks'),
    Input('map', 'click_lat_lng'),
    Input('button-send-hole', 'n_clicks'),
    Input('button-send-obstacle', 'n_clicks'),
    Input('button-send-other', 'n_clicks'),
    State('report-collapse', 'is_open'),
    State('click-layer', 'children'),
    State('report-button', 'children'),
)
def toggle_report_collapse(click_rep, click_lat_lng, click_h, click_obs, click_oth, is_open, markers, b_val):
    if is_open:
        button_text = 'Zgłoś problem'
    else:
        button_text = 'Anuluj'
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger_id == 'report-button':        
        return not is_open, button_text, False, markers
    elif trigger_id == 'map':
        if markers[-1]['type'] == 'CircleMarker':
            markers.pop()
        markers.append(dl.CircleMarker(center=click_lat_lng, children=[dl.Tooltip('({:.3f}, {:.3f})'.format(*click_lat_lng))]))
        return is_open, b_val, False, markers
    else:
        markers.pop()
        markers.append(dl.Marker(position=click_lat_lng, children=[dl.Tooltip('({:.3f}, {:.3f})'.format(*click_lat_lng))]))
        save_coords(click_lat_lng)
        return False, 'Zgłoś problem', True, markers
