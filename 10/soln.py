import sys;

def mth_from_end(line, num):
    return line[-num] if (len(line) >= num) else ''
        

def parse_input():
    if len(sys.argv) < 1:
        print("need input file");
        return;
    with open(sys.argv[1]) as f:
        lines = [ line.rstrip().split() for line in f];
        
    print('\n'.join(list(
        filter(bool,[str(mth_from_end(line[:-1], int(line[-1])))  for line in lines]))));

if __name__ == '__main__':
    parse_input();