import sys;
from collections import defaultdict;
import random;
import time;

class WordStripNode(object):
    def get_beginning(self):
        #print("self {}, prev {}".format(self, self.prev));
        if self.prev != self:
            return self.prev.get_beginning();
        else:
            return self;
    
    def get_front_string(self, length):
        return self.value[:length];

    def get_end_string(self, length):
        return self.value[self.length-length:];

    
    def __init__(self,value, hash_len):
        self.value = value;
        self.prev = self;
        self.next = self;
        self.length = len(value);
        self.front_hash = self.get_front_string(hash_len);
        self.end_hash = self.get_end_string(hash_len);
        self.build_str = self.get_end_string(self.length - hash_len);

    def get_build_string(self,idx):
        if idx:
            return self.build_str;
        return '';

    def merge_strip(self, hash_len):
        nodes = self.get_beginning();
        strip = [nodes.get_front_string(nodes.length)];
        strip.extend([ next.get_build_string(idx) for idx,next in enumerate(nodes)]);
        
        while nodes.next:
            nodes.prev = None;
            temp = nodes.next;
            nodes.next = None;
            nodes = temp;
        return WordStripNode(''.join(strip), hash_len);
        
    def set_prev(self, node):
        #print("setting previous");
        if not self.prev or self.prev != node:
            self.prev = node;
            node.set_next(self);
    
    def set_next(self, node):
        #print("setting next");
        if not self.next or self.next != node:
            self.next = node;
            node.set_prev(self);

    def __len__(self):
        return self.length;
            
    def __str__(self):
        return self.value;
        
    def __repr__(self):
        return self.value;#"'{}' [front '{}',end '{}']".format(self.value,self.front_hash,self.end_hash);
    
    def __hash__(self):
        return hash(self.value);
        
    def __iter__(self):
        temp = self;
        yield temp;
        while temp.next != temp:
            yield temp.next;
            temp = temp.next;
        raise StopIteration;
    
    def __eq__(self, other):
        return self.value == other.value;
     
     
