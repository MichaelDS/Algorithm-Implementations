
#TODO: Use size of left subtree optimize rank and select methods to O(logn)

class TNode(object):
    __slots__ = ('data', 'parent', 'left', 'right', 'color')
    def __init__(self, data = None, parent = None, left = None, right = None,
                 color = None):
        self.data = data
        self.parent = parent
        self.left = left
        self.right = right
        assert not color or color == 'RED' or color == 'BLACK', \
        'color must be \'RED\' or \'BLACK\''
        self.color = color

    def getData(self):
        return self.data
    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return str(self.data)

class BSTree(object):
    '''
    A binary search tree.
    '''
    __slots__ = ('create_node', 'nil', 'root', 'key')
    def __init__(self, data = None, key = lambda x:x, _create_node = TNode, _color = None):
        self.create_node = _create_node              # node constructor
        self.nil = self.create_node(color = _color)  # sentinel node
        self.nil.parent, self.nil.left, self.nil.right = \
        self.nil, self.nil, self.nil
        self.root = self.nil                         # root node
        self.key = key                               # comparison key
        if data:
            for d in data:
                self.insert(d)
    def __contains__(self, x):
        return not (self.search(x) == self.nil)
    def search(self, x, rec = False):
        def tree_search(start, target):
            if start == self.nil or self.key(start.getData()) == target:
                return start
            if target < self.key(start.getData()):
                return tree_search(start.left, target)
            return tree_search(start.right, target)
        if rec:
            return tree_search(self.root, x)
        else:
            start = self.root
            while start != self.nil and self.key(x) != self.key(start.getData()):
                if self.key(x) < self.key(start.getData()):
                    start = start.left
                else:
                    start = start.right
            return start
    def insert(self, x, _color = None):
        parent = self.nil
        start = self.root
        while start != self.nil:
            parent = start
            if self.key(x) < self.key(start.getData()):
                start = start.left
            else:
                start = start.right
        z = self.create_node(x, parent, self.nil, self.nil, _color)
        if parent == self.nil:
            self.root = z           # tree was empty
        elif self.key(z.getData()) <= self.key(parent.getData()):
            parent.left = z
        else:
            parent.right = z
        if _color:
            return z
    def delete(self, x):
        target = self.search(x)
        if target == self.nil:
            raise KeyError(x)
        if target.left == self.nil:
            self._transplant(target, target.right)
        elif target.right == self.nil:
            self._transplant(target, target.left)
        else:
            replacement = self.min(target.right)   # the target's successor; has no left child by definition
            if replacement.parent != target:       # if replacement is not target's right child, transplant right sub-tree
                self._transplant(replacement, replacement.right)
                replacement.right = target.right
                replacement.right.parent = replacement
            self._transplant(target, replacement)
            replacement.left = target.left
            replacement.left.parent = replacement
    def rank(self, x, root = None):
        '''
        Returns the rank (1-based) of the value x in the binary search tree.
        If x is not in the tree, its rank is still returned by computing its
        ordering within the elements of the tree.
        '''
        if not x:
            return 0
        def tree_rank(start):
            if start == self.nil:
                return 0
            if self.key(x) == self.key(start.getData()):
                return self.size(start.left)
            elif self.key(x) < self.key(start.getData()):
                return tree_rank(start.left)
            else:
                return tree_rank(start.left) + 1 + tree_rank(start.right)
        if not root:
            return tree_rank(self.root) + 1
        else:
            return tree_rank(root) + 1
    def select(self, i):
        '''
        Returns the ith order element of the tree.
        '''
        def tree_select(start, i):
            if self.rank(start.getData()) == i:
                return start
            elif self.rank(start.getData()) > i:
                return tree_select(start.left, i)
            else:
                return tree_select(start.right, i-tree_select(start.left, i)-1)
        return tree_select(self.root, i)
    def min(self, start = None):
        if not start:
            start = self.root
        while start.left != self.nil:
            start = start.left
        return start
    def max(self, start = None):
        if not start:
            start = self.root
        while start.right != self.nil:
            start = start.right
        return start
    def successor(self, x):
        start = self.search(x)
        if start.right != self.nil:
            return self.min(start.right)
        parent = start.parent
        while parent != self.nil and start == parent.right:    # while parent is not nil and the current node is its parent's right child
            start = parent
            parent = start.parent
        return parent
    def predecessor(self, x):
        start = self.search(x)
        if start.left != self.nil:
            return self.max(start.left)
        parent = start.parent
        while parent != self.nil and start == parent.left:    # while parent is not nil and the current node is its parent's left child
            start = parent
            parent = start.parent
        return parent
    def height(self):
        def tree_height(x):
            if x == self.nil:
                return 0
            return max(1 + tree_height(x.left), 1 + tree_height(x.right))
        return tree_height(self.root)
    def size(self, root = None):
        def count_nodes(x):
            if x == self.nil:
                return 0
            return(1 + count_nodes(x.left) + count_nodes(x.right))
        if not root:
            return count_nodes(self.root)
        else:
            return count_nodes(root)
    def _transplant(self, u, v, rb = False):
        '''
        Replaces the subtree rooted at u with the subtree rooted at v.
        '''
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v != self.nil or rb:
            v.parent = u.parent
    def left_rotate(self, x):
        '''
        Left-rotates node x.  Note: x is a node as opposed to a (key)value.

                       x
                      / \
                     a   y
                        / \
                       b   g

        mutates into:

                       y
                      / \
                     x   g
                    / \
                   a   b

        Used for maintaining tree balance.
        '''
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
    def right_rotate(self, x):
        '''
        Right-rotates node x.  Note: x is a node as opposed to a (key)value.

                   x
                  / \
                 y   g
                / \
               a   b

        mutates into:

                   y
                  / \
                 a   x
                    / \
                   b   g

        Used for maintaining tree balance.
        '''
        y = x.left
        x.left = y.right
        if y.right != self.nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y
    def __str__(self):
        def tree_walk(x):
            if x == self.nil:
                return ''
            else:
                return tree_walk(x.left) + str(x) + ', ' + tree_walk(x.right)
        return '[' + tree_walk(self.root)[0:-2] + ']'

