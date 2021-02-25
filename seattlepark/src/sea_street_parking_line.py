# -*- coding: utf-8 -*-
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
import dash  # (version 1.11.0)
from dash.dependencies import Input, Output, State
from coordinates_util import CoordinatesUtil

cu = CoordinatesUtil()
print("Reading GeoJson Config..")
cu.sea_parking_geocode()

# mapbox token
mapbox_accesstoken = 'pk.eyJ1IjoicWhzdW4iLCJhIjoiY2tsNGdjMHNlMGR3YTJwcXh6NGNlbGRzNyJ9.R2h8L4RaqEK-2p4BEgUMpg'

maps = [go.Scattermapbox(
    lat=[],  # []
    lon=[],  # []
    mode='lines',  # Determine the drawing mode for the scatter trace.
    marker=go.scattermapbox.Marker(
        size=4,
        color="green",
    ),
    hoverinfo="text",
    hoverlabel=dict(
        bgcolor="white",
        font_size=10
    ),
    visible=True
)]

# Seattle latitude and longitude values
latitude = 47.620506
longitude = -122.349274

# Set up the map layout
layout = go.Layout(
    margin=dict(
        l=0,  # left margin
        r=20,  # right margin
        b=20,  # bottom margin
        t=50,  # top margin
    ),

    mapbox1=dict(
        domain={'x': [0.1, 1], 'y': [0, 1]},
        center=dict(lat=latitude, lon=longitude),
        accesstoken=mapbox_accesstoken,
        zoom=11,
    ),

    xaxis2={
        'zeroline': False,
        "showline": False,
        "showticklabels": True,
        'showgrid': False,
        'domain': [0, 1],
        'side': 'left',
        'anchor': 'x2',
    },
    yaxis2={
        'domain': [0, 1],
        'anchor': 'y2',
        'autorange': 'reversed',
    },
    paper_bgcolor='rgb(255, 255, 255)',
    plot_bgcolor='rgb(204, 204, 204)'
)

# plotly.graph_objects.Figure: Create and add a new annotation to the figure's layout.
fig = go.Figure(data=maps, layout=layout)
#####################################################################
# This is the part to initiate Dash app

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    # html.H1: title
    html.Div(html.H1("Seattle Parking"), style={'text-align': 'center', 'color': 'blue'}),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                dcc.Input(
                    id='destination',
                    type='text',
                    placeholder="Destination?".format("text"),
                    debounce=True,
                    # pattern=r"[0-9].[0-9]*",  # Regex: string must start with letters only
                    # spellCheck=True,
                    autoComplete="on",
                    inputMode='latin',
                    name='text',
                    autoFocus=True,
                ),
                html.Br(),  # break lines
                html.Br(),
                dcc.Input(
                    id='accept_distance',
                    type='text',
                    # value=0.5,
                    placeholder="Acceptable Distance (mi)".format("text"),
                    debounce=True,
                    autoComplete="on",
                    inputMode='latin',
                    name='text',
                    autoFocus=True,
                ),
                html.Br(),
                html.Br(),
                html.Button('Submit', id='submit', n_clicks=0),
            ]),
            html.Br(),
            html.Div(id='message'),
        ]
            , style={'width': '25vh', 'display': 'inline-block', 'text-align': 'center', 'vertical-align': 'top',
                     'margin-top': '100px', 'margin-left': '150px'}
        ),
        html.Div(
            dcc.Graph(
                id='seattle_street_map',
                figure=fig,
                style={"height": "95vh", "margin-top": "-20px"},
                config={
                    'displayModeBar': False  # removes map options from dcc graph
                }
            )
            , style={'width': '170vh', 'display': 'inline-block', 'margin-right': '-20vh'}
        ),
    ],
        style={'width': '195vh', 'display': 'inline-block'}
    ),

    html.Div(children='''
        Data source from Seattle GIS Gov
    ''')
]
)


# ------------------------------------------------------------------------
# By writing this decorator, we're telling Dash to call this function for us whenever the value of the "input"
# component (the text box) changes in order to update the children of the "output" component on the page
# (the HTML div)
# Whenever an input property changes, the function that the callback decorator wraps will get called automatically.
# Dash provides the function with the new value of the input property as an input argument and
# Dash updates the property of the output component with whatever was returned by the function.

@app.callback(
    Output(component_id='seattle_street_map', component_property='figure'),  # The updated streets are passed to
    # this component_ID: seattle_street_map, which updates the map with the recommended streets
    [Input(component_id='submit', component_property='n_clicks')],  # component_property: the type of input field
    state=[State(component_id='destination', component_property='value'),
           State(component_id='accept_distance', component_property='value')]
)
def submit_data(n_clicks, destination, accept_distance):
    if destination and accept_distance:  # if both strings are not none and not blank, i.e. they are valid strings
        if n_clicks > 0:
            top_spots_on_map = []
            spots = cu.get_parking_spots(destination,
                                         accept_distance)  # return the list of the objects that contains the streets info.
            for spot in spots:
                lats = spot.street_meet_expect_coordinates[0]
                longs = spot.street_meet_expect_coordinates[1]
                top_spots_on_map.append(
                    {
                        "type": "scattermapbox",
                        "lat": lats,
                        "lon": longs,
                        "hoverinfo": "text",
                        "mode": "lines",
                        "text": f"Address: <a href=\"https://www.google.com/maps/place/{spot.street_lat_mid},{spot.street_lon_mid}\" target=_blank>"
                                + spot.street_name + f"</a> <br />Distance: {round(spot.calculated_distance, 2)} miles",
                        "marker": {
                            "size": 4,
                            "color": "green"
                        },
                        "hoverlabel": {
                            "bgcolor": "white",
                            "font_size": 10
                        },
                        "showlegend": False,

                        "visible": True
                    }
                )

            return {
                "data": top_spots_on_map,
                "layout": layout
            }
        else:
            return {
                "data": [
                    {
                        "type": "scattermapbox",
                        "lat": [],
                        "lon": [],
                        "hoverinfo": "text",
                        "mode": "lines",
                        "marker": {
                            "size": 4,
                            "color": "green"
                        },
                        "visible": True
                    }
                ],
                "layout": layout
            }
    else:
        return {
            "data": [
                {
                    "type": "scattermapbox",
                    "lat": [],
                    "lon": [],
                    "hoverinfo": "text",
                    "mode": "lines",
                    "marker": {
                        "size": 4,
                        "color": "green"
                    },
                    "visible": True
                }
            ],
            "layout": layout
        }


# ------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)
