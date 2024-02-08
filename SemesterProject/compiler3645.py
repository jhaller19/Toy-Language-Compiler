import antlr4

from antlr.ToyLexer import ToyLexer
from antlr.ToyParser import ToyParser
from backend.converter.Converter import Converter
from frontend.Semantics import Semantics
from intermediate.util.BackendMode import BackendMode
from optimization.Optimization import Optimization

# Get command line arguments
import sys, os

if sys.argv[1] == '-o':
    fileName = sys.argv[2]
else:
    fileName = sys.argv[1]
input_file = open(fileName, encoding="utf-8")

# Create the ANTLR input stream from the Python input stream
input_stream = antlr4.InputStream(input_file.read())

# Create the lexer
lexer = ToyLexer(input_stream)

# todo add error listener
'''
lexer.removeErrorListeners()
lexer.addErrorListener(syntaxErrorHandler)
'''
tokens = antlr4.CommonTokenStream(lexer)

# Create the parser
parser = ToyParser(tokens)

# todo add error listener
'''
parser.removeErrorListeners()
parser.addErrorListener(syntaxErrorHandler)
'''

# Parse the input
tree = parser.classStart()
if sys.argv[1] == '-o':
    passOpt = Optimization()
    passOpt.visit(tree)

pass2 = Semantics(BackendMode.COMPILER)
pass2.visit(tree)
programId = pass2.getProgramId()
if pass2.getErrorCount() == 0:
    pass3 = Converter()
    objectCode = pass3.visit(tree)
    print(objectCode)
    # write object code to file with name of input file and .java extension
    output_file_name = fileName.replace('.pgm', '.java')
    output_file_name = os.path.basename(output_file_name)
    output_file = open(output_file_name, 'w', encoding="utf-8")
    output_file.write(objectCode)
    output_file.close()
