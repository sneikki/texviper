import json

with open('src/utils/literals.json', 'r') as literals_file:
    literals = json.load(literals_file)


def get_literal(name):
    """ Returns a literal from literals file by a key

    Args:
        name (str): Name of the literal

    Returns:
        str: Corresponding literal or None if no literal was found
    """
    return literals[name] if name in literals else None
