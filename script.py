"""
Please check the README.txt file.

Ali Mirzaee
Rasul Khjeh Mirzaee

FP-Growth Algorithm

"""

class FPTree:
    """ FP Tree """
    def __init__(self):
        self.root = FPNode(None, None)
        self.item_counts = {}

    def insert(self, transaction):
        node = self.root
        for item in transaction:
            child = node.get_child(item)
            if child:   # check if new item is a child or it's not
                child.count += 1
            else:      # create new node for new items
                new_child = FPNode(item, node)
                node.add_child(new_child)
            node = node.get_child(item)
            
            # Track item counts for all items
            if item in self.item_counts:
                self.item_counts[item] += 1
            else:
                self.item_counts[item] = 1

    def traverse(self, support):
        frequent_itemsets = []
        self._traverse(self.root, [], frequent_itemsets, support)
        # Sort by count in descending order, then by itemset length in ascending order
        frequent_itemsets.sort(key=lambda x: (x[0], -len(x[1])), reverse=True)  
        
        # Append most repeated items at the end of the output
        most_repeated_items = sorted(self.item_counts.items(), key=lambda x: x[1], reverse=True)
        for item, count in most_repeated_items:
            if count >= support:
                frequent_itemsets.append((count, [item]))
        
        return frequent_itemsets

    def _traverse(self, node, prefix, frequent_itemsets, support):
        if node is None:
            return

        if node.item is not None and node.count >= support:
            # Store count along with itemset
            frequent_itemsets.append((node.count, prefix + [node.item]))  

        for child in node.children.values():
            self._traverse(child, prefix + [node.item], frequent_itemsets, support)


class FPNode:
    """ FP tree node """
    def __init__(self, item, parent):
        self.item = item
        self.count = 1
        self.parent = parent
        self.children = {}

    def add_child(self, child):
        if child.item in self.children:
            self.children[child.item].count += child.count
        else:
            self.children[child.item] = child

    def get_child(self, item):
        return self.children.get(item)


def main():
    """ Main function """
    # take user file input
    file_path = input("Enter the path of the dataset text file: ")

    dataset = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.replace('dataset', '').replace('[', '').replace(']', '').replace('=', '').replace('\n', '')
            items = line.split(',')
            dataset.append([item for item in items if item.strip() != ''])
    
    # create FP tree
    fp_tree = FPTree()
    for itemset in dataset:
        fp_tree.insert(itemset)
    
    support = int(input('support: '))
    # Set a minimum count of 1 for all itemsets
    frequent_itemsets = fp_tree.traverse(support)  

    for count, itemset in frequent_itemsets:
        print(itemset, "(Count:", count, ")")


if __name__ == "__main__":
    main()