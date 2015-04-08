import sys;
from math import ceil,sqrt;

def is_prime(num):
    '''can check if a number is prime up to 1000'''
    # all primes than divide numbers less than 1000
    primes = [2,3,5,7,11,13,17,19,23,29,31];
    sqrt_num = ceil(sqrt(num));
    for p in (prime for prime in primes if prime <= sqrt_num):
        if num%p == 0:
            return False;
    
    return True;    
    
def is_palindrome(number):
    '''returns true if number is a palindrome'''
    num = str(number);
    palendrome = True;
    for offset in range(len(num)//2):
        if num[offset-1] != num[-offset]:
            palendrome = False;
            break;
    return palendrome;

if __name__ == '__main__':
    max = 1000;
    prime_countdown = (prime for prime in range(max-1, -1, -2) if is_prime(prime));
    highest_prime_palindrome = (num for num in prime_countdown if is_palindrome(num));
    num = next(highest_prime_palindrome);
    print(num);