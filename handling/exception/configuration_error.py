class ConfigurationError(Exception):
    """
    Raised when any manner of configuration sins happen
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
