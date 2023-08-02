class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.conversation = []
        self.access_level = 0  # Set the default access level to 0 (no special access)

    def add_message(self, message_content, is_private=False):
        self.conversation.append((message_content, is_private))

    def get_last_message(self):
        if self.conversation:
            return self.conversation[-1][0]
        else:
            return None
