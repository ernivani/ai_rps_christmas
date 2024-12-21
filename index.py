import tkinter as tk
import random
import time

class RPSAI:
    choices = ["Rock", "Paper", "Scissors"]

    def __init__(self, name: str):
        self.name = name
        self.current_choice = ""
        self.score = 0

    def play(self) -> str:
        self.current_choice = random.choice(self.choices)
        return self.current_choice

def decide_winner(ai1: RPSAI, ai2: RPSAI) -> str:
    """
    Returns:
      - "Tie" if the choices are the same
      - ai1's name if ai1 wins
      - ai2's name if ai2 wins
    """
    if ai1.current_choice == ai2.current_choice:
        return "Tie"

    if (
        (ai1.current_choice == "Rock" and ai2.current_choice == "Scissors") or
        (ai1.current_choice == "Scissors" and ai2.current_choice == "Paper") or
        (ai1.current_choice == "Paper" and ai2.current_choice == "Rock")
    ):
        return ai1.name
    else:
        return ai2.name

class RPSGameUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Rock-Paper-Scissors AI vs AI")

        # Create the AI objects
        self.ai1 = RPSAI("AI 1")
        self.ai2 = RPSAI("AI 2")

        # Add game state variables
        self.is_running = False
        self.delay = 1000  # Delay between games in milliseconds

        # Score labels
        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(pady=5)
        
        self.ai1_score = tk.Label(
            self.score_frame,
            text=f"{self.ai1.name}: 0",
            font=("Arial", 14)
        )
        self.ai1_score.pack(side=tk.LEFT, padx=10)
        
        self.ai2_score = tk.Label(
            self.score_frame,
            text=f"{self.ai2.name}: 0",
            font=("Arial", 14)
        )
        self.ai2_score.pack(side=tk.LEFT, padx=10)

        # Add Christmas tree canvas
        self.canvas_height = 300
        self.canvas_width = 300
        self.tree_canvas = tk.Canvas(
            self.master,
            height=self.canvas_height,
            width=self.canvas_width,
            bg='white'
        )
        self.tree_canvas.pack(pady=10)
        
        # Tree state
        self.tree_parts = [
            "star",
            "top",
            "middle",
            "bottom",
            "trunk"
        ]
        self.current_tree_state = []
        
        # Initial tree drawing (empty)
        self.draw_tree()

        # A label to display the game result
        self.result_label = tk.Label(
            self.master, 
            text="Welcome to RPS AI vs AI!", 
            font=("Arial", 16)
        )
        self.result_label.pack(pady=10)

        # Labels to display the AI choices
        self.ai1_label = tk.Label(
            self.master, 
            text="", 
            font=("Arial", 14)
        )
        self.ai1_label.pack(pady=5)

        self.ai2_label = tk.Label(
            self.master, 
            text="", 
            font=("Arial", 14)
        )
        self.ai2_label.pack(pady=5)

        # Replace play button with start/pause button
        self.play_button = tk.Button(
            self.master,
            text="Start",
            command=self.toggle_game,
            font=("Arial", 12)
        )
        self.play_button.pack(pady=10)

    def toggle_game(self) -> None:
        """Toggle between starting and pausing the game"""
        self.is_running = not self.is_running
        if self.is_running:
            self.play_button.config(text="Pause")
            self.play_continuous()
        else:
            self.play_button.config(text="Start")

    def play_continuous(self) -> None:
        """Play the game continuously with a delay"""
        if self.is_running:
            self.play_game()
            self.master.after(self.delay, self.play_continuous)

    def draw_tree(self):
        self.tree_canvas.delete("all")
        
        # Define tree part coordinates and shapes
        tree_shapes = {
            "star": lambda: self.tree_canvas.create_text(
                150, 30, text="⭐", font=("Arial", 20)
            ),
            "top": lambda: self.tree_canvas.create_polygon(
                150, 50, 100, 100, 200, 100,
                fill="green", outline="darkgreen"
            ),
            "middle": lambda: self.tree_canvas.create_polygon(
                150, 80, 80, 150, 220, 150,
                fill="green", outline="darkgreen"
            ),
            "bottom": lambda: self.tree_canvas.create_polygon(
                150, 130, 60, 220, 240, 220,
                fill="green", outline="darkgreen"
            ),
            "trunk": lambda: self.tree_canvas.create_rectangle(
                130, 220, 170, 270,
                fill="brown", outline="brown"
            )
        }
        
        # Draw only the parts in current_tree_state
        for part in self.current_tree_state:
            tree_shapes[part]()

    def update_tree(self):
        score_diff = self.ai1.score - self.ai2.score
        
        if score_diff > 0: 
            if len(self.current_tree_state) < len(self.tree_parts):
                self.current_tree_state.append(
                    self.tree_parts[len(self.current_tree_state)]
                )
        elif score_diff < 0: 
            if self.current_tree_state:
                self.current_tree_state.pop()
                
        self.draw_tree()

    def play_game(self) -> None:
        choice1 = self.ai1.play()
        choice2 = self.ai2.play()
        winner = decide_winner(self.ai1, self.ai2)

        self.ai1_label.config(text=f"{self.ai1.name} chose: {choice1}")
        self.ai2_label.config(text=f"{self.ai2.name} chose: {choice2}")

        # Update scores
        if winner == self.ai1.name:
            self.ai1.score += 1
        elif winner == self.ai2.name:
            self.ai2.score += 1

        # Update score display
        self.ai1_score.config(text=f"{self.ai1.name}: {self.ai1.score}")
        self.ai2_score.config(text=f"{self.ai2.name}: {self.ai2.score}")
        
        # Update the Christmas tree
        self.update_tree()

        if winner == "Tie":
            self.result_label.config(text="It's a tie!")
        else:
            self.result_label.config(text=f"Winner: {winner}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RPSGameUI(root)
    root.mainloop()