class RBTree(BSTree):
    '''
    A 'RED'-'BLACK' Tree.  Satisfies the following properties:
    1. Every node is either 'RED' or 'BLACK'
    2. The root is 'BLACK'
    3. Every leaf (null) is 'BLACK'
    4. If a node is 'RED', then both its children are 'BLACK'
    5. For each node, all simple paths from the node to descendant leaves
       contain the same number of 'BLACK' nodes.
    '''
    #__slots__ = ('create_node', 'nil', 'root', 'key')
    def __init__(self, data = None, key = lambda x:x):
        super(RBTree, self).__init__(data = data, key = key, _color = 'BLACK')
    def insert(self, x):
        self.insert_fixup(super(RBTree, self).insert(x, 'RED'))
    def insert_fixup(self, z):
        while z.parent.color == 'RED':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'RED':
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        super(RBTree, self).left_rotate(z)
                    z.parent.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    super(RBTree, self).right_rotate(z.parent.parent)
            else: # z.parent == z.parent.parent.right
                y = z.parent.parent.left
                if y.color == 'RED':
                    z.parent.color = 'BLACK'
                    y.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        super(RBTree, self).right_rotate(z)
                    z.parent.color = 'BLACK'
                    z.parent.parent.color = 'RED'
                    super(RBTree, self).left_rotate(z.parent.parent)
        self.root.color = 'BLACK'
        def delete(self, z):
            z = super(RBTree, self).search(z)
            y = z
            y_original_color = y.color
            if z.left == self.nil:
                x = z.right
                super(RBTree, self).transplant(z, z.right, rb = True)
            elif z.right == self.nil:
                x = z.left
                super(RBTree, self).transplant(z, z.left, rb = True)
            else:
                y = super(RBTree, self).min(z.right)
                y_original_color = y.color
                x = y.right
                if y.parent == z:
                    x.parent = y
                else:
                    super(RBTree, self).transplant(y, y.right, rb = True)
                    y.right = z.right
                    y.right.parent = y
                super(RBTree, self).transplant(z, y, rb = True)
                y.left = z.left
                y.left.parent = y
                y.color = z.color
                if y_original_color == 'BLACK':
                    self.delete_fixup(x)
        def delete_fixup(self, x):
            while x != self.root and x.color == 'BLACK':
                if x == x.parent.left:
                    w = x.parent.right
                    if w.color == 'RED':
                        w.color = 'BLACK'
                        x.parent.color = 'RED'
                        super(RBTree, self).left_rotate(x.parent)
                        w = x.parent.right
                    if w.left.color == 'BLACK' and w.right.color == 'BLACK':
                        w.color = 'RED'
                        x = x.parent
                    else:
                        if w.right.color == 'BLACK':
                            w.left.color = 'BLACK'
                            w.color = 'RED'
                            super(RBTree, self).right_rotate(w)
                            w = x.parent.right
                        w.color = x.parent.color
                        x.parent.color = 'BLACK'
                        w.right.color = 'BLACK'
                        super(RBTree, self).left_rotate(x.parent)
                        x = self.root
                else: # x == x.parent.right
                    w = x.parent.left
                    if w.color == 'RED':
                        w.color = 'BLACK'
                        x.parent.color = 'RED'
                        super(RBTree, self).right_rotate(x.parent)
                        w = x.parent.left
                    if w.right.color == 'BLACK' and w.left.color == 'BLACK':
                        w.color = 'RED'
                        x = x.parent
                    else:
                        if w.left.color == 'BLACK':
                            w.right.color = 'BLACK'
                            w.color = 'RED'
                            super(RBTree, self).left_rotate(w)
                            w = x.parent.left
                        w.color = x.parent.color
                        x.parent.color = 'BLACK'
                        w.left.color = 'BLACK'
                        super(RBTree, self).right_rotate(x.parent)
                        x = self.root
            x.color = 'BLACK'
