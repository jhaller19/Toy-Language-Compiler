grammar Toy;
@header{
}

classStart           : classHeader '{' classLevelBlock '}' ;
classHeader     : CLASS classIdentifier ;
classLevelBlock : declarations mainProcedure;

classIdentifier     locals [ SymTableEntry entry = None ]
    : IDENTIFIER ;

block         : declarations compoundStatement ;
declarations  : ( constantsPart ';' )? ( typesPart ';' )?
                ( variablesPart ';' )? ( routinesPart ';')? ;

constantsPart           : CONST constantDefinitionsList ;
constantDefinitionsList : constantDefinition ( ';' constantDefinition )* ;
constantDefinition      : constantIdentifier '=' constant ;

constantIdentifier  locals [ Typespec type = None, SymTableEntry entry = None ]
    : IDENTIFIER ;

constant    locals [ Typespec type = None, Object value = None ]
    : sign? ( IDENTIFIER | unsignedNumber )
    | characterConstant
    | stringConstant
    | booleanConstant
    ;

sign : '-' | '+' ;

typesPart           : TYPE typeDefinitionsList ;
typeDefinitionsList : typeDefinition ( ';' typeDefinition )* ;
typeDefinition      : typeIdentifier '=' typeSpecification ;

typeIdentifier  locals [ Typespec type = None, SymTableEntry entry = None ]
    : IDENTIFIER ;

typeSpecification   locals [ Typespec type = None, SymbolTableEntry entry = None]
    : simpleType        # simpleTypespec
    | iteratorType      # iteratorTypespec
    | arrayType         # arrayTypespec
    | recordType        # recordTypespec
    ;

iteratorType: | ITERATOR'('variableIdentifier')';


simpleType   locals [ Typespec type = None ]
    : typeIdentifier    # typeIdentifierTypespec
    ;


arrayType
    : ARRAY typeSpecification '[' arrayDimensionList ']'  ;
arrayDimensionList : integerConstant ( ',' integerConstant )* ;

recordType  locals [ SymTableEntry entry = None ]
    : STRUCT '{' recordFields ';'? '}' ;
recordFields : variableDeclarationsList ;

variablesPart            : VAR variableDeclarationsList ;
variableDeclarationsList : variableDeclarations ( ';' variableDeclarations )* ;
variableDeclarations     : typeSpecification variableIdentifierList;
variableIdentifierList   : variableIdentifier ( ',' variableIdentifier )* ;

variableIdentifier  locals [ Typespec type = None, SymTableEntry entry = None ]
    : IDENTIFIER ;

routinesPart      : routineDefinition ( ';' routineDefinition)* ;
routineDefinition : ( procedureHead | functionHead ) '{' block '}' ;
procedureHead     : PROCEDURE routineIdentifier (parameters? | '()') ;
functionHead      : FUNCTION typeIdentifier routineIdentifier (parameters? | '()') ;

routineIdentifier   locals [ Typespec type = None, SymTableEntry entry = None ]
    : IDENTIFIER ;

parameters                : '(' parameterDeclarationsList ')' ;
parameterDeclarationsList : parameterDeclarations ( ',' parameterDeclarations )* ;
parameterDeclarations     : typeIdentifier '*'?  parameterIdentifierList ;
parameterIdentifierList   : parameterIdentifier ( ',' parameterIdentifier )* ;

parameterIdentifier locals [ Typespec type = None, SymTableEntry entry = None ]
    : IDENTIFIER ;

statement : compoundStatement
          | assignmentStatement
          | hasNextStatement
          | nextStatement
          | ifStatement
          | whileStatement
          | printfStatement
          | readStatement
          | procedureCallStatement
          | emptyStatement
          ;

hasNextStatement: IDENTIFIER'.' 'hasNext' '()' ;
nextStatement: IDENTIFIER'.' 'next' '()' ;

readStatement   : READ '(' variable ')' ;
printfStatement: 'printf' '(' stringConstant (',' argumentList)? ')' ;

compoundStatement : '{' statementList '}';
mainProcedure : PROCEDURE MAIN '()' '{' statementList '}' ;
emptyStatement : ;

statementList       : statement ( ';' statement )* ;
assignmentStatement : lhs '=' rhs ;

lhs locals [ Typespec type = None ]
    : variable ;
rhs : nextStatement | expression ;

ifStatement    : IF '(' expression '){' trueStatement '}' ( ELSE '{' falseStatement '}')? ;
trueStatement  : statement ;
falseStatement : statement ;


whileStatement  : WHILE '(' (hasNextStatement | expression)  '){' statement '}';


procedureCallStatement : procedureName (('(' argumentList? ')') | '()') ;

