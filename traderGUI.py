import dash
import dash_core_components as dcc
import dash_html_components as html
import zmq
import json
import os
from util import *
from dash.dependencies import Input, Output
import time

params = {'ready': 0,
          'posUpperLimit': 0,
          'posLowerLimit': 0,
          'spread': 10.0,
          'buysellSkew': 0.0,
          'alphaMultiplier': 0.0,
          'positionSkew': 0.0}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def createZmqPublisher():
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind(commandEndPoint)
    return publisher
print(os.getpid())
pub = createZmqPublisher()
if __name__ == '__main__':
    page_content = [html.Div(id='state')]
    print(len("{:<15}".format("123")))

    app = dash.Dash(__name__)



    def valueSetter(value, name):
        params[name] = value
        print(params)
        return 'changed'


    for key in params:
        page_content.append(html.Div([html.Div(["{:<20}:".format(key)]), dcc.Input(id=key, type='float', value=params[key]),
                                      html.Div(id=key+"state", children='ready',style = {'display':'none'})]))

    page_content.append(html.Button('Submit', id='submit-val', n_clicks=0))
    page_content.append(html.Div(id='state'))
    app.layout = html.Div(page_content)

    for key in params:
        app.callback(Output(component_id=key+'state', component_property='children'),
                     [Input(component_id=key, component_property='value'),
                      Input(component_id=key, component_property='id')])(valueSetter)

    @app.callback(Output('state', 'children'),
    [Input('submit-val', 'n_clicks')])
    def buttonReact(click):
        print("ready")
        pub.send_string(commandTopic + json.dumps(params))
        print(os.getpid())
        return str(params)
    app.run_server(debug=False,threaded=True,host= '0.0.0.0')
