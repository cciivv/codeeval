import sys;

def sentence_reconstructor(words):
    return ' '.join([words[i] for i in range(1,len(words)+1)]);

def input_parser(line):
    scrambled_sentence, swap_indices = line.rstrip().split(';');
    
    scrambled_sentence = scrambled_sentence.split();
    swap_indices = swap_indices.split();
    
    swap_indices = [int(entry) for entry in swap_indices];
    missing_no = sum(range(1,len(scrambled_sentence)+1));
    
    words = {};
    for i in range(len(swap_indices)):
        num = swap_indices[i];
        missing_no -= num;
        words[num] = scrambled_sentence[i];
    if missing_no:
        words[missing_no] = scrambled_sentence[-1];

    return words;
    
def codeeval_input_output():
    if len(sys.argv) <=1:
        print("need input file");
    else:
        input_lines = [];
        with open(sys.argv[1]) as f:
            input_lines = [line for line in f];
            
        output = [sentence_reconstructor(input_parser(line)) for line in input_lines];
        print('\n'.join(output));

if __name__ == '__main__':
    codeeval_input_output();