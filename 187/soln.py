import sys;
from collections import defaultdict;
import time;

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
    #print("testing prime compliments of ", input);
    if (input,range) not in cache:
        comp = [x for x in cache[input[0]] if x <= range and x in cache[input[1]]];
        comp.sort();
        cache[(input,range)] = tuple(comp);
    #print("{} and {} (when max is {}), share compliments = {}".format(a,b,range,cache[(input,range)]));
    return cache[(input,range)];


def extend_prime_gap(last_value, value, max_value, seen, cache):
    last = get_shared_prime_compliments(last_value, value, cache, max_value);
    #print("last value = {}, test_value = {}, max_v = {}, shared compliments = {}".format(last_value,value,max_value,last));
    #print("\t", seen['sequence']);
    if last:
        seen['build'].append(last);
        seen['length'] += 1;
        seen['last'] = value;
        seen['sequence'].append(value);
        seen[value] = 1;    
        return True;
    else:
        return False;

def contract_prime_gap(value, seen):
    seen.pop(value);
    seen['last'] = seen['sequence'].pop();
    seen['length'] -= 1;
    seen['build'].pop();

def prime_gap_helper_edge(max_value, values, seen, cache):
    seq_len = seen['length'];
    last_value = seen['last'];
    test_value = max_value;
    #print("test adding last element");
    if extend_prime_gap(last_value, test_value, max_value, seen, cache):
        seen['done'].append(seen['build'][:]);
        #print("added end", test_value, "to sequence[ = ", seen['sequence']);
        #print("found one edge",seen['sequence'], seen['build']);
        contract_prime_gap(test_value, seen);
        #print("removing end", test_value, "from sequence[ = ", seen['sequence']);
    return seen['done'];

    
def prime_gap_helper(max_value, values, seen, cache):
    seq_len = seen['length'];
    last_value = seen['last'];
    #print("gap helper, len = ", seq_len, "last value = ", last_value, " values = ", values, "max_v =", max_value);
    for number in [x for x in values if x not in seen]:
        if extend_prime_gap(last_value, number, max_value, seen, cache):
            #print("adding ", number, "to sequence[ = ", seen['sequence']);
            if seq_len == (max_value/2)-1:
                last_value = seen['last'];
                test_value = max_value;
                #print("test adding last element");
                if extend_prime_gap(last_value, test_value, max_value, seen, cache):
                    seen['done'].append(seen['build'][:]);
                    #print("added end", test_value, "to sequence [ = ", seen['sequence']);
                    #print("found one     ",seen['sequence'], seen['build']);
                    contract_prime_gap(test_value, seen);
                    #print("removing end", test_value, "from sequence [ = ", seen['sequence']);
            prime_gap_helper(max_value, values, seen, cache);
            contract_prime_gap(number, seen);
            #print("removing ", number, "from sequence[ = ", seen['sequence']);
    return seen['done'];


def get_prime_gapped_permutations(values, cache):
    
    tail = values.pop();
    seen = {tail: 1, 'last': tail, 'length':1, 'sequence':[tail], 'build': [], 'done': []};
    done = [];
    if len(values) == 0:
        return prime_gap_helper_edge(tail, values, seen, cache);
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
            if gap[0] in targets:
                return (False, {});
            targets[gap[0]];
    
    for idx, gap in enumerate(gaps):
        gaps[idx] = [x for x in gap if x not in targets];
    return (True, targets);

def num_ways(gaps, values_seen):
    #print("gaps = ", gaps, "values seen=", values_seen, "len", len(gaps));
    if len(gaps) < 1:
        return 1;
    if len(gaps) == 1:
        return len([x for x in gaps[0] if x not in values_seen]);
    ways = 0;
    for num in (v for v in gaps[0] if v not in values_seen):
            values_seen[num] = 1;
            ways += num_ways(gaps[1:], values_seen);
            values_seen.pop(num);
    return ways;

def uniques_exist(gaps):
    if not gaps:
        return False;
    for x in gaps:
        if len(x) == 1:
            return True;
    #return len(min(gaps, key=len)) == 1
    return False;

def no_path_exists(gaps, all_removed, max_value):

    global num_no_path;
    global num_multi;
    needed = (max_value+1)//2 - len(all_removed);
    len_dict = defaultdict(lambda: defaultdict(lambda: 0));
    if not needed:
        return False;
    for gap in gaps:
        tgap = tuple(gap);
        len_dict[len(gap)][tgap] += 1;
        if needed:
            for n in gap:
                if n not in all_removed:
                    all_removed[n] = 1;
                    needed -= 1;
    if needed:
        num_no_path += 1;
        return True;

    for length in len_dict:
        for set in len_dict[length]:
            if len_dict[length][set] > length:
                #print(len_dict[length]);
                num_multi += 1;
                return True;
    
    return False;
    
num_double_single = 0;
num_no_path = 0;
num_multi = 0;
def num_odd_fills(gaps, max_value):
    global num_double_single;
    idx = 0;
    #print(gaps);
    no_double_singletons = True;
    all_removed = {};
    while uniques_exist(gaps) and no_double_singletons:
        #print("\t",gaps);
        no_double_singletons, removed = remove_singletons(gaps);
        all_removed.update(removed);
    
    
    gaps = list(filter(bool,gaps));
    if no_path_exists(gaps, all_removed, max_value):
        if not no_double_singletons:
            num_double_single += 1;
        return 0;
    
    #print("then", gaps, "no_double_singletons =", no_double_singletons);
    
    if no_double_singletons:
        if len(gaps) == 0:
            return 1;
        gaps.sort(key=len);
        result = num_ways(gaps, {});
        #if not result:
        #    print("zero gap = ",gaps, "\n");
        return result;
    else:
        num_double_single += 1; 
        return 0;
    
def num_patterns(length, cache):
    #odd numbers can't make proper value since there will always be an even number sum
    
    global num_double_single;
    global num_no_path;
    global num_multi;
    if length%2:
        return 0;

    #build the cache if it hasn't been already
    prime_compliment_cache(cache);
    print("start", length);
    evens = [x for x in range(1,length+1) if not x%2];
    t = time.time();
    gaps = get_prime_gapped_permutations(evens, cache);
    print(len(gaps));
    num_double_single = 0;
    num_no_path = 0;
    num_multi = 0;
    max_per_gap = defaultdict(lambda: 0);
    result = 0;
    for gap in gaps:
        temp = num_odd_fills(gap,length);
        max_per_gap[temp]+=1;
        result += temp;
    #result = sum( map( num_odd_fills, gaps));
    print("time = ", (time.time() - t));
    print("bad gaps", num_double_single);
    print("no path gaps", num_no_path);
    print("no multi", num_multi);
    print("gap result distribution",max_per_gap);
    return result;

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