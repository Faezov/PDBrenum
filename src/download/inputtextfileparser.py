import re


def input_text_file_parser(filename):
    # Define a regular expression pattern to split on comma, space, tab, or new line
    pattern = re.compile(r'[,\s\t\n]+')

    # Read the entire file and split it using the defined pattern
    with open(filename, 'r') as file:
        file_contents = file.read()
        parsed_elements = pattern.split(file_contents)

    # Filter out any empty strings and elements shorter than 4 characters
    parsed_elements = [elem for elem in parsed_elements if elem and len(elem) >= 4]

    return parsed_elements


# Example usage
# filename = '../../input.txt'
# parsed_list = input_text_file_parser(filename)
# print(parsed_list)
