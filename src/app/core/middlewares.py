class UpdateLastActivityMiddleware:
    """"Upgrade last_activity en cada solicitud del usuario"""

    def __init__(self, get_response):
        self.get_response = get_response
