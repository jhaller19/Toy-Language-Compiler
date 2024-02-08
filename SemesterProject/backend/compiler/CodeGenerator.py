from backend.compiler.Instruction import Instruction
from intermediate.symtable.Predefined import Predefined
from intermediate.symtable.SymTableEntry import SymTableEntry
from intermediate.symtable.Kind import Kind
from intermediate.type.Typespec import Typespec, Form


class CodeGenerator:
    SUFFIX = '.j'
    count = 0

    def __init__(self, programName=None, compiler=None, parent=None):
        if parent is not None:
            self.compiler = compiler
            self.objectFile = parent.objectFile
            self.objectFileName = parent.objectFileName
            self.programName = parent.programName
            self.localVariables = parent.localVariables
            self.localStack = parent.localStack
        else:
            self.programName = programName
            self.localVariables = None
            self.localStack = None
            self.compiler = compiler
            self.objectFileName = str(programName) + self.SUFFIX

            # Create the Jasmin object file. NOT SURE
            self.objectFile = open(self.objectFileName, 'w')

    def getObjectFileName(self):
        return self.objectFileName

    def close(self):
        self.objectFile.close()

    def getLocalVariables(self):
        return self.localVariables

    def getLocalStack(self):
        return self.localStack

    def emitLine(self):
        self.objectFile.write('\n')
        self.objectFile.flush()

    def emitComment(self, text):
        self.objectFile.write(';\n')
        self.objectFile.write(';' + text + '\n')
        self.objectFile.write(';\n')
        self.objectFile.flush()

    def emitCommentCtx(self, ctx):
        text = str(ctx.start.line) + ' ' + ctx.getText()  # not sure

        if len(text) <= 72:
            self.emitComment(text)
        else:
            self.emitComment(text[:72] + ' ...')

    def emitLabel(self, label):
        self.objectFile.write(label.__str__() + ':\n')
        self.objectFile.flush()

    def emitLabelInt(self, value: int, label):
        self.objectFile.write('\t' + str(value) + ': ' + label + '\n')
        self.objectFile.flush()

    def emitLabelString(self, value, label):
        self.objectFile.write('\t' + str(value) + ': ' + label + '\n')
        self.objectFile.flush()

    def emitDirective(self, directive):
        self.objectFile.write(directive.value + '\n')
        self.objectFile.flush()
        CodeGenerator.count += 1

    def emitDirectiveOp(self, directive, operand):
        self.objectFile.write(directive.value + ' ' + str(operand) + '\n')
        self.objectFile.flush()
        CodeGenerator.count += 1

    def emitDirectiveOpInt(self, directive, operand: int):
        self.objectFile.write(directive.value + ' ' + str(operand) + '\n')
        self.objectFile.flush()
        CodeGenerator.count += 1

    def emitDirectiveOp2(self, directive, operand1, operand2):
        self.objectFile.write(directive.value + ' ' + str(operand1) + ' ' + str(operand2) + '\n')
        self.objectFile.flush()
        CodeGenerator.count += 1

    def emitDirectiveOp3(self, directive, operand1, operand2, operand3):
        self.objectFile.write(directive.value + ' ' + str(operand1) + ' ' + str(operand2) + ' ' + operand3 + '\n')
        self.objectFile.write(directive.value + ' ' + str(operand1) + ' ' + str(operand2) + ' ' + operand3 + '\n')
        self.objectFile.write(directive.value + ' ' + str(operand1) + ' ' + str(operand2) + ' ' + operand3 + '\n')
        self.objectFile.flush()
        CodeGenerator.count += 1

    def emitInstruction(self, instruction):
        instruction = instruction.lower()
        self.objectFile.write('\t' + instruction + '\n')
        self.objectFile.flush()
        self.localStack.increase(Instruction.instructions.get(instruction))
        CodeGenerator.count += 1

    def emitInstructionOp(self, instruction, operand):
        instruction = instruction.lower()
        self.objectFile.write('\t' + instruction + ' ' + str(operand) + '\n')
        self.objectFile.flush()
        self.localStack.increase(Instruction.instructions.get(instruction))
        CodeGenerator.count += 1

    '''
    def emitIntructionOpInt(self, instruction, operand: int):
        self.objectFile.write('\t' + instruction + ' ' + str(operand) + '\n')
        self.objectFile.flush()
        self.localStack.increase('stackUse')
        CodeGenerator.count += 1

    def emitInstructionOpFloat(self, instruction, operand: float):
        self.objectFile.write('\t' + instruction + ' ' + str(operand) + '\n')
        self.objectFile.flush()
        self.localStack.increase('stackUse')
        CodeGenerator.count += 1
    '''

    def emitInstructionLabel(self, instruction, label):
        instruction = instruction.lower()
        self.objectFile.write('\t' + instruction + '\t' + label.__str__() + '\n')
        self.objectFile.flush()
        self.localStack.increase(Instruction.instructions.get(instruction))
        CodeGenerator.count += 1

    def emitInstructionOp2(self, instruction, operand1, operand2):
        instruction = instruction.lower()
        self.objectFile.write('\t' + instruction + '\t' + str(operand1) + ' ' + str(operand2) + '\n')
        self.objectFile.flush()
        self.localStack.increase(Instruction.instructions.get(instruction))
        CodeGenerator.count += 1

    def emitLoadConstant(self, value):
        if type(value) != str:
            if value == 0:
                self.emitInstruction('ICONST_0')
            elif value == 1:
                self.emitInstruction('ICONST_1')
            elif value == 2:
                self.emitInstruction('ICONST_2')
            elif value == 3:
                self.emitInstruction('ICONST_3')
            elif value == 4:
                self.emitInstruction('ICONST_4')
            elif value == 5:
                self.emitInstruction('ICONST_5')
            elif value == -1:
                self.emitInstruction('ICONST_M1')
            elif -128 <= value <= 127:
                self.emitInstructionOp('BIPUSH', value)
            elif -32768 <= value <= 32767:
                self.emitInstructionOp('SIPUSH', value)
            else:
                self.emitInstructionOp('LDC', value)
        else:
            if ord(value) == 0:
                self.emitInstruction('ICONST_0')
            elif ord(value) == 1:
                self.emitInstruction('ICONST_1')
            elif ord(value) == 2:
                self.emitInstruction('ICONST_2')
            elif ord(value) == 3:
                self.emitInstruction('ICONST_3')
            elif ord(value) == 4:
                self.emitInstruction('ICONST_4')
            elif ord(value) == 5:
                self.emitInstruction('ICONST_5')
            elif ord(value) == -1:
                self.emitInstruction('ICONST_M1')
            elif -128 <= ord(value) <= 127:
                self.emitInstructionOp('BIPUSH', ord(value))
            elif -32768 <= ord(value) <= 32767:
                self.emitInstructionOp('SIPUSH', ord(value))
            else:
                self.emitInstructionOp('LDC', value)


    def emitLoadConstantFloat(self, value: float):
        if value == 0.0:
            self.emitInstruction('FCONST_0')
        elif value == 1.0:
            self.emitInstruction('FCONST_1')
        elif value == 2.0:
            self.emitInstruction('FCONST_2')
        else:
            self.emitInstructionOp('LDC', value)

    def emitLoadConstantString(self, value: str):
        self.emitInstructionOp('LDC', '"' + value + '"')

    def emitLoadValue(self, variableId: SymTableEntry):
        type = variableId.getType().baseType()
        kind = variableId.getKind()
        nestingLevel = variableId.getSymtable().getNestingLevel()

        # Constant
        if kind == Kind.CONSTANT:
            value = variableId.getValue()

            if type == Predefined.integerType:
                self.emitLoadConstant(value)
            elif type == Predefined.realType:
                self.emitLoadConstant(value)
            elif type == Predefined.charType:
                ch = value
                self.emitLoadConstant(ch)
            else:
                self.emitLoadConstant(value)

        # Enumeration constant
        elif kind == Kind.ENUMERATION_CONSTANT:
            value = variableId.getValue()
            self.emitLoadConstant(value)

        elif nestingLevel == 1:
            variableName = variableId.getName()
            name = self.programName + '/' + variableName
            self.emitInstructionOp2('GETSTATIC', name, self.typeDescriptorT(type))

        else:
            slot = variableId.getSlotNumber()
            self.emitLoadLocal(type, slot)

    def emitLoadLocal(self, type, index):
        form = None

        if type != None:
            type = type.baseType()
            form = type.getForm()

        if (type == Predefined.integerType) or (type == Predefined.booleanType) or (type == Predefined.charType) or (
                form == Form.ENUMERATION):
            match index:
                case 0:
                    self.emitInstruction('ILOAD_0')
                case 1:
                    self.emitInstruction('ILOAD_1')
                case 2:
                    self.emitInstruction('ILOAD_2')
                case 3:
                    self.emitInstruction('ILOAD_3')
                case _:
                    self.emitInstructionOp('ILOAD', index)

        elif type == Predefined.realType:
            match index:
                case 0:
                    self.emitInstruction('FLOAD_0')
                case 1:
                    self.emitInstruction('FLOAD_1')
                case 2:
                    self.emitInstruction('FLOAD_2')
                case 3:
                    self.emitInstruction('FLOAD_3')
                case _:
                    self.emitInstructionOp('FLOAD', index)

        else:
            match index:
                case 0:
                    self.emitInstruction('ALOAD_0')
                case 1:
                    self.emitInstruction('ALOAD_1')
                case 2:
                    self.emitInstruction('ALOAD_2')
                case 3:
                    self.emitInstruction('ALOAD_3')
                case _:
                    self.emitInstructionOp('ALOAD', index)

    def emitStoreValue(self, targetId, targetType):
        if targetId is None:
            self.emitStoreToArrayElement(targetType)
        elif targetId.getKind() == Kind.RECORD_FIELD:
            self.emitStoreToRecordField(targetId)
        else:
            self.emitStoreToUnmodifiedVariable(targetId, targetType)

    def emitStoreToUnmodifiedVariable(self, targetId, targetType: Typespec):
        nestingLevel = targetId.getSymtable().getNestingLevel()
        slot = targetId.getSlotNumber()

        if nestingLevel == 1:
            targetName = targetId.getName()
            name = self.programName + '/' + targetName
            self.emitRangeCheck(targetType)
            self.emitInstructionOp2('PUTSTATIC', name, self.typeDescriptorT(targetType.baseType()))
        else:
            self.emitRangeCheck(targetType)
            self.emitStoreLocal(targetType.baseType(), slot)

    def emitStoreLocal(self, type, slot):
        form = None

        if type != None:
            type = type.baseType()
            form = type.getForm()

        if (type == Predefined.integerType) or (type == Predefined.booleanType) or (type == Predefined.charType) or (
                form == Form.ENUMERATION):
            match slot:
                case 0:
                    self.emitInstruction('ISTORE_0')
                case 1:
                    self.emitInstruction('ISTORE_1')
                case 2:
                    self.emitInstruction('ISTORE_2')
                case 3:
                    self.emitInstruction('ISTORE_3')
                case _:
                    self.emitInstructionOp('ISTORE', slot)

        elif type == Predefined.realType:
            match slot:
                case 0:
                    self.emitInstruction('FSTORE_0')
                case 1:
                    self.emitInstruction('FSTORE_1')
                case 2:
                    self.emitInstruction('FSTORE_2')
                case 3:
                    self.emitInstruction('FSTORE_3')
                case _:
                    self.emitInstructionOp('FSTORE', slot)

        else:
            match slot:
                case 0:
                    self.emitInstruction('ASTORE_0')
                case 1:
                    self.emitInstruction('ASTORE_1')
                case 2:
                    self.emitInstruction('ASTORE_2')
                case 3:
                    self.emitInstruction('ASTORE_3')
                case _:
                    self.emitInstructionOp('ASTORE', slot)

    def emitStoreToArrayElement(self, elmtType: Typespec):
        form = None

        if elmtType is not None:
            elmtType = elmtType.baseType()
            form = elmtType.getForm()

        self.emitInstruction(
            'IASTORE' if elmtType == Predefined.integerType else 'FASTORE' if elmtType == Predefined.realType else 'BASTORE' if elmtType == Predefined.booleanType else 'CASTORE' if elmtType == Predefined.charType else 'IASTORE' if form == Form.ENUMERATION else 'AASTORE')

    def emitStoreToRecordField(self, fieldId):
        fieldName = fieldId.getName()
        fieldType = fieldId.get_type()
        recordType = fieldId.getSymtable().getOwner().get_type()

        recordTypePath = recordType.getRecordTypePath()
        fieldPath = recordTypePath + '/' + fieldName

        self.emitInstructionOp2('PUTFIELD', fieldPath, self.typeDescriptorT(fieldType))

    def emitCheckCast(self, type: Typespec):
        descriptor = self.typeDescriptorT(type)

        if descriptor[0] != 'L':
            descriptor = descriptor[1:-1]

        self.emitInstructionOp('CHECKCAST', descriptor)

    def emitReturnValue(self, type: Typespec):
        form = None

        if type is not None:
            type = type.baseType()
            form = type.getForm()

        if (type == Predefined.integerType) or (type == Predefined.booleanType) or (type == Predefined.charType) or (
                form == Form.ENUMERATION):
            self.emitInstruction('IRETURN')
        elif type == Predefined.realType:
            self.emitInstruction('FRETURN')
        else:
            self.emitInstruction('ARETURN')

    def emitRangeCheck(self, targetType: Typespec):
        pass

    def typeDescriptorS(self, id: SymTableEntry):
        type: Typespec = id.getType()
        return self.typeDescriptorT(type) if type is not None else 'V'

    def typeDescriptorT(self, type: Typespec):
        form = type.getForm()
        buffer = ''

        while form == Form.ARRAY:
            buffer += '['
            type = type.getArrayElementType()
            form = type.getForm()

        type = type.baseType()
        str = ''

        if type == Predefined.integerType:
            str = 'I'
        elif type == Predefined.realType:
            str = 'F'
        elif type == Predefined.booleanType:
            str = 'Z'
        elif type == Predefined.charType:
            str = 'C'
        elif type == Predefined.stringType:
            str = 'Ljava/lang/String;'
        elif form == Form.ENUMERATION:
            str = 'I'
        else:
            str = 'L' + type.getRecordTypePath() + ';'

        return buffer + str

    def objectTypeName(self, type):
        form = type.getForm()
        buffer = ''
        isArray = False

        while form == Form.ARRAY:
            buffer += '['
            type = type.getArrayElementType()
            form = type.getForm()
            isArray = True

        if isArray:
            buffer += 'L'

        type = type.baseType()
        str = ''

        if type == Predefined.integerType:
            str = 'java/lang/Integer'
        elif type == Predefined.realType:
            str = 'java/lang/Float'
        elif type == Predefined.booleanType:
            str = 'java/lang/Boolean'
        elif type == Predefined.charType:
            str = 'java/lang/Character'
        elif type == Predefined.stringType:
            str = 'Ljava/lang/String;'
        elif form == Form.ENUMERATION:
            str = 'Ljava/lang/Integer;'
        else:
            str = 'L' + type.getRecordTypePath() + ';'

        buffer += str
        if isArray:
            buffer += ';'

        return buffer

    def convertString(self, pascalString):
        unquoted = pascalString[1:-1]
        return unquoted.replace("''", "'").replace("\"", "\\\"")

    def valueOfSignature(self, type):
        javaType = self.objectTypeName(type)
        typeCode = self.typeDescriptorT(type)

        return "%s/valueOf(%s)L%s;" % (javaType, typeCode, javaType)
