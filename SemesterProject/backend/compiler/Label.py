class Label:
    index = 0

    def __init__(self):
        Label.index += 1
        self.label = "L" + str(Label.index).zfill(3)

    def __str__(self):
        return self.label
