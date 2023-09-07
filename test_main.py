import io

from main import (
    convert_to_bin_str,
    huffman_code_tree_stack,
    build_tree,
    decode_code_string,
    encode_to_stream,
    decode_from_stream,
    Node,
    calculate_frequency,
    get_length
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
    frequencies = [('a', 4), ('b', 2), ('c', 1)]
    root = build_tree(frequencies)
    assert root.data == (None, 7)
    assert root.right.data == ('a', 4)
    root2 = build_tree([])
    assert root2.data == (None, 0)
    assert root2.left == root2.right is None


def test_huffman_code_tree_stack():
    frequencies = [('a', 4), ('b', 2), ('c', 1)]
    root = build_tree(frequencies)
    dict_test = huffman_code_tree_stack(root)
    assert len(dict_test) == 3
    assert set(dict_test.keys()) == {'a', 'b', 'c'}
    assert huffman_code_tree_stack(Node((None, 0))) == dict()


def test_decode_code_string():
    frequencies = [('a', 4), ('b', 2), ('c', 1)]
    root = build_tree(frequencies)
    assert decode_code_string(root, '11111111') == ('', 'aaaaaaaa')
    assert decode_code_string(root, '01010101') == ('', 'bbbb')
    assert decode_code_string(root, '10101010') == ('0', 'abbb')
    assert decode_code_string(root, '00000000') == ('', 'cccc')


def test_encode_to_stream():
    frequencies = [('a', 4), ('b', 2), ('c', 1)]
    root = build_tree(frequencies)
    d = huffman_code_tree_stack(root)

    def encode_to_stream_wrapper(string, d_):
        stream = io.BytesIO()
        ext = encode_to_stream(string, d_, stream)
        buffer = stream.getvalue()
        return buffer, ext

    assert encode_to_stream_wrapper("abcc", d) == (b'\xa0', '1')
    assert encode_to_stream_wrapper("aaabcc", d) == (b'\xe8', '0')
    assert encode_to_stream_wrapper("", d) == (b'', '0')
    assert encode_to_stream_wrapper("", dict()) == (b'', '0')


def test_decoding_stream():
    frequencies = [('a', 4), ('b', 2), ('c', 1)]
    root = build_tree(frequencies)

    def decoding_stream_wrapper(ext, encoded_bytes):
        decoded_stream = io.StringIO()
        encoded_stream = io.BytesIO(encoded_bytes)
        decode_from_stream(root, ext, encoded_stream, decoded_stream)
        value = decoded_stream.getvalue()
        decoded_stream.close()
        encoded_stream.close()
        return value

    assert decoding_stream_wrapper(1, b'\xa0') == 'abcc'


def test_calculate_frequency():
    assert calculate_frequency('aaabbcd') == [('d', 1), ('c', 1), ('b', 2), ('a', 3)]
    assert calculate_frequency('') == []


def test_get_length():
    def get_length_wrapper(string):
        return get_length(io.StringIO(string))

    assert get_length_wrapper('') == 0
    assert get_length_wrapper('123456789') == 9
    assert get_length(io.StringIO('string')) == 6
