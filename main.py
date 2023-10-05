import hashlib

#------------------------------------------------------#
# This is just a basic brute force attempt at trying
# different nonces and seeing how high we can get.
# Leaving this running for a while, the highest level
# I managed to get was level 9.
#------------------------------------------------------#
def compute_hash(name, nonce):
    data = f"Internship2023{name}{nonce}".encode()
    return hashlib.sha256(data).hexdigest()


def score_hash(target, hash_value):
    score = 0
    for t, h in zip(target, hash_value):
        if t == h:
            score += 1
        else:
            break
    return score


def find_nonce(name, target):
    nonce = 0
    max_score = 0
    best_nonce = None

    while True:
        current_hash = compute_hash(name, nonce)
        current_score = score_hash(target, current_hash)

        if current_score > max_score:
            max_score = current_score
            best_nonce = nonce
            print(f"New best score: {max_score} with nonce {best_nonce}. Hash: {current_hash}")

            if max_score > 100:
                break

        nonce += 1

    return best_nonce


name = "Manjot Mann"
target = "21e8000000000000000000000000000000000000000000000000000000000000"
best_nonce = find_nonce(name, target)

print(f"The best nonce found is: {best_nonce}")