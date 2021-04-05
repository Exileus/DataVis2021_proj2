# Imports
import dash
import ast

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from whitenoise import WhiteNoise

from chessboard import getChessboard, getHeatmap
from styles import *

# Read the .csv file with the preprocessed data.
url = "https://raw.githubusercontent.com/Exileus/DataVis2021_proj2/main/chess_app.csv"
df_original = pd.read_csv(
    url,
    sep=",",
    dtype={"pawns": int, "knights": int, "bishops": int, "rooks": int, "queens": int},
    converters={
        "wKing_sqr": ast.literal_eval,
        "bKing_sqr": ast.literal_eval,
        "wQueen_sqr": ast.literal_eval,
        "bQueen_sqr": ast.literal_eval,
        "wRook_sqr": ast.literal_eval,
        "bRook_sqr": ast.literal_eval,
        "wRook2_sqr": ast.literal_eval,
        "bRook2_sqr": ast.literal_eval,
        "wBishop_sqr": ast.literal_eval,
        "bBishop_sqr": ast.literal_eval,
        "wBishop2_sqr": ast.literal_eval,
        "bBishop2_sqr": ast.literal_eval,
        "wKnight_sqr": ast.literal_eval,
        "bKnight_sqr": ast.literal_eval,
        "wKnight2_sqr": ast.literal_eval,
        "bKnight2_sqr": ast.literal_eval,
    },
)

# Calculate min and max elo
min_elo, max_elo = df_original["avg_Elo"].min(), df_original["avg_Elo"].max()

# Define function to output an 8*8 dataframe based on a df and a list of column names to parse.


def board_output(df, col_list):
    brd = np.zeros((8, 8))
    for col_name in col_list:
        for tup in df[col_name]:
            if tup == (None, None):
                pass
            else:
                brd[tup] += 1

    return pd.DataFrame(brd)


# Define global variables for later.
g_color = "white_color"
g_piece = "King"

# Define a dictionary to be used to update the board with the correct columns.
color_piece_dict = cp_dict = {
    ("white_color", "King"): ["wKing_sqr"],
    ("black_color", "King"): ["bKing_sqr"],
    ("white_color", "Queen"): ["wQueen_sqr"],
    ("black_color", "Queen"): ["bQueen_sqr"],
    ("white_color", "Rook"): ["wRook_sqr", "wRook2_sqr"],
    ("black_color", "Rook"): ["bRook_sqr", "bRook2_sqr"],
    ("white_color", "Bishop"): ["wBishop_sqr", "wBishop2_sqr"],
    ("black_color", "Bishop"): ["bBishop_sqr", "bBishop2_sqr"],
    ("white_color", "Knight"): ["wKnight_sqr", "wKnight2_sqr"],
    ("black_color", "Knight"): ["bKnight_sqr", "bKnight2_sqr"],
}


# Set stylesheets and app.
# ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
external_stylesheets = [dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "CHESS KINGDOM"
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root="static/")


# Defining app layout
margin_bottom = "50px"

# Banner

banner = dbc.Row(
    children=[
        dbc.Col(
            html.Img(
                src="/assets/apple-touch-icon.png",
                id="logo",
                style={"border-radius": "50%"},
            ),
            width=2,
            align="left",
        ),
        dbc.Col(
            html.H1("A Visualization of Endgame Chess Pieces"),
            align="center",
            width=10,
        ),
    ],
    style={"margin-bottom": "50px", "margin-top": "-30px"},
    align="center",
)

# Graph
graph = dcc.Graph(
    id="chessboard",
    config={
        "displayModeBar": False,
        "scrollZoom": False,
        "showAxisDragHandles": False,
    },
)
#
c_white_black = dbc.Col(
    style={"margin-bottom": margin_bottom},
    children=[
        html.Div("Pieces to Visualize"),
        dbc.ButtonGroup(
            [
                dbc.Button(
                    "White",
                    color="secondary",
                    n_clicks=0,
                    id="white_color",
                    outline=True,
                ),
                dbc.Button(
                    "Black",
                    color="dark",
                    n_clicks=0,
                    id="black_color",
                    outline=True,
                ),
            ]
        ),
    ],
)

