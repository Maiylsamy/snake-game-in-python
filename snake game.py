import tkinter as tk
import random


class SnakeGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake Game")
        self.geometry("400x450")

        self.canvas = tk.Canvas(self, width=400, height=400, bg="black")
        self.canvas.pack()

        self.score = 0
        self.score_label = tk.Label(self, text="Score: 0", font=("Arial", 14))
        self.score_label.pack()

        self.restart_button = tk.Button(self, text="Restart", command=self.restart_game)
        self.restart_button.pack()

        self.snake = [(10, 10)]
        self.food = self.generate_food()
        self.direction = (0, 1)

        self.draw_game()
        self.bind("<KeyPress>", self.on_key_press)
        self.update_game()

    def generate_food(self):
        return random.randint(0, 39), random.randint(0, 39)

    def draw_game(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, 400, 400, fill="black")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x * 10, y * 10, (x + 1) * 10, (y + 1) * 10, fill="green")
        x, y = self.food
        self.canvas.create_oval(x * 10, y * 10, (x + 1) * 10, (y + 1) * 10, fill="red")

    def move_snake(self):
        head = self.snake[0]
        dx, dy = self.direction
        new_head = (head[0] + dx, head[1] + dy)
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = self.generate_food()
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
        else:
            self.snake.pop()

    def check_collision(self):
        head = self.snake[0]
        return (
                head[0] < 0 or head[0] >= 40 or
                head[1] < 0 or head[1] >= 40 or
                head in self.snake[1:]
        )

    def update_game(self):
        if self.check_collision():
            self.game_over()
            return
        self.move_snake()
        self.draw_game()
        self.after(100, self.update_game)

    def game_over(self):
        self.score_label.config(text="Game Over! Score: 0")
        self.restart_button.pack()
        self.unbind("<KeyPress>")  # Remove key event binding

    def restart_game(self):
        self.destroy()  # Destroy current instance
        SnakeGame()  # Create new instance

    def on_key_press(self, event):
        key = event.keysym
        if key == "Up" and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == "Down" and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == "Left" and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == "Right" and self.direction != (-1, 0):
            self.direction = (1, 0)


if __name__ == "__main__":
    app = SnakeGame()
    app.mainloop()
