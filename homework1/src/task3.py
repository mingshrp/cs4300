# Explanation: 
# 1. Check if a number is positive, negative, or zero
# 2. Generate the first ten prime numbers
# 3. Calculate the sum of numbers from 1 to 100 using while loop

# if statement
def check_number(num):
    if num > 0:
        return "Positive"
    elif num < 0:
        return "Negative"
    else:
        return "Zero"

# for loop - first 10 prime #s
# func to check if num is prime 
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def first_ten_primes():
    primes = []
    num = 2

    while len(primes) < 10:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes
    
# while loop - sum 1-100
def sum_1_to_100():
    total = 0
    num = 1
    while (num<=100):
        total += num
        num += 1 
    return total