import antlr4

from antlr.ToyLexer import ToyLexer
from antlr.ToyParser import ToyParser
from backend.compiler.Compiler import Compiler
from backend.converter.Converter import Converter
from frontend.Semantics import Semantics
from intermediate.util.BackendMode import BackendMode
from optimization.Optimization import Optimization

#Get command line arguments
import sys

#fileName = sys.argv[1]
fileName = 'my_tests/hangman_jasmin.txt'
input_file = open(fileName, encoding="utf-8")

# Create the ANTLR input stream from the Python input stream
input_stream = antlr4.InputStream(input_file.read())

# Create the lexer
lexer = ToyLexer(input_stream)

#todo add error listener
'''
lexer.removeErrorListeners()
lexer.addErrorListener(syntaxErrorHandler)
'''
tokens = antlr4.CommonTokenStream(lexer)

# Create the parser
parser = ToyParser(tokens)

#todo add error listener
'''
parser.removeErrorListeners()
parser.addErrorListener(syntaxErrorHandler)
'''

# Parse the input
tree = parser.classStart()

passOpt = Optimization()
passOpt.visit(tree)

pass2 = Semantics(BackendMode.COMPILER)
pass2.visit(tree)

programId = pass2.getProgramId()
pass3 = Compiler(programId.getName())
pass3.visit(tree)
print(pass3.getObjectFileName())
# pass3 = Converter()
# objectCode = pass3.visit(tree)
# print(objectCode)
