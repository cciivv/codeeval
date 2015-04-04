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
        self.connected = {};
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
        return hash((self.value,self.depth,parent_value));


class BeadTree(object):
    def __init__(self, root_value, goal_depth):
        self.depth = 1;
        self.goal_depth = goal_depth;
        self.head = BeadNode(root_value, None);
        self.depth_members = defaultdict(lambda: []);
        self.members_depths = defaultdict(lambda: []);
        self.depth_members[1] = [self.head];
        self.members_depths[self.head.value] = [1];
        self.complete_lock = threading.Lock();
        self.completed = 0;
        

    def grow_bud(self, bud, others, results):
        #print("others members_depths - ",others.members_depths);
        #print("growth node input", [x for x in range(1,self.goal_depth+1) if x not in others.members_depths]);
        for growth in bud.next([x for x in range(1,self.goal_depth+1) if x not in others.members_depths]):
            results.append(1);
            self.depth_members[self.depth+1].append(growth);
            self.members_depths[growth.value].append(self.depth+1);
        
        if self.goal_depth - self.depth in others.depth_members:
            #print("goal_depth - depth", self.goal_depth - self.depth);
            #print("others depth members[goal-depth]", others.depth_members[self.goal_depth - self.depth]);
            for bead in [o for o in others.depth_members[self.goal_depth-self.depth] if o.value in CACHE[bud.value]]:
                #print("bead for connection = ", bead);
                if bead.depth + bud.depth == self.goal_depth and bud not in bead.connected:
                    bead.connected[bud] = 1;
                    bud.connected[bead] = 1;
                    #print("-=-=-=-=-Connected to ", bead);
                    self.complete_lock.acquire();
                    #print("-=-=-=-=-incr-=-=-=-=-");
                    if self.head.value in CACHE[others.head.value] and self.goal_depth > 2:
                        self.completed += 1;
                    self.completed += 1;
                    self.complete_lock.release();
            
            

    def grow(self, others):
        threads = [];
        results = [];
        if self.depth in self.depth_members:
            for bud in [ x for x in self.depth_members[self.depth]]:
                #print("growing from bud = ",bud);
                threads.append(threading.Thread(target=self.grow_bud, args=(bud,others,results)));
            for thread in threads:
                thread.start();
            #for thread in threads:
                thread.join();
            #print(self.depth, results);
            if results:
                self.depth += 1;

    def get_num_finished(self):
        return self.completed;


class Necklace(object):
    def __init__(self, beads):
        self.length = beads;
        self.trees = [BeadTree(beads, beads), BeadTree(beads-1, beads)];
        self.completed = 0;
        
        
    def build(self):
        ''' running for len//2 should get all connections''' 
        for _ in range(1, self.length+2//2):
            #print("in build, members_depth = ", self.trees[1].members_depths);
            self.trees[0].grow(self.trees[1]);
            self.trees[1].grow(self.trees[0]);
        for tree in self.trees:
            self.completed += tree.get_num_finished();
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