class ProgressModel:
    def __init__(self, percentage: float = 0):
        self.percentage = percentage
        self._request_update = None