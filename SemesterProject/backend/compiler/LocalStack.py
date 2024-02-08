class LocalStack:
    def __init__(self):
        self.size = 0
        self.maxSize = 0

    def reset(self):
        self.size = 0
        self.maxSize = 0

    def getSize(self):
        return self.size

    def increase(self, amount):
        self.size += amount
        self.maxSize = max(self.maxSize, self.size)

    def decrease(self, amount):
        self.size -= amount
        if self.size < 0:
            self.size = 0

    def capacity(self):
        return self.maxSize