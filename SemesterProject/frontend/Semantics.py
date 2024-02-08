from antlr.ToyParser import ToyParser
from antlr.ToyVisitor import ToyVisitor
from frontend.SemanticErrorHandler import SemanticErrorHandler, Code
from intermediate.symtable.Predefined import Predefined
from intermediate.symtable.Routine import Routine
from intermediate.symtable.SymTable import SymTable
from intermediate.symtable.SymTableEntry import Kind
from intermediate.symtable.SymTableStack import SymTableStack
from intermediate.type.Typespec import Typespec, Form
from intermediate.type.TypeChecker import TypeChecker
from intermediate.util.BackendMode import BackendMode


# TODO visitMainMethod

class Semantics(ToyVisitor):
    def __init__(self, mode):
        self.mode = mode
        self.symTableStack = SymTableStack()
        self.error = SemanticErrorHandler()
        self.symbol_table = {}
        self.current_scope = None
        self.classId = None
        Predefined.initialize(self.symTableStack)

    def getProgramId(self):
        return self.classId

    def getErrorCount(self):
        return self.error.getCount()

    def visitClassStart(self, ctx):
        self.visit(ctx.classHeader())
        self.visit(ctx.classLevelBlock().declarations())
        self.visit(ctx.classLevelBlock().mainProcedure())  # same as compound statement

    def visitClassHeader(self, ctx):
        idCtx = ctx.classIdentifier()
        className = idCtx.IDENTIFIER().getText()
        self.classId = self.symTableStack.enterLocal(className, Kind.CLASS)
        self.classId.setRoutineSymtable(self.symTableStack.push())
        self.symTableStack.setProgramId(self.classId)
        self.symTableStack.getLocalSymTable().setOwner(self.classId)
        idCtx.entry = self.classId

    def visitConstantDefinition(self, ctx):
        idCtx = ctx.constantIdentifier()
        constantName = idCtx.IDENTIFIER().getText().lower()
        constantId = self.symTableStack.lookupLocal(constantName)

        if constantId is None:
            constCtx = ctx.constant()
            constValue = self.visit(constCtx)

            constantId = self.symTableStack.enterLocal(constantName, Kind.CONSTANT)
            constantId.setValue(constValue)
            constantId.setType(constCtx.type_)

            idCtx.entry = constantId
            idCtx.type_ = constCtx.type_
        else:
            self.error.flagCtx(Code.REDECLARED_IDENTIFIER, ctx)

            idCtx.entry = constantId
            idCtx.type_ = Predefined.integerType

        constantId.appendLineNumber(ctx.start.line)

    def visitConstant(self, ctx):
        if ctx.IDENTIFIER() is not None:
            constantName = ctx.IDENTIFIER().getText().lower()
            constantId = self.symTableStack.lookup(constantName)

            if constantId is not None:
                kind = constantId.getKind()
                if kind is not Kind.CONSTANT and kind is not Kind.ENUMERATION_CONSTANT:
                    self.error.flagCtx(Code.INVALID_CONSTANT, ctx)

                ctx.type_ = constantId.getType()
                ctx.value = constantId.getValue()

                constantId.appendLineNumber(ctx.start.getLine())
            else:
                self.error.flagCtx(Code.UNDECLARED_IDENTIFIER, ctx)

                ctx.type_ = Predefined.integerType
                ctx.value = 0
        elif ctx.characterConstant() is not None:
            ctx.type_ = Predefined.charType
            ctx.value = ctx.characterConstant().getText()[1]  # ord?
        elif ctx.stringConstant() is not None:
            toyString = ctx.stringConstant().STRING().getText()
            unquoted = toyString[1:-1]
            ctx.type_ = Predefined.stringType
            ctx.value = unquoted.replace("''", "'").replace("\"", "\\\"")
        elif ctx.unsignedNumber().integerConstant() is not None:
            ctx.type_ = Predefined.integerType
            ctx.value = int(ctx.unsignedNumber().integerConstant().getText())
        elif ctx.unsignedNumber().realConstant() is not None:
            ctx.type_ = Predefined.realType
            ctx.value = float(ctx.unsignedNumber().realConstant().getText())
        elif ctx.booleanConstant() is not None:
            ctx.type_ = Predefined.booleanType
            ctx.value = ctx.booleanConstant().getText() == "true"
        return ctx.value

    def visitTypeDefinition(self, ctx):
        idCtx = ctx.typeIdentifier()
        typeName = idCtx.IDENTIFIER().getText().lower()
        typeId = self.symTableStack.lookupLocal(typeName)

        typespecCtx = ctx.typeSpecification()

        if isinstance(typespecCtx, ToyParser.RecordTypespecContext):
            typeId = self.createRecordType(typespecCtx, typeName)
        elif typeId is None:
            self.visit(typespecCtx)

            typeId = self.symTableStack.enterLocal(typeName, Kind.TYPE)
            typeId.setType(typespecCtx.type_)
            typespecCtx.type_.setIdentifier(typeId)
        else:
            self.error.flagCtx(Code.REDECLARED_IDENTIFIER, ctx)

        idCtx.entry = typeId
        idCtx.type_ = typespecCtx.type_

        typeId.appendLineNumber(ctx.start.line)

    def visitRecordTypespec(self, ctx: ToyParser.RecordTypespecContext):
        recordTypeName = SymTable.generateUnnamedName()
        self.createRecordType(ctx, recordTypeName)

    def createRecordType(self, ctx, recordTypeName):
        recordTypeCtx = ctx.recordType()
        recordType = Typespec(Form.RECORD)

        typeId = self.symTableStack.enterLocal(recordTypeName, Kind.TYPE)
        typeId.setType(recordType)
        recordType.setIdentifier(typeId)

        recordTypePath = self.createRecordTypePath(recordType)
        recordType.setRecordTypePath(recordTypePath)

        recordSymTable = self.createRecordSymTable(recordTypeCtx.recordFields(), typeId)
        recordType.setRecordSymTable(recordSymTable)

        recordTypeCtx.entry = typeId
        recordTypeCtx.type_ = recordType
        return typeId

    def createRecordTypePath(self, recordType):
        recordId = recordType.getIdentifier()
        parentId = recordId.getSymtable().getOwner()
        path = recordId.getName()

        while parentId.getKind() is Kind.TYPE and parentId.getType().getForm() is Form.RECORD:
            path = parentId.getName() + "$" + path
            parentId = parentId.getSymtable().getOwner()

        path = parentId.getName() + "$" + path
        return path

    def createRecordSymTable(self, ctx: ToyParser.RecordFieldsContext, ownerId):
        recordSymTable = self.symTableStack.push()

        recordSymTable.setOwner(ownerId)
        self.visit(ctx.variableDeclarationsList())
        recordSymTable.resetVariables(Kind.RECORD_FIELD)
        self.symTableStack.pop()

        return recordSymTable

    def visitSimpleTypespec(self, ctx: ToyParser.SimpleTypespecContext):
        self.visit(ctx.simpleType())
        ctx.type_ = ctx.simpleType().type_

    def visitTypeIdentifierTypespec(self, ctx: ToyParser.TypeIdentifierTypespecContext):
        self.visit(ctx.typeIdentifier())
        ctx.type_ = ctx.typeIdentifier().type_

    def visitTypeIdentifier(self, ctx: ToyParser.TypeIdentifierContext):
        typeName = ctx.IDENTIFIER().getText().lower()
        typeId = self.symTableStack.lookup(typeName)

        if typeId is not None:
            if typeId.getKind() is not Kind.TYPE:
                self.error.flagCtx(Code.INVALID_TYPE, ctx)
                ctx.type_ = Predefined.integerType
            else:
                ctx.type_ = typeId.getType()
            typeId.appendLineNumber(ctx.start.line)
        else:
            self.error.flagCtx(Code.INVALID_TYPE, ctx)
            ctx.type_ = Predefined.integerType

        ctx.entry = typeId

    def visitIteratorTypespec(self, ctx:ToyParser.IteratorTypespecContext):
        itType = Typespec(Form.ITERATOR)
        ctx.type_ = itType
        ctx.entry = self.symTableStack.lookupLocal(ctx.children[0].children[2].getText().lower())

    def visitArrayTypespec(self, ctx: ToyParser.ArrayTypespecContext):
        arrayType = Typespec(Form.ARRAY)
        arrayCtx = ctx.arrayType()
        arrayDimensionListCtx = arrayCtx.arrayDimensionList()

        ctx.type_ = arrayType

        count = len(arrayDimensionListCtx.integerConstant())
        elementType = None
        for i in range(count):
            intCtx = arrayDimensionListCtx.integerConstant(i)
            self.visit(intCtx)
            arrayType.setArrayIndexType(Predefined.integerType)
            arrayType.setArrayElementCount(int(intCtx.getText()))

            if i < count - 1:
                if elementType is None:
                    elementType = Typespec(Form.ARRAY)
                arrayType.setArrayElementType(elementType)
                arrayType = elementType
                elementType = elementType.getArrayElementType()
        self.visit(arrayCtx.typeSpecification())
        elementType = arrayCtx.typeSpecification().type_
        arrayType.setArrayElementType(elementType)

        return None

    def visitVariableDeclarations(self, ctx: ToyParser.VariableDeclarationsContext):
        typeCtx = ctx.typeSpecification()
        self.visit(typeCtx)

        listCtx = ctx.variableIdentifierList()

        # Loop over the variables being declared.
        for idCtx in listCtx.variableIdentifier():
            lineNumber = idCtx.start.line
            variableName = idCtx.IDENTIFIER().getText().lower()
            variableId = self.symTableStack.lookupLocal(variableName)

            if variableId is None:
                variableId = self.symTableStack.enterLocal(variableName, Kind.VARIABLE)
                variableId.setType(typeCtx.type_)

                # Assign slot numbers to local variables.
                symTable = variableId.getSymtable()
                if symTable.getNestingLevel() > 1:
                    variableId.setSlotNumber(len(symTable.values()))
                idCtx.entry = variableId
            else:
                self.error.flagCtx(Code.REDECLARED_IDENTIFIER, idCtx)

            variableId.appendLineNumber(lineNumber)

    '''
    @Override
    @SuppressWarnings("unchecked")
    public Object visitRoutineDefinition(ToyParser.RoutineDefinitionContext ctx) {
        ToyParser.FunctionHeadContext funcCtx = ctx.functionHead();
        ToyParser.ProcedureHeadContext procCtx = ctx.procedureHead();
        ToyParser.RoutineIdentifierContext idCtx;
        ToyParser.ParametersContext parameters;
        boolean functionDefinition = funcCtx != null;
        Typespec returnType = null;
        String routineName;

        if (functionDefinition) {
            idCtx = funcCtx.routineIdentifier();
            parameters = funcCtx.parameters();
        } else {
            idCtx = procCtx.routineIdentifier();
            parameters = procCtx.parameters();
        }

        routineName = idCtx.IDENTIFIER().getText().toLowerCase();
        SymTableEntry routineId = symTableStack.lookupLocal(routineName);

        if (routineId != null) {
            error.flag(REDECLARED_IDENTIFIER, ctx.getStart().getLine(), routineName);
            return null;
        }

        routineId = symTableStack.enterLocal(routineName, functionDefinition ? FUNCTION : PROCEDURE);
        routineId.setRoutineCode(DECLARED);
        idCtx.entry = routineId;

        // Append to the parent routine's list of subroutines.
        SymTableEntry parentId = symTableStack.getLocalSymTable().getOwner();
        parentId.appendSubroutine(routineId);

        routineId.setRoutineSymTable(symTableStack.push());
        idCtx.entry = routineId;

        SymTable symTable = symTableStack.getLocalSymTable();
        symTable.setOwner(routineId);

        if (parameters != null) {
            ArrayList<SymTableEntry> parameterIds = (ArrayList<SymTableEntry>) visit(parameters.parameterDeclarationsList());
            routineId.setRoutineParameters(parameterIds);

            for (SymTableEntry paramId : parameterIds) {
                paramId.setSlotNumber(symTable.nextSlotNumber());
            }
        }

        if (functionDefinition) {
            ToyParser.TypeIdentifierContext typeIdCtx = funcCtx.typeIdentifier();
            visit(typeIdCtx);
            returnType = typeIdCtx.type;

            if (returnType.getForm() != SCALAR) {
                error.flag(INVALID_RETURN_TYPE, typeIdCtx);
                returnType = Predefined.integerType;
            }

            routineId.setType(returnType);
            idCtx.type_ = returnType;
        } else {
            idCtx.type_ = null;
        }

        visit(ctx.block().declarations());

        // Enter the function's associated variable into its symbol table.
        if (functionDefinition) {
            SymTableEntry assocVarId = symTableStack.enterLocal(routineName, VARIABLE);
            assocVarId.setSlotNumber(symTable.nextSlotNumber());
            assocVarId.setType(returnType);
        }

        visit(ctx.block().compoundStatement());
        routineId.setExecutable(ctx.block().compoundStatement());

        symTableStack.pop();
        return null;
    }
    '''

    def visitRoutineDefinition(self, ctx):
        funcCtx = ctx.functionHead()
        procCtx = ctx.procedureHead()
        idCtx = None
        parameters = None
        functionDefinition = funcCtx is not None
        returnType = None
        routineName = ""

        if functionDefinition:
            idCtx = funcCtx.routineIdentifier()
            parameters = funcCtx.parameters()
        else:
            idCtx = procCtx.routineIdentifier()
            parameters = procCtx.parameters()

        routineName = idCtx.IDENTIFIER().getText().lower()
        routineId = self.symTableStack.lookupLocal(routineName)

        if routineId is not None:
            self.error.flag(Code.REDECLARED_IDENTIFIER, ctx.start.line, routineName)

        routineId = self.symTableStack.enterLocal(routineName, Kind.FUNCTION if functionDefinition else Kind.PROCEDURE)
        routineId.setRoutineCode(Routine.DECLARED)
        idCtx.entry = routineId

        # Append to the parent routine's list of subroutines.
        parentId = self.symTableStack.getLocalSymTable().getOwner()
        parentId.appendSubroutine(routineId)

        routineId.setRoutineSymtable(self.symTableStack.push())
        idCtx.entry = routineId

        symTable = self.symTableStack.getLocalSymTable()
        symTable.setOwner(routineId)

        if parameters is not None:
            parameterIds = self.visit(parameters.parameterDeclarationsList())
            routineId.setRoutineParameters(parameterIds)

            for paramId in parameterIds:
                paramId.setSlotNumber(symTable.nextSlotNumber())

        if functionDefinition:
            typeIdCtx = funcCtx.typeIdentifier()
            self.visit(typeIdCtx)
            returnType = typeIdCtx.type_

            if returnType.getForm() != Form.SCALAR:
                self.error.flagCtx(Code.INVALID_RETURN_TYPE, typeIdCtx)
                returnType = Predefined.integerType

            routineId.setType(returnType)
            idCtx.type_ = returnType
        else:
            idCtx.type_ = None

        self.visit(ctx.block().declarations())

        # Enter the function's associated variable into its symbol table.
        if functionDefinition:
            assocVarId = self.symTableStack.enterLocal(routineName, Kind.VARIABLE)
            assocVarId.setSlotNumber(symTable.nextSlotNumber())
            assocVarId.setType(returnType)

        self.visit(ctx.block().compoundStatement())
        routineId.setExecutable(ctx.block().compoundStatement())

        self.symTableStack.pop()

    '''
    @Override
    @SuppressWarnings("unchecked")
    public Object visitParameterDeclarationsList(ToyParser.ParameterDeclarationsListContext ctx) {
        ArrayList<SymTableEntry> parameterList = new ArrayList<>();

        // Loop over the parameter declarations.
        for (ToyParser.ParameterDeclarationsContext dclCtx : ctx.parameterDeclarations()) {
            ArrayList<SymTableEntry> parameterSublist = (ArrayList<SymTableEntry>) visit(dclCtx);
            parameterList.addAll(parameterSublist);
        }

        return parameterList;
    }
    '''

    def visitParameterDeclarationsList(self, ctx):
        parameterList = []

        # Loop over the parameter declarations.
        for dclCtx in ctx.parameterDeclarations():
            parameterSublist = self.visit(dclCtx)
            parameterList.extend(parameterSublist)

        return parameterList

    '''
    @Override
    public Object visitParameterDeclarations(ToyParser.ParameterDeclarationsContext ctx) {
        Kind kind = ctx.VAR() != null ? REFERENCE_PARAMETER : VALUE_PARAMETER;
        ToyParser.TypeIdentifierContext typeCtx = ctx.typeIdentifier();

        visit(typeCtx);
        Typespec paramType = typeCtx.type;

        ArrayList<SymTableEntry> parameterSublist = new ArrayList<>();

        // Loop over the parameter identifiers.
        ToyParser.ParameterIdentifierListContext paramListCtx = ctx.parameterIdentifierList();
        for (ToyParser.ParameterIdentifierContext paramIdCtx : paramListCtx.parameterIdentifier()) {
            int lineNumber = paramIdCtx.getStart().getLine();
            String paramName = paramIdCtx.IDENTIFIER().getText().toLowerCase();
            SymTableEntry paramId = symTableStack.lookupLocal(paramName);

            if (paramId == null) {
                paramId = symTableStack.enterLocal(paramName, kind);
                paramId.setType(paramType);

                if ((kind == REFERENCE_PARAMETER) && (mode != EXECUTOR) && (paramType.getForm() == SCALAR)) {
                    error.flag(INVALID_REFERENCE_PARAMETER, paramIdCtx);
                }
            } else {
                error.flag(REDECLARED_IDENTIFIER, paramIdCtx);
            }

            paramIdCtx.entry = paramId;
            paramIdCtx.type_ = paramType;

            parameterSublist.add(paramId);
            paramId.appendLineNumber(lineNumber);
        }

        return parameterSublist;
    }
    '''

    def visitParameterDeclarations(self, ctx: ToyParser.ParameterDeclarationsContext):
        kind = Kind.REFERENCE_PARAMETER if False else Kind.VALUE_PARAMETER
        typeCtx = ctx.typeIdentifier()

        self.visit(typeCtx)
        paramType = typeCtx.type_

        parameterSublist = []

        # Loop over the parameter identifiers.
        paramListCtx = ctx.parameterIdentifierList()
        for paramIdCtx in paramListCtx.parameterIdentifier():
            lineNumber = paramIdCtx.start.line
            paramName = paramIdCtx.IDENTIFIER().getText().lower()
            paramId = self.symTableStack.lookupLocal(paramName)

            if paramId is None:
                paramId = self.symTableStack.enterLocal(paramName, kind)
                paramId.setType(paramType)

                if (kind == Kind.REFERENCE_PARAMETER) and (self.mode != BackendMode.EXECUTOR) and (
                        paramType.getForm() == Form.SCALAR):
                    self.error.flagCtx(Code.INVALID_REFERENCE_PARAMETER, paramIdCtx)
            else:
                self.error.flagCtx(Code.REDECLARED_IDENTIFIER, paramIdCtx)

            paramIdCtx.entry = paramId
            paramIdCtx.type_ = paramType

            parameterSublist.append(paramId)
            paramId.appendLineNumber(lineNumber)

        return parameterSublist

    '''
    @Override
    public Object visitAssignmentStatement(ToyParser.AssignmentStatementContext ctx) {
        ToyParser.LhsContext lhsCtx = ctx.lhs();
        ToyParser.RhsContext rhsCtx = ctx.rhs();

        visitChildren(ctx);

        Typespec lhsType = lhsCtx.type;
        Typespec rhsType = rhsCtx.expression().type;

        if (!TypeChecker.areAssignmentCompatible(lhsType, rhsType)) {
            error.flag(INCOMPATIBLE_ASSIGNMENT, rhsCtx);
        }

        return null;
    }
    '''

    def visitAssignmentStatement(self, ctx):
        lhsCtx = ctx.lhs()
        rhsCtx = ctx.rhs()

        self.visitChildren(ctx)

        lhsType = lhsCtx.type_
        rhsType = None
        if rhsCtx.expression() is not None:
            rhsType = rhsCtx.expression().type_

            if not TypeChecker.areAssignmentCompatible(lhsType, rhsType):
                self.error.flagCtx(Code.INCOMPATIBLE_ASSIGNMENT, rhsCtx)

    '''
    @Override
    public Object visitLhs(ToyParser.LhsContext ctx) {
        ToyParser.VariableContext varCtx = ctx.variable();
        visit(varCtx);
        ctx.type_ = varCtx.type;

        return null;
    }
    '''
    def visitGetArgCallFactor(self, ctx:ToyParser.GetArgCallFactorContext):
        ctx.type_ = Predefined.stringType

    def visitLhs(self, ctx):
        varCtx = ctx.variable()
        self.visit(varCtx)
        ctx.type_ = varCtx.type_

    '''
    @Override
    public Object visitIfStatement(ToyParser.IfStatementContext ctx) {
        ToyParser.ExpressionContext exprCtx = ctx.expression();
        ToyParser.TrueStatementContext trueCtx = ctx.trueStatement();
        ToyParser.FalseStatementContext falseCtx = ctx.falseStatement();

        visit(exprCtx);
        Typespec exprType = exprCtx.type;

        if (!TypeChecker.isBoolean(exprType)) {
            error.flag(TYPE_MUST_BE_BOOLEAN, exprCtx);
        }

        visit(trueCtx);
        if (falseCtx != null) visit(falseCtx);

        return null;
    }
    '''

    def visitIfStatement(self, ctx):
        exprCtx = ctx.expression()
        trueCtx = ctx.trueStatement()
        falseCtx = ctx.falseStatement()

        self.visit(exprCtx)
        exprType = exprCtx.type_

        if not TypeChecker.isBoolean(exprType):
            self.error.flagCtx(Code.TYPE_MUST_BE_BOOLEAN, exprCtx)

        self.visit(trueCtx)
        if falseCtx is not None:
            self.visit(falseCtx)

    '''
    @Override
    public Object visitCaseStatement(ToyParser.CaseStatementContext ctx) {
        ToyParser.ExpressionContext exprCtx = ctx.expression();
        visit(exprCtx);
        Typespec exprType = exprCtx.type;
        Form exprTypeForm = exprType.getForm();

        if (((exprTypeForm != SCALAR) && (exprTypeForm != ENUMERATION) && (exprTypeForm != SUBRANGE)) || (exprType == Predefined.realType)) {
            error.flag(TYPE_MISMATCH, exprCtx);
            exprType = Predefined.integerType;
        }

        HashSet<Object> constants = new HashSet<>();
        ToyParser.CaseBranchListContext branchListCtx = ctx.caseBranchList();

        // Loop over the CASE branches.
        ctx.jumpTable = new HashMap<>();
        for (ToyParser.CaseBranchContext branchCtx : branchListCtx.caseBranch()) {
            ToyParser.CaseConstantListContext constListCtx = branchCtx.caseConstantList();
            ToyParser.StatementContext stmtCtx = branchCtx.statement();

            if (constListCtx != null) {
                // Loop over the CASE constants in each branch.
                for (ToyParser.CaseConstantContext caseConstCtx : constListCtx.caseConstant()) {
                    ToyParser.ConstantContext constCtx = caseConstCtx.constant();
                    Object constValue = visit(constCtx);

                    caseConstCtx.type_ = constCtx.type;
                    caseConstCtx.value = null;

                    if (constCtx.type_ != exprType) {
                        error.flag(TYPE_MISMATCH, constCtx);
                    } else if ((constCtx.type_ == Predefined.integerType) || (constCtx.type.getForm() == ENUMERATION)) {
                        caseConstCtx.value = (Integer) constValue;
                    } else if (constCtx.type_ == Predefined.charType) {
                        caseConstCtx.value = (Character) constValue;
                    } else if (constCtx.type_ == Predefined.stringType) {
                        caseConstCtx.value = (String) constValue;
                    }

                    if (constants.contains(caseConstCtx.value)) {
                        error.flag(DUPLICATE_CASE_CONSTANT, constCtx);
                    } else {
                        constants.add(caseConstCtx.value);
                        ctx.jumpTable.put(caseConstCtx.value,stmtCtx);
                    }
                }
            }

            if (stmtCtx != null) visit(stmtCtx);
        }

        return null;
    }


    def visitCaseStatement(self, ctx):
        exprCtx = ctx.expression()
        self.visit(exprCtx)
        exprType = exprCtx.type
        exprTypeForm = exprType.getForm()

        if exprTypeForm not in [Kind.SCALAR, Kind.ENUMERATION, Kind.SUBRANGE] or exprType == Predefined.realType:
            self.error.flagCtx(Kind.TYPE_MISMATCH, exprCtx)
            exprType = Predefined.integerType

        constants = set()
        branchListCtx = ctx.caseBranchList()

        ctx.jumpTable = {}

        for branchCtx in branchListCtx.caseBranch():
            constListCtx = branchCtx.caseConstantList()
            stmtCtx = branchCtx.statement()

            if constListCtx is not None:
                for caseConstCtx in constListCtx.caseConstant():
                    constCtx = caseConstCtx.constant()
                    constValue = self.visit(constCtx)

                    caseConstCtx.type_ = constCtx.type
                    caseConstCtx.value = None

                    if constCtx.type_ != exprType:
                        self.error.flagCtx(Code.TYPE_MISMATCH, constCtx)
                    elif constCtx.type_ == Predefined.integerType or constCtx.type.getForm() == Kind.ENUMERATION:
                        caseConstCtx.value = int(constValue)
                    elif constCtx.type_ == Predefined.charType:
                        caseConstCtx.value = chr(constValue)
                    elif constCtx.type_ == Predefined.stringType:
                        caseConstCtx.value = str(constValue)

                    if caseConstCtx.value in constants:
                        self.error.flagCtx(Kind.DUPLICATE_CASE_CONSTANT, constCtx)
                    else:
                        constants.add(caseConstCtx.value)
                        ctx.jumpTable[caseConstCtx.value] = stmtCtx

            if stmtCtx is not None:
                self.visit(stmtCtx)


    @Override
    public Object visitRepeatStatement(ToyParser.RepeatStatementContext ctx) {
        ToyParser.ExpressionContext exprCtx = ctx.expression();
        visit(exprCtx);
        Typespec exprType = exprCtx.type;

        if (!TypeChecker.isBoolean(exprType)) {
            error.flag(TYPE_MUST_BE_BOOLEAN, exprCtx);
        }

        visit(ctx.statementList());
        return null;
    }
    '''

    def visitRepeatStatement(self, ctx):
        exprCtx = ctx.expression()
        self.visit(exprCtx)
        exprType = exprCtx.type_

        if not TypeChecker.isBoolean(exprType):
            self.error.flagCtx(Code.TYPE_MUST_BE_BOOLEAN, exprCtx)

        self.visit(ctx.statementList())

    '''
    @Override
    public Object visitWhileStatement(ToyParser.WhileStatementContext ctx) {
        ToyParser.ExpressionContext exprCtx = ctx.expression();
        visit(exprCtx);
        Typespec exprType = exprCtx.type;

        if (!TypeChecker.isBoolean(exprType)) {
            error.flag(TYPE_MUST_BE_BOOLEAN, exprCtx);
        }

        visit(ctx.statement());
        return null;
    }
    '''

    def visitWhileStatement(self, ctx):
        if ctx.expression() is not None:
            exprCtx = ctx.expression()
            self.visit(exprCtx)
            exprType = exprCtx.type_

            if not TypeChecker.isBoolean(exprType):
                self.error.flagCtx(Code.TYPE_MUST_BE_BOOLEAN, exprCtx)

        self.visit(ctx.statement())

    '''
    @Override
    public Object visitForStatement(ToyParser.ForStatementContext ctx) {
        ToyParser.VariableContext varCtx = ctx.variable();
        visit(varCtx);

        String controlName = varCtx.variableIdentifier().getText().toLowerCase();
        Typespec controlType = Predefined.integerType;

        if (varCtx.entry != null) {
            controlType = varCtx.type;

            if ((controlType.getForm() != SCALAR) || (controlType == Predefined.realType) || (controlType == Predefined.stringType) || (varCtx.modifier().size() != 0)) {
                error.flag(INVALID_CONTROL_VARIABLE, varCtx);
            }
        } else {
            error.flag(UNDECLARED_IDENTIFIER, ctx.getStart().getLine(), controlName);
        }

        ToyParser.ExpressionContext startCtx = ctx.expression().get(0);
        ToyParser.ExpressionContext endCtx = ctx.expression().get(1);

        visit(startCtx);
        visit(endCtx);

        if (startCtx.type_ != controlType) error.flag(TYPE_MISMATCH, startCtx);
        if (startCtx.type_ != endCtx.type) error.flag(TYPE_MISMATCH, endCtx);

        visit(ctx.statement());
        return null;
    }
    '''

    def visitForStatement(self, ctx):
        varCtx = ctx.variable()
        self.visit(varCtx)

        controlName = varCtx.variableIdentifier().getText().lower()
        controlType = Predefined.integerType

        if varCtx.entry is not None:
            controlType = varCtx.type_

            if (controlType.getForm() != Form.SCALAR) or (controlType == Predefined.realType) or (
                    controlType == Predefined.stringType) or (len(varCtx.modifier()) != 0):
                self.error.flagCtx(Code.INVALID_CONTROL_VARIABLE, varCtx)
        else:
            self.error.flag(Code.UNDECLARED_IDENTIFIER, ctx.start.line, controlName)

        startCtx = ctx.expression()[0]
        endCtx = ctx.expression()[1]

        self.visit(startCtx)
        self.visit(endCtx)

        if startCtx.type_ != controlType:
            self.error.flagCtx(Code.TYPE_MISMATCH, startCtx)
        if startCtx.type_ != endCtx.type:
            self.error.flagCtx(Code.TYPE_MISMATCH, endCtx)

        self.visit(ctx.statement())

    '''
    @Override
    public Object visitProcedureCallStatement(ToyParser.ProcedureCallStatementContext ctx) {
        ToyParser.ProcedureNameContext nameCtx = ctx.procedureName();
        ToyParser.ArgumentListContext listCtx = ctx.argumentList();
        String name = ctx.procedureName().getText().toLowerCase();
        SymTableEntry procedureId = symTableStack.lookup(name);
        boolean badName = false;

        if (procedureId == null) {
            error.flag(UNDECLARED_IDENTIFIER, nameCtx);
            badName = true;
        } else if (procedureId.getKind() != PROCEDURE) {
            error.flag(NAME_MUST_BE_PROCEDURE, nameCtx);
            badName = true;
        }

        // Bad procedure name. Do a simple arguments check and then leave.
        if (badName) {
            for (ToyParser.ArgumentContext exprCtx : listCtx.argument()) {
                visit(exprCtx);
            }
        }

        // Good procedure name.
        else {
            ArrayList<SymTableEntry> params = procedureId.getRoutineParameters();
            checkCallArguments(listCtx, params);
        }

        nameCtx.entry = procedureId;
        return null;
    }
    '''

    def visitProcedureCallStatement(self, ctx):
        nameCtx = ctx.procedureName()
        listCtx = ctx.argumentList()
        name = ctx.procedureName().getText().lower()
        procedureId = self.symTableStack.lookup(name)
        badName = False

        if procedureId is None:
            self.error.flagCtx(Code.UNDECLARED_IDENTIFIER, nameCtx)
            badName = True
        elif procedureId.getKind() != Kind.PROCEDURE:
            self.error.flagCtx(Code.NAME_MUST_BE_PROCEDURE, nameCtx)
            badName = True

        # Bad procedure name. Do a simple arguments check and then leave.

        if badName:
            #for exprCtx in listCtx.argument():
                #self.visit(exprCtx)
            pass

        # Good procedure name.
        else:
            params = procedureId.getRoutineParameters()
            self.checkCallArguments(listCtx, params)

        nameCtx.entry = procedureId

    '''
    @Override
    public Object visitFunctionCallFactor(ToyParser.FunctionCallFactorContext ctx) {
        ToyParser.FunctionCallContext callCtx = ctx.functionCall();
        ToyParser.FunctionNameContext nameCtx = callCtx.functionName();
        ToyParser.ArgumentListContext listCtx = callCtx.argumentList();
        String name = callCtx.functionName().getText().toLowerCase();
        SymTableEntry functionId = symTableStack.lookup(name);
        boolean badName = false;

        ctx.type_ = Predefined.integerType;

        if (functionId == null) {
            error.flag(UNDECLARED_IDENTIFIER, nameCtx);
            badName = true;
        } else if (functionId.getKind() != FUNCTION) {
            error.flag(NAME_MUST_BE_FUNCTION, nameCtx);
            badName = true;
        }

        // Bad function name. Do a simple arguments check and then leave.
        if (badName) {
            for (ToyParser.ArgumentContext exprCtx : listCtx.argument()) {
                visit(exprCtx);
            }
        }

        // Good function name.
        else {
            ArrayList<SymTableEntry> parameters = functionId.getRoutineParameters();
            checkCallArguments(listCtx, parameters);
            ctx.type_ = functionId.getType();
        }

        nameCtx.entry = functionId;
        nameCtx.type_ = ctx.type;

        return null;
    }
    '''

    def visitFunctionCallFactor(self, ctx):
        callCtx = ctx.functionCall()
        nameCtx = callCtx.functionName()
        listCtx = callCtx.argumentList()
        name = callCtx.functionName().getText().lower()
        functionId = self.symTableStack.lookup(name)
        badName = False

        ctx.type_ = Predefined.integerType

        if functionId is None:
            self.error.flagCtx(Code.UNDECLARED_IDENTIFIER, nameCtx)
            badName = True
        elif functionId.getKind() != Kind.FUNCTION:
            self.error.flagCtx(Code.NAME_MUST_BE_FUNCTION, nameCtx)
            badName = True

        # Bad function name. Do a simple arguments check and then leave.
        if badName:
            for exprCtx in listCtx.argument():
                self.visit(exprCtx)

        # Good function name.
        else:
            parameters = functionId.getRoutineParameters()
            self.checkCallArguments(listCtx, parameters)
            ctx.type_ = functionId.getType()

        nameCtx.entry = functionId
        nameCtx.type_ = ctx.type_

    '''
    /**
     * Perform semantic operations on procedure and function call arguments.
     *
     * @param listCtx    the ArgumentListContext.
     * @param parameters the arraylist of parameters to fill.
     */
    private void checkCallArguments(ToyParser.ArgumentListContext listCtx, ArrayList<SymTableEntry> parameters) {
        int paramsCount = parameters.size();
        int argsCount = listCtx != null ? listCtx.argument().size() : 0;

        if (paramsCount != argsCount) {
            error.flag(ARGUMENT_COUNT_MISMATCH, listCtx);
            return;
        }

        // Check each argument against the corresponding parameter.
        for (int i = 0; i < paramsCount; i++) {
            ToyParser.ArgumentContext argCtx = listCtx.argument().get(i);
            ToyParser.ExpressionContext exprCtx = argCtx.expression();
            visit(exprCtx);

            SymTableEntry paramId = parameters.get(i);
            Typespec paramType = paramId.getType();
            Typespec argType = exprCtx.type;

            // For a VAR parameter, the argument must be a variable
            // with the same datatype.
            if (paramId.getKind() == REFERENCE_PARAMETER) {
                if (expressionIsVariable(exprCtx)) {
                    if (paramType != argType) {
                        error.flag(TYPE_MISMATCH, exprCtx);
                    }
                } else {
                    error.flag(ARGUMENT_MUST_BE_VARIABLE, exprCtx);
                }
            }

            // For a value parameter, the argument type must be
            // assignment compatible with the parameter type.
            else if (!TypeChecker.areAssignmentCompatible(paramType, argType)) {
                error.flag(TYPE_MISMATCH, exprCtx);
            }
        }
    }
    '''

    def checkCallArguments(self, listCtx, parameters):
        paramsCount = len(parameters)
        argsCount = len(listCtx.argument()) if listCtx else 0

        if paramsCount != argsCount:
            self.error.flagCtx(Code.ARGUMENT_COUNT_MISMATCH, listCtx)
            return

        # Check each argument against the corresponding parameter.
        for i in range(paramsCount):
            argCtx = listCtx.argument()[i]
            exprCtx = argCtx.expression()
            self.visit(exprCtx)

            paramId = parameters[i]
            paramType = paramId.getType()
            argType = exprCtx.type_

            # For a VAR parameter, the argument must be a variable
            # with the same datatype.
            if paramId.getKind() == Kind.REFERENCE_PARAMETER:
                if self.expressionIsVariable(exprCtx):
                    if paramType != argType:
                        self.error.flagCtx(Code.TYPE_MISMATCH, exprCtx)
                else:
                    self.error.flagCtx(Code.ARGUMENT_MUST_BE_VARIABLE, exprCtx)

            # For a value parameter, the argument type must be
            # assignment compatible with the parameter type.
            elif not TypeChecker.areAssignmentCompatible(paramType, argType):
                if TypeChecker.isString(paramType.baseType()):
                    self.error.flagCtx(Code.TYPE_MUST_BE_STRING, exprCtx)
                else:
                    self.error.flagCtx(Code.TYPE_MISMATCH, exprCtx)

    '''
    /**
     * Determine whether an expression is a variable only.
     *
     * @param exprCtx the ExpressionContext.
     * @return true if it's an expression only, else false.
     */
    private boolean expressionIsVariable(ToyParser.ExpressionContext exprCtx) {
        // Only a single simple expression?
        if (exprCtx.simpleExpression().size() == 1) {
            ToyParser.SimpleExpressionContext simpleCtx = exprCtx.simpleExpression().get(0);
            // Only a single term?
            if (simpleCtx.term().size() == 1) {
                ToyParser.TermContext termCtx = simpleCtx.term().get(0);

                // Only a single factor?
                if (termCtx.factor().size() == 1) {
                    return termCtx.factor().get(0) instanceof ToyParser.VariableFactorContext;
                }
            }
        }

        return false;
    }
    '''

    def expressionIsVariable(self, exprCtx):
        # Only a single simple expression?
        if len(exprCtx.simpleExpression()) == 1:
            simpleCtx = exprCtx.simpleExpression()[0]
            # Only a single term?
            if len(simpleCtx.term()) == 1:
                termCtx = simpleCtx.term()[0]

                # Only a single factor?
                if len(termCtx.factor()) == 1:
                    return isinstance(termCtx.factor()[0], ToyParser.VariableFactorContext)

        return False

    '''
    @Override
    public Object visitExpression(ToyParser.ExpressionContext ctx) {
        ToyParser.SimpleExpressionContext simpleCtx1 = ctx.simpleExpression().get(0);

        // First simple expression.
        visit(simpleCtx1);

        Typespec simpleType1 = simpleCtx1.type;
        ctx.type_ = simpleType1;

        ToyParser.RelOpContext relOpCtx = ctx.relOp();

        // Second simple expression?
        if (relOpCtx != null) {
            ToyParser.SimpleExpressionContext simpleCtx2 = ctx.simpleExpression().get(1);
            visit(simpleCtx2);

            Typespec simpleType2 = simpleCtx2.type;
            if (!TypeChecker.areComparisonCompatible(simpleType1, simpleType2)) {
                error.flag(INCOMPATIBLE_COMPARISON, ctx);
            }

            ctx.type_ = Predefined.booleanType;
        }

        return null;
    }
    '''

    def visitExpression(self, ctx):
        simpleCtx1 = ctx.simpleExpression()[0]
        self.visit(simpleCtx1)
        simpleType1 = simpleCtx1.type_
        ctx.type_ = simpleType1
        relOpCtx = ctx.relOp()

        # Second simple expression?
        if relOpCtx is not None:
            simpleCtx2 = ctx.simpleExpression()[1]
            self.visit(simpleCtx2)
            simpleType2 = simpleCtx2.type_
            if not TypeChecker.areComparisonCompatible(simpleType1, simpleType2):
                self.error.flagCtx(Code.INCOMPATIBLE_COMPARISON, ctx)
            ctx.type_ = Predefined.booleanType

    '''
    @Override
    public Object visitSimpleExpression(ToyParser.SimpleExpressionContext ctx) {
        int count = ctx.term().size();
        ToyParser.SignContext signCtx = ctx.sign();
        boolean hasSign = signCtx != null;
        ToyParser.TermContext termCtx1 = ctx.term().get(0);

        if (hasSign) {
            String sign = signCtx.getText();
            if (!sign.equals("+") && !sign.equals("-")) {
                error.flag(INVALID_SIGN, signCtx);
            }
        }

        // First term.
        visit(termCtx1);
        Typespec termType1 = termCtx1.type;

        // Loop over any subsequent terms.
        for (int i = 1; i < count; i++) {
            String op = ctx.addOp().get(i - 1).getText().toLowerCase();
            ToyParser.TermContext termCtx2 = ctx.term().get(i);
            visit(termCtx2);
            Typespec termType2 = termCtx2.type;

            // Both operands boolean ==> boolean result. Else type mismatch.
            if (op.equals("or")) {
                if (!TypeChecker.isBoolean(termType1)) {
                    error.flag(TYPE_MUST_BE_BOOLEAN, termCtx1);
                }
                if (!TypeChecker.isBoolean(termType2)) {
                    error.flag(TYPE_MUST_BE_BOOLEAN, termCtx2);
                }
                if (hasSign) {
                    error.flag(INVALID_SIGN, signCtx);
                }

                termType2 = Predefined.booleanType;
            } else if (op.equals("+")) {
                // Both operands integer ==> integer result
                if (TypeChecker.areBothInteger(termType1, termType2)) {
                    termType2 = Predefined.integerType;
                }

                // Both real operands ==> real result
                // One real and one integer operand ==> real result
                else if (TypeChecker.isAtLeastOneReal(termType1, termType2)) {
                    termType2 = Predefined.realType;
                }

                // Both operands string ==> string result
                else if (TypeChecker.areBothString(termType1, termType2)) {
                    if (hasSign) error.flag(INVALID_SIGN, signCtx);
                    termType2 = Predefined.stringType;
                }

                // Type mismatch.
                else {
                    if (!TypeChecker.isIntegerOrReal(termType1)) {
                        error.flag(TYPE_MUST_BE_NUMERIC, termCtx1);
                        termType2 = Predefined.integerType;
                    }
                    if (!TypeChecker.isIntegerOrReal(termType2)) {
                        error.flag(TYPE_MUST_BE_NUMERIC, termCtx2);
                        termType2 = Predefined.integerType;
                    }
                }
            } else  // -
            {
                // Both operands integer ==> integer result
                if (TypeChecker.areBothInteger(termType1, termType2)) {
                    termType2 = Predefined.integerType;
                }

                // Both real operands ==> real result
                // One real and one integer operand ==> real result
                else if (TypeChecker.isAtLeastOneReal(termType1, termType2)) {
                    termType2 = Predefined.realType;
                }

                // Type mismatch.
                else {
                    if (!TypeChecker.isIntegerOrReal(termType1)) {
                        error.flag(TYPE_MUST_BE_NUMERIC, termCtx1);
                        termType2 = Predefined.integerType;
                    }
                    if (!TypeChecker.isIntegerOrReal(termType2)) {
                        error.flag(TYPE_MUST_BE_NUMERIC, termCtx2);
                        termType2 = Predefined.integerType;
                    }
                }
            }

            termType1 = termType2;
        }

        ctx.type_ = termType1;
        return null;
    }
    '''

    def visitSimpleExpression(self, ctx: ToyParser.SimpleExpressionContext):
        count = len(ctx.term())
        signCtx = ctx.sign()
        hasSign = signCtx is not None
        termCtx1 = ctx.term()[0]

        if hasSign:
            sign = signCtx.getText()
            if sign != "+" and sign != "-":
                self.error.flagCtx(Code.INVALID_SIGN, signCtx)

        # First term.
        self.visit(termCtx1)
        termType1 = termCtx1.type_

        # Loop over any subsequent terms.
        for i in range(1, count):
            op = ctx.addOp()[i - 1].getText().lower()
            termCtx2 = ctx.term()[i]
            self.visit(termCtx2)
            termType2 = termCtx2.type_

            # Both operands boolean ==> boolean result. Else type mismatch.
            if op == "or":
                if not TypeChecker.isBoolean(termType1) and not TypeChecker.isBoolean(termType2):
                    self.error.flag(Code.INVALID_OPERATOR, termCtx1.start.line, op)
                elif not TypeChecker.isBoolean(termType1):
                    self.error.flagCtx(Code.TYPE_MUST_BE_BOOLEAN, termCtx1)
                elif not TypeChecker.isBoolean(termType2):
                    self.error.flagCtx(Code.TYPE_MUST_BE_BOOLEAN, termCtx2)
                if hasSign:
                    self.error.flagCtx(Code.INVALID_SIGN, signCtx)

                termType2 = Predefined.booleanType
            elif op == "+":
                # Both operands integer ==> integer result
                if TypeChecker.areBothInteger(termType1, termType2):
                    termType2 = Predefined.integerType

                # Both real operands ==> real result
                # One real and one integer operand ==> real result
                elif TypeChecker.isAtLeastOneReal(termType1, termType2):
                    termType2 = Predefined.realType

                # Both operands string ==> string result
                elif TypeChecker.areBothString(termType1, termType2):
                    if hasSign:
                        self.error.flagCtx(Code.INVALID_SIGN, signCtx)
                    termType2 = Predefined.stringType

                # Type mismatch.
                else:
                    if not TypeChecker.isIntegerOrReal(termType1) and not TypeChecker.isIntegerOrReal(termType2):
                        self.error.flag(Code.INVALID_OPERATOR, termCtx1.start.line, op)
                    elif not TypeChecker.isIntegerOrReal(termType1):
                        self.error.flagCtx(Code.TYPE_MUST_BE_NUMERIC, termCtx1)
                        termType2 = Predefined.integerType
                    elif not TypeChecker.isIntegerOrReal(termType2):
                        self.error.flagCtx(Code.TYPE_MUST_BE_NUMERIC, termCtx2)
                        termType2 = Predefined.integerType
            else:  # -
                # Both operands integer ==> integer result
                if TypeChecker.areBothInteger(termType1, termType2):
                    termType2 = Predefined.integerType

                # Both real operands ==> real result
                # One real and one integer operand ==> real result
                elif TypeChecker.isAtLeastOneReal(termType1, termType2):
                    termType2 = Predefined.realType

                # Type mismatch.
                else:
                    if not TypeChecker.isIntegerOrReal(termType1) and not TypeChecker.isIntegerOrReal(termType2):
                        self.error.flag(Code.INVALID_OPERATOR, termCtx1.start.line, op)
                    elif not TypeChecker.isIntegerOrReal(termType1):
                        self.error.flagCtx(Code.TYPE_MUST_BE_NUMERIC, termCtx1)
                        termType2 = Predefined.integerType
                    elif not TypeChecker.isIntegerOrReal(termType2):
                        self.error.flagCtx(Code.TYPE_MUST_BE_NUMERIC, termCtx2)
                        termType2 = Predefined.integerType

            termType1 = termType2

        ctx.type_ = termType1

    '''
    @Override
    public Object visitTerm(ToyParser.TermContext ctx) {
        int count = ctx.factor().size();
        ToyParser.FactorContext factorCtx1 = ctx.factor().get(0);

        // First factor.
        visit(factorCtx1);
        Typespec factorType1 = factorCtx1.type;

        // Loop over any subsequent factors.
        for (int i = 1; i < count; i++) {
            String op = ctx.mulOp().get(i - 1).getText().toLowerCase();
            ToyParser.FactorContext factorCtx2 = ctx.factor().get(i);
            visit(factorCtx2);
            Typespec factorType2 = factorCtx2.type;

            switch (op) {
                case "*":
                    // Both operands integer  ==> integer result
                    if (TypeChecker.areBothInteger(factorType1, factorType2)) {
                        factorType2 = Predefined.integerType;
                    }

                    // Both real operands ==> real result
                    // One real and one integer operand ==> real result
                    else if (TypeChecker.isAtLeastOneReal(factorType1, factorType2)) {
                        factorType2 = Predefined.realType;
                    }

                    // Type mismatch.
                    else {
                        if (!TypeChecker.isIntegerOrReal(factorType1)) {
                            error.flag(TYPE_MUST_BE_NUMERIC, factorCtx1);
                            factorType2 = Predefined.integerType;
                        }
                        if (!TypeChecker.isIntegerOrReal(factorType2)) {
                            error.flag(TYPE_MUST_BE_NUMERIC, factorCtx2);
                            factorType2 = Predefined.integerType;
                        }
                    }
                    break;
                case "/":
                    // All integer and real operand combinations ==> real result
                    if (TypeChecker.areBothInteger(factorType1, factorType2) || TypeChecker.isAtLeastOneReal(factorType1, factorType2)) {
                        factorType2 = Predefined.realType;
                    }

                    // Type mismatch.
                    else {
                        if (!TypeChecker.isIntegerOrReal(factorType1)) {
                            error.flag(TYPE_MUST_BE_NUMERIC, factorCtx1);
                            factorType2 = Predefined.integerType;
                        }
                        if (!TypeChecker.isIntegerOrReal(factorType2)) {
                            error.flag(TYPE_MUST_BE_NUMERIC, factorCtx2);
                            factorType2 = Predefined.integerType;
                        }
                    }
                    break;
                case "div":
                case "mod":
                    // Both operands integer ==> integer result. Else type mismatch.
                    if (!TypeChecker.isInteger(factorType1)) {
                        error.flag(TYPE_MUST_BE_INTEGER, factorCtx1);
                        factorType2 = Predefined.integerType;
                    }
                    if (!TypeChecker.isInteger(factorType2)) {
                        error.flag(TYPE_MUST_BE_INTEGER, factorCtx2);
                        factorType2 = Predefined.integerType;
                    }
                    break;
                case "and":
                    // Both operands boolean ==> boolean result. Else type mismatch.
                    if (!TypeChecker.isBoolean(factorType1)) {
                        error.flag(TYPE_MUST_BE_BOOLEAN, factorCtx1);
                        factorType2 = Predefined.booleanType;
                    }
                    if (!TypeChecker.isBoolean(factorType2)) {
                        error.flag(TYPE_MUST_BE_BOOLEAN, factorCtx2);
                        factorType2 = Predefined.booleanType;
                    }
                    break;
            }

            factorType1 = factorType2;
        }

        ctx.type_ = factorType1;
        return null;
    }
    '''

    def visitTerm(self, ctx: ToyParser.TermContext):
        count = len(ctx.factor())
        factorCtx1 = ctx.factor()[0]

        # First factor.
        self.visit(factorCtx1)
        factorType1 = factorCtx1.type_

        # Loop over any subsequent factors.
        for i in range(1, count):
            op = ctx.mulOp()[i - 1].getText().lower()
            factorCtx2 = ctx.factor()[1]
            self.visit(factorCtx2)
            factorType2 = factorCtx2.type_

            if op == "*":
                # Both operands integer ==> integer result
                if TypeChecker.areBothInteger(factorType1, factorType2):
                    factorType2 = Predefined.integerType

                # Both real operands ==> real result
                # One real and one integer operand ==> real result
                elif TypeChecker.isAtLeastOneReal(factorType1, factorType2):
                    factorType2 = Predefined.realType

                # Type mismatch.
                else:
                    if not TypeChecker.isIntegerOrReal(factorType1):
                        self.error.flagCtx(Code.TYPE_MUST_BE_NUMERIC, factorCtx1)
                        factorType2 = Predefined.integerType
                    if not TypeChecker.isIntegerOrReal(factorType2):
                        self.error.flagCtx(Code.TYPE_MUST_BE_NUMERIC, factorType2)
                        factorType2 = Predefined.integerType

            elif op == "/":
                # All integer and real operand combinations ==> real result
                if TypeChecker.areBothInteger(factorType1, factorType2) or TypeChecker.isAtLeastOneReal(factorType1,
                                                                                                        factorType2):
                    factorType2 = Predefined.realType

                # Type mismatch.
                else:
                    if not TypeChecker.isIntegerOrReal(factorType1):
                        self.error.flagCtx(Code.TYPE_MUST_BE_NUMERIC, factorCtx1)
                        factorType2 = Predefined.integerType
                    if not TypeChecker.isIntegerOrReal(factorType2):
                        self.error.flagCtx(Code.TYPE_MUST_BE_NUMERIC, factorType2)
                        factorType2 = Predefined.integerType

            elif op == "div" or op == "mod":
                # Both operands integer ==> integer result. Else type mismatch.
                if not TypeChecker.isInteger(factorType1):
                    self.error.flagCtx(Code.TYPE_MUST_BE_INTEGER, factorCtx1)
                    factorType2 = Predefined.integerType
                if not TypeChecker.isInteger(factorType2):
                    self.error.flagCtx(Code.TYPE_MUST_BE_INTEGER, factorType2)
                    factorType2 = Predefined.integerType

            elif op == "and":
                # Both operands boolean ==> boolean result. Else type mismatch.
                if not TypeChecker.isBoolean(factorType1):
                    self.error.flagCtx(Code.TYPE_MUST_BE_BOOLEAN, factorCtx1)
                    factorType2 = Predefined.booleanType
                if not TypeChecker.isBoolean(factorType2):
                    self.error.flagCtx(Code.TYPE_MUST_BE_BOOLEAN, factorType2)
                    factorType2 = Predefined.booleanType

            factorType1 = factorType2

        ctx.type_ = factorType1

    '''
    @Override
    public Object visitVariableFactor(ToyParser.VariableFactorContext ctx) {
        ToyParser.VariableContext varCtx = ctx.variable();
        visit(varCtx);
        ctx.type_ = varCtx.type;

        return null;
    }

    @Override
    public Object visitVariable(ToyParser.VariableContext ctx) {
        ToyParser.VariableIdentifierContext varIdCtx = ctx.variableIdentifier();

        visit(varIdCtx);
        ctx.entry = varIdCtx.entry;
        ctx.type_ = variableDatatype(ctx, varIdCtx.type);

        return null;
    }

    @Override
    public Object visitVariableIdentifier(ToyParser.VariableIdentifierContext ctx) {
        String variableName = ctx.IDENTIFIER().getText().toLowerCase();
        SymTableEntry variableId = symTableStack.lookup(variableName);

        if (variableId != null) {
            int lineNumber = ctx.getStart().getLine();
            ctx.type_ = variableId.getType();
            ctx.entry = variableId;
            variableId.appendLineNumber(lineNumber);

            Kind kind = variableId.getKind();
            switch (kind) {
                case TYPE, PROGRAM, PROGRAM_PARAMETER, PROCEDURE, UNDEFINED -> error.flag(INVALID_VARIABLE, ctx);
                default -> {
                }
            }
        } else {
            error.flag(UNDECLARED_IDENTIFIER, ctx);
            ctx.type_ = Predefined.integerType;
        }

        return null;
    }

    /**
     * Determine the datatype of a variable that can have modifiers.
     *
     * @param varCtx  the VariableContext.
     * @param varType the variable's datatype without the modifiers.
     * @return the datatype with any modifiers.
     */
    private Typespec variableDatatype(ToyParser.VariableContext varCtx, Typespec varType) {
        Typespec type = varType;

        // Loop over the modifiers.
        for (ToyParser.ModifierContext modCtx : varCtx.modifier()) {
            // Subscripts.
            if (modCtx.indexList() != null) {
                ToyParser.IndexListContext indexListCtx = modCtx.indexList();

                // Loop over the subscripts.
                for (ToyParser.IndexContext indexCtx : indexListCtx.index()) {
                    if (type.getForm() == ARRAY) {
                        Typespec indexType = type.getArrayIndexType();
                        ToyParser.ExpressionContext exprCtx = indexCtx.expression();
                        visit(exprCtx);

                        if (indexType.baseType() != exprCtx.type.baseType()) {
                            error.flag(TYPE_MISMATCH, exprCtx);
                        }

                        // Datatype of the next dimension.
                        type = type.getArrayElementType();
                    } else {
                        error.flag(TOO_MANY_SUBSCRIPTS, indexCtx);
                    }
                }
            } else  // Record field.
            {
                if (type.getForm() == RECORD) {
                    SymTable symTable = type.getRecordSymTable();
                    ToyParser.FieldContext fieldCtx = modCtx.field();
                    String fieldName = fieldCtx.IDENTIFIER().getText().toLowerCase();
                    SymTableEntry fieldId = symTable.lookup(fieldName);

                    // Field of the record type?
                    if (fieldId != null) {
                        type = fieldId.getType();
                        fieldCtx.entry = fieldId;
                        fieldCtx.type_ = type;
                        fieldId.appendLineNumber(modCtx.getStart().getLine());
                    } else {
                        error.flag(INVALID_FIELD, modCtx);
                    }
                }

                // Not a record variable.
                else {
                    error.flag(INVALID_FIELD, modCtx);
                }
            }
        }

        return type;
    }

    @Override
    public Object visitNumberFactor(ToyParser.NumberFactorContext ctx) {
        ToyParser.NumberContext numberCtx = ctx.number();
        ToyParser.UnsignedNumberContext unsignedCtx = numberCtx.unsignedNumber();
        ToyParser.IntegerConstantContext integerCtx = unsignedCtx.integerConstant();

        ctx.type_ = (integerCtx != null) ? Predefined.integerType : Predefined.realType;

        return null;
    }

    @Override
    public Object visitCharacterFactor(ToyParser.CharacterFactorContext ctx) {
        ctx.type_ = Predefined.charType;
        return null;
    }

    @Override
    public Object visitStringFactor(ToyParser.StringFactorContext ctx) {
        ctx.type_ = Predefined.stringType;
        return null;
    }

    @Override
    public Object visitNotFactor(ToyParser.NotFactorContext ctx) {
        ToyParser.FactorContext factorCtx = ctx.factor();
        visit(factorCtx);

        if (factorCtx.type_ != Predefined.booleanType) {
            error.flag(TYPE_MUST_BE_BOOLEAN, factorCtx);
        }

        ctx.type_ = Predefined.booleanType;
        return null;
    }

    @Override
    public Object visitParenthesizedFactor(ToyParser.ParenthesizedFactorContext ctx) {
        ToyParser.ExpressionContext exprCtx = ctx.expression();
        visit(exprCtx);
        ctx.type_ = exprCtx.type;

        return null;
    }
    }
    '''

    def visitVariableFactor(self, ctx):
        varCtx = ctx.variable()
        self.visit(varCtx)
        ctx.type_ = varCtx.type_

    def visitVariable(self, ctx):
        varIdCtx = ctx.variableIdentifier()

        self.visit(varIdCtx)
        ctx.entry = varIdCtx.entry
        ctx.type_ = self.variableDatatype(ctx, varIdCtx.type_)
        return None

    def visitVariableIdentifier(self, ctx):
        variableName = ctx.IDENTIFIER().getText().lower()
        variableId = self.symTableStack.lookup(variableName)

        if variableId is not None:
            lineNumber = ctx.start.line
            ctx.type_ = variableId.getType()
            ctx.entry = variableId
            variableId.appendLineNumber(lineNumber)

            kind = variableId.getKind()
            if kind in [Kind.TYPE, Kind.CLASS, Kind.PROGRAM_PARAMETER, Kind.PROCEDURE, Kind.UNDEFINED]:
                self.error.flagCtx(Code.INVALID_VARIABLE, ctx)
        else:
            self.error.flagCtx(Code.UNDECLARED_IDENTIFIER, ctx)
            ctx.type_ = Predefined.integerType
        return None

    def variableDatatype(self, varCtx, varType):
        type = varType
        if type is not None and type.getForm() == Form.ITERATOR:
            return type
        for modCtx in varCtx.modifier():
            if modCtx.indexList() is not None:  # Subscripts
                indexListCtx = modCtx.indexList()
                for indexCtx in indexListCtx.index():
                    if type.getForm() == Form.ARRAY:
                        indexType = type.getArrayIndexType()
                        exprCtx = indexCtx.expression()
                        self.visit(exprCtx)
                        if indexType.baseType() != exprCtx.type_.baseType():
                            self.error.flagCtx(Code.TYPE_MISMATCH, exprCtx)
                        type = type.getArrayElementType()
                    else:
                        self.error.flagCtx(Code.TOO_MANY_SUBSCRIPTS, indexCtx)
            else:  # Record field
                if type.getForm() == Form.RECORD:
                    symTable = type.getRecordSymTable()
                    fieldCtx = modCtx.field()
                    fieldName = fieldCtx.IDENTIFIER().getText().lower()
                    fieldId = symTable.lookup(fieldName)
                    if fieldId is not None:
                        type = fieldId.getType()
                        fieldCtx.entry = fieldId
                        fieldCtx.type_ = type
                        fieldId.appendLineNumber(modCtx.start.line)
                    else:
                        self.error.flagCtx(Code.INVALID_FIELD, modCtx)
                else:
                    self.error.flagCtx(Code.INVALID_FIELD, modCtx)
        return type

    def visitNumberFactor(self, ctx):
        numberCtx = ctx.number()
        unsignedCtx = numberCtx.unsignedNumber()
        integerCtx = unsignedCtx.integerConstant()

        ctx.type_ = Predefined.integerType if integerCtx is not None else Predefined.realType

    def visitBooleanFactor(self, ctx:ToyParser.BooleanFactorContext):
        ctx.type_ = Predefined.booleanType
    def visitCharacterFactor(self, ctx):
        ctx.type_ = Predefined.charType

    def visitStringFactor(self, ctx):
        ctx.type_ = Predefined.stringType

    def visitNotFactor(self, ctx):
        factorCtx = ctx.factor()
        self.visit(factorCtx)
        if factorCtx.type_ != Predefined.booleanType:
            self.error.flagCtx(Code.TYPE_MUST_BE_BOOLEAN, factorCtx)

        ctx.type_ = Predefined.booleanType

    def visitParenthesizedFactor(self, ctx):
        exprCtx = ctx.expression()
        self.visit(exprCtx)
        ctx.type_ = exprCtx.type_
