# auth/models.py

class User:
    def __init__(self, email, name, provider):
        self.email = email
        self.name = name
        self.provider = provider  # google / facebook