procedureName   locals [ SymTableEntry entry = None ]
    : IDENTIFIER ;

argumentList : argument ( ',' argument )* ;
argument     : expression ;

expression  locals [ Typespec type = None ]
    : simpleExpression (relOp simpleExpression)? ;

simpleExpression    locals [ Typespec type = None ]
    : sign? term (addOp term)* ;

term    locals [ Typespec type = None ]
    : factor (mulOp factor)* ;

factor  locals [ Typespec type = None ]
    : variable             # variableFactor
    | number               # numberFactor
    | characterConstant    # characterFactor
    | stringConstant       # stringFactor
    | booleanConstant      # booleanFactor
    | functionCall         # functionCallFactor
    | getArgCall           # getArgCallFactor
    | '!' factor           # notFactor
    | '(' expression ')'   # parenthesizedFactor
    ;

getArgCall: 'getArg' '(' integerConstant ')';

booleanConstant: TRUE | FALSE;

variable    locals [ Typespec type = None, SymTableEntry entry = None ]
    : variableIdentifier modifier* ;

modifier  : '[' indexList ']' | '.' field ;
indexList : index ( ',' index )* ;
index     : expression ;

field   locals [ Typespec type = None, SymTableEntry entry = None ]
    : IDENTIFIER ;

functionCall : functionName '(' argumentList? ')' ;
functionName     locals [ Typespec type = None, SymTableEntry entry = None ]
    : IDENTIFIER ;

number          : sign? unsignedNumber ;
unsignedNumber  : integerConstant | realConstant ;
integerConstant : INTEGER ;
realConstant    : REAL;

characterConstant : CHARACTER ;
stringConstant    : STRING ;

relOp : '==' | '<>' | '<' | '<=' | '>' | '>=' ;
addOp : '+' | '-' | OR ;
mulOp : '*' | '/' | DIV | MOD | AND ;

fragment A : ('a' | 'A') ;
fragment B : ('b' | 'B') ;
fragment C : ('c' | 'C') ;
fragment D : ('d' | 'D') ;
fragment E : ('e' | 'E') ;
fragment F : ('f' | 'F') ;
fragment G : ('g' | 'G') ;
fragment H : ('h' | 'H') ;
fragment I : ('i' | 'I') ;
fragment J : ('j' | 'J') ;
fragment K : ('k' | 'K') ;
fragment L : ('l' | 'L') ;
fragment M : ('m' | 'M') ;
fragment N : ('n' | 'N') ;
fragment O : ('o' | 'O') ;
fragment P : ('p' | 'P') ;
fragment Q : ('q' | 'Q') ;
fragment R : ('r' | 'R') ;
fragment S : ('s' | 'S') ;
fragment T : ('t' | 'T') ;
fragment U : ('u' | 'U') ;
fragment V : ('v' | 'V') ;
fragment W : ('w' | 'W') ;
fragment X : ('x' | 'X') ;
fragment Y : ('y' | 'Y') ;
fragment Z : ('z' | 'Z') ;

MAIN    : M A I N ;
CLASS     : C L A S S ;
CONST     : C O N S T ;
TYPE      : T Y P E ;
ARRAY     : A R R A Y ;
RECORD    : R E C O R D ;
STRUCT    : S T R U C T ;
VAR       : V A R ;
DIV       : D I V ;
MOD       : M O D ;
AND       : A N D ;
OR        : O R ;
NOT       : N O T ;
IF        : I F ;
THEN      : T H E N ;
ELSE      : E L S E ;
WHILE     : W H I L E ;
PROCEDURE : P R O C E D U R E ;
FUNCTION  : F U N C T I O N ;
NEW : N E W ;
TRUE : T R U E;
FALSE : F A L S E;
READ : R E A D ;
ITERATOR : I T E R A T O R ;

IDENTIFIER : [a-zA-Z][a-zA-Z0-9]* ;
INTEGER    : [0-9]+ ;

REAL       : INTEGER '.' INTEGER
           | INTEGER ('e' | 'E') ('+' | '-')? INTEGER
           | INTEGER '.' INTEGER ('e' | 'E') ('+' | '-')? INTEGER
           ;

NEWLINE : '\r'? '\n' -> skip  ;
WS      : [ \t]+ -> skip ;

QUOTE     : '\'' ;
CHARACTER : QUOTE CHARACTER_CHAR QUOTE ;
STRING    : QUOTE STRING_CHAR* QUOTE ;

fragment CHARACTER_CHAR : ~('\'')   // any non-quote character
                        ;

fragment STRING_CHAR : QUOTE QUOTE  // two consecutive quotes
                     | ~('\'')      // any non-quote character
                     ;

COMMENT
    :   '/*' .*? '*/' -> skip
    ;

