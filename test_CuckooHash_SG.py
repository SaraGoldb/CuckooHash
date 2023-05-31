import pytest
from CuckooHash_SG import CuckooHash
from random import*

# Initialize a CuckooHash object of a given size with a given number of keys.
def makeCuckooHash(size, numKeys):
    c = CuckooHash(size)
    for i in range(numKeys):
        c.insert(str(i), i)  # String i is the key and int i is the data
    return c

# Check if a given str follows the correct CuckooHash str format.
# NOTE: this only works if the int's are single digits.
def compare(s, numKeys):
    # if the str doesn't start or end as a list, it is wrong
    if s[0] != '[' or s[-1] != ']': return False
    
    # Slice off the list brackets
    z = s[1:-1]
    
    # Check sections of the str by each key-data tuple (9 char length sections).
    # Example of a section: "('0', 0), "
    
    # jumping by sections of 9 char length
    for i in range(0, numKeys*9, 10):
        
        # assume the str section is incorrect
        same = False
        
        # the CuckooHash in not in sorted order, so the key-data could be any
        # of the numbers from 0 to numKeys. If the key-data is one of these,
        # then change our same bool variable to True
        for j in range(numKeys):
            if z[i:i+8] == "('%d', %d)"%(j, j): same = True
        
        # if after checking the tuple to be any of the number from 0 to numKeys
        # and the tuple is incorrect or we are not yet at the end of the list
        # and there is no ", " following the tuple, return False
        if same == False or (i+9 < numKeys*9 and z[i+8:i+10] != ", "): 
            return False
    
    # If we've made it here the str is probably correct, so return True.
    # This does not check if the keys inserted are all there, just if the str
    # is correct.
    return True

# Make a small CuckooHash to check that my compare method works correctly
def test_compare():
    size, numKeys = 10, 2
    c = makeCuckooHash(size, numKeys)
    assert str(c) == [('0', 0), ('1', 1)] or [('1', 1), ('0', 0)]
    assert compare(str(c), numKeys) # returns True

# Make a CuckooHash of single digit numbers and check that str returns  
# correctly using my compare method.
def test_str():
    size, numKeys = 50, 5
    c = makeCuckooHash(size, numKeys)
    assert compare(str(c), numKeys)

    size, numKeys = 60, 7
    c = makeCuckooHash(size, numKeys)
    assert compare(str(c), numKeys)
    
    size, numKeys = 70, 10
    c = makeCuckooHash(size, numKeys)
    assert compare(str(c), numKeys)
    
# Make a small CuckooHash to check that len returns numKeys. 
# Note: if I check with a bigger CuckooHash of more keys, the method may 
# crash if insert and grow do not work correctly, which are tested 
# seperatley below.
def test_len():
    size = 5
    numKeys = size//2
    c = makeCuckooHash(size, numKeys)
    assert len(c) == numKeys

# Make a CuckooHash with half of size keys (as we are not testing grow in this
# test and do not want to insert too many keys) and check that find returns
# the int i associated with the string i from 0 to numKeys non-inclusive
def find_true(size):
    numKeys = size//2
    c = makeCuckooHash(size, numKeys)
    for i in range(numKeys):
        assert c.find(str(i)) == i

# Test find on a small CuckooHash
def test_find_true_small():
    find_true(randint(1, 5))
    find_true(randint(7, 10))
    find_true(randint(11, 15))
    
# Test find on a medium CuckooHash
def test_find_true_medium():
    find_true(randint(30, 50))
    find_true(randint(100, 200))
    find_true(randint(300, 500))

# Test find on a large CuckooHash
def test_find_true_large():
    find_true(randint(1000, 2000))
    find_true(randint(5000, 9000))
    find_true(randint(10000, 20000))

# Make a CuckooHash with half of size keys (as we are not testing grow in this
# test and do not want to insert too many keys) and check that find returns
# None for the string i from numKeys to numKeys times two non-inclusive.
def find_false(size):
    numKeys = size//2
    c = makeCuckooHash(size, numKeys)
    for i in range(numKeys, (numKeys*2)):
        assert not c.find(str(i))  

# Test find returns None for keys that are not in a small CuckooHash.
def test_find_false_small():
    find_false(randint(1, 5))
    find_false(randint(7, 10))
    find_false(randint(11, 15))
    
# Test find returns None for keys that are not in a medium CuckooHash.
def test_find_false_medium():
    find_false(randint(30, 50))
    find_false(randint(100, 200))
    find_false(randint(300, 500))
    
# Test find returns None for keys that are not in a large CuckooHash.
def test_find_false_large():
    find_false(randint(1000, 2000))
    find_false(randint(5000, 9000))
    find_false(randint(10000, 20000))    
    
# Test the insert methof works correctly by asserting the length of the 
# CuckooHash matches the number of keys inserted, find returns the right
# data, and finding keys not in the CuckooHash returns None
def insert_test(size, numKeys = -1):
    # Unless otherwise specified, number of keys to insert are a third of size
    if numKeys == -1: numKeys = size//3
    
    # Make a CuckooHash object of the given size with the given number of keys
    c = makeCuckooHash(size, numKeys)
    
    # Make sure the correct amount of keys were inserted
    assert len(c) == numKeys
    
    # Make sure that all the key-data pairs can be found
    #  (the key is the string version of the number and the data is the int
    #  version of the number, starting from 0 till numKeys non-inclusive).
    for i in range(numKeys):
        assert c.find(str(i)) == i
    
    # Make sure that no Nodes were inserted incorrectly. 
    # The numbers from numKeys and on should not have been inserted.
    for i in range(numKeys, numKeys*2):
        assert not c.find(str(i))
    
