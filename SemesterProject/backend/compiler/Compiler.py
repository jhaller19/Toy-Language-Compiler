from antlr.ToyParser import ToyParser
from antlr.ToyVisitor import ToyVisitor
from backend.compiler.CodeGenerator import CodeGenerator
from backend.compiler.ExpressionGenerator import ExpressionGenerator
from backend.compiler.ProgramGenerator import ProgramGenerator
from backend.compiler.StatementGenerator import StatementGenerator
from intermediate.symtable.Predefined import Predefined


class Compiler(ToyVisitor):

    def __init__(self, programName=None, outputPath=None, parent=None, recordId=None):
        self.expressionCode = None
        self.statementCode = None
        if programName is not None:
            self.programName = programName
        if outputPath is not None:
            self.outputPath = outputPath
        if parent is not None:
            self.outputPath = None
            self.code = parent.code
            self.programCode = parent.programCode
            self.programName = parent.programName
        else:
            self.code = CodeGenerator(programName=programName, compiler=self)
        if recordId is not None:
            recordTypePath = recordId.getType().getRecordTypePath()
            self.createNewGenerators(self.code)
            self.programCode.emitRecord(recordId, recordTypePath)

    def createNewGenerators(self, parentGenerator):
        self.programCode = ProgramGenerator(parentGenerator, self)
        self.statementCode = StatementGenerator(self.programCode, self)
        self.expressionCode = ExpressionGenerator(self.programCode, self)

    def getObjectFileName(self):
        return self.code.getObjectFileName()

    def getOutputPath(self):
        return self.outputPath

    def visitClassStart(self, ctx: ToyParser.ClassStartContext):
        self.createNewGenerators(self.code)
        self.programCode.emitProgram(ctx)
        return None

    def visitRoutineDefinition(self, ctx: ToyParser.RoutineDefinitionContext):
        self.createNewGenerators(self.code)
        self.programCode.emitRoutine(ctx)
        return None

    def visitStatement(self, ctx: ToyParser.StatementContext):
        if ctx.compoundStatement() is None and ctx.emptyStatement() is None:
            self.statementCode.emitCommentCtx(ctx)

        return self.visitChildren(ctx)

    def visitAssignmentStatement(self, ctx: ToyParser.AssignmentStatementContext):
        self.statementCode.emitAssignment(ctx)
        return None

    def visitIfStatement(self, ctx: ToyParser.IfStatementContext):
        self.statementCode.emitIf(ctx)
        return None

    def visitWhileStatement(self, ctx: ToyParser.WhileStatementContext):
        self.statementCode.emitWhile(ctx)
        return None

    def visitProcedureCallStatement(self, ctx: ToyParser.ProcedureCallStatementContext):
        self.statementCode.emitProcedureCall(ctx)
        return None

    def visitExpression(self, ctx: ToyParser.ExpressionContext):
        self.expressionCode.emitExpression(ctx)
        return None

    def visitVariableFactor(self, ctx: ToyParser.VariableFactorContext):
        self.expressionCode.emitLoadValueCtx(ctx.variable())
        return None

    def visitVariable(self, ctx: ToyParser.VariableContext):
        self.expressionCode.emitLoadVariable(ctx)
        return None

    def visitNumberFactor(self, ctx: ToyParser.NumberFactorContext):
        if ctx.type_ == Predefined.integerType:
            self.expressionCode.emitLoadIntegerConstant(ctx.number())
        else:
            self.expressionCode.emitLoadRealConstant(ctx.number())

        return None

    def visitCharacterFactor(self, ctx: ToyParser.CharacterFactorContext):
        self.expressionCode.emitLoadConstant(ctx.getText()[1])
        return None

    def visitStringFactor(self, ctx: ToyParser.StringFactorContext):
        jasminString = self.convertString(ctx.getText())
        self.expressionCode.emitLoadConstant(jasminString)
        return None

    def convertString(self, pascalString):
        unquoted = pascalString[1:-1]
        return unquoted.replace("''", "'").replace("\"", "\\\"")

    def visitFunctionCallFactor(self, ctx: ToyParser.FunctionCallFactorContext):
        self.statementCode.emitFunctionCall(ctx.functionCall())
        return None

    def visitNotFactor(self, ctx: ToyParser.NotFactorContext):
        self.expressionCode.emitNotFactor(ctx)
        return None

    def visitParenthesizedFactor(self, ctx: ToyParser.ParenthesizedFactorContext):
        return self.visit(ctx.expression())

    def visitPrintfStatement(self, ctx: ToyParser.PrintfStatementContext):
        self.statementCode.emitPrintf(ctx)
        return None

    def visitReadStatement(self, ctx: ToyParser.ReadStatementContext):
        self.statementCode.emitRead(ctx)
        return None
