class HeaderSet(list):
    def __init__(self, headers=None):
        if headers:
            headers = [h.split(':', 1) if isinstance(h, str) else h for h in headers]
            headers = [(k.strip(), v.strip()) for k, v in headers]
        super().__init__(headers)

