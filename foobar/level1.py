import string

def solution(x):
    chars = string.ascii_lowercase
    reverse = chars[::-1]
    d = {}
    for a, b in zip(reverse, chars):
        d[a] = b
    return ''.join(map(lambda c: d[c] if d.get(c) else c, x))

print(solution('A ab'))