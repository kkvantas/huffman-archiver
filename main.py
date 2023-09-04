from collections import Counter
import io
import argparse


def get_instructions():
    action = {'encode': encode_to_file,
              'decode': decode_from_file,
              }
    parser = argparse.ArgumentParser(description='Choose action and file name')
    parser.add_argument('action', type=str, help='Choose encode or decode pls', choices=list(action.keys()))
    parser.add_argument('name', type=str, help='Write name of file')
    args = parser.parse_args()
    return action[args.action](args.name)


class Node:
    def __init__(self, data, left=None, right=None):
        self.left = left
        self.right = right
        self.data = data

    def children(self):
        return self.left, self.right


def read_text(name):
    """
    read
    :param name: name of file
    :return: read file data
    """
    with open(f'{name}.txt', 'r', encoding='utf-8') as file:
        return file.read()


def save_list(list_of_freq, name):
    """Saves list of frequencies to file named as f_name.txt in a current directory.
    Uses `\n` as separator.

    :param list_of_freq: A list of tuples where 1st value - letter, 2nd - frequency
    :type list_of_freq: list
    :param name: Name of file
    :type name: str
    """
    with open(f'f_{name}.txt', 'a') as f_text:
        for i in list_of_freq:
            line = str(i[0]) + '=' + str(i[-1]) + '\n'
            f_text.write(line)


def get_list(name):
    """
    Takes f_name.txt and returns list of tuples.
    :param name: File name
    :return: list of tuples with frequencies AND INT EXTENTION
    """
    with open(f'f_{name}.txt', 'r') as f_text:
        frequency = f_text.read()
        ext = frequency[-2]
        frequency = frequency[:-5].split('\n')
        for i in frequency:
            if i == '':
                indx = frequency.index(i)
                frequency[indx] = '\n' + frequency[indx+1]
                frequency.pop(indx+1)
                break
        lst = list(map(lambda x: (x[0], int(x[2:])), frequency))
        return lst, int(ext)


def get_frequency(name):
    """
    Get text and count frequencies.
    :param name: name of file
    :return: list of tuples where 1st - letter, 2nd - int frequency
    """
    text = read_text(name)
    return Counter(text).most_common()[::-1]


def build_tree(frequency):
    """
    Takes frequencies and makes objs of Node class, then built l-r tree.
    :param frequency: list of tuples
    :return: root of tree
    """
    if not len(frequency):
        raise ValueError('Passing an empty nodes list is not supported')
    nodes = []
    for i in frequency:
        nodes.append(Node(i))
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
    return d


def huffman_code_tree_stack(name):
    """
    By name of file gets frequency and root, then write codes of letters via stack.
    Additional saves a list of frequency BECAUSE THIS FUNCTION CALLED ONLY IN CASE OF ENCODING.
    :param name: name of fine
    :return: dict where key - letter and code - value
    """
    frequency = get_frequency(name)
    root = build_tree(frequency)
    save_list(frequency, name)
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
    """
    :param i: integer which is encoded b-str
    :return: binary string but type just STR!!
    """
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
    """
    Decode binary string (which is actually just STR) to letters via huffman tree.
    :param root: root of the tree
    :param code_string: string of code
    :return: leftover(a piece of last coded letter, which tail is in next string), decoded letters
    """
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


def encode_to_file(name):
    """
    It is a kind of decorator to work with files like with stream
    :param name: name of encoded file
    :return: calls function encode_to_stream with args: text(already read there), dict of letters and codes,
    special uwu file for encoding, name of encoded file
    """
    text = read_text(name)
    # frequencies = calculate_frequencies(text)
    # root = build_tree(frequencies)
    # d = huffman_code_tree_stack(root)
    d = huffman_code_tree_stack(name)
    with open(f'{name}.uwu', 'wb') as output:
        return encode_to_stream(text, d, output, name)
    # save_list(frequencies, name)


def encode_to_stream(text, d, output, name):
    """
    This function was "decorated" for the sake of stream
    :param text: text for encoding
    :param d: dict with letters and codes
    :param output: special uwu file for encoding, WB
    :param name: name of encoded file
    :return: Nothing. Saves extention (int number of '0' which was added to finish final byte) to the end
    of file with frequencies.
    """
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
    print('file encoded!')
    save_list(str(ext), name)


def decode_from_file(name):
    """
    It is a kind of decorator to work with files like with stream. Getting here list of frequency,
     ext(int of zeros ammount in last byte), root, open encoded file(RB) and file in which decode(W+)
    :param name: name of file to decode
    :return: calls function decode_from_stream
    """
    frequency, ext = get_list(name)
    root = build_tree(frequency)
    with open(f'{name}.uwu', 'rb') as encoded_file:
        with open(f'{name}_encoded.txt', 'w+', encoding='utf8') as output_file:
            return decode_from_stream(root, ext, encoded_file, output_file)


def decode_from_stream(root, ext, encoded_stream, decoded_stream):
    """
    This function was "decorated" for the sake of stream
    :param root: root of huffman tree (obj of Node class)
    :param ext: int of zeros ammount in last byte
    :param encoded_stream: encoded uwu file(RB)
    :param decoded_stream: file in which decode(W+)
    :return: Nothing. Writes decoded file.
    """
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
    get_instructions()
# TODO: processing empty files

























