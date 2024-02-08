from antlr.ToyParser import ToyParser
from antlr.ToyVisitor import ToyVisitor
import io
import codecs

from backend.converter.CodeGenerator import CodeGenerator
from intermediate.symtable.Kind import Kind
from intermediate.symtable.Predefined import Predefined
from intermediate.symtable.SymTable import SymTable
from intermediate.type.Typespec import Form


class Converter(ToyVisitor):
    def __init__(self):
        self.code = None
        self.programName = None
        self.programVariables = True
        self.recordFields = False
        self.currentSeparator = ""
        self.typeNameTable = {
            "integer": "int",
            "real": "double",
            "boolean": "boolean",
            "char": "char",
            "string": "String"
        }

    def visitClassStart(self, ctx: ToyParser.ClassStartContext):
        # Create an in-memory buffer
        buf = io.StringIO()
        # Create a StreamWriter to write to the buffer
        self.code = CodeGenerator(buf)
        self.visit(ctx.classHeader())

        # Execution timer and runtime standard input.
        self.code.indent()
        self.code.emitLineCode("private static java.util.Scanner _sysin = " +
                               "new java.util.Scanner(System.in);")
        self.code.emitLine()

        # Level 1 declarations.
        idCtx = ctx.classHeader().classIdentifier()
        self.visit(ctx.classLevelBlock().declarations())
        self.emitUnnamedRecordDefinitions(idCtx.entry.getRoutineSymtable())

        # Main.
        self.code.emitLine()
        self.code.emitLineCode("public static void main(String[] args)")
        self.code.emitLineCode("{")
        self.code.indent()

        # Allocate structured data.
        # self.emitAllocateStructuredVariables("", idCtx.entry.getRoutineSymtable())
        self.code.emitLine()

        # Main statement.
        self.visit(ctx.classLevelBlock().mainProcedure().statementList())

        self.code.dedent()
        self.code.emitLineCode("}")

        self.code.dedent()
        self.code.emitLineCode("}")

        return buf.getvalue()

    def visitClassHeader(self, ctx):
        # Get the program name
        self.programName = ctx.classIdentifier().entry.getName()

        # Emit the Python program class
        self.code.emitLineCode("class " + self.programName + "{")
        self.code.indent()

        return None

    def visitConstantDefinition(self, ctx):
        # Get the constant name and type
        idCtx = ctx.constantIdentifier()
        constCtx = ctx.constant()
        constantName = idCtx.getText()
        type = constCtx.type_
        pascalTypeName = type.getIdentifier().getName()
        javaTypeName = self.typeNameTable.get(pascalTypeName)

        # Emit the constant definition
        self.code.emitStart()
        if self.programVariables:
            self.code.emit("static ")
        self.code.emitEnd("final " + javaTypeName + " " + constantName + " = "
                          + constCtx.getText().replace('\'' , "\"") + ";")

        return None

    def visitReadStatement(self, ctx:ToyParser.ReadStatementContext):
        self.code.emitStartCode(ctx.variable().getText() + " = _sysin.next().charAt(0);")
    def visitTypeDefinition(self, ctx):
        # Get the type name and form
        idCtx = ctx.typeIdentifier()
        typeName = idCtx.entry.getName()
        if idCtx.type_ is None or idCtx.type_.form != Form.ARRAY:
            self.code.emitEnd("static class " + typeName)
            self.visit(ctx.typeSpecification())
        # typeCtx = ctx.typeSpecification()
        # form = typeCtx.type_.getForm()
        #
        # # Emit the type definition
        # if form == Form.ENUMERATION:
        #     self.code.emitStart()
        #     if self.programVariables:
        #         self.code.emit("static ")
        #     self.code.emit("class " + typeName + "(Enum):")
        #     self.code.indent()
        #     self.visit(typeCtx)
        # elif form == Form.RECORD:
        #     self.code.emitStart()
        #     if self.programVariables:
        #         self.code.emit("static ")
        #     self.code.emitEnd("class " + typeName + ":")
        #     self.code.emitLine("{")
        #     self.code.indent()
        #
        #     self.emitUnnamedRecordDefinitions(typeCtx.type.getRecordSymTable())
        #     self.visit(typeCtx)
        #
        #     self.code.dedent()
        #     self.code.emitLine("}")
        #     self.code.emitLine()

        return None

    def visitGetArgCall(self, ctx: ToyParser.GetArgCallContext):
        return "args[" + str(ctx.integerConstant().INTEGER()) + "]"

    def emitUnnamedRecordDefinitions(self, symTable):
        # Loop to look for names of unnamed record types.
        for id in symTable.sortedEntries():
            if (id.getKind() == Kind.TYPE) and (id.getType().getForm() == Form.RECORD) and (
                    id.getName().startswith(SymTable.UNNAMED_PREFIX)):
                self.code.emitStart()
                if self.programVariables:
                    self.code.emit("public static ")
                self.code.emitEnd("class " + id.getName())
                self.code.emitLine("{")
                self.code.indent()
                # self.emitRecordFields(id.getType().getRecordSymTable())
                self.code.dedent()
                self.code.emitLine("}")
                self.code.emitLine()

        return None

    def visitVariableDeclarations(self, ctx):
        typeCtx = ctx.typeSpecification()
        listCtx = ctx.variableIdentifierList()

        for varCtx in listCtx.variableIdentifier():
            self.code.emitStart()
            if typeCtx.type_.getForm() == Form.ITERATOR:
                varName = varCtx.getText()
                self.code.emitStartCode(
                    'static Iterator_' + varName + ' ' + varName + ' = new Iterator_' + varName + '();\n')
                self.code.emit('static class Iterator_' + varName + '{\n')
                self.code.emitStartCode('static int i = 0;\n')
                self.code.emitStartCode('public boolean hasNext(){\n')
                self.code.emitStartCode('return i < ' + str(typeCtx.entry.getType().getArrayElementCount()) + ';\n')
                self.code.emitStartCode('}\n')
                self.code.emitStartCode(
                    'public ' + self.typeName(typeCtx.entry.getType().getArrayElementType()) + ' next(){\n')
                self.code.emitStartCode('return ' + typeCtx.entry.name + '[i++];\n')
                self.code.emitStartCode('}\n')
                self.code.emitStartCode('}\n')
            else:
                if self.programVariables and not self.recordFields:
                    self.code.emit("private static ")
                self.code.emit(self.typeName(typeCtx.type_))
                self.code.emit(" " + varCtx.getText())
                if typeCtx.type_.getForm() == Form.ARRAY:
                    self.emitArraySpecifier(typeCtx.type_)
                    self.code.emit(" = new " + self.typeName(typeCtx.type_) + "[" + str(
                        typeCtx.type_.getArrayElementCount()) + "]")
                elif typeCtx.type_.getForm() == Form.RECORD:
                    self.emitRecordSpecifier(typeCtx.type_)
                self.code.emitEnd(";")

        return None

    def emitRecordSpecifier(self, recordType):
        self.code.emit(" = new " + recordType.identifier.name + "()")

    def emitArraySpecifier(self, type):
        brackets = ""

        while type.getForm() == Form.ARRAY:
            brackets += "[]"
            type = type.getArrayElementType()

        self.code.emit(brackets)

    def typeName(self, pascalType):
        form = pascalType.getForm()
        typeId = pascalType.getIdentifier()
        pascalTypeName = typeId.getName() if typeId is not None else None

        if form == Form.ARRAY:
            elemType = pascalType.getArrayBaseType()
            pascalTypeName = elemType.getIdentifier().getName()
            javaTypeName = self.typeNameTable.get(pascalTypeName)
            return javaTypeName if javaTypeName is not None else pascalTypeName
        elif form == Form.SUBRANGE:
            baseType = pascalType.baseType()
            pascalTypeName = baseType.getIdentifier().getName()
            return self.typeNameTable.get(pascalTypeName)
        elif form == Form.ENUMERATION:
            return pascalTypeName if pascalTypeName is not None else "int"
        elif form == Form.RECORD:
            return pascalTypeName
        else:
            return self.typeNameTable.get(pascalTypeName)

    def visitTypeIdentifier(self, ctx):
        pascalType = ctx.type_
        javaTypeName = self.typeName(pascalType)
        self.code.emit(javaTypeName)
        return None

    def visitVariableIdentifierList(self, ctx):
        separator = " "

        for varCtx in ctx.variableIdentifier():
            self.code.emit(separator)
            self.code.emit(varCtx.getText())
            separator = ", "
        return None

    '''
    def emitAllocateStructuredVariables(self, lhsPrefix, symTable):
        # Loop over all the symbol table's identifiers to emit
        # code to allocate array and record variables.
        for id in symTable.sortedEntries():
            if id.getKind() == Kind.VARIABLE:
                self.emitAllocateStructuredData(lhsPrefix, id)

    # TODO allocate structured data
    def emitAllocateStructuredData(self, lhsPrefix, variableId):
        variableType = variableId.getType()
        form = variableType.getForm()
        variableName = variableId.getName()

        if form == Form.ARRAY:
            self.code.emitStart(lhsPrefix + variableName + " = ")
            elemType = self.emitNewArray(variableType)
            self.code.emitEnd(";")
    
            if elemType.isStructured():
                emitNewArrayElement(lhsPrefix, variableName, variableType)
        elif form == Form.RECORD:
            self.code.emitStart(lhsPrefix + variableName + " = ")
            self.emitNewRecord(lhsPrefix, variableName, variableType)
    '''

    def visitStatementList(self, ctx):
        for stmtCtx in ctx.statement():
            if not stmtCtx.emptyStatement():
                self.code.emitStart()
                self.visit(stmtCtx)

        return None

    def visitCompoundStatement(self, ctx):
        self.code.emit("{")
        self.code.indent()
        self.visitChildren(ctx)
        self.code.dedent()
        self.code.emitLineCode("}")

        return None

    def visitAssignmentStatement(self, ctx):
        lhs = self.visit(ctx.lhs().variable())
        expr = None
        if ctx.rhs().expression() is not None:
            expr = self.visit(ctx.rhs().expression())
        else:
            expr = self.visit(ctx.rhs().nextStatement())
        self.code.emit(f"{lhs} = {expr};")
        return None

    def visitExpression(self, ctx):
        simpleCtx1 = ctx.simpleExpression()[0]
        relOpCtx = ctx.relOp()
        simpleText1 = self.visit(simpleCtx1)
        text = simpleText1

        # Second simple expression?
        if relOpCtx is not None:
            op = relOpCtx.getText()

            if op == "=":
                op = "=="
            elif op == "<>":
                op = "!="

            simpleCtx2 = ctx.simpleExpression()[1]
            simpleText2 = self.visit(simpleCtx2)

            # Python has a built-in way to compare strings.
            if simpleCtx1.type_ == Predefined.stringType:
                text = simpleText1 + "." + "compareTo(" + simpleText2 + ") " + op + " 0"
            else:
                text = simpleText1 + " " + op + " " + simpleText2

        return text

    def visitSimpleExpression(self, ctx):
        count = len(ctx.term())
        text = ""

        if (ctx.sign() is not None) and (ctx.sign().getText() == "-"):
            text += "-"

        # Loop over the simple expressions.
        for i in range(count):
            termCtx = ctx.term(i)
            text += str(self.visit(termCtx))

            if i < count - 1:
                addOp = ctx.addOp(i).getText().lower()
                if addOp == "or":
                    addOp = "||"

                text += " " + addOp + " "

        return text

    def visitVariableFactor(self, ctx: ToyParser.VariableFactorContext):
        return self.visit(ctx.variable())

    def visitHasNextStatement(self, ctx: ToyParser.HasNextStatementContext):
        self.code.emit(ctx.getText())
        return None

    def visitNextStatement(self, ctx: ToyParser.NextStatementContext):
        return ctx.getText()

    def visitVariable(self, ctx):
        idCtx = ctx.variableIdentifier()
        variableId = idCtx.entry
        variableName = variableId.getName()
        type = ctx.variableIdentifier().type_
        if type.getForm() == Form.ITERATOR:
            return variableName

        if type != Predefined.booleanType and variableId.getKind() == Kind.ENUMERATION_CONSTANT:
            variableName = type.getIdentifier().getName() + "." + variableName

        for modCtx in ctx.modifier():
            if modCtx.indexList() is not None:
                for indexCtx in modCtx.indexList().index():
                    indexType = type.getArrayIndexType()
                    minIndex = 0

                    if indexType.getForm() == Form.SUBRANGE:
                        minIndex = indexType.getSubrangeMinValue()

                    exprCtx = indexCtx.expression()
                    expr = self.visit(exprCtx)
                    subscript = expr if minIndex == 0 else (
                        "(" + expr + ")+" + str(-minIndex) if minIndex < 0 else "(" + expr + ")-" + str(minIndex))

                    variableName += "[" + subscript + "]"

                    type = type.getArrayElementType()
            else:
                fieldCtx = modCtx.field()
                fieldName = fieldCtx.entry.getName()
                variableName += "." + fieldName
                type = fieldCtx.type_

        return variableName

    def visitNumberFactor(self, ctx):
        return ctx.getText()

    def visitCharacterFactor(self, ctx):
        return ctx.getText()

    def visitStringFactor(self, ctx):
        pascalString = ctx.stringConstant().STRING().getText()
        return '"' + self.convertString(pascalString) + '"'

    def convertString(self, pascalString):
        return pascalString[1:-1].replace("''", "'").replace('"', '\\"')

    def visitBooleanFactor(self, ctx: ToyParser.BooleanFactorContext):
        if ctx.booleanConstant().TRUE() is not None:
            return "true"
        else:
            return "false"

    def visitFunctionCallFactor(self, ctx):
        callCtx = ctx.functionCall()
        funcNameCtx = callCtx.functionName()
        functionName = funcNameCtx.entry.getName()
        text = functionName + "("
        if callCtx.argumentList() is not None:
            text += self.visit(callCtx.argumentList())

        text += ")"
        return text

    def visitNotFactor(self, ctx: ToyParser.NotFactorContext):
        return "!" + self.visit(ctx.factor())

    def visitArgumentList(self, ctx):
        text = ""
        separator = ""

        for argCtx in ctx.argument():
            text += separator
            text += str(self.visit(argCtx.expression()))
            separator = ", "

        return text

    def visitParenthesizedFactor(self, ctx):
        return "(" + self.visit(ctx.expression()) + ")"

    def visitWhileStatement(self, ctx):
        self.code.emitStartCode("while(")
        if ctx.expression() is not None:
            self.code.emit(self.visit(ctx.expression()))
        else:
            self.code.emit(ctx.hasNextStatement().getText())
        self.code.emit(")")
        self.visit(ctx.statement())
        return None

    def visitIfStatement(self, ctx: ToyParser.IfStatementContext):
        self.code.emitStartCode("if(")
        self.code.emit(self.visit(ctx.expression()))
        self.code.emit(")")
        self.visit(ctx.trueStatement())

        if ctx.ELSE() is not None:
            self.code.emitStartCode("else ")
            self.visit(ctx.falseStatement())

        return None

    def visitRoutineDefinition(self, ctx):
        if ctx.procedureHead() is not None:
            self.visit(ctx.procedureHead())
            self.programVariables = False
            self.visit(ctx.block())
            self.programVariables = True
            self.code.emitLineCode("}")
        else:
            self.visit(ctx.functionHead())
            self.programVariables = False
            returnType = self.typeNameTable[ctx.functionHead().routineIdentifier().type_.getIdentifier().getName()]
            returnVarName = ctx.functionHead().routineIdentifier().entry.getName()
            self.code.emitLineCode(returnType + " " + returnVarName + ";")
            self.visit(ctx.block())
            self.programVariables = True
            self.code.emit("return " + returnVarName + ";")
            self.code.emitLineCode("}")
        return None

    def visitProcedureHead(self, ctx):
        name = ctx.routineIdentifier().entry.getName()
        self.code.emitStartCode("public static void ")
        self.code.emit(name)
        self.code.emit("(")
        if ctx.parameters() is not None:
            for i in range(len(ctx.parameters().parameterDeclarationsList().parameterDeclarations())):
                p = ctx.parameters().parameterDeclarationsList().parameterDeclarations(i)
                self.visit(p)
                if i != len(ctx.parameters().parameterDeclarationsList().parameterDeclarations()) - 1:
                    self.code.emit(",")
        self.code.emitEnd("){")
        return None

    def visitFunctionHead(self, ctx):
        name = ctx.routineIdentifier().entry.getName()
        self.code.emitStartCode("public static ")
        self.code.emit(self.typeNameTable.get(ctx.routineIdentifier().type_.getIdentifier().getName()) + " ")
        self.code.emit(name)
        self.code.emit("(")
        if ctx.parameters() is not None:
            for i in range(len(ctx.parameters().parameterDeclarationsList().parameterDeclarations())):
                p = ctx.parameters().parameterDeclarationsList().parameterDeclarations(i)
                self.visit(p)
                if i != len(ctx.parameters().parameterDeclarationsList().parameterDeclarations()) - 1:
                    self.code.emit(",")
        self.code.emitEnd("){")
        return None

    def visitPrintfStatement(self, ctx:ToyParser.PrintfStatementContext):
        self.code.emitStartCode('System.out.' + ctx.getText().replace('\'', "\"") + ';')

    def visitParameterDeclarations(self, ctx):
        typeCtx = ctx.typeIdentifier()
        listCtx = ctx.parameterIdentifierList()
        for i in range(len(listCtx.parameterIdentifier())):
            paramCtx = listCtx.parameterIdentifier(i)
            s = paramCtx.entry.getName()
            self.code.emit(self.typeName(typeCtx.type_))
            self.code.emit(" " + paramCtx.entry.getName())
            # if (typeCtx.type.getForm() == ARRAY) emitArraySpecifier(typeCtx.type);
            if i != len(listCtx.parameterIdentifier()) - 1:
                self.code.emit(",")
        return None

    def visitProcedureCallStatement(self, ctx):
        procNameCtx = ctx.procedureName()
        procedureName = procNameCtx.entry.getName()

        self.code.emit(procedureName)
        self.code.emit("(")

        if ctx.argumentList() is not None:
            self.code.emit(str(self.visit(ctx.argumentList())))

        self.code.emitEnd(");")
        return None

    def visitTerm(self, ctx):
        count = len(ctx.factor())
        text = ""

        # Loop over the terms.
        for i in range(count):
            factorCtx = ctx.factor()[i]
            text += self.visit(factorCtx)

            if i < count - 1:
                mulOpStr = ctx.mulOp()[i].getText().lower()
                mulOp = ""

                if mulOpStr == "and":
                    mulOp = " && "
                elif mulOpStr == "div":
                    mulOp = "/"
                elif mulOpStr == "mod":
                    mulOp = "%"
                else:
                    mulOp = mulOpStr

                text += mulOp

        return text

    def visitRecordTypespec(self, ctx):
        fieldsCtx = ctx.recordType().recordFields()
        self.code.emit(" {")
        self.recordFields = True
        self.visit(fieldsCtx.variableDeclarationsList())
        self.recordFields = False
        self.code.emit("}")

        return None


