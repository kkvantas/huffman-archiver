from collections import Counter


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

def encoding(text, d):
    code = ''
    for i in text:
        code = code + d[i]
    ext = 8 - len(code) % 8
    code = code + ext * '0'
    return ''.join(chr(int(x, 2)) for x in map(''.join, zip(*[iter(code)] * 8)))


def encoding_to_file(text, d):
    with open('output.uwu', 'wb') as output:
        byte = ''
        for i in text:
            if len(byte + d[i]) < 8:
                byte = byte + d[i]
                if i == text[-1]:
                    ext = 8 - len(byte)
                    byte = byte + ext * '0'
                    output.write(int(byte, 2).to_bytes(1, byteorder='big'))
            elif len(byte + d[i]) > 8:
                byte = (byte + d[i])[:8]
                tail = (byte + d[i])[9:]
                output.write(int(byte, 2).to_bytes(1, byteorder='big'))
                byte = tail
            elif len(byte + d[i]) == 8:
                byte = byte + d[i]
                output.write(int(byte, 2).to_bytes(1, byteorder='big'))
    return output, ext


def calc_to_bin(i):
    n = 8
    strin = ''
    while n:
        strin = str(i & 0b00000001) + strin
        i = i >> 1
        n -= 1
    return strin



def decoding(node, ext):
    with open('output.uwu', 'rb') as output:
        with open('final.txt', 'w') as final:
            byte = output.read()
            sum = ''
            for i in byte:
                if i == byte[-1]:
                    i = calc_to_bin(i)
                    i = i[:-ext]
                else:
                    i = calc_to_bin(i)
                sum += i
            orig_node = node
            for num in sum:
                if num == '1':
                    node = node.right
                    if node.data[0]:
                        final.write(node.data[0])
                        node = orig_node
                elif num == '0':
                    node = node.left
                    if node.data[0]:
                        final.write(node.data[0])
                        node = orig_node






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
            nodes = sorted(nodes, key=lambda freq: freq.data[1])

    node = nodes[0]

    d1 = dict()
    huffman_code_tree_recursive(node, d1)

    output, ext = encoding_to_file(text, d1)


    decoding(node, ext)




























