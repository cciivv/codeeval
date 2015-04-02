import sys;

def find_cycle(line):
    mu = -1;
    for sep in range(1,len(line)):
        tort = len(line)-1;
        hare = tort - sep;
        if line[hare] == line[tort]:
            mu = sep;
            break;
        if mu >= 0:
            break;
    
    for first in range(0,len(line)-mu):
        if line[first] == line[first+mu]:
            break;
    cyc = line[first:first+mu];
    return cyc;
    
def cycle_finder():
    if len(sys.argv) <= 1:
        print("need input file");
    with open(sys.argv[1]) as f:
        inputs = [line.rstrip().split() for line in f];
    
    output = [' '.join(find_cycle(input)) for input in inputs];
    print("\n".join(output));

if __name__ == '__main__':
    cycle_finder()