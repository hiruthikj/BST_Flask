from random import randint

from bst_final import BST


def main():
    bst = BST()

    bst.add_items(10, 5, 15, 1, 7, 25, 17)
    # arr = [1,2,3,4,5,6]

    bst.add_items(50)
    inserted = [50]
    cnt = 0
    while cnt < 30:
        num = randint(0, 100)
        if num in inserted:
            continue
        bst.add_item(num)
        # sleep(3)
        inserted.append(num)
        cnt += 1

    # x = tree.createTree(arr)
    # tree.preorderTraverse(x)

    # bst.build_tree(inserted)
    # bst.search_item(bst.root, int(input("Search: ")))
    # print(bst.get_height())
    # bst.remove_item(100)
    # print('PreOrderTraversal : ')
    # bst.preorderTraverse(bst.root)
    # print('\n')
    # print('PostOrderTraversal : ')
    # bst.postorderTraverse(bst.root)
    # print('\n')
    # print('InOrderTraversal : ')
    # bst.inorderTraverse(bst.root)
    # print('\n')

    print("Program Terminated")
    exit(0)


if __name__ == "__main__":
    main()
