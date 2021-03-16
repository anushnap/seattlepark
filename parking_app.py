# -*- coding: utf-8 -*-
import dash  # (version 1.11.0)
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State

from coordinates_util import CoordinatesUtil

app = dash.Dash(__name__)
server = app.server
display_parking_spots(app)



def display_parking_spots(dash_app):
    """
    This is to display the recommended parking streets on the Dash map.

    Parameters
    ----------
    dash_app: object
        create the Dash app.

    Returns
    -------
    JSON
        recommended parking spots to be marked on the scatter mapbox.
    """
    print("Reading GeoJson Config..")
    cu = CoordinatesUtil()

    # mapbox token
    mapbox_access_token = cu.decode_data('resources/mapbox_token')

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
            accesstoken=mapbox_access_token,
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

    fig = go.Figure(data=maps, layout=layout)

    dash_app.layout = html.Div(children=[
        html.Div(html.H1("Seattle Parking"), style={'text-align': 'center',
                                                    'color': 'blue'}),
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    dcc.Input(
                        id='destination',
                        type='text',
                        placeholder="Destination?",
                        debounce=True,
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
                        placeholder="Acceptable Distance (mi)",
                        pattern=r"^[0-9]\d*(\.\d+)?$",
                        debounce=True,
                        autoComplete="on",
                        inputMode='latin',
                        name='text',
                        autoFocus=True,
                    ),
                    html.Br(),
                    html.Br(),
                    html.Button('Submit', id='submit', n_clicks=0),
                    html.Div([
                        html.P(id="error", children=[""])
                    ],
                        style={'height': '30px', 'color': 'red'}
                    )
                ],
                    style={'height': '400px', 'text-align': 'center',
                           'display': 'inline-block'}),
            ],
                style={'width': '20%', 'display': 'inline-block',
                       'text-align': 'center', 'vertical-align': 'top',
                       'margin-top': '100px', 'margin-left': '150px'}
            ),
            html.Div(
                dcc.Graph(
                    id='seattle_street_map',
                    figure=fig,
                    style={"height": "95vh", "margin-top": "-20px"},
                    config={
                        'displayModeBar': False
                    }
                ),
                style={'width': '70%', 'display': 'inline-block',
                       'margin-right': '-20vh'}
            ),
        ],
            style={'width': '100%', 'display': 'inline-block'}
        ),

        html.Div(children='''
            Data source from Seattle GIS Gov
        ''')
    ]
    )

    # ------------------------------------------------------------------------
    # By writing this decorator, we're telling Dash to call this function for
    # us whenever the value of the "input" component (the text box) changes
    # in order to update the children of the "output" component on the page
    # (the HTML div). Whenever an input property changes, the function that
    # the callback decorator wraps will get called automatically. Dash
    # provides the function with the new value of the input property as an
    # input argument and Dash updates the property of the output component
    # with whatever was returned by the function.

    @dash_app.callback(
        Output(component_id='seattle_street_map',
               component_property='figure'),
        Output("error", "children"),
        [Input(component_id='submit', component_property='n_clicks')],
        state=[State(component_id='destination', component_property='value'),
               State(component_id='accept_distance',
                     component_property='value')]
    )
    def submit_data(n_clicks, destination, accept_distance):
        return create_parking_spots(n_clicks, destination, accept_distance,
                                    layout, cu)


def create_parking_spots(n_clicks, destination, accept_distance, layout, cu):
    """
    This function refreshes the map when the submit button is clicked with
    user input destination address and acceptable distance.

    Parameters
    ----------
    n_clicks: integer
        the number of the submit button got clicked.

    destination: str
        the user input destination address.

    accept_distance: str
        the user input of acceptable walking distance from the
        destination address.

    layout: object
        set up the map layout

    cu: object
        object to call the functions in CoordinatesUtil

    Returns
    -------
    JSON
        recommended parking spots to be marked on the scatter mapbox.
    """
    if destination and accept_distance:
        if n_clicks > 0:
            top_spots_on_map = []
            spots, destination_coordinates = \
                cu.get_parking_spots(destination, accept_distance)
            if not destination_coordinates or not spots or len(spots) == 0:
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
                       }, "Input Address is Invalid!"
            for spot in spots:
                lats = spot.street_meet_expect_coordinates[0]
                longs = spot.street_meet_expect_coordinates[1]
                street_details = f"Address: " \
                                 f"<a " \
                                 f"href=\"https://www.google.com/maps/" \
                                 f"place/" \
                                 f"{spot.street_lat_mid}," \
                                 f"{spot.street_lon_mid}\" " \
                                 f"target=_blank>" + \
                                 spot.street_name + f"</a> <br />" \
                                 f"Distance: " \
                                 f"{round(spot.calculated_distance, 2)} " \
                                 f"miles" \
                                 f"<br />Spots Available: " \
                                 f"{spot.spaceavail}"
                top_spots_on_map.append(
                    {
                        "type": "scattermapbox",
                        "lat": lats,
                        "lon": longs,
                        "mode": "lines",
                        "marker": {
                            "size": 4,
                            "color": "green"
                        },
                        "hovertemplate": f"{street_details}<extra></extra>",
                        "hoverlabel": {
                            "bgcolor": "white",
                            "font_size": 10
                        },
                        "showlegend": False,

                        "visible": True
                    }
                )
            destination_address_link = f"Address: <a href=" \
                                       f"\"https://www.google.com/" \
                                       f"maps/place/" \
                                       f"{destination_coordinates[0]}," \
                                       f"{destination_coordinates[1]}\" " \
                                       f"target=_blank>" + destination + \
                                       "</a>"
            top_spots_on_map.append(
                {
                    "type": "scattermapbox",
                    "lat": [destination_coordinates[0]],
                    "lon": [destination_coordinates[1]],
                    "mode": "point",
                    "marker": {
                        "size": 8,
                        "color": "red"
                    },
                    "hovertemplate": f"{destination_address_link}"
                                     f"<extra></extra>",
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
                   }, ""
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
                   }, ""
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
               }, ""


# ------------------------------------------------------------------------

if __name__ == '__main__':
    app = dash.Dash(__name__)
    display_parking_spots(app)
    app.run_server(debug=False)
