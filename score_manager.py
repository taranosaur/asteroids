import json

class ScoreManager:
    def __init__(self, file_path="high_score.json"):
        self.file_path = file_path
        self.current_score = 0
        self.high_score = self.load_high_score()

    def add_score(self, points):
        """Add points to the current score."""
        self.current_score += points
        if self.current_score > self.high_score:
            self.high_score = self.current_score
            self.save_high_score()

    def reset_score(self):
        """Reset the current score."""
        self.current_score = 0

    def get_current_score(self):
        """Return the current score."""
        return self.current_score

    def get_high_score(self):
        """Return the high score."""
        return self.high_score

    def load_high_score(self):
        """Load the high score from the JSON file."""
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return data.get("high_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0  # Default to 0 if the file doesn't exist or is invalid

    def save_high_score(self):
        """Save the high score to the JSON file."""
        with open(self.file_path, "w") as file:
            json.dump({"high_score": self.high_score}, file)
