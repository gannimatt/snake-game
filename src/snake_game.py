import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=400, height=400, bg='black')
        self.canvas.pack()
        # Start snake in the middle of the canvas, heading right
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
        key = event.keysym
        direction_map = {
            'Left': 'Left', 'Right': 'Right', 'Up': 'Up', 'Down': 'Down',
            'a': 'Left', 'd': 'Right', 'w': 'Up', 's': 'Down'
        }
        if key in direction_map:
            new_direction = direction_map[key]
            # Check for reversing direction
            if (new_direction == 'Left' and self.snake_direction != 'Right') or \
                    (new_direction == 'Right' and self.snake_direction != 'Left') or \
                    (new_direction == 'Up' and self.snake_direction != 'Down') or \
                    (new_direction == 'Down' and self.snake_direction != 'Up'):
                self.snake_direction = new_direction
        elif key == 'r' and not self.running:
            self.canvas.delete('all')
            self.snake = [(200, 200), (190, 200), (180, 200)]
            self.snake_direction = 'Right'
            self.food = self.place_food()
            self.running = True
            self.score = 0
            self.score_display = self.canvas.create_text(30, 10, text="Score: 0", fill="white", font=('Arial', 14))
            self.game_loop()
        elif key == 'x' and not self.running:
            self.master.destroy()

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.snake_direction == 'Left':
            head_x -= 10
        elif self.snake_direction == 'Right':
            head_x += 10
        elif self.snake_direction == 'Up':
            head_y -= 10
        elif self.snake_direction == 'Down':
            head_y += 10

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
    root.title("Snake Game")
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
