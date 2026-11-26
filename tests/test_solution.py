import random
import subprocess
import sys


def run(tokens):
    result = subprocess.run(
        [sys.argv[1]], input=" ".join(map(str, tokens)) + "\n",
        text=True, capture_output=True, check=True, timeout=5,
    )
    return list(map(int, result.stdout.split()))


def serialize(tree):
    if tree is None:
        return [-1]
    value, left, right = tree
    return [value] + serialize(left) + serialize(right)


def prune(tree):
    if tree is None:
        return None
    value, left, right = tree
    left, right = prune(left), prune(right)
    return (value, left, right) if value or left or right else None


def generate(depth):
    if depth == 0 or random.random() < 0.3:
        return None
    return (random.randrange(2), generate(depth - 1), generate(depth - 1))


samples = [
    ([1, -1, 0, 0, -1, -1, 1, -2], [1, -1, 0, -1, 1, -1, -1]),
    ([1, 0, 0, -1, -1, 0, -1, -1, 1, 0, -1, -1, 1, -2],
     [1, -1, 1, -1, 1, -1, -1]),
    ([1, 1, 1, 0, -1, -1, -1, 1, -1, -1, 0, 0, -1, -1, 1, -2],
     [1, 1, 1, -1, -1, 1, -1, -1, 0, -1, 1, -1, -1]),
]
for tokens, expected in samples:
    assert run(tokens) == expected

random.seed(2048)
for _ in range(500):
    tree = generate(10)
    tokens = serialize(tree)
    expected = serialize(prune(tree))
    assert run(tokens + [-2]) == expected
    while tokens and tokens[-1] == -1:
        tokens.pop()
    assert run(tokens + [-2]) == expected

n = 49999
assert run([0] * n + [-2]) == [-1]
assert run([0] * (n - 1) + [1, -2]) == [0] * (n - 1) + [1] + [-1] * (n + 1)
right_chain = [item for _ in range(n - 1) for item in (0, -1)] + [1]
assert run(right_chain + [-2]) == right_chain + [-1, -1]
print("Passed samples, 1000 randomized cases, and maximum-depth cases.")
