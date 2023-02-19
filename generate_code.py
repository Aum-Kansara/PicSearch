import random
import string


def generateEventCode():
    code_length = 6
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for i in range(code_length))
    return code