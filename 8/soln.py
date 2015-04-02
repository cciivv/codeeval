import sys;

def reverse_words():
    if len(sys.argv) <= 1:
        print("need input file");
    with open(sys.argv[1]) as f:
        lines = [ list(line.rstrip().split(" ")) for line in f];
    
    output = [];
    for line in lines:
        output.append(" ".join([ line[x] for x in range(len(line)-1, -1, -1)]));
    print ("\n".join(output));

if __name__ == '__main__':
    reverse_words();