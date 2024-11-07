class Value:
    def __init__(self, type: "Value", value: object):
        self.type = type
        self.value = value

        self.start_position = None
        self.start_line = None
        self.end_position = None
        self.end_line = None

