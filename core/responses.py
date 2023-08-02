import random

# Function to generate response based on user object
def generate_response(user):
    last_message = user.get_last_message()
    p_message = last_message.lower() if last_message else ""

    if 'hello' in p_message:
        return f'Hey! your id are : {user.user_id}'

    if 'roll' in p_message:
        if user.access_level >= 1:  # Check if the user has access level 1 or higher to use this command
            return str(random.randint(1, 6))
        else:
            return "You don't have permission to use this command."

    if '!help' in p_message:
        if user.access_level >= 2:  # Check if the user has access level 2 or higher to use this command
            return "`This is a help message that you can modify.`"
        else:
            return "You don't have permission to use this command."

    # Default response if no specific condition is met
    return 'Yeah, I don\'t know. Try typing "!help".'
