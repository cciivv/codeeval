import sys

def fizz_buzz(fizz_mod, buzz_mod, count):
    out = [];
    for num in range(1,count + 1):
        if num%fizz_mod == 0 and num%buzz_mod == 0:
            out.append("FB");
        elif num%fizz_mod == 0:
            out.append("F");
        elif num%buzz_mod == 0:
            out.append("B");
        else:
            out.append(str(num));
    return out;

ins = [];
out = [];
if len(sys.argv) <= 1:
    #print("BAD ARGS");
    sys.exit();
else:
    with open(sys.argv[1]) as f:
        ins = [line.strip("\n").split() for line in f];
        
    for line in ins:        
        #if len(line) != 3:
            #print("not enough args, line =", line);
        #    continue;
        #try:
        fizz_mod = int(line[0]);
        buzz_mod = int(line[1]);
        count = int(line[2]);
        #except ValueError:
            #print("could not use line =", line);
        #    continue;
        out.append(' '.join(fizz_buzz(fizz_mod, buzz_mod, count)));
    print('\n'.join(out), end = '');