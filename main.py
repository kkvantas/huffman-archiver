from collections import Counter
import io


class Node:
    def __init__(self, data, left=None, right=None):
        self.left = left
        self.right = right
        self.data = data

    def children(self):
        return self.left, self.right


def build_tree(nodes=list):
    while len(nodes) > 1:
        nodes.append(Node((None, nodes[0].data[1] + nodes[1].data[1]), nodes[0], nodes[1]))
        del nodes[:2]
        nodes = sorted(nodes, key=lambda x: x.data[1])

def huffman_code_tree_recursive(n, d, st=''):
    if n:
        if type(n.data[0]) is str:
            d[n.data[0]] = st
        (l, r) = n.children()
        huffman_code_tree_recursive(l, d, st + '0')
        huffman_code_tree_recursive(r, d, st + '1')


def huffman_code_tree_stack(n, d):
    stack = [(n, '')]
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


def get_length(file):
    file.seek(0, io.SEEK_END)
    length = file.tell()
    file.seek(0, io.SEEK_SET)
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
        length = get_length(output)
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
    return output, ext


def decoding(root, ext):
    with open('output.uwu', 'rb') as output:
        with open('final.txt', 'w', encoding='utf8') as final:
            length = get_length(output)
            string = ''
            #root = node
            for i in range(1, length+1):
                byte = output.read(1)
                byte = int.from_bytes(byte, "big")
                string += convert_to_bin_str(byte)
                if i == length:
                    string = string[:-ext]
                string, letters = decode_code_string(root, string)
                if len(letters):
                    final.write(letters)


if __name__ == "__main__":
    with open('text.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    frequency = Counter(text).most_common()[::-1]

    nodes = []

    for i in frequency:
        nodes.append(Node(i))

    build_tree(nodes)

    node = nodes[0]

    d1 = dict()
    huffman_code_tree_stack(node, d1)

    print(d1)

    output, ext = encoding_to_file(text, d1)

    decoding(node, ext)




























