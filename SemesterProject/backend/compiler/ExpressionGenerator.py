from antlr.ToyParser import ToyParser
from backend.compiler.CodeGenerator import CodeGenerator
from backend.compiler.Label import Label
from intermediate.symtable.Predefined import Predefined
from intermediate.type.Typespec import Form


class ExpressionGenerator(CodeGenerator):
    def __init__(self, parent, compiler):
        super().__init__(parent=parent, compiler=compiler)

    def emitExpression(self, ctx):
        simpleCtx1 = ctx.simpleExpression()[0]
        relOpCtx = ctx.relOp()
        type1 = simpleCtx1.type_
        self.emitSimpleExpression(simpleCtx1)

        if relOpCtx is not None:
            op = relOpCtx.getText()
            simpleCtx2 = ctx.simpleExpression()[1]
            type2 = simpleCtx2.type_

            integerMode = False
            realMode = False
            charMode = False

            if type1 == Predefined.integerType and type2 == Predefined.integerType:
                integerMode = True
            elif type1 == Predefined.realType or type2 == Predefined.realType:
                realMode = True
            elif type1 == Predefined.charType and type2 == Predefined.charType:
                charMode = True

            trueLabel = Label()
            exitLabel = Label()

            if integerMode or charMode:
                self.emitSimpleExpression(simpleCtx2)

                match op:
                    case "==": self.emitInstructionLabel('IF_ICMPEQ', trueLabel)
                    case "<>": self.emitInstructionLabel('IF_ICMPNE', trueLabel)
                    case "<": self.emitInstructionLabel('IF_ICMPLT', trueLabel)
                    case "<=": self.emitInstructionLabel('IF_ICMPLE', trueLabel)
                    case ">": self.emitInstructionLabel('IF_ICMPGT', trueLabel)
                    case ">=": self.emitInstructionLabel('IF_ICMPGE', trueLabel)

            elif realMode:
                if type1 == Predefined.integerType:
                    self.emitInstruction('I2F')
                self.emitSimpleExpression(simpleCtx2)
                if type2 == Predefined.integerType:
                    self.emitInstruction('I2F')

                self.emitInstruction('FCMPG')

                match op:
                    case "==": self.emitInstructionLabel('IFEQ', trueLabel)
                    case "<>": self.emitInstructionLabel('IFNE', trueLabel)
                    case "<": self.emitInstructionLabel('IFLT', trueLabel)
                    case "<=": self.emitInstructionLabel('IFLE', trueLabel)
                    case ">": self.emitInstructionLabel('IFGT', trueLabel)
                    case ">=": self.emitInstructionLabel('IFGE', trueLabel)

            else:
                self.emitSimpleExpression(simpleCtx2)
                self.emitInstructionOp('INVOKEVIRTUAL', "java/lang/String.compareTo(Ljava/lang/String;)I")
                self.localStack.decrease(1)

                match op:
                    case "==": self.emitInstructionLabel('IFEQ', trueLabel)
                    case "<>": self.emitInstructionLabel('IFNE', trueLabel)
                    case "<": self.emitInstructionLabel('IFLT', trueLabel)
                    case "<=": self.emitInstructionLabel('IFLE', trueLabel)
                    case ">": self.emitInstructionLabel('IFGT', trueLabel)
                    case ">=": self.emitInstructionLabel('IFGE', trueLabel)

            self.emitInstruction('ICONST_0')
            self.emitInstructionLabel('GOTO', exitLabel)
            self.emitLabel(trueLabel)
            self.emitInstruction('ICONST_1')
            self.emitLabel(exitLabel)
            self.localStack.decrease(1)

    def emitSimpleExpression(self, ctx):
        count = len(ctx.term())
        negate = ctx.sign() is not None and ctx.sign().getText() == '-'

        termCtx1 = ctx.term()[0]
        type1 = termCtx1.type_
        self.emitTerm(termCtx1)

        if negate:
            self.emitInstruction('INEG' if type1 == Predefined.integerType else 'FNEG')

        for i in range(1, count):
            op = ctx.addOp()[i-1].getText().lower()
            termCtx2 = ctx.term()[i]
            type2 = termCtx2.type_

            integerMode = False
            realMode = False
            booleanMode = False

            if type1 == Predefined.integerType and type2 == Predefined.integerType:
                integerMode = True
            elif type1 == Predefined.realType or type2 == Predefined.realType:
                realMode = True
            elif type1 == Predefined.booleanType and type2 == Predefined.booleanType:
                booleanMode = True

            if integerMode:
                self.emitTerm(termCtx2)
                if op == '+':
                    self.emitInstruction('IADD')
                elif op == '-':
                    self.emitInstruction('ISUB')
            elif realMode:
                if type1 == Predefined.integerType:
                    self.emitInstruction('I2F')
                self.emitTerm(termCtx2)
                if type2 == Predefined.integerType:
                    self.emitInstruction('I2F')

                if op == '+':
                    self.emitInstruction('FADD')
                elif op == '-':
                    self.emitInstruction('FSUB')
            elif booleanMode:
                self.emitTerm(termCtx2)
                self.emitInstruction('IOR') #not sure
            else:
                self.emitInstructionOp('NEW', "java/lang/StringBuilder")
                self.emitInstruction('DUP_X1')
                self.emitInstruction('SWAP')
                self.emitInstructionOp('INVOKESTATIC', "java/lang/String/valueOf(Ljava/lang/Object;)" + "Ljava/lang/String;")
                self.emitInstructionOp('INVOKESPECIAL',"java/lang/StringBuilder/<init>" +
                                    "(Ljava/lang/String;)V" )
                self.localStack.decrease(1)
                self.emitTerm(termCtx2)
                self.emitInstructionOp('INVOKEVIRTUAL', "java/lang/StringBuilder/append(Ljava/lang/String;)" +
                     "Ljava/lang/StringBuilder;")
                self.localStack.decrease(1)
                self.emitInstructionOp('INVOKEVIRTUAL', "java/lang/StringBuilder/toString()" +
                        "Ljava/lang/String;")
                self.localStack.decrease(1)

    def emitTerm(self, ctx):
        count = len(ctx.factor())
        # First factor.
        factorCtx1 = ctx.factor()[0]
        type1 = factorCtx1.type_
        self.compiler.visit(factorCtx1)

        # Loop over the subsequent factors.
        for i in range(1, count):
            op = ctx.mulOp()[i-1].getText().lower()
            factorCtx2 = ctx.factor()[i]
            type2 = factorCtx2.type_

            integerMode = False
            realMode = False

            if type1 == Predefined.integerType and type2 == Predefined.integerType:
                integerMode = True
            elif type1 == Predefined.realType or type2 == Predefined.realType:
                realMode = True

            if integerMode:
                self.compiler.emitFactor(factorCtx2)
                match op:
                    case "*": self.emitInstruction('IMUL')
                    case "/": self.emitInstruction('FDIV')
                    case 'div': self.emitInstruction('IDIV')
                    case 'mod': self.emitInstruction('IREM')
            elif realMode:
                if type1 == Predefined.integerType:
                    self.emitInstruction('I2F')
                self.compiler.visit(factorCtx2)
                if type2 == Predefined.integerType:
                    self.emitInstruction('I2F')

                if op == '*':
                    self.emitInstruction('FMUL')
                elif op == '/':
                    self.emitInstruction('FDIV')
            else:
                self.compiler.visit(factorCtx2)
                self.emitInstruction('IAND')

    def emitNotFactor(self, ctx):
        self.compiler.visit(ctx.factor())
        self.emitInstruction('ICONST_1')
        self.emitInstruction('IXOR')

    def emitLoadValueCtx(self, varCtx: ToyParser.VariableContext):
        variableType = self.emitLoadVariable(varCtx)

        modifierCount = len(varCtx.modifier())
        if modifierCount > 0:
            lastModCtx = varCtx.modifier()[modifierCount - 1]

            if lastModCtx.indexList() is not None:
                self.emitLoadArrayElementValue(variableType)
            else:
                self.emitLoadRecordFieldValue(lastModCtx.field(), variableType)

    def emitLoadVariable(self, varCtx):
        variableId = varCtx.entry
        variableType = variableId.getType()
        modifierCount = len(varCtx.modifier())

        # Scalar value or structure address.
        self.emitLoadValue(variableId)

        # Loop over subscript and field modifiers.
        for i in range(modifierCount):
            modCtx = varCtx.modifier()[i]
            lastModifier = i == modifierCount - 1

            # Subscript
            if modCtx.indexList() is not None:
                variableType = self.emitLoadArrayElementAccess(
                                modCtx.indexList(), variableType, lastModifier)

            # Field
            elif not lastModifier:
                variableType = self.emitLoadRecordField(modCtx.field(), variableType)

        return variableType

    def emitLoadArrayElementAccess(self, indexListCtx, elmtType, lastModifier):
        indexCount = len(indexListCtx.index())

        # Loop over the subscripts.
        for i in range(indexCount):
            indexCtx = indexListCtx.index()[i]
            self.emitExpression(indexCtx.expression())

            indexType = elmtType.getArrayIndexType()

            #TODO check if this is correct
            if indexType.getForm() == Form.SUBRANGE:
                min = indexType.getSubrangeMinValue()
                if min != 0:
                    self.emitLoadConstant(min)
                    self.emitInstruction('ISUB')

            if not lastModifier or (i < indexCount - 1):
                self.emitInstruction('AALOAD')
            elmtType = elmtType.getArrayElementType()

        return elmtType

    def emitLoadArrayElementValue(self, elmtType):
        form = Form.SCALAR

        if elmtType is not None:
            elmtType = elmtType.baseType()
            form = elmtType.getForm()

        # Load a character from a string.
        if elmtType == Predefined.charType:
            #self.emitInstructionOp('INVOKEVIRTUAL', "java/lang/StringBuilder.charAt(I)C")
            self.emitInstruction('CALOAD')

        # Load an array element.
        else:
            match elmtType:
                case Predefined.integerType: self.emitInstruction('IALOAD')
                case Predefined.realType: self.emitInstruction('FALOAD')
                case Predefined.booleanType: self.emitInstruction('BALOAD')
                case _:
                    if form == Form.ENUMERATION:
                        self.emitInstruction('IALOAD')
                    else:
                        self.emitInstruction('AALOAD')

    def emitLoadRecordFieldValue(self, fieldCtx, recordType):
        self.emitLoadRecordField(fieldCtx, recordType)
    def emitLoadRecordField(self, fieldCtx, recordType):
        fieldId = fieldCtx.entry
        fieldName = fieldId.getName()
        fieldType = recordType.type_

        recordTypePath = recordType.getRecordTypePath()
        fieldPath = recordTypePath + '/' + fieldName
        self.emitInstructionOp2('GETFIELD', fieldPath, self.typeDescriptorT(fieldType))

        return fieldType

    def emitLoadIntegerConstant(self, intCtx):
        value = int(intCtx.getText())
        self.emitLoadConstant(value)

    def emitLoadRealConstant(self, realCtx):
        value = float(realCtx.getText())
        self.emitLoadConstant(value)