piece_selector = dbc.ButtonGroup(
    style={"margin-bottom": margin_bottom},
    children=[
        dbc.Button(
            "King",
            color=(button_color := "primary"),
            n_clicks=0,
            outline=True,
            id="King",
        ),
        dbc.Button(
            "Queen",
            color=button_color,
            n_clicks=0,
            outline=True,
            id="Queen",
        ),
        dbc.Button(
            "Rook",
            color=button_color,
            n_clicks=0,
            outline=True,
            id="Rook",
        ),
        dbc.Button(
            "Bishop",
            color=button_color,
            n_clicks=0,
            outline=True,
            id="Bishop",
        ),
        dbc.Button(
            "Knight",
            color=button_color,
            n_clicks=0,
            outline=True,
            id="Knight",
        ),
    ],
)
c_elo_slider = dbc.Col(
    style={"margin-bottom": margin_bottom},
    children=[
        html.Div("Elo range:"),
        dcc.RangeSlider(
            id="elo_slider",
            min=min_elo,
            max=max_elo,
            value=[min_elo, max_elo],
            step=10,
            pushable=1,
            allowCross=False,
            marks={
                i: str(i)
                for i in range(
                    int(min_elo) - 1,
                    int(max_elo) + 1,
                    int((max_elo - min_elo + 2) // 10),
                )
            },
        ),
    ],
)
c_moves_slider = dbc.Col(
    style={"margin-bottom": margin_bottom},
    children=[
        html.Div("Game duration Slider (Moves)"),
        dcc.RangeSlider(
            id="moves_slider",
            min=1,
            max=50,
            value=[8, 30],
            step=1,
            pushable=1,
            allowCross=False,
            marks={i: str(i) for i in range(0, 50, 5)},
        ),
    ],
)

c_total_games = dbc.Col(
    children=[
        dbc.Row(
            style={"margin-bottom": margin_bottom},
            children=[html.Div("Total Games"), html.Div(id="game_count")],
        ),
        dbc.Row(
            style={"margin-bottom": margin_bottom},
            children=[html.Div("White Wins"), html.Div(id="white_wins")],
        ),
        dbc.Row(
            style={"margin-bottom": margin_bottom},
            children=[html.Div("Black Wins"), html.Div(id="black_wins")],
        ),
        dbc.Row(
            style={"margin-bottom": margin_bottom},
            children=[html.Div("Draws"), html.Div(id="draw")],
        ),
    ]
)

c_dropdown = dbc.Col(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem("Status", header=True),
            dbc.DropdownMenuItem("All"),
            dbc.DropdownMenuItem("Draws"),
            dbc.DropdownMenuItem("Checkmate"),
            dbc.DropdownMenuItem("Resignation"),
            dbc.DropdownMenuItem("Time Forfeit"),
        ],
        label="Status",
    )
)

app.layout = dbc.Jumbotron(  # ADD SETTINGS HERE
    children=[
        # Banner
        # Main Layout
        dbc.Row(  # ADD SETTINGS HERE
            children=[
                # PARAMETER SETTINGS COLUMN
                dbc.Col(
                    children=[
                        banner,
                        c_white_black,
                        piece_selector,
                        c_elo_slider,
                        c_moves_slider,
                        c_dropdown,
                        c_total_games,
                    ]
                ),
                # CHESS BOARD COLUMN
                dbc.Col(width={"size": 6}, children=[graph]),
            ],
        ),
    ],
)


@app.callback(
    Output("chessboard", "figure"),
    Output("game_count", "children"),
    Output("white_wins", "children"),
    Output("black_wins", "children"),
    Output("draw", "children"),
    Input("white_color", "n_clicks"),
    Input("black_color", "n_clicks"),
    Input("King", "n_clicks"),
    Input("Queen", "n_clicks"),
    Input("Rook", "n_clicks"),
    Input("Bishop", "n_clicks"),
    Input("Knight", "n_clicks"),
    Input("elo_slider", "value"),
    Input("moves_slider", "value"),
)
def update_chessboard(
    white_color,
    black_color,
    King,
    Queen,
    Rook,
    Bishop,
    Knight,
    elo_range,
    move_range,
):
    # Filters go here.
    dff = df_original[
        (df_original["avg_Elo"] >= int(elo_range[0]))
        & (df_original["avg_Elo"] <= int(elo_range[1]))
        & (df_original["moves"] >= int(move_range[0]))
        & (df_original["moves"] <= int(move_range[-1]))
    ]

    # Before further manipulation, get the number of games from the filtered dataframe.
    game_count = dff.shape[0]
    game_results = dff.Winner.value_counts().to_dict()

    if "white" in game_results.keys():
        white_wins = game_results["white"]
    else:
        white_wins = 0
    if "black" in game_results.keys():
        black_wins = game_results["black"]
    else:
        black_wins = 0
    if "draw" in game_results.keys():
        draw = game_results["draw"]
    else:
        draw = 0

    # Then retrieve the column of interest.
    global g_color
    global g_piece

    trigger_button = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if trigger_button in ["white_color", "black_color"]:
        g_color = trigger_button
    if trigger_button in ["King", "Queen", "Rook", "Bishop", "Knight"]:
        g_piece = trigger_button

    df = board_output(dff, cp_dict[g_color, g_piece])

    # Transform it for the heatmap.
    df = (
        df.stack()
        .reset_index()
        .rename(columns={"level_0": "rows", "level_1": "cols", 0: "freq"})
    )
    df["rows"] = df["rows"].replace({i: list(range(8))[::-1][i] for i in range(8)})
    chessboard = getChessboard(800)
    chessboard.add_trace(getHeatmap(dataframe=df))

    return chessboard, game_count, white_wins, black_wins, draw


# Statring the dash app
if __name__ == "__main__":
    app.run_server(debug=True)
