class LocalVariables:
    def __init__(self, index):
        self.reserved = []
        for i in range(index + 1):
            self.reserved.append(True)

    def reserve(self):
        for i in range(len(self.reserved)):
            if not self.reserved[i]:
                self.reserved[i] = True
                return i

        self.reserved.append(True)
        return len(self.reserved) - 1

    def release(self, index):
        self.reserved[index] = False

    def count(self):
        return len(self.reserved)
