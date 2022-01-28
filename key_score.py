class KeyScore:
    def __init__(self, s=0, t=0):
        self.score = s
        self.time = t

    def __repr__(self):
        return f"({self.score}, {self.time})"

    def __lt__(self, other):
        if self.score > other.score:
            return True
        elif self.score < other.score:
            return False
        else:
            if self.time < other.time:
                return True
            else:
                return False
