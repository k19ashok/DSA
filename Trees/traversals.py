from collections import deque


class TreeNode:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value


class Tree:
    def __init__(self, root):
        self.root = root

    def level_order(self):
        print("Level Order Traversal")
        queue = deque([root])
        while queue:
            node = queue.popleft()
            print(node, end=" ")
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        print()

    def pre_order(self):
        print("Pre Order Traversal")
        stack = [self.root]
        while stack:
            node = stack.pop()
            print(node, end=" ")
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        print()

    def in_order(self):
        print("In Order Traversal")
        curr = self.root
        stack = []
        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            print(curr, end=" ")
            curr = curr.right
        print()

    def post_order(self):
        print("Post Order Traversal")
        stack = [self.root]
        ans = []
        while stack:
            node = stack.pop()
            ans.append(node)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        print(*reversed(ans))

    def height(self):
        def find_height(node):
            if not node:
                return 0
            return 1 + max(find_height(node.left), find_height(node.right))
        return find_height(self.root)
    
    def is_balanced(self):
        def balanced(node):
            if not node:
                return 0
            lh = balanced(node.left)
            rh = balanced(node.right)
            if lh == -1 or rh == -1:
                return -1
            if abs(lh - rh) > 1:
                return -1
            return 1 + max(lh, rh)
        return balanced(self.root) != -1


root = TreeNode(5)
root.left = TreeNode(2)
root.right = TreeNode(1)
root.left.left = TreeNode(3)
root.left.right = TreeNode(9)
root.right.left = TreeNode(8)
root.right.right = TreeNode(7)
root.right.right.right = TreeNode(100)

t = Tree(root)
t.level_order()
t.pre_order()
t.in_order()
t.post_order()
print("Height - ", t.height())
