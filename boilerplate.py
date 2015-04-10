import sys;
def input_parser(line):
    return line;

def codeeval_input_output():
    if len(sys.argv) <=1:
        print("need input file");
    else:
        input_lines = [];
        with open(sys.argv[1]) as f:
            input_lines = [line for line in f];
            
        output = [*********(input_parser(line)) for line in input_lines];
        print('\n'.join(output));


if __name__ == '__main__':
    codeeval_input_output();