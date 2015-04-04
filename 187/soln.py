import sys;
import threading;
from collections import defaultdict;

#since input is always less than 18, max sum = 35
#below are all primes less than 35
#(that can be created by adding numbers that are monotonically increasing)
primes = { 3: 0, 5: 0, 7: 0, 11: 0, 13: 0, 17: 0, 19: 0, 23: 0, 29: 0, 31: 0};

#notes
'''
    even numbers can't be next to each other, nor can odds
    first intuition is to rotate evens or odds through the list and then check
    but it's probably more complex than that, need to go through all permutations
    we can simplify the process by only using values that can sum to a prime,
    will probably reach a state where 
'''


def prime_bead_compliments(number, max, cache):
    """ take a number and list of available numbers, and return a list of possible complimentary values"""
    return [x for x in range(1,max+1) if x in cache[number]];

def prime_compliment_cache(cache):
    if not cache:
        for n in range(1,19):
            cache[n] = {};
            for c in (x for x in range(1,19) if x != n and x%2 != n%2):
                if (n + c) in primes:
                    cache[n][c] = 1;
        #print(cache);


def get_shared_prime_compliments(a, b, cache, range):
    input = (a,b) if b>a else (b,a);
    if (input,range) not in cache:
           cache[(input,range)] = [x for x in cache[input[0]] if x <= range and x in cache[input[1]]];
    return cache[(input,range)];


def extend_prime_gap(last_value, value, max_value, seen, cache):
    last = get_shared_prime_compliments(last_value, value, cache, max_value);
    if last:
        seen['build'].append(last);
        seen['length'] += 1;
        seen['last'] = value;
        seen['sequence'].append(value);
        seen[value] = 1;
        
        return True;
    else:
        return False;


def prime_gap_helper(max_value, values, seen, cache):
    seq_len = seen['length'];
    last_value = seen['last'];
    if seq_len == max_value/2 - 1:
        if extend_prime_gap(last_value, max_value, max_value, seen, cache):
            seen['done'].append(seen['build']);
    else:
        for number in [x for x in values if x not in seen]:
            if extend_prime_gap(last_value, number, max_value, seen, cache):
                prime_gap_helper(max_value, values, seen, cache);
                seen.pop(number);
                seen['last'] = seen['sequence'].pop();
                seen['length'] -= 1;
                seen['build'].pop();
    return seen['done'];


def get_prime_gapped_permutations(values, cache):
    tail = values.pop();
    seen = {tail: 1, 'last': tail, 'length':1, 'sequence':[tail], 'build': [], 'done': []};
    done = [];
    return prime_gap_helper(tail, values, seen, cache);


def popualte_histogram(gaps):
    histogram = defaultdict(lambda: 0);
    for gap in gaps:
        for value in gap:
            histogram[value] += 1;
    return histogram;


def remove_singletons(gaps):
    targets = defaultdict(lambda:1);
    for gap in gaps:
        if len(gap) == 1:
            targets[gap[0]];
        
    for idx, gap in enumerate(gaps):
        gaps[idx] = [x for x in gap if x not in targets];


def num_ways(gaps, values_seen):
    if len(gaps) < 1:
        return -1;
    if len(gaps) == 1:
        return len([x for x in gaps[0] if x not in values_seen]);
    ways = 0;
    for num in (v for v in gaps[0] if v not in values_seen):
            values_seen[num] = 1;
            ways += num_ways(gaps[1:], values_seen);
            values_seen.pop(num);
    return ways;

def num_odd_fills(gaps):
        #know there is going to be at least one since get_prime_permutations
        #only returns possible even sequences
        remove_singletons(gaps);
        return num_ways(gaps, {});
    
def num_patterns(length, cache):
    #odd numbers can't make proper value since there will always be an even number sum
    if length%2:
        return 0;

    #build the cache if it hasn't been already
    prime_compliment_cache(cache);
    
    #print("===================START=", length);
    evens = [x for x in range(1,length+1) if not x%2];
    return sum( map( num_odd_fills, get_prime_gapped_permutations(evens, cache)));

def parse_input():
    if len(sys.argv) <= 1:
        print("need input file argument");
    with open(sys.argv[1]) as f:
        lines = [ int(line.rstrip()) for line in f];
        
    cache = {};

    print("\n".join([ str(num_patterns(line,cache)) for line in lines]));
    #print(CACHE[1]);

if __name__ == '__main__':
    parse_input();