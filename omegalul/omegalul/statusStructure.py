from line import Line

class TreeNode(object): 
    def __init__(self, line):
        # val = seg
        self.line = line
        self.left = None
        self.right = None
        self.height = 1
    
    def copy(self, node):
        self.line = node.line
        self.left = node.left
        self.right = node.right
        self.height = node.height
       
        
class StatusStructure(object): 
    def __init__(self):
        self.root = None
        
    def _insert(self, root, point, line): 
        if not root: 
            return TreeNode(line) 
        elif root.line.compare_lower(point, line) > 0: 
            root.left = self._insert(root.left, point, line) 
        else:
            root.right = self._insert(root.right, point, line) 
        root.height = 1 + max(self.getHeight(root.left), 
                           self.getHeight(root.right)) 
        balance = self.getBalance(root) 
        if balance > 1 and root.line.compare_lower(point, line) > 0: 
            return self.rightRotate(root) 
        if balance < -1 and root.line.compare_lower(point, line) < 0: 
            return self.leftRotate(root) 
        if balance > 1 and root.line.compare_lower(point, line) < 0: 
            root.left = self.leftRotate(root.left) 
            return self.rightRotate(root) 
        if balance < -1 and root.line.compare_lower(point, line) > 0: 
            root.right = self.rightRotate(root.right) 
            return self.leftRotate(root) 
        return root 
    
    def insert(self, point, lines):
        if type(lines) != list:
            lines = [lines]
        
        for line in lines:
            self.root = self._insert(self.root, point, line)
        
    def _print_name(self):
        print(list(map(lambda x: x.line.name, self.inOrder())))
  
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
    
    def delete(self, point, line):
        self.root = self._delete(self.root, point, line) 
    
    def delete_list(self, point, lines):
        for line in lines:
            self.delete(point, line)
    
    def _delete(self, root, point, line): 
        if not root: 
            return root 
        elif root.line.compare_upper(point, line) > 0: 
            root.left = self._delete(root.left, point, line) 
        elif root.line.compare_upper(point, line) < 0: 
            root.right = self._delete(root.right, point, line) 
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
            root.line = temp.line 
            root.right = self._delete(root.right, point, temp.line) 
                                      
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
       
    def find_segments_contain(self, point):
        L = []
        C = []
        L_C = []
        self._find_segments_contain(self.root, point, L, C, L_C)
        return L, C, L_C
    
    def _find_segments_contain(self, root, point, L, C, L_C):
        if not root: 
            return 
        elif root.line.point_location(point) > 0: 
            self._find_segments_contain(root.right, point, L, C, L_C) 
        elif root.line.point_location(point) < 0: 
            self._find_segments_contain(root.left, point, L, C, L_C) 
        else:
            if root.left is not None:
                self._find_segments_contain(root.left, point, L, C, L_C) 
            if root.line.lower_endpoint == point:
                L.append(root.line)
            else:
                C.append(root.line)
            L_C.append(root.line)
            if root.right is not None:
                self._find_segments_contain(root.right, point, L, C, L_C)
            
                
    def find_left_neighbor(self, point):
        left_neighbor = TreeNode(None)
        self._find_left_neighbor(self.root, point, left_neighbor)
        return left_neighbor.line

    def find_right_neighbor(self, point):
        right_neighbor = TreeNode(None)
        self._find_right_neighbor(self.root, point, right_neighbor)
        return right_neighbor.line
    
    def _find_left_neighbor(self, root, point, left_neighbor):
        if not root: 
            return 
        elif root.line.point_location(point) > 0: 
            left_neighbor.copy(root)
            self._find_left_neighbor(root.right, point, left_neighbor) 
        elif root.line.point_location(point) <= 0: 
            self._find_left_neighbor(root.left, point, left_neighbor) 
    
    def _find_right_neighbor(self, root, point, right_neighbor):
        if not root: 
            return 
        elif root.line.point_location(point) >= 0: 
            self._find_right_neighbor(root.right, point, right_neighbor) 
        elif root.line.point_location(point) < 0: 
            right_neighbor.copy(root)
            self._find_right_neighbor(root.left, point, right_neighbor)
    
    def find_leftmost(self, point):
        lm_node = TreeNode(None)
        self._find_leftmost(self.root, point, lm_node)
        return lm_node.line
        
    def _find_leftmost(self, root, point, lm_node):
        if not root:
            return
        elif root.line.point_location(point) > 0:
            self._find_leftmost(root.right, point, lm_node)
        elif root.line.point_location(point) < 0:
            self._find_leftmost(root.left, point, lm_node)
        else:
            self._find_leftmost(root.right, point, lm_node)
            lm_node.copy(root)
            self._find_leftmost(root.left, point, lm_node)
            
    def find_rightmost(self, point):
        rm_node = TreeNode(None)
        self._find_rightmost(self.root, point, rm_node)
        return rm_node.line
        
    def _find_rightmost(self, root, point, rm_node):
        if not root:
            return
        elif root.line.point_location(point) > 0:
            self._find_rightmost(root.right, point, rm_node)
        elif root.line.point_location(point) < 0:
            self._find_rightmost(root.left, point, rm_node)
        else:
            self._find_rightmost(root.left, point, rm_node)
            rm_node.copy(root)
            self._find_rightmost(root.right, point, rm_node)
    
if __name__ == '__main__':
    def print_res(nodes):
        r = []
        for node in nodes:
            r.append(node.line.name)
        print(r)
    line_1 = Line((0, 0), (1, 2))
    line_2 = Line((1, 2), (2, 3))
    line_3 = Line((2, 3), (3, 2))
    line_4 = Line((3, 2), (2, 1))
    line_5 = Line((2, 1), (0, 0))
    line_6 = Line((2, 1), (2, 3))
    line_7 = Line((1, 2), (4, 2))
    line_8 = Line((1, 1), (1, 1.5))
    line_9 = Line((1, 1.5), (1.5, 1))
    line_10 = Line((1.5, 1), (1, 1))
    line_11 = Line((0, 0), (3, 3))
    lines = [line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8, line_9, line_10, line_11]
    i = 1
    for line in lines:
        line.name = 'line_'+str(i)
        i += 1
    T = StatusStructure()
    T.insert((2, 3), [line_2, line_3, line_6])
    T.insert((3, 3), [line_11])
    T.delete_list((2.5, 2.5), [line_3, line_11])
    T.insert((2.5, 2.5), [line_3, line_11])
    T.delete_list((1, 2), [line_2])
    T.insert((1, 2), [line_1, line_7])
    T.delete_list((2, 2), [line_7, line_6, line_11])
    T.insert((2, 2), [line_7, line_6, line_11])
    print_res(T.inOrder())
    '''
    T.delete((0, 6), line_1)
    T.delete((2, 6), line_2)
    print_res(T.inOrder())
    T.insert((2, 6), line_3)
    T.insert((5, 6), line_6)
    T.insert((7, 6), line_7)
    print_res(T.inOrder())
    T.delete((4, 5), line_4)
    print_res(T.inOrder())
    T.insert((6, 5), line_5)
    T.delete((6, 5), line_6)
    print_res(T.inOrder())
    T.delete((6, 5), line_7)
    print_res(T.inOrder())
    T.insert((6, 5), line_6)
    T.insert((6, 5), line_7)
    print_res(T.inOrder())
    L_p, C_p, L_C = T.find_segments_contain((6, 5))
    '''