class WordStrip(object):
    
    def _remove(self, node, search_hash, hash_string):
        self.unused_nodes.pop(node);
        #print(search_hash);
        #print(hash_string);
        #print(node);
        search_hash[hash_string].remove(node);
        if not search_hash[hash_string]:
            search_hash.pop(hash_string);

        self.remaining -= 1;

    def _build_search_hash(self, type):
        search_hash = defaultdict(lambda: []);
        
        adder = (lambda node: print("error", node));
        if type == 'backward':
            adder = (lambda node: search_hash[node.end_hash].append(node));
        elif type == 'forward':
            adder = (lambda node: search_hash[node.front_hash].append(node));
        
        for node in self.unused_nodes:
            adder(node);
        return search_hash;
    
    
    def _match_in_direction(self, starter, direction='forward', run=0):
        get_match_string = (lambda node: print("error", node));
        set_direction = (lambda node: print("error 2", node));
        if direction == 'backward':
            get_match_string = (lambda node: node.get_front_string(self.hash_len));
            get_search_string = (lambda node: node.get_end_string(self.hash_len));
            set_direction = (lambda node_list, new_member: node_list.set_prev(new_member));
        elif direction == 'forward':
            get_match_string = (lambda node: node.get_end_string(self.hash_len));
            get_search_string = (lambda node: node.get_front_string(self.hash_len));
            set_direction = (lambda node_list, new_member: node_list.set_next(new_member));

        search_hash = self._build_search_hash(direction);

        
        match = get_match_string(starter);
            
        #print("starting with '{}'".format(starter), "'{}' '{}'".format(direction, get_match_string(starter)));
        #print("starting search_hash", search_hash);
        end = starter;
        can_match = True;
        matched = 0;
        while can_match and self.remaining:
            #print("searching this hash", search_hash);
            match_list = search_hash.setdefault(match);
            if match_list:
                #print("'{}' matched to [{}]".format(match, match_list));
                len_list = len(match_list);
                if len_list == 1:
                    matched += 1;
                    connection = match_list[0];
                    #print("matched with '{}'".format(connection));
                    self._remove(connection, search_hash, get_search_string(connection));
                    set_direction(end, connection);
                    end = connection;
                    match = get_match_string(connection);
                    #print("new match string = '{}'".format(match));
                else:
                    #print("matched multiple", match_list);
                    can_match = False;
            else:
                can_match = False;
            
        merged = [];
        #print("merging if not zero", matched);
        if matched:
            merged.append(end.merge_strip(self.hash_len));
            #for merger in merged:
            #    print(" New string = '{}'['{}' '{}']".format(merger,merger.front_hash, merger.end_hash));
        else:
            merged.append(starter);
        #time.sleep(5);
        return merged;
            
    def _build_strip(self):
        #print("\n\n\n {} remain, unused = ".format(self.remaining), self.unused_nodes);

        merged = [];
        starter = random.choice(list(self.unused_nodes.keys()));
        self.unused_nodes.pop(starter);
        self.remaining -= 1;
        #print(starter);
        
        next_results = self._match_in_direction(starter,direction='backward');
        merged.extend(self._match_in_direction(next_results[0], run = 1));
        #print(merged);
        return merged;

    def __init__(self, unused):
        self.unused_nodes = {};
        self.duplicate_nodes = defaultdict(lambda: []);
        
        self.remaining = 0;
        self.remaining_duplicates = 0;
        self.max_key = 0;
        self.min_key = 0;
        self.found_duplicates = False;
        
        self.remaining = len(unused);
        #self.hash_len = min(len(snip) for snip in unused) - 1;
        #assume all snips same length
        self.hash_len = len(unused[0]) - 1;
        for node in unused:
            temp = WordStripNode(node, self.hash_len);
            if temp in self.unused_nodes or temp in self.duplicate_nodes:
                self.found_duplicates = True;
                self.remaining -= 1;
                #print("duplicate = ", temp);
                self.remaining_duplicates += 1;
                self.duplicate_nodes[temp].append(temp);
            else:
                self.unused_nodes[temp] = temp;
        
        
        merged = [];
        
        while self.remaining != 1 or self.remaining_duplicates != 0:
            #print("unused =", self.unused_nodes);
            merged = self._build_strip();
            for merger in merged:
                self.unused_nodes[merger] = merger;
                self.remaining += 1;
            
            #print("now there are", self.remaining," elements remaining in the unused list = ", self.unused_nodes, "also duplicates remaining =", self.remaining_duplicates);
            keys_to_remove = [];
            for dup in self.duplicate_nodes:
                duplicates = self.duplicate_nodes[dup];
                new_node = duplicates.pop();
                if new_node not in self.unused_nodes:
                    self.remaining_duplicates -= 1;
                    #print("!!!!!!!!!!!!!!!!adding in duplicate!!!!!!!!!!!!!!!!!!!!!!!!", new_node);
                    self.unused_nodes[new_node] = new_node;
                    self.remaining += 1;
                else:
                    duplicates.append(new_node);
                    
                if not duplicates:
                    keys_to_remove.append(dup);
            #if self.found_duplicates:
            #    print("after duplicate injection, there are now", self.remaining, "elements remaining, unused = ", self.unused_nodes);
            for key in keys_to_remove:
                self.duplicate_nodes.pop(key);
        
        self.output = merged[0].value;
        #print(self.output);

def word_glue(pieces):
    strip = WordStrip(pieces);
    return strip.output;    


def test_output(ins, outs, idx):
    for i in range(idx):
        if outs[i] != ins[i]:
            print("line {}, mismatch {} != {}".format(i, output[i], expected_output[i]));
        else:
            print("line {} good".format(i)); 

    
def parse_input():
    lines = [];
    if len(sys.argv) <= 1:
        return 1;
    elif len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            #test = list(line for line in f);
            #for idx,line in enumerate(test):
            #    if idx < 10:
            #        print(line);
            lines = [line.strip('|\n').split('|') for line in f];
        output = [word_glue(line) for line in lines];
       
        print('\n'.join(output));
    else:
        with open(sys.argv[1]) as f:
            lines = [line.strip('|\n').split('|') for line in f];
        output = [word_glue(line) for line in lines];

        print(output);
        output_lines =[]
        with open(sys.argv[2]) as f:
            output_lines = [line.strip() for line in f];
        expected_output = [line for line in output_lines];
        
        test_output(output, expected_output, min(len(output),len(expected_output)));

if __name__ == '__main__':
    parse_input();