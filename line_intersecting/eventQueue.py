from line import Line

class TreeNode(object): 
    def __init__(self, point, line): 
        self.point = point 
        self.left = None
        self.right = None
        self.height = 1
        if line is None:
            self.lines = []
        else:
            self.lines = [line]
        
def compare(p, q):
    px, py = p
    qx, qy = q
    if py != qy:
        return py - qy
    return qx - px

class EventQueue(object): 
    def __init__(self):
        self.root = None
        
    def _insert(self, root, point, line=None): 
        if not root: 
            return TreeNode(point, line) 
        elif compare(point, root.point) < 0: 
            root.left = self._insert(root.left, point, line) 
        elif compare(point, root.point) > 0:
            root.right = self._insert(root.right, point, line) 
        else:
            if line is not None:
                root.lines.append(line)
            return root
        root.height = 1 + max(self.getHeight(root.left), 
                           self.getHeight(root.right)) 
        balance = self.getBalance(root) 
        if balance > 1 and compare(point, root.point) < 0: 
            return self.rightRotate(root) 
        if balance < -1 and compare(point, root.point) > 0: 
            return self.leftRotate(root) 
        if balance > 1 and compare(point, root.point) > 0: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
        if balance < -1 and compare(point, root.point) < 0: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
        return root 
    
    def insert_line(self, line):
        upper_end = line.upper_endpoint
        lower_end = line.lower_endpoint
        self.root = self._insert(self.root, upper_end, line)
        self.root = self._insert(self.root, lower_end, None)
    
    def insert(self, point):
        self.root = self._insert(self.root, point, None)
  
    def leftRotate(self, z): 
        y = z.right 
        T2 = y.left 
        y.left = z 
        z.right = T2 
        z.height = 1 + max(self.getHeight(z.left), 
                         self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                         self.getHeight(y.right)) 
        return y 
  
    def rightRotate(self, z): 
  
        y = z.left 
        T3 = y.right 
        y.right = z 
        z.left = T3 
        z.height = 1 + max(self.getHeight(z.left), 
                        self.getHeight(z.right)) 
        y.height = 1 + max(self.getHeight(y.left), 
                        self.getHeight(y.right)) 
        return y 
  
    def getHeight(self, root): 
        if not root: 
            return 0
        return root.height 
  
    def getBalance(self, root): 
        if not root: 
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right) 
  
    def _inOrder(self, root, result): 
        if not root: 
            return
  
        self._inOrder(root.left, result) 
        result.append(root)
        self._inOrder(root.right, result)
        
    def inOrder(self):
        result = []
        self._inOrder(self.root, result)
        return result
    
    def delete(self, point):
        self.root = self._delete(self.root, point)
        
    def get_max(self):
        current = self.root
        while (current.right != None):
            current = current.right
        return current
    
    def pop_next_event(self):
        current = self.get_max()
        self.delete(current.point)
        return current
    
    def _delete(self, root, key): 
        if not root: 
            return root 
        elif compare(key, root.point) < 0: 
            root.left = self._delete(root.left, key) 
        elif compare(key, root.point) > 0: 
            root.right = self._delete(root.right, key) 
        else: 
            if root.left is None: 
                temp = root.right 
                root = None
                return temp 
            elif root.right is None: 
                temp = root.left 
                root = None
                return temp 
            temp = self.getMinValueNode(root.right) 
            root.point = temp.point 
            root.lines = temp.lines
            root.right = self._delete(root.right, 
                                      temp.point) 
        if root is None: 
            return root 
        root.height = 1 + max(self.getHeight(root.left), 
                            self.getHeight(root.right)) 
        balance = self.getBalance(root) 
        if balance > 1 and self.getBalance(root.left) >= 0: 
            return self.rightRotate(root) 
        if balance < -1 and self.getBalance(root.right) <= 0: 
            return self.leftRotate(root) 
        if balance > 1 and self.getBalance(root.left) < 0: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
        if balance < -1 and self.getBalance(root.right) > 0: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
        return root 

    def getMinValueNode(self, root): 
        if root is None or root.left is None: 
            return root 
  
        return self.getMinValueNode(root.left) 
    
    def is_empty(self):
        return self.root is None
    
if __name__ == '__main__':
    line_1 = Line((1, 8), (0, 6))
    line_2 = Line((1, 8), (2, 6))
    line_3 = Line((2, 6), (1, 4))
    line_4 = Line((3, 7), (4, 5))
    line_5 = Line((3, 3), (6, 5))
    line_6 = Line((5, 6), (7, 4))
    line_7 = Line((5, 4), (7, 6))
    lines = [line_1, line_2, line_3, line_4, line_5, line_6, line_7]
    i = 1
    for line in lines:
        line.name = 'line_'+str(i)
        i += 1
    Q = EventQueue()
    for line in lines:
        Q.insert_line(line)
    def print_q(Q):
        lul = []
        for node in Q.inOrder():
            lul.append(node.point)
        print(lul)