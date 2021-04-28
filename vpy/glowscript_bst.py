GlowScript 3.1 VPython
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
        scene.height = 500

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

            inserted = False
            for i in range(len(self.node_list)):
                curr_node = self.node_list[i]
                if new_node.value < curr_node.value:
                    self.node_list.insert(i, new_node)
                    inserted = True
                    break
            if not inserted:
                self.node_list.append(new_node)

            # self.node_list.append(new_node)

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
            inserted = False
            for i in range(len(self.node_list)):
                curr_node = self.node_list[i]
                if new_node.value < curr_node.value:
                    self.node_list.insert(i, new_node)
                    inserted = True
                    break
            if not inserted:
                self.node_list.append(new_node)

            # self.node_list.append(new_node)
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
            inserted = False
            for i in range(len(self.node_list)):
                curr_node = self.node_list[i]
                if new_node.value < curr_node.value:
                    self.node_list.insert(i, new_node)
                    inserted = True
                    break
            if not inserted:
                self.node_list.append(new_node)

            # self.node_list.append(new_node)
            parent.right = new_node

        self.label_dict[value] = [
            label(
                pos=new_node.pos, text=value, color=color.black, height=self.font_size
            ),
            arrow(pos=parent.pos, axis=new_node.pos - parent.pos, color=color.yellow)
        ]

        # self.refactor()
        self.refactor2()
        print("adding ", value)

    def search_item(self, node, value, show_animation=True):
        if node is None:
            return None

        if show_animation:
            node.color = color.magenta
            if self.get_arrow(node):
                self.get_arrow(node).color = color.magenta
            sleep(1)
            node.color = color.cyan
            if self.get_arrow(node):
                self.get_arrow(node).color = color.yellow

        if node.value == value:
            if show_animation:
                node.color = color.green
                sleep(2)
                node.color = color.cyan
            return node

        elif value < node.value:
            return self.search_item(node.left, value, show_animation)
        elif value > node.value:
            return self.search_item(node.right, value, show_animation)

    def remove_item(self, value):
        if len(self.node_list) == 1:
            to_return = self.root
            self.root = None
            self.label_dict = {}
            self.node_list = []
            return to_return

        node = self.search_item(self.root, value)
        if node is None:
            return None

        node.color = color.red

        v = vector(0, 0, 5)
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

            # print(self.node_list)
            # for i in range(len(self.node_list)):
            #     temp_node = self.node_list[i]
            #     print(temp_node)
            #     print(temp_node.value)
            #     if temp_node.value == value:
            #         self.node_list.pop(i)

            del node

        elif self.child_count(node) == 1:
            while t < 2:
                rate(1 / dt)
                node.pos += v * dt
                self.label_dict[node.value][0].pos = node.pos
                t += dt

            # print(node)
            # print(dir(node))
            if node is self.root:
                label_ = self.get_label(node)
                label_.visible = False
                del self.label_dict[node.value]

                child_ = node.left if node.right is None else node.left
                arr_ = self.get_arrow(child_)
                arr_.visible = False

                self.root.parent = None
                self.root = child_

                to_return = node
                node.visible = False
                del node

                self.refactor2()
                return to_return
            
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
            # for i in range(len(self.node_list)):
            #     temp_node = self.node_list[i]
            #     print(temp_node.value)
            #     if temp_node.value == value:
            #         self.node_list.pop(i)

            del node

        else:
            next_inorder_value = self.get_next_inorder(node).value
            to_return = self.remove_item(next_inorder_value)

            self.get_label(node).text = next_inorder_value
            self.label_dict[next_inorder_value] = self.label_dict[node.value]
            del self.label_dict[node.value]
            
            node.value = next_inorder_value

    
        # self.refactor()
        self.refactor2()
        return to_return

    def refactor2(self):
        if self.root is None:
            return

        to_remove = []
        for i in range(len(self.node_list)):
            if self.node_list[i] != self.search_item(self.root, self.node_list[i].value, False):
                to_remove.append(self.node_list[i].value)

        for (i, node) in enumerate(self.node_list):
            temp_node = self.node_list[i]
            # print("dir: ", dir(temp_node))
            if temp_node.value in to_remove:
                try:
                    self.node_list = self.node_list[:i] + self.node_list[i+1:]
                except:
                    self.node_list.pop(i)

        n = len(self.node_list)
        
        root_idx = 0
        for i in range(len(self.node_list)):
            if self.node_list[i] == self.root:
                root_idx = i
                break

        self.root.pos = vector(0,0,0)

        count = 1
        for i in range(root_idx + 1, n):
            node = self.node_list[i]
            node.pos = vector( count * self.level_breadth, -self.get_depth(node) * self.level_hgt , 0)
            count += 1

        count = 1
        for i in range(root_idx - 1, -1, -1):
            node = self.node_list[i]
            node.pos = vector( -count * self.level_breadth, -self.get_depth(node) * self.level_hgt , 0)
            count += 1

        for i in range(n):
            node = self.node_list[i]
            self.get_label(node).pos = node.pos
            
            if node is not self.root:
                self.get_arrow(node).pos = node.parent.pos
                self.get_arrow(node).axis = node.pos - node.parent.pos
            


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
        last_ele = None

        while len(queue) > 0:
            node = queue.pop()
            last_ele = node
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

        if last_ele:
            scene.center = self.root.pos + vector(0, last_ele.pos.y, 0)

    def build_tree(self, items):
        mid = len(items) // 2
        self.add_item(items[mid])
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

    def get_next_inorder(self,node):
        curr_node = node.right
        while curr_node.left:
            curr_node = curr_node.left

        return curr_node

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
            w = wtext(text='<h1>Inorder Traversal</h1>',pos=scene.title_anchor)
            print("Inorder Traversal :")
            bst.inorderTraverse(bst.root)
            bst.change_color()
            print()
            w.delete()
        elif inputs[0] == "preord":
            w = wtext(text='<h1>Preorder Traversal</h1>',pos=scene.title_anchor)
            print("Preorder Traversal :")
            bst.preorderTraverse(bst.root)
            bst.change_color()
            print()
            w.delete()
        elif inputs[0] == "postord":
            w = wtext(text='<h1>Postorder Traversal</h1>',pos=scene.title_anchor)
            print("Postorder Traversal :")
            bst.postorderTraverse(bst.root)
            bst.change_color()
            print()
            w.delete()
        elif inputs[0] == "S":
            w = wtext(text='<h1>Search</h1>',pos=scene.title_anchor)
            val = int(inputs[1])
            node = bst.search_item(bst.root, val)
            if node is None:
                print(f"{val} is not present")
            else:
                print(f"{node.value} found!!")
            w.delete()
        elif inputs[0] == "I":
            w = wtext(text='<h1>Insertion</h1>',pos=scene.title_anchor)
            val = int(inputs[1])
            node_list_vals = [ node.value for node in bst.node_list ]
            while val in node_list_vals:
                get_input("Enter a value not present in the tree: ")
                wait_for_input()
                val = int(inp_str)
            bst.search_item(bst.root, val)
            bst.add_item(val)
            print()
            w.delete()
        elif inputs[0] == "D":
            w = wtext(text='<h1>Deletion</h1>',pos=scene.title_anchor)
            val = int(inputs[1])
            node = bst.remove_item(val)
            if node is None:
                print(f"{val} is not present")
            else:
                print(f"{val} deleted")
            print()
            w.delete()

        elif inputs[0] == "X":
            break

    print("Program Terminated")
    # exit(0)


if __name__ == "__main__":
    main()
