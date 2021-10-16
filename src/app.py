import os

# General
import pandas as pd
import numpy as np
import time
import datetime
import math
from datetime import date
import base64
import io
import socket
import random

# DASH & Plotly
import dash
from   dash import html
from   dash import dcc

import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import request

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.graph_objs.area import hoverlabel


countries  = pd.read_csv('data/ChessRating.csv')['Country'].unique()


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],title='Chess-Data-Vis')

app.layout = html.Div(id = 'king-container',children = [

    # This is my Top - Bar!  Don't touch it :p
    html.Div(className='Top-Bar', children=[
        html.H2(['Chess Data Visualizer'])
    ]),

    #Here I am starting my Tabs
    dcc.Tabs([
        ##########################################   TAB 1 ################################################################
        dcc.Tab(className='Tabs',label='Vizualize all Countries', children=[

            # Let's start making the rows for the Graphs and selections
            dbc.Row(className='second-row', children=[
                dbc.Col([
                    html.P("Select Countries:"),
                    dcc.Dropdown(
                        id='select-countries',
                        className='dropdowm',
                        options=[{'label': x, 'value': x}
                                 for x in countries],
                        clearable=True,
                        multi=True,
                        placeholder='Select Countries',
                    ),
                ]), # End of first columns in second row
                dbc.Col([
                    html.P("Select X:"),
                    dcc.Dropdown(
                        id='select-x',
                        className='dropdowm',
                        options=[{'label': x, 'value': x}
                                 for x in ['Classic','Rapid','Blitz']],
                        clearable=True,
                        placeholder='Select x',
                    ),

                ]), # Second Columns in second Row
                dbc.Col([
                    html.P("Select Y:"),
                    dcc.Dropdown(
                        id='select-y',
                        className='dropdowm',
                        options=[{'label': x, 'value': x}
                                 for x in ['Classic', 'Rapid', 'Blitz']],
                        clearable=True,
                        placeholder='Select y',
                    ),
                ]), # Third Columns in second Row
                dbc.Col([
                    html.P("Select Z:"),
                    dcc.Dropdown(
                        id='select-z',
                        className='dropdowm',
                        options=[{'label': x, 'value': x}
                                 for x in ['Classic', 'Rapid', 'Blitz']],
                        clearable=True,
                        placeholder='Select z',
                    ),
                ]),  # Third Columns in second Row
                dbc.Col([]),
                dbc.Col([]),

            ]),  # End of second row

            dbc.Row(className='third-row', children=[
                        dbc.Col([
                            html.Div(className='graph-container',children = [
                                dcc.Graph(id = 'graph-countries')
                            ])
                        ])

            ]), # End of third Row children
        ]), # End of Tab 1
        ##########################################   TAB 1   end    ##############################################

        ##########################################   TAB 2 #######################################################
        dcc.Tab(className='Tabs',label='Vizualize per Country', children=[
            dbc.Row(className='second-row', children=[
                dbc.Col([
                    html.P("Select Countries:"),
                    dcc.Dropdown(
                        id='select-country',
                        className='dropdowm',
                        options=[{'label': x, 'value': x}
                                 for x in countries],
                        clearable=True,
                        placeholder='Select Country',
                    ),
                ]),  # End of first columns in second row
                dbc.Col([
                    html.P("Select Person:"),
                    dcc.Dropdown(
                        id='select-person',
                        className='dropdowm',
                        # options=[{'label': x, 'value': x}
                        #          for x in ['Classic', 'Rapid', 'Blitz']],
                        clearable=True,
                        placeholder='Select Person',
                    ),

                ]),  # Second Columns in second Row
                dbc.Col([]),
                dbc.Col([]),
                dbc.Col([]),
                dbc.Col([]),

            ]),  # End of second row

            dbc.Row(className='third-row', children=[
                dbc.Col([
                    html.Div(className='graph-container', children=[
                        dcc.Graph(id='graph-people')
                    ])
                ])

            ]),  # End of third Row children


        ]),
        ##########################################   TAB 2   end    ##############################################
    ]), # End of Tabs

]) # End of King Container
##############################################################################################################
###########################    Starting of Callbacks    ######################################################
##############################################################################################################

###########################   Update Graphs for People     ###################################################
##############################################################################################################
@app.callback(
    Output('graph-people', 'figure'),
    [
        Input('select-person', 'value')
    ])

def graph_updater_2(person):

    if person == None:
        raise  PreventUpdate
    else:
        #Here Holding the data for the selected person
        data        = pd.read_csv('data/ChessRating.csv')
        data_person = data[data['Name'] == person]

        #Here calculate the mean for all the data
        avg_classic = data['Classic'].mean()
        avg_rapid   = data['Rapid'].mean()
        avg_blitz   = data['Blitz'].mean()
        avg_age     = data['Age'].mean()


        games = ['Classic', 'Rapid', 'Blitz','Age']
        fig = go.Figure(data=[
            go.Bar(name=person,  x=games, y=[  float(data_person['Classic']),
                                               float(data_person['Rapid']),
                                               float(data_person['Blitz']),
                                               float(data_person['Age'])
                                             ]),

            go.Bar(name='average', x=games, y=[avg_classic,
                                               avg_rapid,
                                               avg_blitz,
                                               avg_age
                                               ])
        ])
        # Change the bar mode
        fig.update_layout(barmode='group')

        fig.update_layout(height=650)
        fig.update_layout(title=person+' vs  Average Data')

        return fig





###########################   Update Values for People     ###################################################
##############################################################################################################
@app.callback(
    Output('select-person', 'options'),
    [
        Input('select-country', 'value')
    ])

def make_option(country):
    '''This functions return the correct option accordingly with the selection of the countries
    for the correct corresponding people'''

    print('\nTriggerd!')

    if country == None:
        raise PreventUpdate
    else:
        data = pd.read_csv('data/ChessRating.csv')

        # Keeping only what is needed
        dataBuff = pd.DataFrame(columns= data.columns)


        dataBuff = dataBuff.append(data[data['Country'] == country])

        final_names = dataBuff['Name'].tolist()

        opt = [{'label': x, 'value': x} for x in final_names]

        print('options are:\n',*opt,sep = '\n')

        return opt


###########################    Graph for Countries      ######################################################
##############################################################################################################
@app.callback(
    Output('graph-countries', 'figure'),
    [
    Input('select-countries', 'value'),
    Input('select-x', 'value'),
    Input('select-y', 'value'),
    Input('select-z', 'value'),

    ])
def graph_updater(countries,x_sel,y_sel,z_sel):
    '''This function takes the selection of the user and making the corresponding Graph for all countries'''

    if x_sel == None or (y_sel == None or z_sel == None):
        raise PreventUpdate
    else:
        data = pd.read_csv('data/ChessRating.csv')

        if countries != None:

            dataBuff = pd.DataFrame(columns= data.columns)

            for elem in countries:
                dataBuff = dataBuff.append(data[data['Country'] == elem])

            if len(dataBuff) !=0:
                data = dataBuff


        fig = px.scatter_3d(data,
                            x=x_sel, y=y_sel, z=z_sel,
                            color="Country",
                            hover_data=['Name','Age'])

        fig.update_layout(height=650)
        fig.update_layout(title='Chess Players per Countries')


        return fig



if __name__ == '__main__':

    app.run_server(debug=True)








































