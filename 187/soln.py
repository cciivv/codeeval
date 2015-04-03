import sys;

#since input is always less than 18, max sum = 35
#below are all primes less than 35
#(that can be created by adding numbers that are monotonically increasing)
primes = { 3: 0, 5: 0, 7: 0, 11: 0, 13: 0, 17: 0, 19: 0, 23: 0,29: 0, 31: 0};

#notes
'''
    even numbers can't be next to each other, nor can odds
    first intuition is to rotate evens or odds through the list and then check
    but it's probably more complex than that, need to go through all permutations
    we can simplify the process by only using values that can sum to a prime,
    will probably reach a state where 
'''
    

def prime_complements(number, available):
    """ take a number and list of available numbers, and return a list of possible complimentary values"""
    compliment = [];
    for trial in [ x for x in available if x%2 != number%2]:
        if (number + trial) in primes:
            compliment.append(trial);
    return compliment;

    

class BeadNode(object):
    def __init__(self, value, parent, remaining):
        self.value = value;
        self.parent = parent;
        self.remaining = remaining;
        self.possible = prime_complements(self.value, self.remaining);
    
    def next(self):
        if self.possible:
            value = self.possible.pop();
            self.remaining.remove(value);
            return BeadNode(value, self, self.remaining[:]);
        else:
            return None;
            
    def prev(self):
        self.parent.remaining.append(self.value);
    
    def __str__(self):
        return "{} {} {}".format(repr(self.value),repr(self.remaining),repr(self.possible));



class Necklace(object):
    def __init__(self, beads):
        if beads <= 0:
            return None;
        self.length = 1;
        self.max_length = beads;
        self.beads = beads;
        self.head = BeadNode(beads, None, list(range(1,beads)));
        self.tail = self.head;
        self.completed = [];
        
    def add_bead(self):
        next = self.tail.next();
        if next:
            self.tail = next;
            self.length += 1;
            return True;
        else:
            return False;
    
    def remove_bead(self):
        self.tail.prev();
        self.tail = self.tail.parent;
        self.length -= 1;
        
    def build(self):
        while self.head.possible or self.tail.possible:
            #print(self);
            while self.add_bead():
                #print("\t bead added\n\t", self);
                if self.length == self.max_length:
                    #print("END REACHED");
                    self.completed.extend(prime_complements(self.head.value, [self.tail.value]));
            self.remove_bead();
    
    def __str__(self):
        chain = [];
        p = self.tail;
        while p:
            chain.insert(0,str(p));
            p = p.parent;
        return '->'.join(chain);

def num_patterns(length):
    string = Necklace(length);
    string.build();
    return len(string.completed);


def parse_input():
    if len(sys.argv) <= 1:
        print("need input file argument");
    with open(sys.argv[1]) as f:
        lines = [ int(line.rstrip()) for line in f];
    
    print("\n".join([ str(num_patterns(line)) for line in lines]));

if __name__ == '__main__':
    parse_input();