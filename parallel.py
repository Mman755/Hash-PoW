import hashlib
import concurrent.futures


#------------------------------------------------------#
# This is a naive attempt at trying to parallelise
# the work among multiple processors, does not seem to
# work too well however and my brings my CPU temp to 100+ LOL.
# However I thought I might try it anyways as I have some experience
# in parallelism in Java.
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

def worker(name, target, start_nonce, end_nonce):
    nonce = start_nonce
    max_score = 0
    best_nonce = None

    while True:
        current_hash = compute_hash(name, nonce)
        current_score = score_hash(target, current_hash)

        if current_score > max_score:
            max_score = current_score
            best_nonce = nonce
            print(nonce)

            if max_score >= 15:
                print("We are done here")
                return best_nonce, max_score

        nonce += 1

    return best_nonce, max_score

def find_nonce_parallel(name, target):
    NUM_WORKERS = 5 # Adjust based on your available cores
    CHUNK_SIZE = 10000000  # Adjust based on desired range for each worker

    best_nonce = None
    max_score = 0

    with concurrent.futures.ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = [executor.submit(worker, name, target, i * CHUNK_SIZE, (i+1) * CHUNK_SIZE - 1) for i in range(NUM_WORKERS)]

        for future in concurrent.futures.as_completed(futures):
            nonce, score = future.result()
            if score > max_score:
                max_score = score
                best_nonce = nonce
                print(f"New best score: {max_score} with nonce {best_nonce}")

                if max_score > 20:
                    break

    return best_nonce

if __name__ == '__main__':
    name = "Manjot Mann"
    target = "21e8000000000000000000000000000000000000000000000000000000000000"
    best_nonce = find_nonce_parallel(name, target)

    print(f"The best nonce found is: {best_nonce}")
