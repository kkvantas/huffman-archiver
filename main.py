from collections import Counter
import io


class Node:
    def __init__(self, data, left=None, right=None):
        self.left = left
        self.right = right
        self.data = data

    def children(self):
        return self.left, self.right


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


def encoding_to_file(text, d):
    with open('output.uwu', 'wb') as output:
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
    return output, ext


def convert_to_bin_str(i):
    n = 8
    string = ''
    while n:
        string = str(i & 0b00000001) + string
        i = i >> 1
        n -= 1
    return string


def decoding(node, ext):
    with open('output.uwu', 'rb') as output:
        with open('final.txt', 'w') as final:
            output.seek(0, io.SEEK_END)
            length = output.tell()
            output.seek(0, io.SEEK_SET)
            string = ''
            orig_node = node
            for i in range(1, length+1):
                byte = output.read(1)
                byte = int.from_bytes(byte, "big")
                string += convert_to_bin_str(byte)
                if i == length:
                    string = string[:-ext]
                node = orig_node
                count = 0
                for num in string:
                    leftover = ''
                    if num == '1':
                        node = node.right
                    elif num == '0':
                        node = node.left
                    if node.data[0]:
                        final.write(node.data[0])
                        node = orig_node
                        leftover = string[(count+1):]

                    count += 1
                string = leftover




if __name__ == "__main__":
    with open('text.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    frequency = Counter(text).most_common()[::-1]

    nodes = []

    for i in frequency:
        nodes.append(Node(i))

    while len(nodes) > 1:
        nodes.append(Node((None, nodes[0].data[1] + nodes[1].data[1]), nodes[0], nodes[1]))
        del nodes[:2]
        nodes = sorted(nodes, key=lambda x: x.data[1])

    node = nodes[0]

    d1 = dict()
    huffman_code_tree_stack(node, d1)

    print(d1)

    output, ext = encoding_to_file(text, d1)

    decoding(node, ext)




























