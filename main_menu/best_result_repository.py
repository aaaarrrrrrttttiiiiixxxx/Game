class BestResultRepository:
    def __init__(self):
        self.result = 0

    def save_result(self, result):
        if result > self.result:
            self.result = result
