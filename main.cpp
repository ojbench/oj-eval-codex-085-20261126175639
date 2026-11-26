#include <iostream>
#include <vector>

struct Node {
    int value;
    int left = -1;
    int right = -1;
    bool keep = false;
};

struct Slot {
    int parent;
    bool right;
};

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    std::vector<Node> nodes;
    std::vector<Slot> pending{{-1, false}};
    int root = -1;
    int value;
    while (std::cin >> value && value != -2) {
        if (pending.empty()) {
            break;
        }
        const Slot slot = pending.back();
        pending.pop_back();
        if (value == -1) {
            continue;
        }
        const int index = static_cast<int>(nodes.size());
        nodes.push_back(Node{value});
        if (slot.parent == -1) {
            root = index;
        } else if (slot.right) {
            nodes[slot.parent].right = index;
        } else {
            nodes[slot.parent].left = index;
        }
        // Preorder fills the left slot first; omitted trailing slots stay null.
        pending.push_back({index, true});
        pending.push_back({index, false});
    }

    // Every descendant has a larger preorder index than its ancestors.
    for (int i = static_cast<int>(nodes.size()) - 1; i >= 0; --i) {
        Node& node = nodes[i];
        node.keep = node.value == 1 ||
                    (node.left != -1 && nodes[node.left].keep) ||
                    (node.right != -1 && nodes[node.right].keep);
    }

    std::vector<int> traversal{root};
    bool first = true;
    while (!traversal.empty()) {
        const int index = traversal.back();
        traversal.pop_back();
        if (!first) {
            std::cout << ' ';
        }
        first = false;
        if (index == -1 || !nodes[index].keep) {
            std::cout << -1;
        } else {
            const Node& node = nodes[index];
            std::cout << node.value;
            traversal.push_back(node.right);
            traversal.push_back(node.left);
        }
    }
    std::cout << '\n';
}
