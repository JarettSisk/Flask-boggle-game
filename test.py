from unittest import TestCase
from flask import json
from flask.json import jsonify

from werkzeug.test import Client
from app import app, boggle_game
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    def test_home_route(self):
        with app.test_client() as client:
            """Checks that we are getting back our index.html template"""
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertIn("<h1>BOGGLE!</h1>", html)

    def test_start_game(self):
        with app.test_client() as client:
            """Checks to ensure we are getting the board as json, and that the list is not empty"""
            res = client.get("/start-game")
            res_json = res.get_json()

            self.assertIn("game-board", res_json)
            self.assertIsNot(len(res_json["game-board"]), 0)
    
    def test_game_over(self):
        with app.test_client() as client:
            """Check for valid response, and that boggle_game.high_score == highScore"""
            res = client.post("/game-over", json={"highScore" : 10})
            res_json = res.get_json()

            self.assertIn("games-played", res_json)
            self.assertEqual(boggle_game.high_score, 10)
            self.assertIsInstance(res_json["games-played"], int)

    def test_submit_guess(self):
        with app.test_client() as client:
            """Check for response key, The returned results value will effect the scoring logic on front end"""
            res = client.post("/submit-guess", json={"guess" : "j"})
            res_json = res.get_json()

            self.assertIn("result", res_json)