# Test insert on a small CuckooHash, not forcing the CuckooHash to grow
def test_insert_small():
    insert_test(randint(1, 5))
    insert_test(randint(7, 10))
    insert_test(randint(11, 15))

# Test insert on a medium CuckooHash, not forcing the CuckooHash to grow
def test_insert_medium():
    insert_test(randint(20, 30))
    insert_test(randint(40, 50))
    insert_test(randint(60, 70))

# Test insert on a large CuckooHash, not forcing the CuckooHash to grow
def test_insert_large():
    insert_test(randint(100, 200))
    insert_test(randint(300, 400))
    insert_test(randint(500, 600))

# Force a CuckooHash to grow by inserting a small amount more than size keys
def test_insert_force_grow_small():
    insert_test(3, randint(5, 10))
    insert_test(5, randint(10, 20))
    insert_test(10, randint(20, 30))

# Force a CuckooHash to grow by inserting a medium amount more than size keys
def test_insert_force_grow_medium():
    insert_test(30, randint(100, 200))
    insert_test(100, randint(250, 300))
    insert_test(300, randint(350, 500))

# Force a CuckooHash to grow by inserting a large amount more than size keys.
def test_insert_force_grow_large():
    insert_test(randint(10, 80), randint(1000, 2000))
    insert_test(randint(10, 80), randint(10000, 20000))
    
# Force an initially small CuckooHash to grow by inserting 100,000 keys. 
def test_insert_force_grow_100k():
    insert_test(randint(10, 100), 100000)
    
# Force an initially small CuckooHash to grow by inserting between 150,000 and 
# 500,000 keys.
def test_insert_force_grow_XL_torture():
    insert_test(randint(20, 30), randint(150000, 250000))
    insert_test(randint(100, 500), randint(300000, 500000))
    
# Test that delete works when deleting one key.
def test_delete_one():
    # Make a CuckooHash with half of size keys
    size = 5
    numKeys = size//2
    c = makeCuckooHash(size, numKeys)
    
    # assert that delete returns the correct key-data
    assert c.delete(str(0)) == (str(0), 0)
    
    # assert that the key-data can no longer be found in the CuckooHash
    assert c.find(str(0)) == None
    
    # assert that the length of the CuckooHash is one less than before
    assert len(c) == numKeys-1
    
    # assert that all other keys are still in the CuckooHash
    for i in range(1, numKeys-1):
        assert c.find(str(i)) == i

# Test that delete works when deleting all keys.
def delete_all(size):
    # Make a CuckooHash with half of size keys
    numKeys = size//2
    c = makeCuckooHash(size, numKeys)
    
    # Delete each node and assert that the proper key-data tuple are returned
    # upon deletion
    for i in range(numKeys):
        assert c.delete(str(i)) == (str(i), i)
        
    # Assert that the length after deleting all keys is 0
    assert len(c) == 0
    
    # Assert that all keys can no longer be found
    for i in range(numKeys):
        assert not c.find(str(i))

# Test delete all on a small CuckooHash
def test_delete_all_small():
    delete_all(randint(1, 3))
    delete_all(randint(5, 10))
    delete_all(randint(20, 30))

# Test delete all on a medium CuckooHash
def test_delete_all_medium():
    delete_all(randint(20, 50))
    delete_all(randint(100, 200))
    delete_all(randint(300, 500))

# Test delete all on a large CuckooHash
def test_delete_all_large():
    delete_all(randint(1000, 2000))
    delete_all(randint(3000, 4000))
    delete_all(randint(5000, 8000))
    
# Test delete does not delete anything when given a key that is not in the
# CuckooHash
def delete_false(size):
    # Make a CuckooHash with half of size keys
    numKeys = size//2
    c = makeCuckooHash(size, numKeys)
    
    # Attempt to delete keys that are not in the CuckooHash and assert that
    # None is returned
    for i in range(numKeys, (numKeys*2)):
        assert not c.delete(str(i))
        
    # Assert that after false deletion numKeys is unaffected.
    assert len(c) == numKeys
    
    # Assert that after false deletion all other nodes remain present.
    for i in range(numKeys):
        assert c.find(str(i)) == i

# Test falsely deleting works on one false deletion
def test_delete_false_one():
    delete_false(1)
    
# Test falsely deleting works on a small CuckooHash
def test_delete_false_small():
    delete_false(randint(2, 5))
    delete_false(randint(10, 15))
    delete_false(randint(15, 20))
    
# Test falsely deleting works on a medium CuckooHash
def test_delete_false_mdeium():
    delete_false(randint(30, 50))
    delete_false(randint(100, 200))
    delete_false(randint(300, 500))  
          
# Test falsely deleting works on a large CuckooHash
def test_delete_false_large():
    delete_false(randint(1000, 2000))
    delete_false(randint(3000, 4000))
    delete_false(randint(5000, 8000))
   
pytest.main(["-v", "-s", "test_CuckooHash_SG.py"])


# Created by Sarale Goldberger