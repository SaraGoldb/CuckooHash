from BitHash import BitHash, ResetBitHash

# I hereby certify that this program is solely the result of my own work and 
# is in compliance with the Academic Integrity policy of the course syllabus 
# and the academic integrity policy of the CS department.
# Signed Chaya (Sarale) Goldberger, 05/21/2023

class Node(object):
    def __init__(self, k, d):
        self.key = k
        self.data = d

class CuckooHash(object):
    
    # Given an int called size, initialize a CuckooHash object with two empty 
    # lists of size length, and an attribute of 0 keys so far.
    # Ensure that the input parameter size if is greater than 0.
    def __init__(self, size):
        assert size > 0
        self.__hashArr1 = [None] * size
        self.__hashArr2 = [None] * size
        self.__numKeys = 0
        
    # Return how many keys have been inserted into the CuckooHash    
    def __len__(self): return self.__numKeys 
        
    # Given a key, search the CuckooHash arrays for the data associated with it.
    # If the key can be found, return its data. Otherwise return None.
    def find(self, k):
        # Try to find the given key in array 1 by hashing the key and looking
        # at the corresponding position in the array. If found, return its data.
        pos = BitHash(k, 1) % len(self.__hashArr1)
        n = self.__hashArr1[pos]
        if n and n.key == k: return n.data
        
        # If they key could not be found find in array 1, try with array 2.
        pos = BitHash(k, 2) % len(self.__hashArr2)
        n = self.__hashArr2[pos]
        if n and n.key == k: return n.data
        
        # If the key could not be found in either, return None
        return None
    
    # Insert a new node with the given key and data.
    def insert(self, k, d):
        # Return False if key is already in either hash array
        if self.find(k): return False

        # If the arrays are getting too full, i.e. the amount of keys is more
        # than half the underlying storage, grow them and then try insert.
        if self.__numKeys >= len(self.__hashArr1): self.__grow()
        
        # Create a new Node with the key-data pair
        n = Node(k, d)
        
        # Starting with the first array
        arr, arrNum = self.__hashArr1, 1
        # for no more than 16 total loops
        for i in range(16):
            # Hash the key into the current array
            pos = BitHash(n.key, arrNum) % len(arr)
            # if the position in current array is empty, insert, increment 
            # numKeys, and return True
            if not arr[pos]: 
                arr[pos] = n
                self.__numKeys += 1
                return True                      
            
            # If the position is filled, push n into that position and
            # attempt to reinsert the evicted Node into the other array by 
            # changing the arr and arrNum pointers and looping again.
            # The loop will stop either when all Nodes have been successfully 
            # inserted and the method returns True or if there is an infinite 
            # eviction loop.
            arr[pos], n = n, arr[pos]
            if arrNum == 1: arr, arrNum = self.__hashArr2, 2
            else:           arr, arrNum = self.__hashArr1, 1 
           
        # If we've made it here, insertion has failed because we ran into an
        # infinite eviction loop. Solution: rehash, grow both arrays, and 
        # reinsert everything. Then reattmept the insert with the most recently
        # displaced Node.
        self.__grow()
        self.insert(n.key, n.data)
    
    # Grow the arrays, reset bithash, rehash and reinsert everything.
    def __grow(self):
        # Reset the bit hash
        ResetBitHash()
        
        # Increase the size of the arrays by 1.5 (as not to be too crazy with
        # the amount of storage we are using up).
        size = int(len(self.__hashArr1)*1.5)
        
        # Create a temporary CuckooHash object of size array length
        temp = CuckooHash(size)
        
        # for each Node in both arrays, insert into temp
        for i in range(len(self.__hashArr1)):
            if self.__hashArr1[i]: 
                temp.insert(self.__hashArr1[i].key, self.__hashArr1[i].data)
            if self.__hashArr2[i]: 
                temp.insert(self.__hashArr2[i].key, self.__hashArr2[i].data)
                                
        # Set the arrays to point to the new arrays.
        self.__hashArr1 = temp.__hashArr1
        self.__hashArr2 = temp.__hashArr2
        temp = None  # Garbage collect temp

    
    # Given a key, find and delete the corresponding Node, and return the key
    # data pair as a tuple. Otherwise, return None.
    def delete(self, k):
        # Try to find the given key in array 1 by hashing the key and looking
        # at the corresponding position in the array. If found, set
        # that pos in the array to None and return the deleted key-data pair.
        pos = BitHash(k, 1) % len(self.__hashArr1)
        n = self.__hashArr1[pos]
        if n and n.key == k: 
            self.__hashArr1[pos] = None
            self.__numKeys -= 1
            return (n.key, n.data)
        
        # If could not be found in array 1, try to find in array 2 and delete.
        pos = BitHash(k, 2) % len(self.__hashArr2)
        n = self.__hashArr2[pos]
        if n and n.key == k: 
            self.__hashArr2[pos] = None
            self.__numKeys -= 1
            return (n.key, n.data)
        
        # if could not find in either, do nothing and return None.
        
    # Accessor str method for printing the CuckooHash object Nodes
    def __str__(self):
        # create a list of all Nodes from both arrays
        temp = []
        for i in range(len(self.__hashArr1)):
            n = self.__hashArr1[i]
            if n: temp += [(n.key, n.data)]
            n = self.__hashArr2[i]
            if n: temp += [(n.key, n.data)]
        
        # return the string of the list
        return str(temp)
    
    # Accessor method that returns the keys in a list
    def getKeys(self):
        # Create a temporary list
        temp = []
        
        # For each non-None node in both hash arrays, add all keys to temp list
        for i in range(len(self.__hashArr1)):
            n = self.__hashArr1[i]
            if n: temp += [n.key]
            n = self.__hashArr2[i]
            if n: temp += [n.key]
            
        # Return the list
        return temp
    
    # Accessor method that returns the data in a list
    def getData(self):
        # Create a temporary list
        temp = []
        
        # For each non-None node in both hash arrays, add all data to temp list
        for i in range(len(self.__hashArr1)):
            n = self.__hashArr1[i]
            if n: temp += [n.data]
            n = self.__hashArr2[i]
            if n: temp += [n.data]      
        
        # Return the list
        return temp
        
    
