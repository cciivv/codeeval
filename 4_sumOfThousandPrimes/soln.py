from math import ceil,sqrt;

def prime_generator(needed, primes):
    def is_prime(num):
        '''can check if a number is prime up to 1000'''     
        sqrt_num = ceil(sqrt(num));
        for p in (prime for prime in primes if prime <= sqrt_num):
            if num%p == 0:
                return False;
        primes.append(num);
        return True;
        
    n = 2;
    count = 1;
    yield n;
    n += 1;
    while count < needed:
        #print(n);
        if is_prime(n):
            #print("yielding", n);
            yield n;
            count += 1;
        n += 2;
    
def prime_sum(first_n):
    primes = prime_generator(first_n, [2]);
    return sum(prime for prime in primes);
    
if __name__ == '__main__':
    print(prime_sum(1000));