from main import convert_to_bin_str, huffman_code_tree_stack
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


def test_huffman_code_tree_stack():
    assert huffman_code_tree_stack()
