import sys;

def output_n_longest():
    if len(sys.argv) <= 1:
        print("need input file");
    with open(sys.argv[1]) as f:
        input = [list(line.rstrip()) for line in f];
    n = int(''.join(input.pop(0))); 
    lines = [ (len(line), line) for line in input];
    lines.sort(reverse=True);
    output = [ ''.join(lines[idx][1]) for idx in range(min(len(lines), n))];
    print("\n".join(output));
    

if __name__ == '__main__':
    output_n_longest();