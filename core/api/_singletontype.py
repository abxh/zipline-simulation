class SingletonType(type):
    """
    This class is used to generate singleton typed classes.
    """

    _instances: dict[str, object] = {}

    def __call__(cls, *args, **kwargs):
        """
        The code below is invoked, whenever a class is created by the use
        of this class as a metaclass.

        The code in this method can be described by following pseudocode:
            >>> if class is not recorded:
            >>>     record the class and return it
            >>> else:
            >>>     return the previously recorded class
        """
        # Source:
        # https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
