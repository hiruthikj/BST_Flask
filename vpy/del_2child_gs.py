GlowScript 3.0 VPython
# from time import sleep
# from vpython import *


class BST:
    def __init__(self):
        self.root = None
        self.label_dict = {}
        self.node_list = []

        self.level_breadth = 5
        self.level_hgt = 5
        self.radius = 2

        self.font_size = 15

        scene.background = color.white
        scene.autoscale = True

        scene.width = 1280
        scene.height = 620

        print("BST initialted")

    def add_item(self, value):
        rate(1.5)
        if self.root is None:
            new_node = sphere(
                pos=vector(0, 0, 0),
                radius=self.radius,
                color=color.cyan,
                value=value,
                left=None,
                right=None,
                parent=None
            )
            self.node_list.append(new_node)
#issue

            self.label_dict[value] = (
                label(
                    pos=new_node.pos,
                    text=value,
                    color=color.black,
                    height=self.font_size), None
            )
            self.root = new_node
            return self.root

        pointer = self.root
        parent = None
        insert_left = None

        while pointer:
            parent = pointer
            if value < pointer.value:
                pointer = pointer.left
                insert_left = True
            elif value > pointer.value:
                pointer = pointer.right
                insert_left = False

        if insert_left:
            new_node = sphere(
                pos=parent.pos + vector(-self.level_breadth, -self.level_hgt, 0),
                radius=self.radius,
                color=color.cyan,
                value=value,
                left=None,
                right=None,
                parent=parent
            )
            self.node_list.append(new_node)
            parent.left = new_node
        else:
            new_node = sphere(
                pos=parent.pos + vector(self.level_breadth, -self.level_hgt, 0),
                radius=self.radius,
                color=color.cyan,
                value=value,
                left=None,
                right=None,
                parent=parent
            )
            self.node_list.append(new_node)
            parent.right = new_node

        self.label_dict[value] = [
            label(
                pos=new_node.pos, text=value, color=color.black, height=self.font_size
            ),
            arrow(pos=parent.pos, axis=new_node.pos - parent.pos, color=color.yellow)
        ]

        self.refactor()

    def search_item(self, node, value):
        if node is None:
            return None

        node.color = color.magenta
        if self.get_arrow(node):
            self.get_arrow(node).color = color.magenta
        sleep(1)
        node.color = color.cyan
        if self.get_arrow(node):
            self.get_arrow(node).color = color.yellow

        if node.value == value:
            node.color = color.green
            sleep(2)
            node.color = color.cyan

            return node

        elif value < node.value:
            return self.search_item(node.left, value)
        elif value > node.value:
            return self.search_item(node.right, value)

    def remove_item(self, value):
        node = self.search_item(self.root, value)
        if node is None:
            # print(f"Item {value} doesn't exist")
            return None

        node.color = color.red

        v = vector(0, 0, 5)  # + self.label_dict[node.value][1].axis
        dt = 0.05
        t = 0

        if self.is_leaf(node):
            while t < 3:
                rate(1 / dt)
                node.pos += v * dt
                self.label_dict[node.value][0].pos = node.pos
                t += dt

            self.label_dict[node.value][0].visible = False
            self.label_dict[node.value][1].visible = False
            node.visible = False

            if self.is_left(node):
                node.parent.left = None
            else:
                node.parent.right = None

            to_return = node
            del self.label_dict[node.value]
            del node

        elif self.child_count(node) == 1:
            while t < 2:
                rate(1 / dt)
                node.pos += v * dt
                self.label_dict[node.value][0].pos = node.pos
                t += dt

            self.label_dict[node.value][0].visible = False
            self.label_dict[node.value][1].visible = False
            node.visible = False

            if self.is_left(node):
                if node.right is None:
                    self.label_dict[node.left.value][1].pos = node.parent.pos
                    self.label_dict[node.left.value][1].axis = (
                        node.left.pos - node.parent.pos
                    )
                    node.parent.left = node.left
                    node.left.parent = node.parent
                else:
                    self.label_dict[node.right.value][1].pos = node.parent.pos
                    self.label_dict[node.right.value][1].axis = (
                        node.right.pos - node.parent.pos
                    )
                    node.parent.left = node.right
                    node.right.parent = node.parent
            else:
                if node.right is None:
                    self.label_dict[node.left.value][1].pos = node.parent.pos
                    self.label_dict[node.left.value][1].axis = (
                        node.left.pos - node.parent.pos
                    )
                    node.parent.right = node.left
                    node.left.parent = node.parent
                else:
                    self.label_dict[node.right.value][1].pos = node.parent.pos
                    self.label_dict[node.right.value][1].axis = (
                        node.right.pos - node.parent.pos
                    )
                    node.parent.right = node.right
                    node.right.parent = node.parent

            to_return = node
            del self.label_dict[node.value]
            del node
            
        else:
