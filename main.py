from collections import Counter
import io
import argparse


def get_instructions():
    """ Interface. Via terminal user can choose to encode or to decode required file
    :return: Calls function of encoding or decoding with name (of chosen file) param.
    """
    action = {'encode': encode_to_file,
              'decode': decode_from_file,
              }
    parser = argparse.ArgumentParser(description='Choose action and file name')
    parser.add_argument('action', type=str, help='Choose encode or decode pls', choices=list(action.keys()))
    parser.add_argument('name', type=str, help='Write name of file')
    args = parser.parse_args()
    return action[args.action](args.name)


class Node:
    """ Class of a node of a binary tree.
    """
    def __init__(self, data, left=None, right=None):
        """ Assigns values to object properties
        :param data: Letter and number
        :type data: tuple
        :param left: Link to left child node
        :type left: Node class obj
        :param right: Link to right child node
        :type right: Node class obj
        """
        self.left = left
        self.right = right
        self.data = data

    def children(self):
        """
        :return: Link to left and right child nodes
        """
        return self.left, self.right


def read_text(name):
    """ Open and read file name
    :param name: Name of file
    :type name: str
    :return: Read file data
    """
    with open(f'{name}', 'r', encoding='utf-8') as file:
        return file.read()


def save_list(list_of_freq, ext, name):
    """Saves list of frequencies to file named as f_name in a current directory.
    Uses `\n` as separator
    :param list_of_freq: A list of tuples where 1st value - letter, 2nd - frequency
    :type list_of_freq: list or str
    :param name: Name of file
    :type name: str
    :param ext: Number of '0' which was added to finish final byte
    :type ext: str
    """
    with open(f'f_{name}', 'a') as f_text:
        for i in list_of_freq:
            line = str(i[0]) + '=' + str(i[-1]) + '\n'
            f_text.write(line)
        f_text.write(ext)


def load_list(name):
    """ Read and parce file name to list of tuples
    :param name: File name
    :type name: str
    :return: list of tuples with frequencies AND INT EXTENSION
    """
    with open(f'f_{name}', 'r') as f_text:
        frequency = f_text.read()
        ext = frequency[-1]
        if len(frequency) == 1:
            return [], int(ext)
        frequency = frequency[:-2].split('\n')
        for i in frequency:
            if i == '':
                indx = frequency.index(i)
                frequency[indx] = '\n' + frequency[indx+1]
                frequency.pop(indx+1)
                break
        lst = list(map(lambda x: (x[0], int(x[2:])), frequency))
        return lst, int(ext)


def calculate_frequency(text):
    """ Takes text and count frequencies.
    :param text: Transferred text
    :type text: text I/O
    :return: List of tuples where 1st - letter, 2nd - int frequency
    """
    return Counter(text).most_common()[::-1]


def build_tree(frequency):
    """ Takes frequencies and makes objs of Node class, then builds l-r tree
    :param frequency: Tuples where 1st - letter, 2nd - int frequency
    :type frequency: list
    :return: Root of tree
    """
    if not len(frequency):
        return Node((None, 0))
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


def huffman_code_tree_stack(root):
    """ Writes in dict codes of letters via stack
    :param root: Root of huffman tree
    :type root: Node class obj
    :return: dict where key - letter and code - value
    """
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
    """
    Gets length of stream
    :param stream: Various types of I/O
    :return: Length in int
    """
    stream.seek(0, io.SEEK_END)
    length = stream.tell()
    stream.seek(0, io.SEEK_SET)
    return length


def convert_to_bin_str(i):
    """ Convert int to binary string
    :param i: coded oct number
    :type i: int
    :return: binary string, but type just STR!!
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
    """ Decode binary string to letters via huffman tree
    :param root: Root of the tree
    :type root: Node class obj
    :param code_string: String of bin code
    :type code_string: str
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
    """ Gets encoding text, dict of letters and codes, uwu file for encoding
    :param name: Name of encoded file
    :type name: str
    :return: Calls function encode_to_stream with args: encoding text, dict of letters and codes,
    uwu file for encoding, name of encoding file
    """
    text = read_text(name)
    frequency = calculate_frequency(text)
    root = build_tree(frequency)
    d = huffman_code_tree_stack(root)
    with open(f'{name}.uwu', 'wb') as output:
        ext = encode_to_stream(text, d, output)
        save_list(frequency, ext, name)


def encode_to_stream(text, d, output):
    """ Encodes text to binary string and writes them to uwu file
    :param text: Text for encoding
    :type text: io text
    :param d: Dict with letters and codes
    :type d: dict
    :param output: Special uwu file for encoding, WB
    :return: Extension (number of '0' which was added to finish final byte)
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
    return str(ext)


def decode_from_file(name):
    """ Gets a list of frequency, ext(int of zeros amounts in last byte), root,
     opens encoded file(RB) and file in which decode(W+)
    :param name: Name of file to decode
    :type name: str
    :return: Calls function decode_from_stream with args: root of huffman tree, int extension,
    encoded file and file to decode.
    """
    frequency, ext = load_list(name)
    root = build_tree(frequency)
    with open(f'{name}.uwu', 'rb') as encoded_file:
        with open(f'decoded_{name}', 'w+', encoding='utf8') as output_file:
            return decode_from_stream(root, ext, encoded_file, output_file)


def decode_from_stream(root, ext, encoded_stream, decoded_stream):
    """ Decode encoded file
    :param root: root of huffman tree
    :type root: Node class obj
    :param ext: zeros amounts of zeros in last byte
    :type ext: int
    :param encoded_stream: encoded uwu file(RB)
    :param decoded_stream: file in which decode(W+)
    :type decoded_stream: io text
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

