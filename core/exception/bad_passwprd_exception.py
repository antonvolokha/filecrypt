class BadPasswordException(RuntimeError):
    def __init__(self):
        super().__init__('Bad password exception')
