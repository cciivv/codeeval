def increasing_multiples(num, limit):
    n = 1;
    while n <= limit:
        yield n*num;
        n += 1;

def print_multiplication_table(max_input):
    
    table = [\
        [x for x in increasing_multiples(num,max_input)]\
        for num in range(1,max_input+1)];
    
    print('\n'.join(\
            (''.join(("{:>4}".format(value) for value in row)))\
            for row in table));

if __name__ == '__main__':
    print_multiplication_table(12);