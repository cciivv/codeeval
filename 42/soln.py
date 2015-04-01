import sys;
from collections import defaultdict;
import time;

def add_def_zero(table, key, value):
    if key not in table:
        table[key] = 0;
    table[key] += value;
        
def combo_mt(left, right, mod_len):
    """
    elements in left and right need to be combined to find which values they add up to
    """
    mt = defaultdict(lambda:0);
    if len(left) != len(right):
        if len(left) != 0 and len(right) == 0:
            return left;
        elif len(left) == 0 and len(right) != 0:
            return right;
    for l in left:
        for r in right:
            ind = (l,r);
            ind_val = (left[l], right[r])
            adding = abs(l + r);
            subing = abs(l - r)
            combo =  left[l] * right[r];
            mt[adding%mod_len] += combo;
            mt[subing%mod_len] += combo;
            #add_def_zero(mt, adding%mod_len, combo);
            #add_def_zero(mt, subing%mod_len, combo);
    return mt;

def add_mt(left, right):
    """
    elements in each dict are distinct solutions (i.e. different pairings of the same sequence)
    """
    mt = defaultdict(lambda: 0);
    for l in left:
        mt[l] += left[l];
        #add_def_zero(mt, l, left[l]);
    for r in right:
        mt[r] += right[r];
        #add_def_zero(mt, r, right[r]);
    return mt;
    
def mt_val(n, mod_val):
    if len(n) == 0:
        return None;
    num = int(n);
    temp_mt = {(num%mod_val): 1};
    return temp_mt;

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
    
def mt_seq(seq, mods_gcm):
    if len(seq) == 0:
        return {};
    if len(seq) == 1:
        return mt_val(seq[0], mods_gcm);
    lft = left(seq);
    #combination of the left and right halves possible values
    combo_table = combo_mt(mt(lft, mods_gcm), mt(right(seq), mods_gcm),mods_gcm);
    #add in mod value for the whole sequence as a value
    coverall_table = mt(''.join(seq), mods_gcm);
    combo_table = add_mt(combo_table, coverall_table);
    #then add in all the combinations when the two halves are combined
    for window_size in range(2,len(seq)):
        windows = window_bounds(window_size, len(seq), len(lft));
        for window in windows:
            before_table = mt(seq[:window[0]], mods_gcm);
            during_table = mt(''.join(seq[window[0]:window[1]+1]), mods_gcm);
            temp_combo = combo_mt(before_table, during_table, mods_gcm);
            after_table = mt(seq[window[1]+1:], mods_gcm); 
            temp_table = combo_mt(temp_combo, after_table, mods_gcm);
            combo_table = add_mt(combo_table, temp_table);
    return combo_table;

def mt(seq, mods_gcm):
    """ 
    seq: a list of individual digits 
    mods: numbers to check mods of
    """
    cases = {list: lambda t,p: mt_seq(t,p), \
            str: lambda t,p: mt_val(t,p)};
    #check for empty sequence or empty string?
    try:
        mt = cases[type(seq)](seq,mods_gcm);
        return mt;
    except KeyError:
        print("KeyError");
        return None;

num_strip = []
if (len(sys.argv) <= 1):
    print("bad input");
else:
    with open(sys.argv[1]) as f:
        num_lists = [list(line.rstrip()) for line in f];
    primes = [2,3,5,7];
    gcm = 1;
    for p in primes:
        gcm *= p;
    for sequence in num_lists:
        mtable = mt(sequence,gcm);
        uglies = defaultdict(lambda: 0);
        uglies_num = 0;
        for p in primes:
            for mp in range(0,gcm,p):
                if mp in mtable:
                    if mp not in uglies:
                        uglies[mp] += mtable[mp];
                        uglies_num += mtable[mp];
        stop = time.time();
        print(uglies_num);