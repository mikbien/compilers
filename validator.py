from myParser import * 
from myParser import *
from scanner import *
from preprocessor import *
import argparse


parser = argparse.ArgumentParser(description='Validate input file syntax')
parser.add_argument('--input', '-i', required=True, 
                    help='Pass the path to the input file to be processed by the validator')
parser.add_argument('--debug', '-d', action='store_true', default=False, 
                    help='launch the validator in debug mode for more insigtful logs')
args = parser.parse_args()

input_file = args.input
debug = args.debug

with open(input_file) as f:
  input_string = f.read()

if debug is True:
  print(f'\n*********** Validator (debug mode) start ***********\n\n')

input_string = preprocess(input_string, debug)
scanner = Scanner(input_string, debug)
parser = MyParser(scanner, debug)
parser.start()
  
