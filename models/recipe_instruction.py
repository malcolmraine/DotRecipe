class RecipeInstruction(object):
    def __init__(self, text="New instruction"):
        self.text = text

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.text
