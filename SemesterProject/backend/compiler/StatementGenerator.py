from antlr.ToyParser import ToyParser
from backend.compiler.CodeGenerator import CodeGenerator
from backend.compiler.Label import Label
from intermediate.symtable.Predefined import Predefined
from intermediate.symtable.SymTableEntry import SymTableEntry
from intermediate.symtable.Kind import Kind
from intermediate.type.Typespec import Form


def convert(format):
    #replace single quotes with double quotes
    format = format.replace("'", '"')
    return format


class StatementGenerator(CodeGenerator):

    def __init__(self, parent, compiler):
        super().__init__(parent=parent, compiler=compiler)

    def emitAssignment(self, ctx: ToyParser.AssignmentStatementContext):
        varCtx = ctx.lhs().variable()
        exprCtx = ctx.rhs().expression()
        varId = varCtx.entry
        varType = varCtx.type_
        exprType = exprCtx.type_

        # The last modifier, if any, is the variable's last subscript or field.
        modifierCount = len(varCtx.modifier())
        lastModCtx = None
        if modifierCount > 0:
            lastModCtx = varCtx.modifier()[modifierCount - 1]
            self.compiler.visit(varCtx)

        # Emit code to evaluate the expression.
        self.compiler.visit(exprCtx)

        # float variable := integer constant
        if varType == Predefined.realType and exprType.baseType() == Predefined.integerType:
            self.emitInstruction('I2F')

        # Emit code to store the expression value into the target variable.
        # The target variable has no subscripts or fields.
        if lastModCtx is None:
            self.emitStoreValue(varId, varId.getType())

        # The target variable is a field.
        elif lastModCtx.field() is not None:
            self.emitStoreValue(lastModCtx.field().entry, lastModCtx.field().type_)

        # The target variable is an array element.
        else:
            self.emitStoreValue(None, varType)

    def emitIf(self, ctx: ToyParser.IfStatementContext):
        nextLabel = Label()
        self.compiler.visit(ctx.expression())
        if ctx.ELSE() is not None:
            falseLabel = Label()
            self.emitInstructionLabel('IFEQ', falseLabel)
            self.compiler.visit(ctx.trueStatement())
            self.emitInstructionLabel('GOTO', nextLabel)
            self.emitLabel(falseLabel)
            self.compiler.visit(ctx.falseStatement())
            self.emitLabel(nextLabel)
        else:
            self.emitInstructionLabel('IFEQ', nextLabel)
            self.compiler.visit(ctx.trueStatement())
        self.emitLabel(nextLabel)

    def emitWhile(self, ctx: ToyParser.WhileStatementContext):
        loopTopLabel = Label()
        loopExitLabel = Label()

        self.emitLabel(loopTopLabel)

        self.compiler.visit(ctx.expression())
        self.emitInstructionLabel('IFEQ', loopExitLabel)
        self.compiler.visit(ctx.statement())
        self.emitInstructionLabel('GOTO', loopTopLabel)

        self.emitLabel(loopExitLabel)

    def emitProcedureCall(self, ctx: ToyParser.ProcedureCallStatementContext):
        self.emitCall(ctx.procedureName().entry, ctx.argumentList())

    def emitFunctionCall(self, ctx: ToyParser.FunctionCallContext):
        self.emitCall(ctx.functionName().entry, ctx.argumentList())

    def emitCall(self, routineId: SymTableEntry, argListCtx: ToyParser.ArgumentListContext):
        if argListCtx is not None:
            for i in range(routineId.getRoutineParameters().size()):
                argCtx = argListCtx.argument(i)
                self.compiler.visit(argCtx.expression())
                argType = argCtx.expression().type_.getIdentifier().getName()
                paramType = routineId.getRoutineParameters().get(i).getType().getIdentifier().getName()
                # If casting is required.
                if argType == "integer" and paramType == "real":
                    self.emitInstruction('I2F')

        routinePart = routineId.getName() + "("

        for s in routineId.getRoutineParameters():
            type = s.getType().getIdentifier().getName()
            if type == "integer":
                routinePart += "I"
            elif type == "real":
                routinePart += "F"
            elif type == "boolean":
                routinePart += "Z"

        routinePart += ")"

        if routineId.getKind() == Kind.FUNCTION:
            type = routineId.getType().getIdentifier().getName()
            if type == "integer":
                routinePart += "I"
            elif type == "real":
                routinePart += "F"
            elif type == "boolean":
                routinePart += "Z"
        else:
            routinePart += "V"

        # May need to do some casting... for arguments that don't match params.
        self.emitInstructionOp('INVOKESTATIC', self.compiler.programName + "/" + routinePart)

    def emitPrintf(self, ctx: ToyParser.PrintfStatementContext):
        self.emitInstructionOp2('GETSTATIC', "java/lang/System/out", "Ljava/io/PrintStream;")
        argsCtx: ToyParser.ArgumentListContext = ctx.argumentList()
        format = ctx.stringConstant().getText()
        if format is None:
            self.emitInstructionOp('INVOKEVIRTUAL', "java/io/PrintStream.println()V")
            self.localStack.decrease(1)
        else:
            #format = self.compiler.visit(ctx.stringConstant())
            exprCount = 0
            if argsCtx is not None:
                exprCount = len(argsCtx.argument())
            self.emitInstructionOp('LDC', convert(format))
            if exprCount > 0:
                self.emitArgumentsArray(argsCtx, exprCount)
                self.emitInstructionOp('INVOKEVIRTUAL',
                                       "java/io/PrintStream/printf(Ljava/lang/String;[Ljava/lang/Object;)" + "Ljava/io/PrintStream;")
                self.localStack.decrease(2)
                self.emitInstruction('POP')
            else:
                self.emitInstructionOp('INVOKEVIRTUAL', "java/io/PrintStream.print(Ljava/lang/String;)V")
                self.localStack.decrease(2)

    def emitArgumentsArray(self, argsCtx: ToyParser.ArgumentListContext, exprCount: int):
        self.emitLoadConstant(exprCount)
        self.emitInstructionOp('ANEWARRAY', "java/lang/Object")

        index = 0

        for argCtx in argsCtx.argument():
            argText = argCtx.getText()
            exprCtx = argCtx.expression()
            type = exprCtx.type_.baseType()

            if argText[0] != '\'':
                self.emitInstruction('DUP')
                self.emitLoadConstant(index)
                index += 1
                self.compiler.visit(exprCtx)

                form = type.getForm()
                if (form == Form.SCALAR or form == Form.ENUMERATION) and type != Predefined.stringType:
                    self.emitInstructionOp('INVOKESTATIC', self.valueOfSignature(type))

                self.emitInstruction('AASTORE')

    def emitRead(self, argCtx: ToyParser.ReadStatementContext):
        #Char works, have to test others
        varCtx = argCtx.variable()
        varType = varCtx.type_
        if varType == Predefined.integerType:
            self.emitInstructionOp('GETSTATIC', self.programName + "/_sysin Ljava/util/Scanner;")
            self.emitInstructionOp('INVOKEVIRTUAL', "java/util/Scanner/nextInt()I")
            self.emitStoreValue(varCtx.entry, varType)
        elif varType == Predefined.realType:
            self.emitInstructionOp('GETSTATIC', self.programName + "/_sysin Ljava/util/Scanner;")
            self.emitInstructionOp('INVOKEVIRTUAL', "java/util/Scanner/nextFloat()F")
            self.emitStoreValue(varCtx.entry, None)
        elif varType == Predefined.booleanType:
            self.emitInstructionOp('GETSTATIC', self.programName + "/_sysin Ljava/util/Scanner;")
            self.emitInstructionOp('INVOKEVIRTUAL', "java/util/Scanner/nextBoolean()Z")
            self.emitStoreValue(varCtx.entry, None)
        elif varType == Predefined.charType:
            '''
            self.emitInstructionOp('GETSTATIC', self.programName + "/_sysin Ljava/util/Scanner;")
            self.emitInstructionOp('LDC', "\"\"")
            self.emitInstructionOp('INVOKEVIRTUAL', "java/util/Scanner/useDelimiter(Ljava/lang/String;)" + "Ljava/util/Scanner;")
            self.emitInstruction('POP')
            '''
            self.emitInstructionOp('GETSTATIC', self.programName + "/_sysin Ljava/util/Scanner;")
            self.emitInstructionOp('INVOKEVIRTUAL', "java/util/Scanner/next()Ljava/lang/String;")
            self.emitInstruction('ICONST_0')
            self.emitInstructionOp('INVOKEVIRTUAL', "java/lang/String/charAt(I)C")
            self.emitStoreValue(varCtx.entry, varType)
        else:
            self.emitInstructionOp2('GETSTATIC', self.programName + "/_sysin", "Ljava/util/Scanner;")
            self.emitInstructionOp('INVOKEVIRTUAL', "java/util/Scanner/nextLine()Ljava/lang/String;")
            self.emitStoreValue(varCtx.entry, None)
