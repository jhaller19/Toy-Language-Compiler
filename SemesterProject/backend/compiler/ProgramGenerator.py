from antlr.ToyParser import ToyParser
from backend.compiler.CodeGenerator import *
#from backend.Compiler import Compiler
from backend.compiler.Directive import Directive
from backend.compiler.LocalStack import LocalStack
from backend.compiler.LocalVariable import LocalVariables
from backend.compiler.StructuredDataGenerator import StructuredDataGenerator
from intermediate.symtable.Kind import Kind


class ProgramGenerator(CodeGenerator):
    def __init__(self, parent, compiler):
        super().__init__(parent=parent, compiler=compiler)
        self.programLocalsCount = 0
        self.programId = None
        self.localStack = LocalStack()

    def emitProgram(self, ctx: ToyParser.ClassStartContext):
        self.programId = ctx.classHeader().classIdentifier().entry
        programSymTable = self.programId.getRoutineSymtable()

        self.localVariables = LocalVariables(self.programLocalsCount)

        self.emitRecords(programSymTable)

        self.emitDirectiveOp(Directive.CLASS_PUBLIC, self.programName)
        self.emitDirectiveOp(Directive.SUPER, "java/lang/Object")

        self.emitProgramVariables()
        self.emitInputScanner()
        self.emitConstructor()
        self.emitSubroutines(ctx.classLevelBlock().declarations().routinesPart())

        self.emitMainMethod(ctx)

    def emitRecords(self, symtab):
        from backend.compiler.Compiler import Compiler
        for id in symtab.sortedEntries():
            if id.getKind() == Kind.TYPE and id.getType().getForm() == Form.RECORD:
                try:
                    Compiler(id, self.compiler.getOutputPath())
                except IOError as e:
                    raise RuntimeError(e)

    def emitRecord(self, recordId, namePath):
        recordSymtab = recordId.getType().getRecordSymTab()

        self.emitDirectiveOp(Directive.CLASS_PUBLIC, namePath)
        self.emitDirectiveOp(Directive.SUPER, "java/lang/Object")
        self.emitLine()

        self.emitRecords(recordSymtab)

        for id in recordSymtab.sortedEntries():
            if id.getKind() == Kind.RECORD_FIELD:
                self.emitDirectiveOp2(Directive.FIELD, id.getName(), self.typeDescriptorS(id))

        self.emitConstructor()
        self.close()

    def emitProgramVariables(self):
        symTable = self.programId.getRoutineSymtable()
        ids = symTable.sortedEntries()

        self.emitLine()
        self.emitDirectiveOp2(Directive.FIELD_PRIVATE_STATIC, "_sysin", "Ljava/util/Scanner;")

        for id in ids:
            if id.getKind() == Kind.VARIABLE:
                self.emitDirectiveOp2(Directive.FIELD_PRIVATE_STATIC, id.getName(), self.typeDescriptorS(id))

    def emitInputScanner(self):
        self.emitLine()
        self.emitComment("Runtime input scanner")
        self.emitDirectiveOp(Directive.METHOD_STATIC, "<clinit>()V")
        self.emitLine()
        self.emitInstructionOp('NEW', "java/util/Scanner")
        self.emitInstruction('DUP')
        self.emitInstructionOp('GETSTATIC', "java/lang/System/in Ljava/io/InputStream;")
        self.emitInstructionOp('INVOKESPECIAL', "java/util/Scanner/<init>(Ljava/io/InputStream;)V")
        self.emitInstructionOp('PUTSTATIC', self.programName + "/_sysin Ljava/util/Scanner;")
        self.emitInstruction('RETURN')

        self.emitLine()
        self.emitDirectiveOp(Directive.LIMIT_LOCALS, 0)
        self.emitDirectiveOp(Directive.LIMIT_STACK, 3)
        self.emitDirective(Directive.END_METHOD)

        self.localStack.reset()

    def emitConstructor(self):
        self.emitLine()
        self.emitComment("Main class constructor")
        self.emitDirectiveOp(Directive.METHOD_PUBLIC, "<init>()V")
        self.emitDirectiveOp(Directive.VAR, "0 is this L" + self.programName + ";")
        self.emitLine()

        self.emitInstruction('ALOAD_0')
        self.emitInstructionOp('INVOKESPECIAL', "java/lang/Object/<init>()V")
        self.emitInstruction('RETURN')

        self.emitLine()
        self.emitDirectiveOp(Directive.LIMIT_LOCALS, 1)
        self.emitDirectiveOp(Directive.LIMIT_STACK, 1)
        self.emitDirective(Directive.END_METHOD)

        self.localStack.reset()

    def emitSubroutines(self, ctx):
        from backend.compiler.Compiler import Compiler
        if ctx is not None:
            for defnCtx in ctx.routineDefinition():
                Compiler(self.compiler).visit(defnCtx)

    def emitMainMethod(self, ctx: ToyParser.ClassStartContext):
        self.emitLine()
        self.emitComment("MAIN")
        self.emitDirectiveOp(Directive.METHOD_PUBLIC_STATIC, "main([Ljava/lang/String;)V")

        self.emitMainPrologue(self.programName)

        structuredCode = StructuredDataGenerator(self, self.compiler)
        structuredCode.emitData(self.programId)

        self.emitLine()
        self.compiler.visit(ctx.classLevelBlock().mainProcedure())

        self.emitMainEpilogue()

    def emitMainPrologue(self, programId):
        self.emitDirectiveOp(Directive.VAR, "0 is args [Ljava/lang/String;")

    def emitMainEpilogue(self):
        self.emitLine()
        self.emitInstruction('RETURN')
        self.emitLine()

        self.emitDirectiveOp(Directive.LIMIT_LOCALS, self.localVariables.count())
        self.emitDirectiveOp(Directive.LIMIT_STACK, self.localStack.capacity())
        self.emitDirective(Directive.END_METHOD)

        self.close()

    def emitRoutine(self, ctx: ToyParser.RoutineDefinitionContext):
        routineId = ctx.procedureHead().routineIdentifier().entry if ctx.procedureHead() is not None else ctx.functionHead().routineIdentifier().entry
        routineSymTable = routineId.getRoutineSymTable()

        self.emitRoutineHeader(routineId)
        self.emitRoutineLocals(routineId)

        structuredCode = StructuredDataGenerator(self, self.compiler)
        structuredCode.emitData(routineId)

        self.localVariables = LocalVariables(routineSymTable.getMaxSlotNumber())

        stmtCtx = ctx.compoundStatement()
        self.compiler.visit(stmtCtx)

        self.emitRoutineReturn(routineId)
        self.emitRoutineEmpilogue()

    def emitRoutineHeader(self, routineId):
        routineName = routineId.getName()
        parmIds = routineId.getRoutineParameters()
        buffer = ''

        # Procedure or function name.
        buffer += routineName
        buffer += "("

        # Parameter and return type descriptors.
        if parmIds is not None:
            for parmId in parmIds:
                buffer += (self.typeDescriptorS(parmId))
        buffer += ")"
        buffer += self.typeDescriptorS(routineId)

        self.emitLine()
        if routineId.getKind() == Kind.PROCEDURE:
            self.emitComment("PROCEDURE " + routineName)
        else:
            self.emitComment("FUNCTION " + routineName)

        self.emitDirectiveOp(Directive.METHOD_PRIVATE_STATIC, buffer)

    def emitRoutineLocals(self, routineId):
        symTable = routineId.getRoutineSymTable()
        ids = symTable.sortedEntries()

        self.emitLine()

        for id in ids:
            kind = id.getKind()

            if kind == Kind.VARIABLE or kind == Kind.VALUE_PARAMETER or kind == Kind.REFERENCE_PARAMETER:
                slot = id.getSlotNumber()
                self.emitDirectiveOp2(Directive.VAR, slot + " is " + id.getName(), self.typeDescriptorS(id))

    def emitRoutineReturn(self, routineId : SymTableEntry):
        self.emitLine()

        if routineId.getKind() == Kind.FUNCTION:
            type = routineId.getType()

            varName = routineId.getName()
            varId = routineId.getRoutineSymtable().lookup(varName)
            self.emitLoadLocal(type, varId.getSlotNumber())
            self.emitReturnValue(type)

        else:
            self.emitInstruction('RETURN')

    def emitRoutineEpilogue(self):
        self.emitLine()
        self.emitDirectiveOp(Directive.LIMIT_LOCALS, self.localVariables.count())
        self.emitDirectiveOp(Directive.LIMIT_STACK, self.localStack.capacity())
        self.emitDirectiveOp(Directive.END_METHOD)
