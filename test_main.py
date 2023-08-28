import io

from main import (
    convert_to_bin_str,
    huffman_code_tree_stack,
    Node,
    build_tree,
    decode_code_string,
    encode_to_stream,
    decoding_stream
)
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
    with pytest.raises(ValueError):
        build_tree([])


def test_huffman_code_tree_stack():
    node1 = Node(('a', 4))
    node2 = Node(('b', 2))
    node3 = Node(('c', 1))
    lst = [node1, node2, node3]
    root = build_tree(lst)
    dict_test = huffman_code_tree_stack(root)
    assert len(dict_test) == 3
    assert set(dict_test.keys()) == {'a', 'b', 'c'}


def test_decode_code_string():
    node1 = Node(('a', 4))
    node2 = Node(('b', 2))
    node3 = Node(('c', 1))
    lst = [node1, node2, node3]
    root = build_tree(lst)
    assert decode_code_string(root, '11111111') == ('', 'aaaaaaaa')
    assert decode_code_string(root, '01010101') == ('', 'bbbb')
    assert decode_code_string(root, '10101010') == ('0', 'abbb')
    assert decode_code_string(root, '00000000') == ('', 'cccc')


def test_encode_to_stream():
    node1 = Node(('a', 4))
    node2 = Node(('b', 2))
    node3 = Node(('c', 1))
    lst = [node1, node2, node3]
    root = build_tree(lst)
    dict = huffman_code_tree_stack(root)

    def encode_to_stream_wrapper(str, dict):
        stream = io.BytesIO()
        encode_to_stream(str, dict, stream)
        stream.seek(0)
        return stream.read()

    assert encode_to_stream_wrapper("abcc", dict) == b'\xa0'
    assert encode_to_stream_wrapper("aaabcc", dict) == b'\xe8'
    assert encode_to_stream_wrapper("", dict) == b''


def test_decoding_stream():
    node1 = Node(('a', 4))
    node2 = Node(('b', 2))
    node3 = Node(('c', 1))
    lst = [node1, node2, node3]
    root = build_tree(lst)
    dict = huffman_code_tree_stack(root)

    def decoding_stream_wrapper(ext, string):
        stream = io.BytesIO()
        decoding_stream(root, ext, string, stream)
        stream.seek(0)
        return stream.read()

    assert decoding_stream_wrapper(3, '10100000') == 'abc'