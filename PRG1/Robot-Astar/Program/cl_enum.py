class Enum(set):
    """
    Class used to emulate Enum
    """

    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
