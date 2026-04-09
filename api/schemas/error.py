class ErrorResponse:
    """Schema para resposta de erro"""

    def __init__(self, status_code, message, details=None):
        self.status_code = status_code
        self.message = message
        self.details = details

    def to_dict(self):
        response = {
            'status_code': self.status_code,
            'message': self.message,
        }
        if self.details:
            response['details'] = self.details
        return response
