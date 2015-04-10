import sys;

def percentage_of(denominator):
    return lambda numerator: 100.0 * (numerator / denominator);

def lettercase_percentage(line):
    percentage = percentage_of(len(line));
    lowercase = 0.0;
    uppercase = 0.0;
    
    for l in line:
        if l.isupper():
            uppercase += 1;
        else:
            lowercase += 1;
    p_lower = percentage(lowercase);
    p_upper = percentage(uppercase);
    return "lowercase: {0:.2f} uppercase: {1:.2f}".format(p_lower, p_upper);

def codeeval_input_output():
    if len(sys.argv) <=1:
        print("need input file");
    else:
        input_lines = [];
        with open(sys.argv[1]) as f:
            input_lines = [line for line in f];
            
        output = [lettercase_percentage(line.rstrip()) for line in input_lines];
        print('\n'.join(output));


if __name__ == '__main__':
    codeeval_input_output();