class TextManager(dict):
    def __init__(self, data):
        super().__init__(())
        for datum in data:
            assert datum['id'] == datum['category']
            self.setdefault(datum['id'], {})
            self[datum['id']][datum['index']] = datum['text']
