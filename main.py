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
    """ Class of a node of a binary tree
        :param data: Letter and number
        :type data: tuple
        :param left: Reference to left child node
        :type left: class:`Node`
        :param right: Reference to right child node
        :type right: class:`Node`
    """
    def __init__(self, data, left=None, right=None):
        """ Constructor method
        """
        self.left = left
        self.right = right
        self.data = data

    def children(self):
        """
        Returns tuple of reference to :class:`Node` objects of left and right children nodes
        :return: Reference to left and right children nodes
        :rtype tuple
        """
        return self.left, self.right


def read_text(name):
    """ Opens and reads the file name
    :param name: Name of the file
    :type name: str
    :return: Read the file data
    """
    with open(f'{name}', 'r', encoding='utf-8') as file:
        return file.read()


def save_list(list_of_freq, ext, name):
    """Saves a list of frequencies to a file named as f_name in the current directory.
    Uses `\n` as separator
    :param list_of_freq: A list of strings where 1st value is a letter, 2nd is a frequency
    :type list_of_freq: list
    :param name: Name of the file
    :type name: str
    :param ext: The number of '0's added to complete the final byte
    :type ext: str
    """
    with open(f'f_{name}', 'a') as f_text:
        for i in list_of_freq:
            line = str(i[0]) + '=' + str(i[-1]) + '\n'
            f_text.write(line)
        f_text.write(ext)


def load_list(name):
    """ Reads a file and parses it into a list of tuples
    :param name: Name of the file
    :type name: str
    :return: List of tuples with frequencies AND EXTENSION
    :rtype: list, int
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
    """ Takes the text and counts the frequencies
    :param text: read text
    :type text: text I/O
    :return: List of tuples where 1st is a letter, 2nd is a frequency
    :rtype: list
    """
    return Counter(text).most_common()[::-1]


def build_tree(frequency):
    """ Takes frequencies and creates :class:Node objects, then constructs a binary tree
    :param frequency: Tuples where 1st - letter, 2nd - int frequency
    :type frequency: list
    :return: Root of tree
    :rtype: :class:`Node` object
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
    """ Writes in dict codes of letters using a stack
    :param root: Root of huffman tree
    :type root: :class:`Node` object
    :return: A dictionary where key - letter and code - value
    :rtype: dict
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
    """ Retrieves the length of the stream
    :param stream: Various types of I/O
    :return: Length of the stream
    :rtype: int
    """
    stream.seek(0, io.SEEK_END)
    length = stream.tell()
    stream.seek(0, io.SEEK_SET)
    return length


def convert_to_bin_str(i):
    """ Convert int number to binary string
    :param i: Encoded octal number
    :type i: int
    :return: Binary string
    :rtype: str
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
    :type root: :class:`Node` object
    :param code_string: String of bin code
    :type code_string: str
    :return: leftover(a portion of the last encoded letter, with its tail in the next string), decoded letters
    :rtype: str, str
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
    """ Receives the text to encode, a dictionary
    of letters and their corresponding codes, and an output file for encoding
    :param name: Name of encoded file
    :type name: str
    :return: Calls function encode_to_stream
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
    :param output: Special uwu file for encoding
    :return: Extension (The number of 0's added to complete the final byte)
    :rtype: str
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
    """ Gets a list of frequencies, ext(the number of 0's added to complete the final byte), root,
     opens the encoded file and the file to which decoding will be performed
    :param name: Name of file to decode
    :type name: str
    :return: Calls function decode_from_stream
    """
    frequency, ext = load_list(name)
    root = build_tree(frequency)
    with open(f'{name}.uwu', 'rb') as encoded_file:
        with open(f'decoded_{name}', 'w+', encoding='utf8') as output_file:
            decode_from_stream(root, ext, encoded_file, output_file)


def decode_from_stream(root, ext, encoded_stream, decoded_stream):
    """ Decode encoded file
    :param root: root of huffman tree
    :type root: :class:`Node` object
    :param ext: The number of 0's added to complete the final byte
    :type ext: int
    :param encoded_stream: encoded uwu file
    :type encoded_stream: io binary
    :param decoded_stream: file in which decode
    :type decoded_stream: io text
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
