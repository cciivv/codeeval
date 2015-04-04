import sys;
from multiprocessing import Pool, Lock;
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
    
CACHE = {};
def prime_bead_complements(number, max):
    """ take a number and list of available numbers, and return a list of possible complimentary values"""
    return [x for x in range(1,max+1) if x in CACHE[number]];

class BeadNode(object):
    def __init__(self, value, parent):
        self.value = value;
        self.parent = parent;
        self.depth = parent.depth+1 if parent else 1;
        if parent:
            self.chain = parent.chain.copy();
            self.chain[self.value] = self.depth;
        else:
            self.chain = {value: self.depth};
        #print("new node ==", self);

    
    def next(self, possible):
        return [ BeadNode(val, self) for val in possible if val not in self.chain and val in CACHE[self.value]];
            
    def __str__(self):
        parent_value = self.parent.value if self.parent else 0;
        return "[{} (from {}) depth {}-- chain {}, connected to {}]".format(repr(self.value),parent_value,repr(self.depth), self.chain, self.connected);

    def __repr__(self):
        return "{}@depth={}, chain = {}".format(self.value,self.depth,self.chain);
        
    def __hash__(self):
        parent_value = self.parent.value if self.parent else 0;
        return hash((self.value,)+tuple(self.chain.keys()));


class BeadTree(object):
    def __init__(self, root_value, goal_depth):
        self.depth = 1;
        self.goal_depth = goal_depth;
        self.head = BeadNode(root_value, None);
        self.depth_members = defaultdict(lambda: []);
        self.depth_members[1] = [self.head];
        self.complete_lock = Lock();
        self.completed = 0;
        self.work_lock = Lock();
        self.workqueue = [self.head];
        

    def grow_bud(self, bud, results):
        if bud.depth == self.goal_depth and bud in CACHE[self.head.value]:
                #print("-=-=-=-=-Connected to ", bead);
                self.complete_lock.acquire();
                print("-=-=-=-=-incr-=-=-=-=-");
                self.completed += 1;
                self.complete_lock.release();
        else:
            return bud.next([x for x in range(1,self.goal_depth+1)]);
        
    def put_work(buds):
        print(buds);
        self.work_lock.acquire();
        self.workqueue.extend(buds);
        self.work_lock.release();
            

    def grow(self):
        threads = [];
        results = [];
        
        with Pool(processes=4) as pool:
            self.work_lock.acquire();
            while self.workqueue:
                work = [self.workqueue.pop() for _ in range(len(self.workqueue))]
                self.work_lock.release();

                pool.map_async(self.grow_bud, work, callback=self.put_work).wait();
                
                self.work_lock.acquire();
            
            self.work_lock.release();

    def get_num_finished(self):
        return self.completed;


class Necklace(object):
    def __init__(self, beads):
        self.length = beads;
        self.tree = BeadTree(beads, beads);
        self.completed = 0;
        
        
    def build(self):
        ''' running for len should get all connections''' 
        for _ in range(1, self.length):
            self.tree.grow();
        self.completed += self.tree.get_num_finished();
    def __str__(self):
        pass;


def prime_compliment_cache():
    for n in range(1,19):
        if n not in CACHE:
            CACHE[n] = {};
            for c in [x for x in range(1,19) if x != n and x%2 != n%2]:
                if (n + c) in primes:
                    CACHE[n][c] = 1;
        
def num_patterns(length):
    #odd numbers can't make proper value since there will always be an even number sum
    if length%2:
        return 0;

    #print("===================START=", length);
    string = Necklace(length);
    string.build();
    return string.completed;


def parse_input():
    if len(sys.argv) <= 1:
        print("need input file argument");
    with open(sys.argv[1]) as f:
        lines = [ int(line.rstrip()) for line in f];
    
    prime_compliment_cache();
    
    print("\n".join([ str(num_patterns(line)) for line in lines]));
    #print(CACHE[1]);

if __name__ == '__main__':
    parse_input();