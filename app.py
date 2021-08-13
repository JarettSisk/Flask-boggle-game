# Imports
import re
from flask import Flask, json, request, render_template, session, redirect, jsonify
from flask.wrappers import Response
from werkzeug.utils import redirect
app = Flask(__name__)
app.secret_key = "my_secret_key"

from boggle import Boggle

# Init new game
boggle_game = Boggle()


@app.route("/")
def home_route():
    global boggle_game
    """Home route, sets games played and highscore if browser refreshes"""
    GAMES_PLAYED = boggle_game.games_played
    HIGH_SCORE = boggle_game.high_score
    return render_template("index.html", games_played=GAMES_PLAYED, high_score=HIGH_SCORE)

@app.route("/start-game")
def start_game_route():
    """Creates the board and starts the game"""
    session
    GAME_BOARD = boggle_game.make_board()
    session["game-board"] = GAME_BOARD

    return jsonify({"game-board" : GAME_BOARD}) 

@app.route("/game-over", methods=["POST"])
def game_over_route():
    """Increments the amount of times played when the game is over and sets the high score on our boggle_game class"""
    global boggle_game
    # Increment the games played
    boggle_game.games_played += 1
    # Set new high score if higher then current
    new_high_score = request.get_json()["highScore"]
    if new_high_score > boggle_game.high_score:
        boggle_game.high_score = new_high_score
    return jsonify({"games-played" : boggle_game.games_played})



@app.route("/submit-guess", methods=["POST"])
def submit_guess_route():
    global boggle_game
    """Checks the request to see if the guess is valid, then returns the response"""
    guess = request.get_json()["guess"]
    # if no session exists
    if session.get("game-board") == None:
        # create the board and set session to be it
        GAME_BOARD = boggle_game.make_board()
        session["game-board"] = GAME_BOARD
    else:
        # else game board equal to existing session session
        GAME_BOARD = session["game-board"]

    
    result = boggle_game.check_valid_word(GAME_BOARD, guess)
    return jsonify({"result" : result})
