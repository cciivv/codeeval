import sys;

def string_sub(string, substitutions):
    subs_split = substitutions[0].split(",");
    
    search = [subs_split[i] for i in range(0,len(subs_split),2)];
    replacement = [subs_split[i] for i in range(1,len(subs_split),2)];
    
    for idx,subs in enumerate(search):
        old = string;
        string = string.replace(search[idx],'{{{}}}'.format(idx));
    return string.format(*replacement);

def parse_input():
    lines = [];
    if len(sys.argv) <= 1:
        return 1;
    elif len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            lines = [line.strip().split(';') for line in f];

        output = [string_sub(line[0], line[1:]) for line in lines];
        
        print('\n'.join(output));
    else:
        with open(sys.argv[1]) as f:
            lines = [line.strip().split(';') for line in f];
        output = [string_sub(line[0], line[1:]) for line in lines];
        
        output_lines =[]
        with open(sys.argv[2]) as f:
            output_lines = [line.strip() for line in f];
        expected_output = [line for line in output_lines];
        
        for idx in range(len(output)):
            if output[idx] != expected_output[idx]:
                print("line {}, mismatch {} != {}".format(idx, output[idx], expected_output[idx]));
            else:
                print("line {} good".format(idx));
            
if __name__ == '__main__':
    parse_input();