class ScoreManager:
    def __init__(self):
        self._score = 0  # Private variable to store the score

    def increment(self, amount: int):
        self._score += amount

    def reset(self):
        self._score = 0

    def get_score(self) -> int:
        return self._score