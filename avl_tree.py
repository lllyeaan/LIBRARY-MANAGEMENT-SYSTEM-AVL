class Node:
    def __init__(self, book):
        self.book = book
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.height(node.left) - self.height(node.right)

    def right_rotate(self, z):
        y = z.left
        t3 = y.right

        y.right = z
        z.left = t3

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def left_rotate(self, z):
        y = z.right
        t2 = y.left

        y.left = z
        z.right = t2

        z.height = 1 + max(self.height(z.left), self.height(z.right))
        y.height = 1 + max(self.height(y.left), self.height(y.right))
        return y

    def insert(self, root, book):
        if root is None:
            return Node(book)

        # Ubah perbandingan ke int untuk sorting numerik
        if int(book.key) < int(root.book.key):
            root.left = self.insert(root.left, book)
        elif int(book.key) > int(root.book.key):
            root.right = self.insert(root.right, book)
        else:
            # perbarui data jika kunci duplikat
            root.book = book
            return root

        root.height = 1 + max(self.height(root.left), self.height(root.right))

        balance = self.get_balance(root)

        if balance > 1:
            if int(book.key) < int(root.left.book.key):
                return self.right_rotate(root)
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1:
            if int(book.key) > int(root.right.book.key):
                return self.left_rotate(root)
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def search(self, root, key):
        if root is None:
            return None
        if int(key) == int(root.book.key):
            return root.book
        if int(key) < int(root.book.key):
            return self.search(root.left, key)
        return self.search(root.right, key)

    def get_min_value_node(self, root):
        current = root
        while current.left:
            current = current.left
        return current

    def delete(self, root, key):
        if root is None:
            return None

        # Ubah perbandingan ke int
        if int(key) < int(root.book.key):
            root.left = self.delete(root.left, key)
        elif int(key) > int(root.book.key):
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            if root.right is None:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.book = temp.book
            root.right = self.delete(root.right, temp.book.key)

        root.height = 1 + max(self.height(root.left), self.height(root.right))
        balance = self.get_balance(root)

        if balance > 1:
            if self.get_balance(root.left) >= 0:
                return self.right_rotate(root)
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1:
            if self.get_balance(root.right) <= 0:
                return self.left_rotate(root)
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.book)
            self.inorder(root.right)