'''
    public String getProgramName() {
        return programName;
    }

    @Override
    public Object visitProgram(PascalParser.ProgramContext ctx) {
        StringWriter sw = new StringWriter();
        code = new CodeGenerator(new PrintWriter(sw));

        visit(ctx.programHeader());

        // Execution timer and runtime standard input.
        code.indent();
        code.emitLine("private static java.util.Scanner _sysin = " +
                "new java.util.Scanner(System.in);");
        code.emitLine();

        // Level 1 declarations.
        PascalParser.ProgramIdentifierContext idCtx =
                ctx.programHeader().programIdentifier();
        visit(ctx.block().declarations());
        emitUnnamedRecordDefinitions(idCtx.entry.getRoutineSymTable());

        // Main.
        code.emitLine();
        code.emitLine("public static void main(String[] args)");
        code.emitLine("{");
        code.indent();

        // Allocate structured data.
        emitAllocateStructuredVariables("", idCtx.entry.getRoutineSymTable());
        code.emitLine();

        // Main compound statement.
        visit(ctx.block().compoundStatement().statementList());

        code.dedent();
        code.emitLine("}");

        code.dedent();
        code.emitLine("}");

        code.close();
        return sw.toString();
    }

    @Override
    public Object visitProgramHeader(PascalParser.ProgramHeaderContext ctx) {
        programName = ctx.programIdentifier().entry.getName();

        // Emit the Java program class.
        code.emitLine("public class " + programName);
        code.emitLine("{");

        return null;
    }

    @Override
    public Object visitConstantDefinition(
            PascalParser.ConstantDefinitionContext ctx) {
        PascalParser.ConstantIdentifierContext idCtx = ctx.constantIdentifier();
        PascalParser.ConstantContext constCtx = ctx.constant();
        String constantName = idCtx.entry.getName();
        Typespec type = constCtx.type;
        String pascalTypeName = type.getIdentifier().getName();
        String javaTypeName = typeNameTable.get(pascalTypeName);

        code.emitStart();
        if (programVariables) code.emit("private static ");
        code.emitEnd("final " + javaTypeName + " " + constantName + " = "
                + constCtx.getText() + ";");

        return null;
    }

    @Override
    public Object visitTypeDefinition(PascalParser.TypeDefinitionContext ctx) {
        PascalParser.TypeIdentifierContext idCtx = ctx.typeIdentifier();
        String typeName = idCtx.entry.getName();
        PascalParser.TypeSpecificationContext typeCtx = ctx.typeSpecification();
        Form form = typeCtx.type.getForm();

        if (form == ENUMERATION) {
            code.emitStart();
            if (programVariables) code.emit("private static ");
            code.emit("enum " + typeName);
            visit(typeCtx);
        } else if (form == RECORD) {
            code.emitStart();
            if (programVariables) code.emit("public static ");
            code.emitEnd("class " + typeName);
            code.emitLine("{");
            code.indent();

            emitUnnamedRecordDefinitions(typeCtx.type.getRecordSymTable());
            visit(typeCtx);

            code.dedent();
            code.emitLine("}");
            code.emitLine();
        }

        return null;
    }

    @Override
    public Object visitEnumerationTypespec(
            PascalParser.EnumerationTypespecContext ctx) {
        String separator = " {";

        for (PascalParser.EnumerationConstantContext constCtx :
                ctx.enumerationType().enumerationConstant()) {
            code.emit(separator + constCtx.constantIdentifier().entry.getName());
            separator = ", ";
        }

        code.emitEnd("};");
        return null;
    }

    /**
     * Emit a record type definition for an unnamed record.
     *
     * @param symTable the symbol table that can contain unnamed records.
     */
    private void emitUnnamedRecordDefinitions(SymTable symTable) {
        // Loop to look for names of unnamed record types.
        for (SymTableEntry id : symTable.sortedEntries()) {
            if ((id.getKind() == TYPE)
                    && (id.getType().getForm() == RECORD)
                    && (id.getName().startsWith(SymTable.UNNAMED_PREFIX))) {
                code.emitStart();
                if (programVariables) code.emit("public static ");
                code.emitEnd("class " + id.getName());
                code.emitLine("{");
                code.indent();
                emitRecordFields(id.getType().getRecordSymTable());
                code.dedent();
                code.emitLine("}");
                code.emitLine();
            }
        }
    }

    /**
     * Emit the record fields of a record.
     *
     * @param symTable the symbol table of the unnamed record.
     */
    private void emitRecordFields(SymTable symTable) {
        emitUnnamedRecordDefinitions(symTable);

        // Loop over the entries of the symbol table.
        for (SymTableEntry fieldId : symTable.sortedEntries()) {
            if (fieldId.getKind() == RECORD_FIELD) {
                code.emitStart(typeName(fieldId.getType()));
                code.emit(" " + fieldId.getName());
                code.emitEnd(";");
            }
        }
    }

    @Override
    public Object visitRecordTypespec(PascalParser.RecordTypespecContext ctx) {
        PascalParser.RecordFieldsContext fieldsCtx =
                ctx.recordType().recordFields();
        recordFields = true;
        visit(fieldsCtx.variableDeclarationsList());
        recordFields = false;

        return null;
    }

    @Override
    public Object visitVariableDeclarations(
            PascalParser.VariableDeclarationsContext ctx) {
        PascalParser.TypeSpecificationContext typeCtx = ctx.typeSpecification();
        PascalParser.VariableIdentifierListContext listCtx =
                ctx.variableIdentifierList();

        for (PascalParser.VariableIdentifierContext varCtx :
                listCtx.variableIdentifier()) {
            code.emitStart();
            if (programVariables && !recordFields) code.emit("private static ");
            code.emit(typeName(typeCtx.type));

            code.emit(" " + varCtx.entry.getName());
            if (typeCtx.type.getForm() == ARRAY) emitArraySpecifier(typeCtx.type);
            code.emitEnd(";");
        }

        return null;
    }

    /**
     * Emit a pair of empty brackets for each dimension.
     *
     * @param type the array datatype.
     */
    private void emitArraySpecifier(Typespec type) {
        StringBuilder brackets = new StringBuilder();

        while (type.getForm() == ARRAY) {
            brackets.append("[]");
            type = type.getArrayElementType();
        }

        code.emit(brackets.toString());
    }

    /**
     * Convert a Pascal type name to the equivalent Java type name.
     *
     * @param pascalType the datatype name.
     * @return the Java type name.
     */
    private String typeName(Typespec pascalType) {
        Form form = pascalType.getForm();
        SymTableEntry typeId = pascalType.getIdentifier();
        String pascalTypeName = typeId != null ? typeId.getName() : null;

        if (form == ARRAY) {
            Typespec elemType = pascalType.getArrayBaseType();
            pascalTypeName = elemType.getIdentifier().getName();
            String javaTypeName = typeNameTable.get(pascalTypeName);
            return javaTypeName != null ? javaTypeName : pascalTypeName;
        } else if (form == SUBRANGE) {
            Typespec baseType = pascalType.baseType();
            pascalTypeName = baseType.getIdentifier().getName();
            return typeNameTable.get(pascalTypeName);
        } else if (form == ENUMERATION) {
            return pascalTypeName != null ? pascalTypeName : "int";
        } else if (form == RECORD) return pascalTypeName;
        else return typeNameTable.get(pascalTypeName);
    }

    @Override
    public Object visitTypeIdentifier(PascalParser.TypeIdentifierContext ctx) {
        Typespec pascalType = ctx.type;
        String javaTypeName = typeName(pascalType);
        code.emit(javaTypeName);

        return null;
    }

    @Override
    public Object visitVariableIdentifierList(
            PascalParser.VariableIdentifierListContext ctx) {
        String separator = " ";

        for (PascalParser.VariableIdentifierContext varCtx :
                ctx.variableIdentifier()) {
            code.emit(separator);
            code.emit(varCtx.getText());
            separator = ", ";
        }

        return null;
    }

    /**
     * Emit code to allocate data for structured (array or record) variables.
     *
     * @param lhsPrefix the prefix for the target variable name.
     * @param symTable  the symbol table containing the variable names.
     */
    private void emitAllocateStructuredVariables(String lhsPrefix, SymTable symTable) {
        // Loop over all the symbol table's identifiers to emit
        // code to allocate array and record variables.
        for (SymTableEntry id : symTable.sortedEntries()) {
            if (id.getKind() == VARIABLE) {
                emitAllocateStructuredData(lhsPrefix, id);
            }
        }
    }

    /**
     * Emit code to allocate structured (array or record) data.
     *
     * @param lhsPrefix  the prefix for the target variable name.
     * @param variableId the symbol table entry of the target variable.
     */
    private void emitAllocateStructuredData(String lhsPrefix,
                                            SymTableEntry variableId) {
        Typespec variableType = variableId.getType();
        Form form = variableType.getForm();
        String variableName = variableId.getName();

        if (form == ARRAY) {
            code.emitStart(lhsPrefix + variableName + " = ");
            Typespec elemType = emitNewArray(variableType);
            code.emitEnd(";");

            if (elemType.isStructured()) {
                emitNewArrayElement(lhsPrefix, variableName, variableType);
            }
        } else if (form == RECORD) {
            code.emitStart(lhsPrefix + variableName + " = ");
            emitNewRecord(lhsPrefix, variableName, variableType);
        }
    }

    /**
     * Emit a string of bracketed dimension sizes for the array datatype.
     * followed by the "new" array allocation.
     *
     * @param type the array datatype.
     * @return the base datatype of the array.
     */
    private Typespec emitNewArray(Typespec type) {
        StringBuilder sizes = new StringBuilder();

        while (type.getForm() == ARRAY) {
            sizes.append("[").append(type.getArrayElementCount()).append("]");
            type = type.getArrayElementType();
        }

        type = type.baseType();
        String pascalTypeName = type.getIdentifier().getName();
        String javaTypeName = typeNameTable.get(pascalTypeName);

        if (javaTypeName == null) javaTypeName = pascalTypeName;
        code.emit("new " + javaTypeName + sizes);

        return type;
    }

    /**
     * Emit code to allocate an array element.
     *
     * @param lhsPrefix    the prefix for the target variable name.
     * @param variableName the name of the target variable.
     * @param elemType     the element's datatype.
     */
    private void emitNewArrayElement(String lhsPrefix, String variableName,
                                     Typespec elemType) {
        int dimensionCount = 0;

        StringBuilder variableNameBuilder = new StringBuilder(variableName);
        do {
            int elemCount = elemType.getArrayElementCount();
            ++dimensionCount;
            String subscript = "_i" + dimensionCount;
            variableNameBuilder.append("[").append(subscript).append("]");

            code.emitLine("for (int " + subscript + " = 0; " +
                    subscript + " < " + elemCount +
                    "; " + subscript + "++)");
            code.emitStart("{");
            code.indent();

            elemType = elemType.getArrayElementType();
        } while (elemType.getForm() == ARRAY);
        variableName = variableNameBuilder.toString();

        String typeName = elemType.getIdentifier().getName();
        code.emitStart(lhsPrefix + variableName + " = new " + typeName + "()");
        code.emitEnd(";");

        emitNewRecordFields(lhsPrefix + variableName + ".", elemType);

        while (--dimensionCount >= 0) {
            code.dedent();
            code.emitLine("}");
        }
    }

    /**
     * Emit code to allocate a new record.
     *
     * @param lhsPrefix    the prefix for the target variable name.
     * @param variableName the name of the target variable.
     * @param recordType   the record's datatype.
     */
    private void emitNewRecord(String lhsPrefix, String variableName,
                               Typespec recordType) {
        String typePath = recordType.getRecordTypePath();
        int index = typePath.indexOf('$');

        // Don't include the program name in the record type path.
        // Replace each $ with a period.
        typePath = typePath.substring(index + 1).replace('$', '.');
        code.emit("new " + typePath + "();");

        emitNewRecordFields(lhsPrefix + variableName + ".", recordType);
    }

    /**
     * Emit code to allocate a record's fields.
     *
     * @param lhsPrefix  the prefix for the target variable name.
     * @param recordType the record's datatype.
     */
    private void emitNewRecordFields(String lhsPrefix, Typespec recordType) {
        for (SymTableEntry fieldId : recordType.getRecordSymTable().sortedEntries()) {
            if (fieldId.getKind() == RECORD_FIELD) {
                Typespec type = fieldId.getType();

                if (type.isStructured()) {
                    emitAllocateStructuredData(lhsPrefix, fieldId);
                }
            }
        }
    }

    @Override
    public Object visitStatementList(PascalParser.StatementListContext ctx) {
        for (PascalParser.StatementContext stmtCtx : ctx.statement()) {
            if (stmtCtx.emptyStatement() == null) {
                code.emitStart();
                visit(stmtCtx);
            }
        }

        return null;
    }

    @Override
    public Object visitCompoundStatement(
            PascalParser.CompoundStatementContext ctx) {
        code.emit("{");
        code.indent();
        visitChildren(ctx);
        code.dedent();
        code.emitLine("}");

        return null;
    }

    @Override
    public Object visitAssignmentStatement(
            PascalParser.AssignmentStatementContext ctx) {
        String lhs = (String) visit(ctx.lhs().variable());
        String expr = (String) visit(ctx.rhs().expression());
        code.emit(lhs + " = " + expr);
        code.emitEnd(";");

        return null;
    }

    @Override
    public Object visitRepeatStatement(PascalParser.RepeatStatementContext ctx) {
        boolean needBraces = ctx.statementList().statement().size() > 1;

        code.emit("do");
        if (needBraces) code.emitLine("{");
        code.indent();

        visit(ctx.statementList());

        code.dedent();
        if (needBraces) code.emitLine("}");

        code.emitStart("while (!(");
        code.emit((String) visit(ctx.expression()));
        code.emitEnd("));");

        return null;
    }

    @Override
    public Object visitProcedureCallStatement(
            PascalParser.ProcedureCallStatementContext ctx) {
        PascalParser.ProcedureNameContext procNameCtx = ctx.procedureName();
        String procedureName = procNameCtx.entry.getName();

        code.emit(procedureName);
        code.emit("(");

        if (ctx.argumentList() != null) {
            code.emit((String) visit(ctx.argumentList()));
        }

        code.emitEnd(");");
        return null;
    }

    @Override
    public Object visitArgumentList(PascalParser.ArgumentListContext ctx) {
        StringBuilder text = new StringBuilder();
        String separator = "";

        for (PascalParser.ArgumentContext argCtx : ctx.argument()) {
            text.append(separator);
            text.append((String) visit(argCtx.expression()));
            separator = ", ";
        }

        return text.toString();
    }

    @Override
    public Object visitExpression(PascalParser.ExpressionContext ctx) {
        PascalParser.SimpleExpressionContext simpleCtx1 =
                ctx.simpleExpression().get(0);
        PascalParser.RelOpContext relOpCtx = ctx.relOp();
        String simpleText1 = (String) visit(simpleCtx1);
        String text = simpleText1;

        // Second simple expression?
        if (relOpCtx != null) {
            String op = relOpCtx.getText();

            if (op.equals("=")) op = "==";
            else if (op.equals("<>")) op = "!=";

            PascalParser.SimpleExpressionContext simpleCtx2 =
                    ctx.simpleExpression().get(1);
            String simpleText2 = (String) visit(simpleCtx2);

            // Java uses the compareTo method for strings.
            if (simpleCtx1.type == Predefined.stringType) {
                text = "(" + simpleText1 + ")."
                        + "compareTo(" + simpleText2 + ") "
                        + op + " 0";
            } else {
                text = simpleText1 + " " + op + " " + simpleText2;
            }
        }

        return text;
    }

    @Override
    public Object visitSimpleExpression(PascalParser.SimpleExpressionContext ctx) {
        int count = ctx.term().size();
        StringBuilder text = new StringBuilder();

        if ((ctx.sign() != null) && (ctx.sign().getText().equals("-"))) {
            text.append("-");
        }

        // Loop over the simple expressions.
        for (int i = 0; i < count; i++) {
            PascalParser.TermContext termCtx = ctx.term().get(i);
            text.append((String) visit(termCtx));

            if (i < count - 1) {
                String addOp = ctx.addOp().get(i).getText().toLowerCase();
                if (addOp.equals("or")) addOp = "||";

                text.append(" ").append(addOp).append(" ");
            }
        }

        return text.toString();
    }

    @Override
    public Object visitTerm(PascalParser.TermContext ctx) {
        int count = ctx.factor().size();
        StringBuilder text = new StringBuilder();

        // Loop over the terms.
        for (int i = 0; i < count; i++) {
            PascalParser.FactorContext factorCtx = ctx.factor().get(i);
            text.append((String) visit(factorCtx));

            if (i < count - 1) {
                String mulOpStr = ctx.mulOp().get(i).getText().toLowerCase();
                String mulOp = switch (mulOpStr) {
                    case "and" -> " && ";
                    case "div" -> "/";
                    case "mod" -> "%";
                    default -> mulOpStr;
                };

                text.append(mulOp);
            }
        }

        return text.toString();
    }
    
    

    @Override
    public Object visitVariableFactor(PascalParser.VariableFactorContext ctx) {
        return visit(ctx.variable());
    }

    @Override
    public Object visitVariable(PascalParser.VariableContext ctx) {
        PascalParser.VariableIdentifierContext idCtx = ctx.variableIdentifier();
        SymTableEntry variableId = idCtx.entry;
        StringBuilder variableName = new StringBuilder(variableId.getName());
        Typespec type = ctx.variableIdentifier().type;

        if ((type != Predefined.booleanType)
                && (variableId.getKind() == ENUMERATION_CONSTANT)) {
            variableName.insert(0, type.getIdentifier().getName() + ".");
        }

        // Loop over any subscript and field modifiers.
        for (PascalParser.ModifierContext modCtx : ctx.modifier()) {
            // Subscripts.
            if (modCtx.indexList() != null) {
                for (PascalParser.IndexContext indexCtx :
                        modCtx.indexList().index()) {
                    Typespec indexType = type.getArrayIndexType();
                    int minIndex = 0;

                    if (indexType.getForm() == SUBRANGE) {
                        minIndex = indexType.getSubrangeMinValue();
                    }

                    PascalParser.ExpressionContext exprCtx =
                            indexCtx.expression();
                    String expr = (String) visit(exprCtx);
                    String subscript =
                            (minIndex == 0) ? expr
                                    : (minIndex < 0) ? "(" + expr + ")+" + (-minIndex)
                                    : "(" + expr + ")-" + minIndex;

                    variableName.append("[").append(subscript).append("]");

                    type = type.getArrayElementType();
                }
            }

            // Record field.
            else {
                PascalParser.FieldContext fieldCtx = modCtx.field();
                String fieldName = fieldCtx.entry.getName();
                variableName.append(".").append(fieldName);
                type = fieldCtx.type;
            }
        }

        return variableName.toString();
    }

    @Override
    public Object visitNumberFactor(PascalParser.NumberFactorContext ctx) {
        return ctx.getText();
    }

    @Override
    public Object visitCharacterFactor(PascalParser.CharacterFactorContext ctx) {
        return ctx.getText();
    }

    @Override
    public Object visitStringFactor(PascalParser.StringFactorContext ctx) {
        String pascalString = ctx.stringConstant().STRING().getText();
        return '"' + convertString(pascalString) + '"';
    }

    /**
     * Convert a Pascal string to a Java string.
     *
     * @param pascalString the Pascal string.
     * @return the Java string.
     */
    private String convertString(String pascalString) {
        String unquoted = pascalString.substring(1, pascalString.length() - 1);
        return unquoted.replace("''", "'").replace("\"", "\\\"");
    }

    @Override
    public Object visitFunctionCallFactor(
            PascalParser.FunctionCallFactorContext ctx) {
        PascalParser.FunctionCallContext callCtx = ctx.functionCall();
        PascalParser.FunctionNameContext funcNameCtx = callCtx.functionName();
        String functionName = funcNameCtx.entry.getName();

        String text = functionName + "(";

        if (callCtx.argumentList() != null) {
            text += (String) visit(callCtx.argumentList());
        }

        text += ")";
        return text;
    }

    @Override
    public Object visitNotFactor(PascalParser.NotFactorContext ctx) {
        return "!" + visit(ctx.factor());
    }

    @Override
    public Object visitParenthesizedFactor(
            PascalParser.ParenthesizedFactorContext ctx) {
        return "(" + visit(ctx.expression()) + ")";
    }

    @Override
    public Object visitWriteStatement(PascalParser.WriteStatementContext ctx) {
        code.emit("System.out.printf(");
        code.mark();

        String format = createWriteFormat(ctx.writeArguments());
        String arguments = createWriteArguments(ctx.writeArguments());

        code.emit('"' + format + '"');

        if (arguments.length() > 0) {
            code.emit(", ");
            code.split(60);
            code.emit(arguments);
        }

        code.emitEnd(");");
        return null;
    }

    @Override
    public Object visitWritelnStatement(PascalParser.WritelnStatementContext ctx) {
        if (ctx.writeArguments() != null) {
            code.emit("System.out.printf(");
            code.mark();

            String format = createWriteFormat(ctx.writeArguments());
            String arguments = createWriteArguments(ctx.writeArguments());

            code.emit('"' + format + "\\n\"");  // append line feed

            if (arguments.length() > 0) {
                code.emit(", ");
                code.split(60);
                code.emit(arguments);
            }

            code.emitEnd(");");
        } else {
            code.emitEnd("System.out.println();");
        }

        return null;
    }

    /**
     * Create the printf format string.
     *
     * @param ctx the WriteArgumentsContext.
     * @return the format string.
     */
    private String createWriteFormat(PascalParser.WriteArgumentsContext ctx) {
        StringBuilder format = new StringBuilder();

        // Loop over the "write" arguments.
        for (PascalParser.WriteArgumentContext argCtx : ctx.writeArgument()) {
            Typespec type = argCtx.expression().type;
            String argText = argCtx.getText();

            // Append any literal strings.
            if (argText.charAt(0) == '\'') {
                format.append(convertString(argText));
            }

            // For any other expressions, append a field specifier.
            else {
                format.append("%");

                PascalParser.FieldWidthContext fwCtx = argCtx.fieldWidth();
                if (fwCtx != null) {
                    String sign = ((fwCtx.sign() != null)
                            && (fwCtx.sign().getText().equals("-")))
                            ? "-" : "";
                    format.append(sign)
                            .append(fwCtx.integerConstant().getText());

                    PascalParser.DecimalPlacesContext dpCtx =
                            fwCtx.decimalPlaces();
                    if (dpCtx != null) {
                        format.append(".")
                                .append(dpCtx.integerConstant().getText());
                    }
                }

                String typeFlag = type == Predefined.integerType ? "d"
                        : type == Predefined.realType ? "f"
                        : type == Predefined.booleanType ? "b"
                        : type == Predefined.charType ? "c"
                        : "s";
                format.append(typeFlag);
            }
        }

        return format.toString();
    }

    /**
     * Create the string of write arguments.
     *
     * @param ctx the WriteArgumentsContext.
     * @return the string of arguments.
     */
    private String createWriteArguments(PascalParser.WriteArgumentsContext ctx) {
        StringBuilder arguments = new StringBuilder();
        String separator = "";

        // Loop over "write" arguments.
        for (PascalParser.WriteArgumentContext argCtx : ctx.writeArgument()) {
            String argText = argCtx.getText();

            // Not a literal string.
            if (argText.charAt(0) != '\'') {
                arguments.append(separator).append(visit(argCtx.expression()));
                separator = ", ";
            }
        }

        return arguments.toString();
    }

    @Override
    public Object visitReadStatement(PascalParser.ReadStatementContext ctx) {
        if (ctx.readArguments().variable().size() == 1) {
            visit(ctx.readArguments());
        } else {
            code.emit("{");
            code.indent();
            code.emitStart();

            visit(ctx.readArguments());

            code.dedent();
            code.emitLine("}");
        }

        return null;
    }

    @Override
    public Object visitReadlnStatement(PascalParser.ReadlnStatementContext ctx) {
        code.emit("{");
        code.indent();
        code.emitStart();

        visit(ctx.readArguments());
        code.emitLine("_sysin.nextLine();");

        code.dedent();
        code.emitLine("}");

        return null;
    }

    @Override
    public Object visitReadArguments(PascalParser.ReadArgumentsContext ctx) {
        int size = ctx.variable().size();

        // Loop over the read arguments.
        for (int i = 0; i < size; i++) {
            PascalParser.VariableContext varCtx = ctx.variable().get(i);
            String varName = varCtx.getText();
            Typespec type = varCtx.type;

            // Read a character.
            if (type == Predefined.charType) {
                code.emit("{");
                code.indent();

                code.emitStart("_sysin.useDelimiter(\"\");");
                code.emitStart(varName + " = _sysin.next().charAt(0);");
                code.emitStart("_sysin.reset();");

                code.dedent();
                code.emitLine("}");
            }

            // Read any other value.
            else {
                String typeName = type == Predefined.integerType ? "Int"
                        : type == Predefined.realType ? "Double"
                        : type == Predefined.booleanType ? "Boolean"
                        : "";

                code.emit(varName + " = _sysin.next" + typeName + "();");
            }

            if (i < size - 1) code.emitStart();
        }

        return null;
    }
}


'''
