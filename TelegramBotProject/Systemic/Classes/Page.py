class Page:
    def __init__(self, name: str, message_text: str, markup_data: dict[str, dict[str, int|str]] = {}):
        self.name = name
        self.message_text = message_text
        self.markup_data = markup_data