#            while t < 2:
#                rate(1 / dt)
#                node.pos += v * dt
#                self.label_dict[node.value][0].pos = node.pos
#                t += dt
            
            in_arr = []
            for i in self.node_list:
                in_arr.append(i.value)
            in_arr.sort()
            print(in_arr)
            x = in_arr.index(value)+1
            
            
            self.remove_item(in_arr[x])        
            node.value = in_arr[x]
            
            
    
        self.refactor()
        return to_return

    def refactor(self, level_breadth="default", level_hgt="default"):
        if self.root is None:
            return

        if level_breadth == "default":
            level_breadth = self.level_breadth

        if level_hgt == "default":
            level_hgt = self.level_hgt

        tree_depth = self.get_height(self.root)

        queue = []
        queue.append(self.root)
        while len(queue) > 0:
            node = queue.pop()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

            if node is self.root:
                node.radius = 1.5 ** (tree_depth)
                node_label = self.get_label(node)
                node_label.height = max(1.5 ** (tree_depth), 10)
                continue  # no need to move root node position

            node_depth = self.get_depth(node)
            if self.is_left(node):
                node.pos = vector(
                    node.parent.pos.x
                    - level_breadth * 1.5 ** (tree_depth - node_depth)
                    - node.radius,
                    node.parent.pos.y - level_hgt * 1.5 ** (tree_depth - node_depth),
                    node.pos.z
                )
            else:
                node.pos = vector(
                    node.parent.pos.x
                    + level_breadth * 1.5 ** (tree_depth - node_depth)
                    + node.radius,
                    node.parent.pos.y - level_hgt * 1.5 ** (tree_depth - node_depth),
                    node.pos.z
                )
            node.radius = 1.5 ** (tree_depth - node_depth)

            node_label = self.get_label(node)
            node_arrow = self.get_arrow(node)

            node_label.pos = node.pos
            node_label.height = max(1.5 ** (tree_depth - node_depth), 10)

            node_arrow.pos = node.parent.pos
            node_arrow.axis = node.pos - node.parent.pos

    def build_tree(self, items):
        mid = len(items) // 2
        self.add_item(items[mid])
        # self.search_item(self.root,items[mid])
        del items[mid]
        if len(items) > 1:
            self.build_tree(items[0:mid])
            self.build_tree(items[mid : len(items) + 1])
        else:
            if len(items) == 1:
                self.add_item(items[0])

    def get_height(self, node="root"):
        if node == "root":
            node = self.root
        if node is None:
            return 0
        else:
            return 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_depth(self, node):
        if node == self.root:
            return 0
        else:
            return 1 + self.get_depth(node.parent)

    def preorderTraverse(self, v):
        curnode = v
        curnode.color = color.red
        print(curnode.value, end=" ")
        sleep(1)
        if curnode.left != None:
            self.preorderTraverse(curnode.left)
        if curnode.right != None:
            self.preorderTraverse(curnode.right)
        return

    def postorderTraverse(self, v):
        curnode = v
        curnode.color = color.magenta
        if curnode.left != None:
            sleep(1)
            self.postorderTraverse(curnode.left)
        if curnode.right != None:
            sleep(1)
            self.postorderTraverse(curnode.right)
        sleep(1)
        curnode.color = color.red
        print(curnode.value, end=" ")
        return


    def inorderTraverse(self, curnode):
        curnode.color = color.magenta
        if curnode.left != None:
            sleep(1)
            self.inorderTraverse(curnode.left)
        sleep(1)
        curnode.color = color.red
        print(curnode.value, end=" ")

        if curnode.right != None:
            sleep(1)
            self.inorderTraverse(curnode.right)
        return

    def add_items(self, *args):
        for value in args:
            self.add_item(value)

    def is_leaf(self, node):
        return node.left is None and node.right is None

    def is_left(self, node):
        return node is node.parent.left

    def child_count(self, node):
        return (0 if node.left is None else 1) + (0 if node.right is None else 1)

    def get_label(self, node):
        return self.label_dict[node.value][0]

    def get_arrow(self, node):
        return self.label_dict[node.value][1]

    def change_color(self):
        for i in self.node_list:
            i.color = color.cyan

    def get_value(self, node):
        return node.value


inp_str = ""
win = None

def bind_fn(obj):
    global inp_str, win
    inp_str = obj.text
    win.delete()


def get_input(prompt_text=""):
    global inp_str, win
    inp_str = ""
    win = winput(prompt=prompt_text, type='string', bind=bind_fn)
    
        
def wait_for_input():
    global inp_str
    while inp_str == "":
        rate(100)

def main():
    global inp_str, win
    bst = BST()

    get_input("Enter elements to build a Binary Search tree: ")
    wait_for_input()

    arr = list(set(map(int, inp_str.split(" "))))
    arr.sort()
    bst.build_tree(arr)

    while True:
        get_input("Enter operation: ")
        wait_for_input()

        inputs = inp_str.split(" ")
        if inputs[0] == "inord":
            bst.inorderTraverse(bst.root)
            bst.change_color()
            print()
        elif inputs[0] == "preord":
            bst.preorderTraverse(bst.root)
            bst.change_color()
            print()
        elif inputs[0] == "postord":
            bst.postorderTraverse(bst.root)
            bst.change_color()
            print()
        elif inputs[0] == "S":
            val = int(inputs[1])
            node = bst.search_item(bst.root, val)
            if node is None:
                print(f"{val} is not present")
            else:
                print(f"{node.value} found!!")
        elif inputs[0] == "I":
            val = int(inputs[1])
            while val in bst.label_dict.keys():
                get_input("Enter a value not present in the tree: ")
                wait_for_input()
                val = int(inp_str)
            bst.search_item(bst.root, val)
            bst.add_item(val)
            print()
        elif inputs[0] == "D":
            val = int(inputs[1])
            node = bst.remove_item(val)
            if node is None:
                print(f"{val} is not present")
            else:
                print(f"{node.value} deleted")
            print()

        elif inputs[0] == "X":
            break

    print("Program Terminated")
    # exit(0)


if __name__ == "__main__":
    main()
