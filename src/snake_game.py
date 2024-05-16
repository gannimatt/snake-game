import tkinter as tk
import random
from mongodb import store_game_result, dump_data_to_json, clear_output_json
from tkinter.simpledialog import askstring

class SnakeGame:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.canvas = tk.Canvas(master, width=400, height=400, bg='black')
        self.canvas.pack()
        self.snake = [(200, 200), (190, 200), (180, 200)]
        self.snake_direction = 'Right'
        self.food = self.place_food()
        self.running = True
        self.score = 0
        self.score_display = self.canvas.create_text(30, 10, text="Score: 0", fill="white", font=('Arial', 14))
        self.restart_text = None
        self.game_loop()
        self.master.bind("<KeyPress>", self.on_key_press)

    def place_food(self):
        while True:
            x = random.randint(0, 39) * 10
            y = random.randint(0, 39) * 10
            if (x, y) not in self.snake:
                self.canvas.create_rectangle(x, y, x + 10, y + 10, fill='red', tag='food')
                return x, y

    def on_key_press(self, event):
        key_map = {'Left': 'Left', 'Right': 'Right', 'Up': 'Up', 'Down': 'Down', 'a': 'Left', 'd': 'Right', 'w': 'Up', 's': 'Down'}
        if (key := event.keysym) in key_map:
            new_direction = key_map[key]
            if not ((new_direction == 'Left' and self.snake_direction == 'Right') or
                    (new_direction == 'Right' and self.snake_direction == 'Left') or
                    (new_direction == 'Up' and self.snake_direction == 'Down') or
                    (new_direction == 'Down' and self.snake_direction == 'Up')):
                self.snake_direction = new_direction
        elif key == 'r' and not self.running:
            store_game_result(self.username,self.score)  # Store result before closing
            dump_data_to_json("C:\\Users\\ganim\\piton\\snake_s29046\\db\\output.json")
            self.canvas.delete('all')
            self.restart_game()
        elif key == 'x' and not self.running:
            store_game_result(self.username,self.score)  # Store result before closing
            dump_data_to_json("C:\\Users\\ganim\\piton\\snake_s29046\\db\\output.json")
            self.master.destroy()

    def restart_game(self):
        self.snake = [(200, 200), (190, 200), (180, 200)]
        self.snake_direction = 'Right'
        self.food = self.place_food()
        self.running = True
        self.score = 0
        self.score_display = self.canvas.create_text(30, 10, text="Score: 0", fill="white", font=('Arial', 14))
        self.game_loop()

    def move_snake(self):
        head_x, head_y = self.snake[0]
        moves = {'Left': (-10, 0), 'Right': (10, 0), 'Up': (0, -10), 'Down': (0, 10)}
        head_x += moves[self.snake_direction][0]
        head_y += moves[self.snake_direction][1]

        new_head = (head_x, head_y)
        if head_x < 0 or head_y < 0 or head_x >= 400 or head_y >= 400 or new_head in self.snake:
            self.running = False
            self.canvas.create_text(200, 200, text="Game Over", fill="white", font=('Arial', 24))
            self.restart_text = self.canvas.create_text(200, 250, text="Press R to play again or X to exit", fill="white", font=('Arial', 14))
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.canvas.delete('food')
            self.food = self.place_food()
            self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")
        else:
            tail = self.snake.pop()
            self.canvas.create_rectangle(tail[0], tail[1], tail[0] + 10, tail[1] + 10, fill='black')
        self.canvas.create_rectangle(head_x, head_y, head_x + 10, head_y + 10, fill='green')

    def game_loop(self):
        if self.running:
            self.move_snake()
            self.master.after(100, self.game_loop)

def main():
    root = tk.Tk()
    root.withdraw()  # Temporarily hide the main window
    root.title("Snake Game")
    username = askstring("Snake Game", "Enter your username:", parent=root)
    if username:
        root.deiconify()  # Re-show the main window
        game = SnakeGame(root, username)
        root.mainloop()
    else:
        root.destroy()


if __name__ == "__main__":
    main()