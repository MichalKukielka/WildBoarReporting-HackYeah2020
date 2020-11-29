from app import app
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import requests
import pprint
from dash.dependencies import ALL, Input, Output, State
from random import randint
from pathlib import Path
from dash.exceptions import PreventUpdate
import dash
import ast
import json
# import reverse_geocoder as rg


def create_markers():
    response = requests.post("https://us-central1-plant-app-react-native.cloudfunctions.net/getAllCoords", json={'isAdmin': True})
    resp_json = response.json()['body']
    coords = list()
    for boar in resp_json:
        coords.append(dl.Marker(position=(boar['coords']['lat'], boar['coords']['long']), children=dl.Tooltip(f'{boar["boarType"]} - {boar["isAlive"]}')))
    return coords

admin_header = html.Header(
    id='admin-header', 
    children=[
        html.Img(src='assets/min_rol_rgb_color-mini.png', id='logo-min-rol'),
        html.Div(
            id='logo-cont',
            children=[ 
                html.Button('Wyloguj się', id='button-logout'),
                html.Img(src='assets/logo_dzikalizator.png', id='logo-dzik')
            ]
        )
    ]
)

loc_list_title = html.H2('Lista zgłoszeń')


# search_address = dcc.Input(id='address-search', type='search', style={'display': 'inline-block'})
filter_dropdown = dcc.Dropdown(
    id='filter-boars', 
    options=[
        {'value': 'krakowski', 'label': 'krakowski'},
        {'value': 'nowotarski', 'label': 'nowotarski'},
        {'value': 'nowosądecki', 'label': 'nowosądecki'}
    ],
    placeholder='Cała Polska'
)
# search_button = html.Button('Szukaj', id='search-button', style={'display': 'inline-block'})
search_container = html.Div(id='search-container', children=[filter_dropdown])

response = requests.post("https://us-central1-plant-app-react-native.cloudfunctions.net/getAllCoords", json={'isAdmin': True})
boars = response.json()['body']

# result = rg.search(tuple(boars[0]['coords'].values()))
# result = rg.search((50.0801344,20.0042033))
# pprint.pprint(result)
pprint.pprint(boars[1])
# location_list = html.Ol(id='loc-list', children=[html.Li(item) for item in ['Dzik 1', 'Dzik 2', 'Dzik 3']])
boar_list = dbc.ListGroup(
    id='boar-list',
    children=[
    # dbc.ListGroupItem(f'{elem["boarType"]} - {elem["id"]}', id={'type': 'boar-list-item', 'index': index}, action=True) 
    dbc.ListGroupItem(f'Zgłoszenie {index} - {elem["boarType"]}', id={'type': 'boar-list-item', 'index': index}, action=True) 
    for index, elem in enumerate(boars)
])

boar_list_cont = html.Div(children=[boar_list])
loc_list_container = html.Div(id='location-list-container', children=[loc_list_title, search_container, boar_list_cont])

boar_map = dl.Map(
    children=[
        dl.TileLayer(),
        dl.LayerGroup(
            id='click-layer',
            children=create_markers()
        )
     ],
     center=[51.932452, 18.3022974],
     zoom=5,
     style={'width': '100%', 'height': '300px'})
map_container = html.Div(id='panel-map-container', className='panel-block', children=[boar_map])

boar_image_cont = html.Div(id='boar-image-container', className='panel-block', children=html.Img(src='assets/logo_dzikalizator.png', alt='Logo'))

# info = [html.P(f'{key}: {value}') for key, value in boars.items()]
info = html.H2('Wybierz zgłoszenie z listy po lewej.')
info_panel_container = html.Div(id='info-panel-container', className='panel-block', children=info)

hidden = html.Div(id='hidden', style={'visible': 'hidden'})
panel_elements = [loc_list_container, map_container, boar_image_cont, info_panel_container, hidden]

panel_layout = html.Div(
    id='panel-container',
    children=[admin_header, html.Div(id='panel-grid', children=panel_elements)]
)

@app.callback(
    Output('info-panel-container', 'children'),
    Output('boar-image-container', 'children'),
    Output('hidden', 'children'),
    Input({'type': 'boar-list-item', 'index': ALL}, 'n_clicks'),
    State({'type': 'boar-list-item', 'index': ALL}, 'id'), prevent_initial_call=True
)
def get_boar_info(click, index):
    if not click:
        raise PreventUpdate
    images = list(Path('assets/boar_images').glob('*'))
    # print(click, index)
    # print(list(images))
    image = images[randint(0, len(images) - 1)]
    image_el = html.Img(src=str(image))
    trigger_id = ast.literal_eval(dash.callback_context.triggered[0]['prop_id'].split('.')[0])['index']
    # print(index)
    # print(boars[index])
    boar_type = boars[trigger_id]['boarType']
    coords = boars[trigger_id]['coords']
    coords = f'{coords["lat"]}, {coords["long"]}'
    try:
        data = boars[trigger_id]['data']
    except KeyError:
        data = 'Brak'
    spotted_datetime = boars[trigger_id]['dateTime']
    is_alive = boars[trigger_id]['isAlive']
    info = [html.Table(
        children=[
            html.Tr(
                children=[html.Td('Typ dzika:'), html.Td(boar_type)]
            ),
            html.Tr(
                children=[html.Td('Koordynaty:'), html.Td(coords)]
            ),
            html.Tr(
                children=[html.Td('Żywy:'), html.Td(is_alive)]
            ),
            html.Tr(
                children=[html.Td('Data spotkania:'), html.Td(spotted_datetime)]
            ),
            html.Tr(
                children=[html.Td('Dodatkowe informacje:'), html.Td(data)]
            )
        ], style={'float': 'left'}                                                  
    ),
    html.Div(id='butcont', style={'float': 'right'}, children=html.Button('Zamknij zgłoszenie', id='button-close')),
    ]

    # info = [html.P(f'{key}: {value}') for key, value in boars[trigger_id].items()]
    return info, image_el, trigger_id

@app.callback(
    # Output('butcont', 'children'),
    Output('button-close', 'disabled'),
    Input('button-close', 'n_clicks'),
    State('hidden', 'children'),
    State('butcont', 'children')
)
def close_report(click, index, children):
    if not click:
        raise PreventUpdate
    try:
        index = int(json.loads(index))
    except:
        print(index)
    resp = requests.post("https://us-central1-plant-app-react-native.cloudfunctions.net/updateStatus", json={'id': boars[index]['id'], 'status': 'resolved'})
    print(children)
    if resp.status_code == 200:
        alert = dbc.Alert(
            'Zajebiście byku!',
            id='alert-thanks',
            is_open=False,
            duration=4000,
            color='success'
        ),
    else:
        alert = dbc.Alert(
            'Chujowo byku!',
            id='alert-thanks',
            is_open=False,
            duration=4000,
            color='success'
        ),
    # children.append(alert)
    return True