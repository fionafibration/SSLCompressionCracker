# Inspired by the CRIME attack on SSL compression
# Original code from https://pastebin.com/qZdNYgfr by xorninja

import string
import zlib
from itertools import product
from functools import reduce
from progress.bar import Bar


HEADERS = (b"POST / HTTP/1.1\r\n"
           b"Host: thebankserver.com\r\n"
           b"Connection: keep-alive\r\n"
           b"User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1\r\n"
           b"Accept: */*\r\n"
           b"Referer: https://thebankserver.com/\r\n"
           b"Accept-Encoding: gzip,deflate,sdch\r\n"
           b"Accept-Language: en-US,en;q=0.8\r\n"
           b"Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3\r\n"

           # Here's our secret token!
           b"Cookie: secret=2ac8a4ea7909bccb4c81cefd3f7765d4\r\n\r\n")

BODY = b"Cookie: secret="

# So we don't append them every loop
TOTAL = HEADERS + BODY

# All our printable characters
CHARSET = [bytes([c]) for c in string.printable.encode("utf-8")]
# CHARSET = [bytes([c]) for c in range(0, 256)]

# Count of total compression calls
total_compressions = 0


def logistic_normalization(n):
    # https://www.desmos.com/calculator/soj6memcfo
    pass


# Compute a simple heuristic of a candidate
def basic_heuristic(candidate):
    score = 0

    for char in candidate:
        pass


def crack_compression(secret_length=16, matched=b"", target=0, working_product=None, candidate_length=1):
    global total_compressions

    # If we've got enough characters, go on and exit out
    if len(matched) >= secret_length:
        return matched,

    # If we don't already have a list of stuff to begin with, then start with printables
    if working_product is None:
        current_product = set(CHARSET[:])

    # Otherwise try every combination of printables with the best matches from the parent caller
    else:
        current_product = set(product(working_product, CHARSET))

        current_product = set(reduce(lambda a, b: a + b, item) for item in current_product)

    # Get our baseline size
    if target == 0:
        c = zlib.compressobj()

        target = len(c.compress(TOTAL +
                                matched) + c.flush(zlib.Z_SYNC_FLUSH))

    # What we already know is matched
    print("Current matched: %s" % matched)

    # Candidate length
    print("Trying candidates of length: %s" % candidate_length)

    # Total number of things to try
    # Num of previous matches * len(printables)
    # Or just len(printables)
    print("Number of permutations: %s" % len(current_product))

    # Target to achieve. This is the length that was achieved the last try
    print("Target: %s" % target)

    # This is going to be a dictionary of all the compressed lengths of our tries
    length_dict = {}

    # Loading bar
    loading = Bar("Processing")

    # For every group of characters
    for group in loading.iter(current_product):
        total_compressions += 1

        # Compress it and add the length to our table
        c = zlib.compressobj()

        grouplen = len(c.compress(TOTAL +
                                  matched +
                                  group) + c.flush(zlib.Z_SYNC_FLUSH))

        length_dict[group] = grouplen

    # Best length
    # Can be shared by multiple keys
    best_length = min(length_dict.values())

    # Grab all our keys that have the min length
    best_keys = list(filter(lambda x: length_dict[x] == best_length, length_dict.keys()))

    best_keys.sort()

    # Number of keys
    # If it's one then we've matched a character
    unique = len(best_keys)

    # Print some data
    print("Best length is: %s" % best_length)

    print("Number of candidates: %s" % unique)

    print("Candidates: %s" % best_keys[:256])

    # Only one character is shorter
    # Huzzah!
    if unique == 1:
        print("Found Unique!")
        print()

        # Now work from what we already had matched + what we just matched
        matched = matched + list(best_keys)[0]

        return crack_compression(secret_length, matched, best_length)

    elif candidate_length >= 8 * secret_length:
        return best_keys

    # Multiple things could work
    # Try and distinguish with another character
    else:
        print("No Unique!")
        print()

        if unique <= 5:
            second_best_keys = list(filter(lambda x: length_dict[x] == best_length + 1, length_dict.keys()))

            second_best_keys.sort()

            best_keys.extend(second_best_keys[:30])

        # Same as above except we're not matching anything
        # Instead we're supplying all our possible matches so we can brute force them with another character
        return crack_compression(secret_length, matched, best_length, best_keys, candidate_length + 1)


results = crack_compression()
print("\n" * 3)
print("*" * 70)
print("\n")
print("Total Compressions: %s" % total_compressions)
print("Decoded result:")
print("-" * 30)
for result in results:
    print(result.decode("utf-8"))
    print("\n" + "-" * 30)
