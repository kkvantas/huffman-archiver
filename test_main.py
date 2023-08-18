from main import convert_to_bin_str, huffman_code_tree_stack, Node, build_tree
import pytest


def test_convert_to_bin_str():
    assert convert_to_bin_str(0) == '00000000'
    assert convert_to_bin_str(127) == '01111111'
    assert convert_to_bin_str(128) == '10000000'
    assert convert_to_bin_str(255) == '11111111'
    with pytest.raises(ValueError):
        convert_to_bin_str(256)
    with pytest.raises(ValueError):
        convert_to_bin_str(-1)


def test_build_tree():
    node1 = Node(('a', 4))
    node2 = Node(('b', 2))
    node3 = Node(('c', 1))
    lst = [node1, node2, node3]
    root = build_tree(lst)
    assert root.data == (None, 7)
    assert root.right.data == node1.data


def test_huffman_code_tree_stack():
    node1 = Node(('a', 4))
    node2 = Node(('b', 2))
    node3 = Node(('c', 1))
    lst = [node1, node2, node3]
    root = build_tree(lst)
    dict_test = huffman_code_tree_stack(root)
    assert len(dict_test) == 3
    assert set(dict_test.keys()) == {'a', 'b', 'c'}

