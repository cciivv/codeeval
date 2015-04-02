import sys;

cache = {};
primes = [2,3,5,7];
gcm = 210;

def add_def_zero(table, key, value):
    if key not in table:
        table[key] = 0;
    table[key] += value;
    
def combo_mt(left, right):
    """
    elements in left and right need to be combined to find which values they add up to
    """
    mtable = {};
    if len(left) != len(right):
        if len(left) != 0 and len(right) == 0:
            return left;
        elif len(left) == 0 and len(right) != 0:
            return right;
    for l in left:
        for r in right:
            combo =  left[l] * right[r];
            #mt[adding%gcm] += combo;
            #mt[subing%gcm] += combo;
            add_def_zero(mtable, abs(l + r)%gcm, combo);
            add_def_zero(mtable, abs(l - r)%gcm, combo);
    return mtable;

def add_mt(left, right):
    """
    elements in each dict are distinct solutions (i.e. different pairings of the same sequence)
    """
    mt = {};
    for l in left:
        #mt[l] += left[l];
        add_def_zero(mt, l, left[l]);
    for r in right:
        #mt[r] += right[r];
        add_def_zero(mt, r, right[r]);
    return mt;
    
def mt_val(n):
    global cache;
    num = int(n);
    if num not in cache:
        temp_mt = {(num%gcm): 1};
        cache[num] = temp_mt;
        return temp_mt;
    return cache[num];

def left(A):
    return A[:(len(A)//2)]

def right(A):
    l = len(A);
    return A[int((l + 0.5)//2):l]

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

def mt_seq(seq):
    global cache;
    joined = ''.join(seq);
    if joined not in cache:
        seq_len = len(seq);
        if seq_len == 0:
            return {};
        if seq_len == 1:
            return mt_val(seq[0]);
        lft = left(seq);
        lft_len = len(lft);
        #combination of the left and right halves possible values
        #add in mod value for the whole sequence as a value
        combo_table = add_mt( combo_mt(mt(lft),mt(right(seq))), mt(joined));
        #then add in all the combinations when the two halves are combined
        for window_size in range(2,seq_len):
            windows = window_bounds(window_size, seq_len, lft_len);
            for window in windows:
                combo_table = add_mt( \
                                combo_table, \
                                combo_mt( \
                                    combo_mt( \
                                        mt(seq[:window[0]]), \
                                        mt(''.join(seq[window[0]:window[1]+1]))
                                        ), \
                                    mt(seq[window[1]+1:])
                                    )
                                );
        cache[joined] = combo_table;
        return combo_table;
    return cache[joined];


cases = {list: lambda t: mt_seq(t), \
        str: lambda t: mt_val(t)};
    
def mt(seq):
    """ 
    seq: a list of individual digits
    """
    return cases[type(seq)](seq);
    
def count_uglies(mtable, primes):
    uglies = {}
    uglies_num = 0;
    for p in primes:
        for mp in range(0,gcm,p):
            if mp in mtable:
                #have to make sure not to double count...
                if mp not in uglies:
                    add_def_zero(uglies, mp, mtable[mp]);
                    uglies_num += mtable[mp];
    return uglies_num;

def find_uglies():
    if (len(sys.argv) <= 1):
        print("bad input");
    else:
        with open(sys.argv[1]) as f:
            num_lists = [list(line.rstrip()) for line in f];
        uglies = [];
        for sequence in num_lists:
            mtable = mt(sequence);
            uglies.append(count_uglies(mtable, primes));
        print("\n".join(str(x) for x in uglies));

if __name__ == '__main__':
    find_uglies();