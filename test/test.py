class a:
    def __init__(self):
        self.q = 1

class b(a):
    def __init__(self):
        super().__init__()
        super().q = 3
        print(super().q)
        print(self.q)