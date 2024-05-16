import sys
import os
import unittest
from unittest.mock import MagicMock
from tkinter import Tk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from snake_game import SnakeGame


class TestSnakeGame(unittest.TestCase):

    def setUp(self):
        self.root = MagicMock()  # Creating a MagicMock object as a dummy master
        self.username = "test_user"  # Provide a dummy username
        self.game = SnakeGame(self.root, self.username)

    def tearDown(self):
        self.root.destroy()

    def test_initial_state(self):
        self.assertEqual(len(self.game.snake), 3, "Initial snake length should be 3 segments.")


    def test_snake_movement(self):
        initial_snake_coords = self.game.snake.copy()
        self.game.snake_direction = 'Right'
        self.game.move_snake()
        self.assertNotEqual(initial_snake_coords, self.game.snake)

    def test_eating_food(self):
        initial_score = self.game.score
        self.game.snake = [(self.game.food[0] - 10, self.game.food[1])]  # Move snake to food location
        self.game.move_snake()  # Move snake to eat food
        self.assertEqual(self.game.score, initial_score + 1)  # Score should increase after eating food
        self.assertEqual(len(self.game.snake), 2)

    # Snake should grow longer after eating food

    def test_game_over_conditions(self):
        # Mocking canvas create_text method to prevent GUI interactions
        self.game.canvas.create_text = MagicMock()
        self.game.snake[0] = (-10, -10)  # Move snake head out of bounds
        self.game.move_snake()
        self.assertFalse(self.game.running)
        self.assertTrue(self.game.canvas.create_text.called)


    def test_snake_growth(self):
        # Ensure the game is running
        self.game.running = True

        # Get the initial length of the snake
        initial_length = len(self.game.snake)

        # Determine the position directly in front of the snake's head based on current direction
        head_x, head_y = self.game.snake[0]
        if self.game.snake_direction == 'Right':
            new_food_position = (head_x + 10, head_y)
        elif self.game.snake_direction == 'Left':
            new_food_position = (head_x - 10, head_y)
        elif self.game.snake_direction == 'Up':
            new_food_position = (head_x, head_y - 10)
        elif self.game.snake_direction == 'Down':
            new_food_position = (head_x, head_y + 10)

        # Move the food to the new position
        self.game.food = new_food_position

        # Move the snake to eat the food
        self.game.move_snake()

        # Check if the snake's length increased by 1 after eating food
        self.assertEqual(len(self.game.snake), initial_length + 1, "Snake should grow longer after eating food")

    def test_direction_change(self):
        initial_direction = self.game.snake_direction
        self.game.on_key_press(MagicMock(keysym='Up'))  # Change direction to 'Up'
        self.assertEqual(self.game.snake_direction, 'Up')  # Snake direction should change to 'Up'
        self.assertNotEqual(self.game.snake_direction, initial_direction)  # Snake direction should not be the same as initial direction

    def test_food_placement(self):
        initial_food_position = self.game.food
        self.game.food = self.game.snake[0]  # Move food to snake's head
        self.game.move_snake()  # Move snake to eat food
        new_food_position = self.game.food
        self.assertNotEqual(new_food_position, initial_food_position)  # New food position should be different from the initial position

if __name__ == '__main__':
    unittest.main()
