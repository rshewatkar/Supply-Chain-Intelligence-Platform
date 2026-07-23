from app.utils.helpers import (
    batch_iterator,
    current_timestamp,
    generate_uuid,
    timer,
    truncate_text,
)


print(generate_uuid())

print(current_timestamp())

print(truncate_text("Supply Chain Intelligence Platform", 15))


numbers = list(range(10))

for batch in batch_iterator(numbers, 3):
    print(batch)


@timer
def sample():

    total = 0

    for i in range(1000000):
        total += i

    return total


sample()

print("Helpers test passed.")