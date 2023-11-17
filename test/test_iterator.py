def firstn(n):
    num = 0
    while num < n:
        print(f"before {num}")
        yield num
        print(f"after {num}")
        num += 1


# sum_of_first_n = sum(firstn(10))
nums = firstn(10)
while True:
    a = next(nums)
pass
