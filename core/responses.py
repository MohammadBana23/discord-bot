import random


# Function to generate response based on user object
def generate_response(user):
    last_message = user.get_last_message()
    p_message = last_message.lower() if last_message else ""

    if 'hello' in p_message:
        return f'Hey {user.conversation}! How can I assist you?'

    if 'roll' in p_message:
        return str(random.randint(1, 6))

    if '!help' in p_message:
        return "`This is a help message that you can modify.`"

    # Default response if no specific condition is met
    return 'Yeah, I don\'t know. Try typing "!help".'