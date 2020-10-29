import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
import psycopg2
import sqlalchemy as db
from sqlalchemy import create_engine
from app import app
from apps import home, words, sentences, articles

# search_bar = dbc.Row(
#     [
#         dbc.Col(dbc.Input(type="search", placeholder="Search")),
#         dbc.Col(
#             dbc.Button("Search", color="primary", className="ml-2"),
#             width="auto",
#         ),
#     ],
#     no_gutters=True,
#     className="ml-auto flex-nowrap mt-3 mt-md-0",
#     align="center",
# )

app.layout = html.Div([
                dcc.Location(id='url', refresh=False),
                dbc.NavbarSimple(
                    children=[
                        dbc.NavItem(dbc.NavLink("Words", href="/words")),
                        dbc.NavItem(dbc.NavLink("Sentences", href="/sentences")),
                        dbc.NavItem(dbc.NavLink("Articles", href="/articles")),
                        dbc.NavItem(dbc.NavLink("Grammar", href="/grammar")),
                        dbc.NavItem(dbc.NavLink("Diary", href="/diary")),
                        dbc.DropdownMenu(
                            children=[
                                dbc.DropdownMenuItem("More pages", header=True),
                                dbc.DropdownMenuItem("Speaking", href="/speaking"),
                                dbc.DropdownMenuItem("Listening", href="/listening"),
                            ],
                            nav=True,
                            in_navbar=True,
                            label="More",
                        ),
                    ],
                    brand="Learn-Lang",
                    brand_href="/home",
                    color="info",
                    dark=True,
                ),

                html.Div(id='page-content')
            ])

@app.callback (
              Output('page-content', 'children'),
              [Input('url', 'pathname')]
              )

def display_page(pathname):

    if pathname == '/words':
        return words.layout
    elif pathname == '/sentences':
        return sentences.layout
    elif pathname == '/articles':
        return articles.layout
    # elif pathname == '/grammar':
    #     return grammar.layout
    # elif pathname == '/diary':
    #     return diary.layout
    # elif pathname == '/speaking':
    #     return speaking.layout
    # elif pathname == '/listening':
    #     return listening.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(debug=True)