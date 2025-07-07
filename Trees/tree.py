from collections import defaultdict, deque


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

    def __eq__(self, other):
        return self.pre_order() == other.pre_order()

    def level_order(self):
        res = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            res.append(node)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return res

    def pre_order(self):
        res = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            res.append(node)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return res

    def in_order(self):
        res = []
        curr = self.root
        stack = []
        while stack or curr:
            while curr:
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()
            res.append(curr)
            curr = curr.right
        return res

    def post_order(self):
        stack = [self.root]
        ans = []
        while stack:
            node = stack.pop()
            ans.append(node)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return list(reversed(ans))

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
            if lh == -1:
                return -1
            rh = balanced(node.right)
            if rh == -1 or abs(lh - rh) > 1:
                return -1
            return 1 + max(lh, rh)

        return balanced(self.root) != -1

    @property
    def diameter(self):
        m = 0

        def through_height(node):
            nonlocal m
            if node is None:
                return 0
            lh = through_height(node.left)
            rh = through_height(node.right)
            m = max(m, lh + rh)
            return 1 + max(lh, rh)

        through_height(self.root)
        return m

    @property
    def max_path_sum(self):
        m = 0

        def through_height(node):
            nonlocal m
            if node is None:
                return 0
            ls = through_height(node.left)
            rs = through_height(node.right)
            curr_max = max(0, ls, rs) + node.value
            m = max(m, curr_max)
            return curr_max

        through_height(self.root)
        return m

    def zig_zag(self):
        q = deque([self.root])
        ans = []
        even = 0
        while q:
            current_level = deque()
            for _ in range(len(q)):
                node = q.popleft()
                if node.left:
                    q.append(node.left)
                if node.right:
                    q.append(node.right)
                if even:
                    current_level.appendleft(node)
                else:
                    current_level.append(node)
            ans.append(list(current_level))
            even = not even
        return ans

    @staticmethod
    def is_leaf_node(node):
        return node.left is None and node.right is None

    def boundary_traversal(self):
        ans = []
        stack = []
        curr_node = self.root
        while curr_node:
            if not Tree.is_leaf_node(curr_node):
                ans.append(curr_node)
            if curr_node.left:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right

        def in_order():
            stack = []
            curr = self.root
            while curr or stack:
                if curr is None:
                    node = stack.pop()
                    if Tree.is_leaf_node(node):
                        ans.append(node)
                    curr = node.right
                else:
                    stack.append(curr)
                    curr = curr.left

        in_order()
        curr_node = self.root.right
        rside = []
        while curr_node:
            if not Tree.is_leaf_node(curr_node):
                rside.append(curr_node)
            if curr_node.right:
                curr_node = curr_node.right
            else:
                curr_node = curr_node.left

        return ans + rside[::-1]

    def vertical_order(self):
        d = {}
        stack = [(self.root, 0, 0)]
        while stack:
            node, x, y = stack.pop()
            if y not in d:
                d[y] = {}
            if x not in d[y]:
                d[y][x] = []
            d[y][x].append(node)
            if node.left:
                stack.append((node.left, x + 1, y - 1))
            if node.right:
                stack.append((node.right, x + 1, y + 1))
        ans = []
        for y in sorted(d.keys()):
            vertical = []
            for x in sorted(d[y].keys()):
                vertical += list(sorted(d[y][x]))
            ans.append(vertical)
        return ans

    def top_view(self):
        d = {}
        q = deque([[self.root, 0]])
        while q:
            node, y = q.popleft()
            if y not in d:
                d[y] = node

            if node.left:
                q.append([node.left, y - 1])
            if node.right:
                q.append([node.right, y + 1])
        ans = []
        for k in sorted(d.keys()):
            ans.append(d[k])
        return ans

    def bottom_view(self):
        d = {}
        q = deque([[self.root, 0]])
        while q:
            node, y = q.popleft()
            d[y] = node

            if node.left:
                q.append([node.left, y - 1])
            if node.right:
                q.append([node.right, y + 1])
        print(d)
        ans = []
        for k in sorted(d.keys()):
            ans.append(d[k])
        return ans

    @property
    def is_symmetric(self):
        def traverse_lr(node):
            lr = []
            stack = [node]
            while stack:
                node = stack.pop()
                lr.append(node)
                if node.left:
                    stack.append(node.left)
                if node.right:
                    stack.append(node.right)
            return lr

        def traverse_rl(node):
            rl = []
            stack = [node]
            while stack:
                node = stack.pop()
                rl.append(node)
                if node.right:
                    stack.append(node.right)
                if node.left:
                    stack.append(node.left)
            return rl

        return traverse_lr(self.root.left) == traverse_rl(self.root.right)

    def root_to_node(self, node):
        path = []

        def find_recurse(curr):
            if curr is None:
                return False
            if curr.value == node:
                path.append(node)
                return True
            path.append(curr)
            if find_recurse(curr.left):
                return True
            if find_recurse(curr.right):
                return True
            path.pop()
            return False

        find_recurse(self.root)
        return path

    def lca(self, a, b):
        ancestor = None

        def find_recurse(node):
            if node is None:
                return False

            if node.value in (a, b):
                return node.value
            lr = find_recurse(node.left)
            rr = find_recurse(node.right)
            if lr and rr:
                return node
            return lr or rr

        return find_recurse(self.root)


root = TreeNode(5)
root.left = TreeNode(2)
root.right = TreeNode(1)
root.left.left = TreeNode(3)
root.left.right = TreeNode(9)
root.right.left = TreeNode(8)
root.right.right = TreeNode(7)
root.right.right.right = TreeNode(100)

t = Tree(root)

print("Level ", t.level_order())
print("Pre", t.pre_order())
print("In ", t.in_order())
print("Post ", t.post_order())
print("Height - ", t.height())
print("Diameter - ", t.diameter)
print("Max Path Sum - ", t.max_path_sum)
print("Zig Zag - ", t.zig_zag())
print("Boundary -", t.boundary_traversal())
print("Vertical - ", t.vertical_order())
print("Top View - ", t.top_view())
print("Bottom View - ", t.bottom_view())

st = Tree(TreeNode(1))
st.root.left = TreeNode(2)
st.root.right = TreeNode(2)
st.root.left.right = TreeNode(4)
st.root.right.left = TreeNode(4)

print("Is Symmetric - ", st.is_symmetric)

print("Root to node 100", t.root_to_node(9))

print("LCA of 2, 100 is", t.lca(2, 100))
