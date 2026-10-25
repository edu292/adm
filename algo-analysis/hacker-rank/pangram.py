import string

#
# Complete the 'pangrams' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#


def pangrams(s: str):
    alphabet = set(string.ascii_lowercase)

    char_set = set(s.replace(" ", "").lower())
    if char_set == alphabet:
        return "pangram"

    return "not pangram"
