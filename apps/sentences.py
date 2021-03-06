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

engine = create_engine('postgresql://postgres:fe190386@localhost/learning')
con = engine.connect()
dff = pd.read_sql_table('sentences', con)  # db'den veri cektik.
dff = dff.iloc[::-1]

layout = html.Div([
            dbc.Row([
                dbc.Col(
                    dbc.Input(id='nederlands-sentence', className="mb-3", type='text', placeholder="Nederlandse zin..."), width=8
                ),
                dbc.Col(
                    dbc.Input(id='english-sentence', className="mb-3", type='text', placeholder="English sentence..."), width=8
                ),
                dbc.Col([
                    dbc.Button("Add", id='add-2', color="danger", n_clicks=0),
                    dbc.Button("Update", id='update-2', color="info", n_clicks=0),
                    dbc.Button("Delete", id='delete-2', color="warning", n_clicks=0),
                    html.A(dbc.Button("Google", id='google', color="dark", n_clicks=0), href='https://www.google.com/search?q=google+translate&rlz=1C5CHFA_enNL888NL888&oq=google+tra&aqs=chrome.1.69i57j0l4j69i60l3.3144j0j7&sourceid=chrome&ie=UTF-8', target='_blank'),
                    html.A(dbc.Button("Tureng", id='tureng', color="success", n_clicks=0), href='https://tureng.com/tr/turkce-ingilizce', target='_blank')
                    ], width=5
                ),
                dbc.Modal([
                        dbc.ModalHeader("Header"),
                        dbc.ModalBody("The data has been saved to your PostgreSQL database."),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close-centered-2", color="danger", n_clicks=0, className="ml-auto")
                        ),
                ], id="modal-centered-2", centered=True)
            ], className='mt-5', justify='center'),

            dbc.Row(
                dbc.Col(
                     dash_table.DataTable(
                            id='sentences',
                            data=dff.to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in dff.columns],
                            style_cell={'textAlign': 'center','width':'40px','minWidth': '40px', 'maxWidth': '40px', 'overflow': 'hidden','textOverflow': 'ellipsis','font-size':'16px'},
                            fixed_rows={'headers': True, 'data': 0},
                            style_header={'fontWeight': 'bold'},
                            page_action='none',
                            style_table={'height': '250px', 'overflowY': 'auto'},
                            # row_deletable=True,
                            row_selectable='single',
                            selected_rows=[],
                            editable=True,
                            # style_as_list_view=True,
                     ), width=8
                ), className="mt-3", justify='center'
            )
        ])


@app.callback(
            [Output(component_id="modal-centered-2", component_property="is_open"),
             Output(component_id="sentences", component_property="data")],
            [Input(component_id='add-2', component_property='n_clicks'),
             Input(component_id='update-2', component_property='n_clicks'),
             Input(component_id='delete-2', component_property='n_clicks'),
             Input(component_id='close-centered-2', component_property='n_clicks')],
            [State(component_id='nederlands-sentence', component_property='value'),
             State(component_id='english-sentence', component_property='value'),
             State(component_id='modal-centered-2', component_property='is_open'),
             State(component_id='sentences', component_property='data'),
             State(component_id='sentences', component_property='selected_row_ids')
             ]
            )

def save_to_db_2(n_clicks1, n_clicks2, n_clicks3, n_clicks4, sentence1, sentence2, is_open, dataset, selected_row_ids):
    ctx = dash.callback_context
    pie = ctx.triggered[0]['prop_id'].split('.')[0]
    df2 = pd.DataFrame(dataset)
    data = df2.to_dict('records')

    if pie == 'add-2':

        df = pd.DataFrame()
        df['nederlands'] = [sentence1]
        df['english'] = [sentence2]

        df.to_sql('sentences', con, if_exists='append', index=False) # db'ye veri attik.

        dffx = pd.read_sql_table('sentences', con) # db'den veri cektik
        dffx = dffx.iloc[::-1]
        data = dffx.to_dict('records')

        return not is_open, data

    elif pie == 'update-2':

        con.execute("DELETE FROM sentences")
        pg = pd.DataFrame(dataset)
        pg = pg.iloc[::-1]
        pg.to_sql('sentences', con, if_exists='append', index=False)  # db'ye veri attik

        dffx = pd.read_sql_table('sentences', con)  # db'den veri cektik
        dffx = dffx.iloc[::-1]
        data = dffx.to_dict('records')

        return not is_open, data

    elif pie == 'delete-2':

        i = int(selected_row_ids[0])
        con.execute("DELETE FROM sentences WHERE id=%s", (i,))

        dffx = pd.read_sql_table('sentences', con)  # db'den veri cektik
        dffx = dffx.iloc[::-1]
        data = dffx.to_dict('records')

        return not is_open, data

    elif pie == 'close-centered-2':

        return not is_open, data

    else:
        return is_open, data


@app.callback(
            [Output(component_id='nederlands-sentence', component_property='value'),
            Output(component_id='english-sentence', component_property='value')],
            [Input(component_id='sentences', component_property='selected_row_ids')]
            )

def show_details_2 (selected_row_ids):

    if not selected_row_ids is None:

        conn = psycopg2.connect("dbname=learning user=postgres password=fe190386")
        cur = conn.cursor()
        i = int(selected_row_ids[0])
        cur.execute("SELECT * FROM sentences WHERE id=%s", (i,))
        rows = cur.fetchall()
        df = pd.DataFrame(rows)

        return df.iloc[0,2], df.iloc[0,3]

    else:
        return '',''