import sys;
from collections import defaultdict;
import time;

class MismatchedInputError(Exception):
    def __init__(self, value):
        self.value = value;
    def __str__(self):
        return repr(self.value);

def combo_mt(left, right):
    mt = [];
    if len(left) != len(right):
        if len(left) != 0 and len(right) == 0:
            return left;
        elif len(left) == 0 and len(right) != 0:
            return right;
        else:
            raise MismatchedInputError((len(left), len(right)));
    for idx in range(len(left)):
        mod_val = len(left[idx]);
        mods = defaultdict(lambda: 0);
        if len(left[idx]) != len(right[idx]):
            raise Mi/smatchedInputError((idx, len(left[idx]), len(right[idx])));
        pairs = [(i,j) for i in range(mod_val) for j in range(mod_val)];
        for pair in pairs:
            adding = pair[0] + pair[1];
            subing = pair[0] - pair[1];
            if adding < 0:
                adding = -1 * adding;
            if subing < 0:
                subing = -1 * subing;
            mods[adding%mod_val] += left[idx][pair[0]] * right[idx][pair[1]];
            mods[subing%mod_val] += left[idx][pair[0]] * right[idx][pair[1]];
        mt.append(list(mods.values()));
    return mt;

def add_mt(left, right):
    mt = [];
    #print("add_mt, type left", type(left), "type right", type(right));
    if len(left) != len(right):
        raise MismatchedInputError((len(left), len(right)));
    for idx in range(len(left)):
        if len(left[idx]) != len(right[idx]):
            raise MismatchedInputError((idx, len(left[idx]), len(right[idx])));
        mods = [left[idx][j] + right[idx][j] for j in range(len(left[idx]))]
        mt.append(mods);
    return mt;

class ValueGroup():
    def __init__(self, value):
        self.d = dict();
        self.l = [];
    def __str__(self):
        return "d = {}, l = {}".format(repr(self.d), repr(self.l));
    def values(self):
        return self.l;
    def add(self, value):
        if value not in self.d:
            self.l.append(value);
    def __iter___(self):
        self.index = 0;
        return self;
    def __next__(self):
        if self.index == len(self.l):
            raise StopIteration;
        else:
            data = self.l[self.index];
            self.index += 1;
            return data;
    
def mt_val(n, cache, mods):
    #print("mt_val", n, type(n));
    if len(n) == 0:
        return None;
    num = int(n);
    if num not in cache:
        temp_mt = [];
        for p in mods:
            mt = [];
            for m in range(p):
                mt.append( 0 if num%p != m else 1);
            temp_mt.append(mt);
        cache[num] = temp_mt;
    #else:
        #print("\t\t\t\t\t\tcache HIT");
    #print("val = ", cache[num]);
    return cache[num];

def left(A):
    return A[:(len(A)//2)]

def right(A):
    return A[int((len(A) + 0.5)//2):len(A)]

def window_bounds(size, total_len, split):
    """
    size: size of window
    total_len: total length of list
    split: index of first element of right split
    """    
    windows = [];
    num_win = min(total_len - split, split, size - 1, total_len - size + 1);
    front = lambda t: (max(0, split - (size - 1)) + t)
    back = lambda t: (max(split, split + (size - split -1)) + t);
    for i in range(num_win):
        windows.append((front(i), back(i)));
    return windows;
    
def mt_seq(seq, cache, mods):
    #print("mt_seq", seq);
    if ''.join(seq) not in cache:
        if len(seq) == 0:
            return [];
        if len(seq) == 1:
            #print("seq val call", int(seq[0]));
            return mt_val(seq[0], cache, mods);
        lft = left(seq);
        #combination of the left and right halfs possible values
        combo_table = combo_mt(mt(lft, cache, mods), mt(right(seq), cache, mods));
        #print("mt_seq combo of split sequences (left = {}, right = {}) is ..\n{}".format(lft, right(seq), combo_table));
        #add in mod value for the whole sequence as a value
        combo_table = add_mt(combo_table, mt(''.join(seq), cache, mods));
        #print("mt seq add combination of two sides ({} {}), gives ...\n{}".format(''.join(lft), ''.join((seq)), combo_table));
        #then add in all the combinations when the two halves are combined
        for window_size in range(2,len(seq)):
            windows = window_bounds(window_size, len(seq), len(lft));
            for window in windows:
                #print("\t\tadding for window {}".format(''.join(seq[window[0]:window[1]+1])));
                before_table = mt(seq[:window[0]],cache, mods);
                #print("\tbefore ({}) = {}".format(seq[:window[0]], before_table));
                during_table = mt(''.join(seq[window[0]:window[1]+1]), cache, mods)
                #print("\tduring table ({}) = {}".format(''.join(seq[window[0]:window[1]+1]), during_table));
                temp_combo = combo_mt(before_table, during_table);
                #print("\ttemp combo ({} and {}) table = {}".format(seq[:window[0]], ''.join(seq[window[0]:window[1]+1]), temp_combo));
                after_table = mt(seq[window[1]+1:], cache, mods); #after
                #print("\tafter ({}) = {}".format(seq[window[1]+1:], after_table));
                temp_table = combo_mt(temp_combo, after_table);
                #print("\ttemp_table [({} and {}) and {}] table = {}".format(\
                #                                                seq[:window[0]], \
                #                                                ''.join(seq[window[0]:window[1]+1]),\
                #                                                seq[window[1]+1:],\
                #                                                temp_table));
                                            
                #print("\t\ttable for window {} is {}".format(''.join(seq[window[0]:window[1]+1]), temp_table));
                combo_table = add_mt(combo_table, temp_table);\
                                    #combo_mt(combo_mt(mt(seq[:window[0]],cache, mods), #before \ 
                                    #                mt(''.join(seq[window[0]:window[1]+1]), cache, mods)), #during \
                                    #        mt(seq[window[1]+1:], cache, mods))); #after
        #print("final mod table for {} is ...\n{}".format(seq,combo_table));
        cache[''.join(seq)] = combo_table;
    return cache[''.join(seq)];
def mt(seq, cache, mods):
    """ 
    seq: a list of individual digits 
    cache: dict of cached modtables for digit span (represented as a join of digits)
    mods: numbers to check mods of
    """
    cases = {list: lambda t,c,p: mt_seq(t,c,p), \
            str: lambda t,c,p: mt_val(t,c,p)};
    #check for empty sequence or empty string?
    try:
        return cases[type(seq)](seq,cache,mods);
    except KeyError:
        print("KeyError");
        return None;

num_strip = []
if (len(sys.argv) <= 1):
    print("bad input");
else:
    with open(sys.argv[1]) as f:
        num_lists = [list(line.rstrip()) for line in f];
    cache = {};
    primes = [2,3,5,7];
    gcm = 1;
    for p in primes:
        gcm *= p;
    for sequence in num_lists:
        start = time.time();
        mtable = mt(sequence,cache,[gcm]);
        stop_mt = time.time();
        uglies = defaultdict(lambda: 0);
        uglies_num = 0;
        #print(mtable);
        for p in primes:
            for idx in range(0,gcm,p):
                if mtable[0][idx] != 0:
                    if idx not in uglies:
                        uglies_num += mtable[0][idx];
                        uglies[idx] = 1;
                        #print("\tuglies hit, ", idx, "with prime", p, "there are ", uglies[idx], "ways to get this value");
        stop = time.time();
        print(" took {} time for mod_table calculation".format(stop_mt - start));
        print(" took {} time total".format(stop - start));
        print(uglies_num);