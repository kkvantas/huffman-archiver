from collections import Counter
import io


class Node:
    def __init__(self, data, left=None, right=None):
        self.left = left
        self.right = right
        self.data = data

    def children(self):
        return self.left, self.right


def build_tree(nodes):
    if not len(nodes):
        raise ValueError('Passing an empty nodes list is not supported')
    nodes = sorted(nodes, key=lambda x: x.data[1])
    while len(nodes) > 1:
        nodes.append(Node((None, nodes[0].data[1] + nodes[1].data[1]), nodes[0], nodes[1]))
        del nodes[:2]
        nodes = sorted(nodes, key=lambda x: x.data[1])
    return nodes[0]


def huffman_code_tree_recursive(n, d, st=''):
    if n:
        if type(n.data[0]) is str:
            d[n.data[0]] = st
        (l, r) = n.children()
        huffman_code_tree_recursive(l, d, st + '0')
        huffman_code_tree_recursive(r, d, st + '1')


def huffman_code_tree_stack(root):
    stack = [(root, '')]
    d = dict()
    while len(stack):
        node, code = stack.pop()
        char, freq = node.data
        if type(char) is str:
            d[char] = code
        l, r = node.children()
        if r:
            stack.append((r, code + '1'))
        if l:
            stack.append((l, code + '0'))
    return d


def get_length(stream):
    stream.seek(0, io.SEEK_END)
    length = stream.tell()
    stream.seek(0, io.SEEK_SET)
    return length


def convert_to_bin_str(i):
    if i not in range(0, 256):
        raise ValueError
    n = 8
    string = ''
    while n:
        string = str(i & 0b00000001) + string
        i = i >> 1
        n -= 1
    return string


def decode_code_string(root, code_string):
    count = 0
    node = root
    leftover = code_string
    letters = ''
    for num in code_string:
        if node:
            if num == '1':
                node = node.right
            elif num == '0':
                node = node.left
            if node:
                if node.data[0]:
                    letters += node.data[0]
                    leftover = code_string[(count + 1):]
                    node = root
            count += 1
    return leftover, letters


def encoding_to_file(text, d):
    with open('output.uwu', 'wb') as output:
        return encode_to_stream(text, d, output)


def encode_to_stream(text, d, output):
    length = len(text)
    byte = ''
    ext = 0
    count = 1
    for i in text:
        if len(byte + d[i]) < 8:
            byte = byte + d[i]
            if count == length:
                ext = 8 - len(byte)
                byte = byte + ext * '0'
                output.write(int(byte, 2).to_bytes(1, byteorder='big'))
        elif len(byte + d[i]) > 8:
            tail = (byte + d[i])[8:]
            byte = (byte + d[i])[:8]
            output.write(int(byte, 2).to_bytes(1, byteorder='big'))
            byte = tail
        elif len(byte + d[i]) == 8:
            byte = byte + d[i]
            output.write(int(byte, 2).to_bytes(1, byteorder='big'))
            byte = ''
        count += 1
    return ext


def decoding(root, ext):
    with open('output.uwu', 'rb') as encoded_file:
        with open('final.txt', 'w', encoding='utf8') as output_file:
            return decoding_stream(root, ext, encoded_file, output_file)


def decoding_stream(root, ext, encoded_stream, decoded_stream):
    length = get_length(encoded_stream)
    string = ''
    for i in range(1, length+1):
        byte = encoded_stream.read(1)
        byte = int.from_bytes(byte, "big")
        string += convert_to_bin_str(byte)
        if i == length:
            string = string[:-ext]
        string, letters = decode_code_string(root, string)
        if len(letters):
            decoded_stream.write(letters)


if __name__ == "__main__":
    with open('text.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    frequency = Counter(text).most_common()[::-1]

    nodes = []

    for i in frequency:
        nodes.append(Node(i))

    root = build_tree(nodes)

    dict_with_code = huffman_code_tree_stack(root)

    print(dict_with_code)

    ext = encoding_to_file(text, dict_with_code)

    decoding(root, ext)


# TODO: processing empty files

























