import sys;
from itertools import cycle;

def hill_generator( cycler):

    def cycles(char):
        if char.isalpha():
            if next(cycler)%2 == 0:
                return char.upper();
            else:
                return char.lower();
        else:
            return char;
    def hillify(word):
        return ''.join(cycles(char) for char in word);
        
    return hillify;
    
    

def rollercoaster(line):
    hills = hill_generator(cycle(range(2)));
    output = ''.join((hills(word) for word in line.strip()));
    return output;
    
    
def input_parser(line):
    return line;

def codeeval_input_output():
    if len(sys.argv) <=1:
        print("need input file");
    else:
        input_lines = [];
        with open(sys.argv[1]) as f:
            input_lines = [line for line in f];
            
        output = [rollercoaster(input_parser(line)) for line in input_lines];
        print('\n'.join(output));


if __name__ == '__main__':
    codeeval_input_output();