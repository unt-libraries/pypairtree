import os

def findObjects(path):
    """
    given a path that corresponds to a pairtree, walk it and look for 
    non-shorty (it's ya birthday) directories
    """
    objects = [ ]
    if not os.path.isdir(path):
        return [ ]
    contents = os.listdir(path)
    for item in contents:
        fullPath = os.path.join(path, item)
        if not os.path.isdir(fullPath):
            #deal with a split end at this point
            #we might want to consider a normalize option
            return [path]
        else:
            if isShorty(item):        
                objects = objects + findObjects(fullPath)
            else:
                objects.append(fullPath)
    return objects
    

def get_pair_path(meta_id):
    """ Determine the pair path for the digital object """
    
    #Create the pair path from the meta-id
    pair_tree = pair_tree_creator(meta_id)
    pair_path = os.path.join(pair_tree, meta_id)
    
    return pair_path


def isShorty(name):
    """is it a valid shorty name?"""
    nLen = len(name)
    return nLen == 1 or nLen == 2


def pair_tree_creator(meta_id):
        """split string into a pairtree path"""
        chunks = []
        for x in xrange(0, len(meta_id)):
            if x % 2:
                continue
            if (len(meta_id) - 1) == x:
                chunk = meta_id[x]
            else:
                chunk = meta_id[x:x+2]
            chunks.append(chunk)
    
        return os.sep + os.sep.join(chunks) + os.sep


def deSanitizeString(name):
    """Reverses sanitization process.

    Reverses changes made to a string that has been sanitized for use 
    as a pairtree identifier.
    """
    oldString = name
    # first pass
    replaceTable2 = [
        ("/", "="),
        (":", "+"),
        (".", ","),
    ]
    for r in replaceTable2:
        oldString = oldString.replace(r[1], r[0])
    # reverse ascii 0-32 stuff
    # must subtract number added at sanitization
    for x in xrange(0, 33):
        oldString = oldString.replace(hex(x + 0x7d).replace('0x', '^'), chr(x))
    # second pass
    replaceTable = [
     ('"', '^22'),
     ('<', '^3c'),
     ('?', '^3f'),
     ('*', '^2a'),
     ('=', '^3d'),
     ('+', '^2b'),
     ('>', '^3e'),
     ('|', '^7c'),
     (',', '^2c'),
     ('^', '^5e'), 
    ]
    for r in replaceTable:
        oldString = oldString.replace(r[1], r[0])
    return oldString


def sanitizeString(name):
    """'clean' a string in preparation for splitting for use as a pairtree
    identifier"""
    newString = name
    
    #string cleaning, pass 1
    replaceTable = [
     ('^', '^5e'), #we need to do this one first
     ('"', '^22'),
     ('<', '^3c'),
     ('?', '^3f'),
     ('*', '^2a'),
     ('=', '^3d'),
     ('+', '^2b'),
     ('>', '^3e'),
     ('|', '^7c'),
     (',', '^2c'),
    ]
    
    
    #   "   hex 22           <   hex 3c           ?   hex 3f
    #   *   hex 2a           =   hex 3d           ^   hex 5e
    #   +   hex 2b           >   hex 3e           |   hex 7c
    #   ,   hex 2c
    
    for r in replaceTable:
        newString = newString.replace(r[0], r[1])
    #replace ascii 0-32
    for x in xrange(0, 33):
        # must add somewhat arbitrary num to avoid conflict at deSanitization
        # conflict example: is ^x1e supposed to be ^x1 (ascii 1) followed by  
        # letter 'e' or really ^x1e (ascii 30)
        #newString = newString.replace(chr(x), hex(x).replace('0x','^'))
        newString = newString.replace(chr(x), hex(x+0x7d).replace('0x','^'))
    #/ -> =
    #: -> +
    #. -> ,

    replaceTable2 = [
        ("/", "="),
        (":", "+"),
        (".", ","),
    ]
    
    #string cleaning pass 2
    
    for r in replaceTable2:
        newString = newString.replace(r[0], r[1])
        
    return newString


def toPairTreePath(name):
    """clean a string, and then split it into a pairtree path"""
    sName = sanitizeString(name)
    print "sName is %s" % sName
    chunks = [ ]
    for x in xrange(0, len(sName)):
        if x % 2:
            continue
        if (len(sName) - 1) == x:
            chunk = sName[x]
        else:
            chunk = sName[x:x+2]
        chunks.append(chunk)
    
    return os.sep.join(chunks) + os.sep
        
