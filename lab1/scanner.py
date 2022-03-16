import collections
import re

Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

token_specification = [
    ('SCI',     r'-?[1-9](\d*)(?:\.\d+)?[Ee][-+]?\d+'),  #  Scientific notation values
    ('DEC',     r'-?\d*(\.\d+)'),                        #  Decimal values
    ('INT',     r'(?<![\.\w\-eE])-?(\d+)(?![\d\.Ee])'),  #  Integer values
    ('EQ',      r'='),                                   #  Assignment operator
    ('ID',      r'[A-Za-z_0-9]+'),                       #  Identifiers
    ('NEWLINE', r'\n'),                                  #  Line endings
    ('SKIP',    r'([ \t])'),                             #  Skip over spaces, tabs and comments
    ('RBO',     r'\('),                                  #  Round bracket open        
    ('RBC',     r'\)'),                                  #  Round bracket close
    ('SBO',     r'\['),                                  #  Square bracket open
    ('SBC',     r'\]'),                                  #  Square bracket close
    ('LINK',    r'\-\-'),                                #  Link symbol
    ('COMA',    r','),                                   #  Coma
]

keywords = {'voltagesource', 'voltageprobe', 'currentsource', 'currentprobe', 'resistor', 'capacitor', 'inductor', 'diode', 'begin', 'end', 'gnd', 'EOF'}

class Scanner:

    def __init__(self, input, debug):
        self.debug = debug
        self.tokens = []
        self.current_token_number = 0
        re.escape(input)
        if self.debug is True:
            print('**** SCANNER ****\n')
        for token in self.tokenize(input):
            self.tokens.append(token)
        if debug is True:
            print(f'\nRetrieved tokens:\n---\n{self.tokens}\n---\n')
    
    def tokenize(self, input_string):
        
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex).match
        line_number = 1
        current_position = line_start = 0
        match = get_token(input_string)
        while match is not None:
            type = match.lastgroup
            if type == 'NEWLINE':
                yield self.output_token(Token(type, '\n', line_number, match.start() - line_start))
                line_start = current_position
                line_number += 1
            elif type != 'SKIP':
                value = match.group(type)
                if type == 'ID' and value in keywords:
                    type = value.upper()
                yield self.output_token(Token(type, value, line_number, match.start()-line_start))
            current_position = match.end()
            match = get_token(input_string, current_position)
        if current_position != len(input_string):
            raise RuntimeError('Error: Unexpected character %r on line %d' % \
                                (input_string[current_position], line_number))
        yield self.output_token(Token('EOF', '', line_number, current_position-line_start))

    def output_token(self, token):
        if self.debug is True:
            print(f'Yielding token: {token}')
        return token
        
    def next_token(self):
        self.current_token_number += 1
        if self.current_token_number-1 < len(self.tokens):
            return self.tokens[self.current_token_number-1]
        else:
            raise RuntimeError('Error: No more tokens')

