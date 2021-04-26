from bst_final import BST


def main():
    bst = BST()
    print("Enter elements to build a Binary Search tree: ", end="")
    arr = list(set(map(int, input().split(" "))))
    arr.sort()
    bst.build_tree(arr)

    print(
        """
        Inorder - inord
        PostOrder - postord
        PreOrder - preord
        Search - S
        Insert - I
        Deletion - D
        TO EXIT ENTER - X
        """
    )

    while True:
        inputs = input("Enter operation: ").lower().split(" ")
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
        elif inputs[0] == "s":
            val = int(inputs[1])
            node = bst.search_item(bst.root, val)
            if node is None:
                print(f"{val} is not present")
            else:
                print(f"{node.value} found!!")
        elif inputs[0] == "i":
            val = int(inputs[1])
            while val in bst.label_dict.keys():
                val = int(input("Enter a value not present in the tree: "))
            bst.search_item(bst.root, val)
            bst.add_item(val)
            print()
        elif inputs[0] == "d":
            val = int(inputs[1])
            node = bst.remove_item(val)
            if node is None:
                print(f"{val} is not present")
            else:
                print(f"{node.value} deleted")
            print()

        elif inputs[0] == "x":
            break

    print("Program Terminated")
    exit(0)


if __name__ == "__main__":
    main()