def __main():
    
    # Initialize a small CuckooHash object
    c = CuckooHash(5)
    
    # Ensure insert works and len returns correctly.
    c.insert("A", 2017)
    print("Insert (A, 2017):", c, flush=True)
    c.insert("B", 5784)
    print("Insert (B, 5784):", c, flush=True)
    c.insert("C", 3333)
    print("Insert (C, 3333):", c, flush=True)
    print("Number of key-data pairs:", len(c)) # 3
    
    print("Keys:", c.getKeys(), flush=True) # a list with 'A', 'B', 'C'
    print("Data:", c.getData(), flush=True) # a list with 2017, 5784, 3333
        
    print("Find A:", c.find("A"), flush=True) # 2017
    print("Find B:", c.find("B"), flush=True) # 5784
    print("Find D:", c.find("D"), flush=True) # None
    
    # Insert more key-data pairs, force grow, ensure none of the old ones 
    # have been removed and there are no duplicates.
    c.insert("D", 4567)
    print("Insert (D, 4567):", c, flush=True)
    c.insert("E", 1717)
    print("Insert (E, 1717):", c, flush=True)
    c.insert("F", 1111)
    print("Insert (F, 1111):", c, flush=True)
    print("Number of key-data pairs:", len(c)) # 6
    
    print("Delete A:", c.delete("A")) # should return ('A', 2017)
    print("Number of key-data pairs:", len(c)) # 5
    print("After delete A:", c, flush=True) # All Nodes should remain except A

    # Initialize a new CuckooHash object
    c = CuckooHash(30)
    num_keys = 20
    
    # insert as a key the characters from A to P
    # with the data starting from 1 to 20
    for i in range(ord('A'), ord('A')+num_keys):
        c.insert(chr(i), i-ord('A')+1)
    print("\nNew CuckooHash (size %d)"%(len(c))) # 20
    
    # Ensure all the keys from A to P can be found, and return the correct data
    print("Keys:", c.getKeys())
    print("Data: ", end="")
    for i in range(ord('A'), ord('A')+num_keys):
        print(c.find(chr(i)), end=' ') 
    
    
if __name__ == '__main__':
    __main()
    

# Created by Sarale Goldberger