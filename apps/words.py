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

# psycopg2 ile baglanma ornegi
# conn = psycopg2.connect("dbname=learning user=postgres password=fe190386")
# cur = conn.cursor()
# cur.execute("SELECT * FROM allwords WHERE nederlands=%s", (i,))
# rows = cur.fetchall()
# df = pd.DataFrame(rows)

engine = create_engine('postgresql://postgres:fe190386@localhost/learning')
con = engine.connect()
df_all = pd.read_sql_table('allwords', con) # db'den veri cektik.

layout = html.Div([
                html.Div([
                    dbc.Row(
                        dbc.Col(
                            dbc.Jumbotron([
                                html.H1(id='jumbotron-top', className="display-3"),
                                html.Hr(className="my-2"),
                                html.H1(id='jumbotron-bottom', className="display-3"),
                                html.Div([
                                    html.A("<", id='smaller', href=""),
                                    dbc.Button("Learn", id='learn', color="primary", n_clicks=0),
                                    html.A(">", id='bigger', href=""),
                                ], id='middle'),
                                html.P(id='num'),
                                ], id='jumbo'
                            ), width=9
                        ), className="mt-5", justify='center'
                    ),
                    dbc.Row([
                        dbc.Col(
                            dbc.Input(id='nederlands-word', className="mb-3", type='text', placeholder="Nederlandse woord..."), width=2
                        ),
                        dbc.Col(
                            dbc.Input(id='english-word', className="mb-3", type='text', placeholder="English word..."), width=2
                        ),
                        dbc.Col([
                            dbc.Button("Add", id='add-1', color="danger", n_clicks=0),
                            dbc.Button("Update", id='update-1', color="info", n_clicks=0),
                            dbc.Button("Delete", id='delete-1', color="warning", n_clicks=0),
                            html.A(dbc.Button("Google", id='google', color="dark", n_clicks=0), href='https://www.google.com/search?q=google+translate&rlz=1C5CHFA_enNL888NL888&oq=google+tra&aqs=chrome.1.69i57j0l4j69i60l3.3144j0j7&sourceid=chrome&ie=UTF-8', target='_blank'),
                            html.A(dbc.Button("Tureng", id='tureng', color="success", n_clicks=0), href='https://tureng.com/tr/turkce-ingilizce', target='_blank')
                            ], width=4
                        ),
                        dbc.Modal([
                            dbc.ModalHeader("Header"),
                            dbc.ModalBody("The data has been saved to your PostgreSQL database."),
                            dbc.ModalFooter(
                                dbc.Button("Close", id="close-centered-1", color="danger", n_clicks=0, className="ml-auto")
                                )
                        ], id="modal-centered-1", centered=True)
                    ], className='mt-5', justify='center'),

                    dbc.Row(
                        dbc.Col(
                             dash_table.DataTable(
                                    id='all-words',
                                    data=df_all.to_dict('records'),
                                    columns=[{'id': c, 'name': c} for c in df_all.columns],
                                    style_cell={'textAlign': 'center','minWidth': '100px', 'width': '100px', 'maxWidth': '100px','font-size':'16px'},
                                    fixed_rows={'headers': True, 'data': 0},
                                    style_header={'fontWeight': 'bold'},
                                    page_size=20,
                                    # row_deletable=True,
                                    row_selectable='single',
                                    selected_rows=[],
                                    editable=True,
                                    filter_action="native",
                                    # style_as_list_view=True,

                             ), width=9
                        ), className="mt-3", justify='center'
                    )
                ])
            ])

@app.callback(
            [Output(component_id="modal-centered-1", component_property="is_open"),
             Output(component_id="all-words", component_property="data")],
            [Input(component_id='add-1', component_property='n_clicks'),
             Input(component_id='update-1', component_property='n_clicks'),
             Input(component_id='delete-1', component_property='n_clicks'),
             Input(component_id='close-centered-1', component_property='n_clicks')],
            [State(component_id='nederlands-word', component_property='value'),
             State(component_id='english-word', component_property='value'),
             State(component_id='modal-centered-1', component_property='is_open'),
             State(component_id='all-words', component_property='data'),
             State(component_id='all-words', component_property='selected_row_ids')
             ]
            )

def save_to_db_1(n_clicks1, n_clicks2, n_clicks3, n_clicks4, word1, word2, is_open, dataset, selected_row_ids):
    ctx = dash.callback_context
    pie = ctx.triggered[0]['prop_id'].split('.')[0]
    df2 = pd.DataFrame(dataset)
    data = df2.to_dict('records')

    if pie == 'add-1':

        df = pd.DataFrame()
        df['nederlands'] = [word1]
        df['english'] = [word2]

        df.to_sql('allwords', con, if_exists='append', index=False) # db'ye veri attik.

        dffx = pd.read_sql_table('allwords', con) # db'den veri cektik
        # dffx = dffx.iloc[::-1]
        data = dffx.to_dict('records')

        return not is_open, data

    elif pie == 'update-1':

        con.execute("DELETE FROM allwords")
        pg = pd.DataFrame(dataset)
        # pg = pg.iloc[::-1]
        pg.to_sql('allwords', con, if_exists='append', index=False)  # db'ye yeni veriyi attik

        dffx = pd.read_sql_table('allwords', con)  # db'den veri cektik
        # dffx = dffx.iloc[::-1]
        data = dffx.to_dict('records')

        return not is_open, data

    elif pie == 'delete-1':

        i = int(selected_row_ids[0])
        con.execute("DELETE FROM allwords WHERE id=%s", (i,)) # db'den ilgili veriyi sildik

        dffx = pd.read_sql_table('allwords', con)  # db'den veri cektik
        # dffx = dffx.iloc[::-1]
        data = dffx.to_dict('records')

        return not is_open, data

    elif pie == 'close-centered-1':

        return not is_open, data

    else:
        return is_open, data



@app.callback(
            [Output(component_id='jumbotron-top', component_property='children'),
             Output(component_id='jumbotron-bottom', component_property='children'),
             Output(component_id='num', component_property='children')],
            [Input(component_id='all-words', component_property='selected_row_ids'),
             Input(component_id='learn', component_property='n_clicks')],
            [State(component_id='num', component_property='children')]
            )

def show_jumbotron (selected_row_ids, n_clicks, number):
    ctx = dash.callback_context
    pie = ctx.triggered[0]['prop_id'].split('.')[0]
    conn = psycopg2.connect("dbname=learning user=postgres password=fe190386")
    cur = conn.cursor()

    if pie == 'all-words':

        i = int(selected_row_ids[0])
        cur.execute("SELECT * FROM allwords WHERE id=%s", (i,))
        rows = cur.fetchall()
        df = pd.DataFrame(rows)
        return df.iloc[0,1],'?',i

    elif pie == 'learn':

        if n_clicks % 2 == 1:
            if not number == 0:
                i = number
            else:
                i = 1
            cur.execute("SELECT * FROM allwords WHERE id=%s", (i,))
            rows = cur.fetchall()
            df = pd.DataFrame(rows)
            return df.iloc[0,1], df.iloc[0,2], df.iloc[0,0]

        elif n_clicks % 2 == 0:

            i = number+1
            cur.execute("SELECT * FROM allwords WHERE id=%s", (i,))
            rows = cur.fetchall()
            df = pd.DataFrame(rows)
            return df.iloc[0, 1], '?', df.iloc[0,0]

    else:
        return 'Learning', 'Words',0