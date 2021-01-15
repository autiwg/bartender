from uuid import uuid4


def generate_invite_token():
    return str(uuid4())[:8]
