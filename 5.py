class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    # a) Insert (duplicate entries are rejected)
    def insert(self, key):
        new = Node(key)
        if self.root is None:
            self.root = new
            return True
        cur = self.root
        while True:
            if key == cur.data:
                return False                    # duplicate entry
            elif key < cur.data:
                if cur.left is None:
                    cur.left = new
                    return True
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = new
                    return True
                cur = cur.right

    # b) Delete
    def delete(self, key):
        self.root, deleted = self._delete(self.root, key)
        return deleted

    def _delete(self, node, key):
        if node is None:
            return None, False                  # key not found
        if key < node.data:
            node.left, deleted = self._delete(node.left, key)
        elif key > node.data:
            node.right, deleted = self._delete(node.right, key)
        else:
            if node.left is None:               # Case 1 and 2: no left child
                return node.right, True
            if node.right is None:              # Case 2: only left child
                return node.left, True
            succ = node.right                   # Case 3: two children
            while succ.left is not None:        # inorder successor
                succ = succ.left
            node.data = succ.data
            node.right, _ = self._delete(node.right, succ.data)
            deleted = True
        return node, deleted

    # c) Search: returns the level where key is found, else None
    def search(self, key):
        cur, level = self.root, 1
        while cur is not None:
            if key == cur.data:
                return level
            cur = cur.left if key < cur.data else cur.right
            level += 1
        return None

    # d) Display tree (traversals)
    def inorder(self, node, out):
        if node:
            self.inorder(node.left, out)
            out.append(node.data)
            self.inorder(node.right, out)
        return out

    def preorder(self, node, out):
        if node:
            out.append(node.data)
            self.preorder(node.left, out)
            self.preorder(node.right, out)
        return out

    def postorder(self, node, out):
        if node:
            self.postorder(node.left, out)
            self.postorder(node.right, out)
            out.append(node.data)
        return out


def fmt(values):
    return " ".join(map(str, values))


def main():
    t = BST()
    while True:
        print("\n===== Binary Search Tree Menu =====")
        print("1. Insert")
        print("2. Delete")
        print("3. Search")
        print("4. Display (Traversals)")
        print("5. Exit")
        try:
            ch = int(input("Enter your choice: "))

            if ch == 5:
                print("Exiting program.")
                break
            if ch == 1:
                for k in map(int, input("Enter value(s): ").split()):
                    if t.insert(k):
                        print(f"{k} inserted.")
                    else:
                        print(f"{k} is a duplicate entry. Not inserted.")
                continue
            if 2 <= ch <= 4 and t.root is None:
                print("Tree is empty. Insert values first.")
                continue

            if ch == 2:
                k = int(input("Enter value to delete: "))
                if t.delete(k):
                    print(f"{k} deleted.")
                    print("Inorder now:", fmt(t.inorder(t.root, [])))
                else:
                    print(f"{k} not found in tree.")
            elif ch == 3:
                k = int(input("Enter value to search: "))
                level = t.search(k)
                if level:
                    print(f"{k} found at level {level}.")
                else:
                    print(f"{k} not found.")
            elif ch == 4:
                print("Inorder   :", fmt(t.inorder(t.root, [])))
                print("Preorder  :", fmt(t.preorder(t.root, [])))
                print("Postorder :", fmt(t.postorder(t.root, [])))
            else:
                print("Invalid choice! Try again.")
        except ValueError:
            print("Please enter whole numbers only.")


if __name__ == "__main__":
    main()
