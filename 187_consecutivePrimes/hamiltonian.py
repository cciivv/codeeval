import sys

#since input is always less than 18, max sum = 35
#below are all primes less than 35
#(that can be created by adding numbers that are monotonically increasing)
primes = { 3: 0, 5: 0, 7: 0, 11: 0, 13: 0, 17: 0, 19: 0, 23: 0, 29: 0, 31: 0};

class PrimeGraph(object):    
    def create_prime_sum_graph(self, vertexes):
        graph = [[]];
        for v in vertexes:
            graph.append([[]]);
            for n in vertexes:
                connect = 1 if (v+n) in primes else 0;
                graph[v].append(connect);

        graph[0] = graph.pop();
        for idx, col in enumerate(graph):
            col[0] = col.pop();
        return graph;
         
    def __str__(self):
        rows = []
        for row in range(self.highest):
            rows.append("  ".join([str(self.graph[x][row]) for x in range(self.highest)]));
        return "\n".join(rows);
    
    def permanent():
        for i in range(self.num_vertexes):
            for n in range(self.num_vertexes):
                row = (i+n)%self.num_vertexes;
                col = n;
                val = self.graph[row][col];
                if not val:
                    break;
                elif not row or not col:
                    #multiply in special val
                else:
                    #multiply in symettric val
        for i in range(self.num_vertexes):
        
        pass;
    
    def __init__(self, vertexes):
        self.num_vertexes = len(vertexes);
        self.graph = self.create_prime_sum_graph(vertexes);
        self.__repr__ = self.__str__;

def num_hamiltonians(graph):
    pass;
    
def num_prime_necklaces(num_beads):
    if num_beads%2:
        return 0;
        
    print("start", num_beads);
    graph = PrimeGraph(list(range(1,num_beads+1)));
    print(str(graph), "\n\n");
    
    return num_hamiltonians(graph);


def parse_input():
    if len(sys.argv) <= 1:
        print("need input file argument");
    with open(sys.argv[1]) as f:
        inputs = [ int(line.rstrip()) for line in f];
    
    print("\n".join([str(num_prime_necklaces(num_beads)) for num_beads in inputs]));
    #print(CACHE[1]);

if __name__ == '__main__':
    parse_input();