from backend.compiler.CodeGenerator import CodeGenerator
from backend.compiler.Instruction import Instruction
from backend.compiler.Label import Label
from intermediate.symtable.Predefined import Predefined
from intermediate.symtable.SymTableEntry import SymTableEntry
from intermediate.symtable.Kind import Kind
from intermediate.type.Typespec import Form


class StructuredDataGenerator(CodeGenerator):
    def __init__(self, parent, compiler):
        super().__init__(parent=parent, compiler=compiler)

    def emitData(self, routineId):
        symtab = routineId.getRoutineSymtable()
        ids = symtab.sortedEntries()

        # Loop over all the symbol table's identifiers to emit
        # data allocation code for array and record variables.
        for id in ids:
            if id.getKind() == Kind.VARIABLE:
                type = id.getType()
                form = type.getForm()

                if form == Form.ARRAY:
                    self.emitAllocateArray(id, type)
                elif form == Form.RECORD:
                    self.emitAllocateRecord(id, type, 'DUP'.__str__())

    def emitAllocateArray(self, targetId, arrayType):
        elmtType = arrayType
        dimensionCount = 0

        # Count the dimensions and emit a load constant of each element count.
        self.emitLine()
        doWhile = True
        while elmtType.getForm() == Form.ARRAY or doWhile:
            doWhile = False
            elmtCount = elmtType.getArrayElementCount()
            dimensionCount += 1
            self.emitLoadConstant(elmtCount)
            elmtType = elmtType.getArrayElementType()

        # The array element type.
        elmtType = elmtType.baseType()
        elmtForm = elmtType.getForm()
        typeName = None
        if elmtType == Predefined.integerType:
            typeName = "int"
        elif elmtType == Predefined.realType:
            typeName = "float"
        elif elmtType == Predefined.booleanType:
            typeName = "boolean"
        elif elmtType == Predefined.charType:
            typeName = "char"
        elif elmtType == Predefined.stringType:
            typeName = "java/lang/String"
        elif elmtForm == Form.ENUMERATION:
            typeName = "int"
        elif elmtForm == Form.RECORD:
            typeName = elmtType.getIdentifier().getName()

        # One-dimensional array.
        if dimensionCount == 1:
            if elmtForm == Form.RECORD:
                self.emitInstructionOp('ANEWARRAY'.__str__(), elmtType.getRecordTypePath())
                self.emitInstruction('DUP'.__str__())
            elif elmtType == Predefined.stringType:
                self.emitInstructionOp(Instruction.instructions.get('ANEWARRAY'), typeName)
            else:
                self.emitInstructionOp('NEWARRAY'.__str__(), typeName)

        else:
            self.emitInstructionOp2('MULTIANEWARRAY', self.typeDescriptorT(targetId.getType()), str(dimensionCount))
            self.localStack.decrease(dimensionCount-1)
            if elmtForm == Form.RECORD:
                self.emitInstruction('DUP')

        self.emitStoreValue(targetId, targetId.getType())

        if elmtForm == Form.RECORD:
            self.emitAllocateArrayElements(targetId, targetId.getType(), 1, dimensionCount)
            self.emitInstruction('POP')

    def emitAllocateArrayElements(self, targetId, elmtType, dimensionIndex, dimensionCount):
        count = elmtType.getArrayElementCount()
        tempIndex = self.localVariables.reserve()
        loopStartLabel = Label()
        loopExitLabel = Label()

        self.emitLoadConstant(0)
        self.emitStoreLocal(Predefined.integerType, tempIndex)

        self.emitLabel(loopStartLabel)
        self.emitLoadLocal(Predefined.integerType, tempIndex)
        self.emitLoadConstant(count)
        self.emitInstructionLabel('IF_ICMPGE', loopExitLabel)
        self.emitLine()
        self.emitInstruction('DUP')

        form = elmtType.getArrayElementType().getForm()

        # Allocate data for the next array dimension.
        if form == Form.ARRAY:
            self.emitLoadLocal(Predefined.integerType, tempIndex)
            self.emitInstruction('AALOAD')
            self.emitAllocateArrayElements(targetId, elmtType.getArrayElementType(), dimensionIndex+1, dimensionCount)

        elif form == Form.RECORD:
            self.emitLoadLocal(Predefined.integerType, tempIndex)
            self.emitAllocateRecord(None, elmtType.getArrayElementType(), 'DUP_X2')

        # Bottom of the loop:
        # If it's not the last dimension, pop off the copy of the record.
        if dimensionIndex != dimensionCount:
            self.emitInstruction('POP')

        # Increment the temporary variable.
        self.emitInstructionOp2('IINC', tempIndex, 1)
        self.emitInstructionLabel('GOTO', loopStartLabel)
        self.emitLabel(loopExitLabel)

        self.localVariables.release(tempIndex)

    def emitAllocateRecord(self, variableId: SymTableEntry, recordType, dup):
        self.emitInstructionOp('NEW', recordType.getRecordTypePath())
        self.emitInstruction('DUP')
        self.emitInstructionOp('INVOKESPECIAL', recordType.getRecordTypePath() + "/<init>()V")
        self.localStack.decrease(1)

        hasStructuredField = False
        for fieldId in recordType.getRecordSymTable().sortedEntries():
            if fieldId.getKind() == Kind.RECORD_FIELD:
                if fieldId.getType().isStructured():
                    hasStructuredField = True
                    break

        # Duplicate the record address to use to initialize structured fields:
        if hasStructuredField:
            self.emitInstruction('DUP')
        if variableId != None:
            self.emitStoreValue(variableId, variableId.getType())
        else:
            self.emitStoreValue(None, None)

        if hasStructuredField:
            for fieldId in recordType.getRecordSymTable().sortedEntries():
                if fieldId.getKind() == Kind.RECORD_FIELD:
                    fieldType = fieldId.getType()
                    if fieldType.getForm() == Form.ARRAY:
                        self.emitInstruction('DUP')
                        self.emitAllocateArray(fieldId, fieldType)
                    elif fieldType.getForm() == Form.RECORD:
                        self.emitInstruction('DUP')
                        self.emitAllocateRecord(fieldId, fieldType, 'DUP_X2')
            self.emitInstruction('POP')