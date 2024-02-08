# Generated from Toy.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ToyParser import ToyParser
else:
    from ToyParser import ToyParser



# This class defines a complete listener for a parse tree produced by ToyParser.
class ToyListener(ParseTreeListener):

    # Enter a parse tree produced by ToyParser#classStart.
    def enterClassStart(self, ctx:ToyParser.ClassStartContext):
        pass

    # Exit a parse tree produced by ToyParser#classStart.
    def exitClassStart(self, ctx:ToyParser.ClassStartContext):
        pass


    # Enter a parse tree produced by ToyParser#classHeader.
    def enterClassHeader(self, ctx:ToyParser.ClassHeaderContext):
        pass

    # Exit a parse tree produced by ToyParser#classHeader.
    def exitClassHeader(self, ctx:ToyParser.ClassHeaderContext):
        pass


    # Enter a parse tree produced by ToyParser#classLevelBlock.
    def enterClassLevelBlock(self, ctx:ToyParser.ClassLevelBlockContext):
        pass

    # Exit a parse tree produced by ToyParser#classLevelBlock.
    def exitClassLevelBlock(self, ctx:ToyParser.ClassLevelBlockContext):
        pass


    # Enter a parse tree produced by ToyParser#classIdentifier.
    def enterClassIdentifier(self, ctx:ToyParser.ClassIdentifierContext):
        pass

    # Exit a parse tree produced by ToyParser#classIdentifier.
    def exitClassIdentifier(self, ctx:ToyParser.ClassIdentifierContext):
        pass


    # Enter a parse tree produced by ToyParser#block.
    def enterBlock(self, ctx:ToyParser.BlockContext):
        pass

    # Exit a parse tree produced by ToyParser#block.
    def exitBlock(self, ctx:ToyParser.BlockContext):
        pass


    # Enter a parse tree produced by ToyParser#declarations.
    def enterDeclarations(self, ctx:ToyParser.DeclarationsContext):
        pass

    # Exit a parse tree produced by ToyParser#declarations.
    def exitDeclarations(self, ctx:ToyParser.DeclarationsContext):
        pass


    # Enter a parse tree produced by ToyParser#constantsPart.
    def enterConstantsPart(self, ctx:ToyParser.ConstantsPartContext):
        pass

    # Exit a parse tree produced by ToyParser#constantsPart.
    def exitConstantsPart(self, ctx:ToyParser.ConstantsPartContext):
        pass


    # Enter a parse tree produced by ToyParser#constantDefinitionsList.
    def enterConstantDefinitionsList(self, ctx:ToyParser.ConstantDefinitionsListContext):
        pass

    # Exit a parse tree produced by ToyParser#constantDefinitionsList.
    def exitConstantDefinitionsList(self, ctx:ToyParser.ConstantDefinitionsListContext):
        pass


    # Enter a parse tree produced by ToyParser#constantDefinition.
    def enterConstantDefinition(self, ctx:ToyParser.ConstantDefinitionContext):
        pass

    # Exit a parse tree produced by ToyParser#constantDefinition.
    def exitConstantDefinition(self, ctx:ToyParser.ConstantDefinitionContext):
        pass


    # Enter a parse tree produced by ToyParser#constantIdentifier.
    def enterConstantIdentifier(self, ctx:ToyParser.ConstantIdentifierContext):
        pass

    # Exit a parse tree produced by ToyParser#constantIdentifier.
    def exitConstantIdentifier(self, ctx:ToyParser.ConstantIdentifierContext):
        pass


    # Enter a parse tree produced by ToyParser#constant.
    def enterConstant(self, ctx:ToyParser.ConstantContext):
        pass

    # Exit a parse tree produced by ToyParser#constant.
    def exitConstant(self, ctx:ToyParser.ConstantContext):
        pass


    # Enter a parse tree produced by ToyParser#sign.
    def enterSign(self, ctx:ToyParser.SignContext):
        pass

    # Exit a parse tree produced by ToyParser#sign.
    def exitSign(self, ctx:ToyParser.SignContext):
        pass


    # Enter a parse tree produced by ToyParser#typesPart.
    def enterTypesPart(self, ctx:ToyParser.TypesPartContext):
        pass

    # Exit a parse tree produced by ToyParser#typesPart.
    def exitTypesPart(self, ctx:ToyParser.TypesPartContext):
        pass


    # Enter a parse tree produced by ToyParser#typeDefinitionsList.
    def enterTypeDefinitionsList(self, ctx:ToyParser.TypeDefinitionsListContext):
        pass

    # Exit a parse tree produced by ToyParser#typeDefinitionsList.
    def exitTypeDefinitionsList(self, ctx:ToyParser.TypeDefinitionsListContext):
        pass


    # Enter a parse tree produced by ToyParser#typeDefinition.
    def enterTypeDefinition(self, ctx:ToyParser.TypeDefinitionContext):
        pass

    # Exit a parse tree produced by ToyParser#typeDefinition.
    def exitTypeDefinition(self, ctx:ToyParser.TypeDefinitionContext):
        pass


    # Enter a parse tree produced by ToyParser#typeIdentifier.
    def enterTypeIdentifier(self, ctx:ToyParser.TypeIdentifierContext):
        pass

    # Exit a parse tree produced by ToyParser#typeIdentifier.
    def exitTypeIdentifier(self, ctx:ToyParser.TypeIdentifierContext):
        pass


    # Enter a parse tree produced by ToyParser#simpleTypespec.
    def enterSimpleTypespec(self, ctx:ToyParser.SimpleTypespecContext):
        pass

    # Exit a parse tree produced by ToyParser#simpleTypespec.
    def exitSimpleTypespec(self, ctx:ToyParser.SimpleTypespecContext):
        pass


    # Enter a parse tree produced by ToyParser#iteratorTypespec.
    def enterIteratorTypespec(self, ctx:ToyParser.IteratorTypespecContext):
        pass

    # Exit a parse tree produced by ToyParser#iteratorTypespec.
    def exitIteratorTypespec(self, ctx:ToyParser.IteratorTypespecContext):
        pass


    # Enter a parse tree produced by ToyParser#arrayTypespec.
    def enterArrayTypespec(self, ctx:ToyParser.ArrayTypespecContext):
        pass

    # Exit a parse tree produced by ToyParser#arrayTypespec.
    def exitArrayTypespec(self, ctx:ToyParser.ArrayTypespecContext):
        pass


    # Enter a parse tree produced by ToyParser#recordTypespec.
    def enterRecordTypespec(self, ctx:ToyParser.RecordTypespecContext):
        pass

    # Exit a parse tree produced by ToyParser#recordTypespec.
    def exitRecordTypespec(self, ctx:ToyParser.RecordTypespecContext):
        pass


    # Enter a parse tree produced by ToyParser#iteratorType.
    def enterIteratorType(self, ctx:ToyParser.IteratorTypeContext):
        pass

    # Exit a parse tree produced by ToyParser#iteratorType.
    def exitIteratorType(self, ctx:ToyParser.IteratorTypeContext):
        pass


    # Enter a parse tree produced by ToyParser#typeIdentifierTypespec.
    def enterTypeIdentifierTypespec(self, ctx:ToyParser.TypeIdentifierTypespecContext):
        pass

    # Exit a parse tree produced by ToyParser#typeIdentifierTypespec.
    def exitTypeIdentifierTypespec(self, ctx:ToyParser.TypeIdentifierTypespecContext):
        pass


    # Enter a parse tree produced by ToyParser#arrayType.
    def enterArrayType(self, ctx:ToyParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by ToyParser#arrayType.
    def exitArrayType(self, ctx:ToyParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by ToyParser#arrayDimensionList.
    def enterArrayDimensionList(self, ctx:ToyParser.ArrayDimensionListContext):
        pass

    # Exit a parse tree produced by ToyParser#arrayDimensionList.
    def exitArrayDimensionList(self, ctx:ToyParser.ArrayDimensionListContext):
        pass


    # Enter a parse tree produced by ToyParser#recordType.
    def enterRecordType(self, ctx:ToyParser.RecordTypeContext):
        pass

    # Exit a parse tree produced by ToyParser#recordType.
    def exitRecordType(self, ctx:ToyParser.RecordTypeContext):
        pass


    # Enter a parse tree produced by ToyParser#recordFields.
    def enterRecordFields(self, ctx:ToyParser.RecordFieldsContext):
        pass

    # Exit a parse tree produced by ToyParser#recordFields.
    def exitRecordFields(self, ctx:ToyParser.RecordFieldsContext):
        pass


    # Enter a parse tree produced by ToyParser#variablesPart.
    def enterVariablesPart(self, ctx:ToyParser.VariablesPartContext):
        pass

    # Exit a parse tree produced by ToyParser#variablesPart.
    def exitVariablesPart(self, ctx:ToyParser.VariablesPartContext):
        pass


    # Enter a parse tree produced by ToyParser#variableDeclarationsList.
    def enterVariableDeclarationsList(self, ctx:ToyParser.VariableDeclarationsListContext):
        pass

    # Exit a parse tree produced by ToyParser#variableDeclarationsList.
    def exitVariableDeclarationsList(self, ctx:ToyParser.VariableDeclarationsListContext):
        pass


    # Enter a parse tree produced by ToyParser#variableDeclarations.
    def enterVariableDeclarations(self, ctx:ToyParser.VariableDeclarationsContext):
        pass

    # Exit a parse tree produced by ToyParser#variableDeclarations.
    def exitVariableDeclarations(self, ctx:ToyParser.VariableDeclarationsContext):
        pass


    # Enter a parse tree produced by ToyParser#variableIdentifierList.
    def enterVariableIdentifierList(self, ctx:ToyParser.VariableIdentifierListContext):
        pass

    # Exit a parse tree produced by ToyParser#variableIdentifierList.
    def exitVariableIdentifierList(self, ctx:ToyParser.VariableIdentifierListContext):
        pass


    # Enter a parse tree produced by ToyParser#variableIdentifier.
    def enterVariableIdentifier(self, ctx:ToyParser.VariableIdentifierContext):
        pass

    # Exit a parse tree produced by ToyParser#variableIdentifier.
    def exitVariableIdentifier(self, ctx:ToyParser.VariableIdentifierContext):
        pass


    # Enter a parse tree produced by ToyParser#routinesPart.
    def enterRoutinesPart(self, ctx:ToyParser.RoutinesPartContext):
        pass

    # Exit a parse tree produced by ToyParser#routinesPart.
    def exitRoutinesPart(self, ctx:ToyParser.RoutinesPartContext):
        pass


    # Enter a parse tree produced by ToyParser#routineDefinition.
    def enterRoutineDefinition(self, ctx:ToyParser.RoutineDefinitionContext):
        pass

    # Exit a parse tree produced by ToyParser#routineDefinition.
    def exitRoutineDefinition(self, ctx:ToyParser.RoutineDefinitionContext):
        pass


    # Enter a parse tree produced by ToyParser#procedureHead.
    def enterProcedureHead(self, ctx:ToyParser.ProcedureHeadContext):
        pass

    # Exit a parse tree produced by ToyParser#procedureHead.
    def exitProcedureHead(self, ctx:ToyParser.ProcedureHeadContext):
        pass


    # Enter a parse tree produced by ToyParser#functionHead.
    def enterFunctionHead(self, ctx:ToyParser.FunctionHeadContext):
        pass

    # Exit a parse tree produced by ToyParser#functionHead.
    def exitFunctionHead(self, ctx:ToyParser.FunctionHeadContext):
        pass


    # Enter a parse tree produced by ToyParser#routineIdentifier.
    def enterRoutineIdentifier(self, ctx:ToyParser.RoutineIdentifierContext):
        pass

    # Exit a parse tree produced by ToyParser#routineIdentifier.
    def exitRoutineIdentifier(self, ctx:ToyParser.RoutineIdentifierContext):
        pass


    # Enter a parse tree produced by ToyParser#parameters.
    def enterParameters(self, ctx:ToyParser.ParametersContext):
        pass

    # Exit a parse tree produced by ToyParser#parameters.
    def exitParameters(self, ctx:ToyParser.ParametersContext):
        pass


    # Enter a parse tree produced by ToyParser#parameterDeclarationsList.
    def enterParameterDeclarationsList(self, ctx:ToyParser.ParameterDeclarationsListContext):
        pass

    # Exit a parse tree produced by ToyParser#parameterDeclarationsList.
    def exitParameterDeclarationsList(self, ctx:ToyParser.ParameterDeclarationsListContext):
        pass


    # Enter a parse tree produced by ToyParser#parameterDeclarations.
    def enterParameterDeclarations(self, ctx:ToyParser.ParameterDeclarationsContext):
        pass

    # Exit a parse tree produced by ToyParser#parameterDeclarations.
    def exitParameterDeclarations(self, ctx:ToyParser.ParameterDeclarationsContext):
        pass


    # Enter a parse tree produced by ToyParser#parameterIdentifierList.
    def enterParameterIdentifierList(self, ctx:ToyParser.ParameterIdentifierListContext):
        pass

    # Exit a parse tree produced by ToyParser#parameterIdentifierList.
    def exitParameterIdentifierList(self, ctx:ToyParser.ParameterIdentifierListContext):
        pass


    # Enter a parse tree produced by ToyParser#parameterIdentifier.
    def enterParameterIdentifier(self, ctx:ToyParser.ParameterIdentifierContext):
        pass

    # Exit a parse tree produced by ToyParser#parameterIdentifier.
    def exitParameterIdentifier(self, ctx:ToyParser.ParameterIdentifierContext):
        pass


    # Enter a parse tree produced by ToyParser#statement.
    def enterStatement(self, ctx:ToyParser.StatementContext):
        pass

    # Exit a parse tree produced by ToyParser#statement.
    def exitStatement(self, ctx:ToyParser.StatementContext):
        pass


    # Enter a parse tree produced by ToyParser#hasNextStatement.
    def enterHasNextStatement(self, ctx:ToyParser.HasNextStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#hasNextStatement.
    def exitHasNextStatement(self, ctx:ToyParser.HasNextStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#nextStatement.
    def enterNextStatement(self, ctx:ToyParser.NextStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#nextStatement.
    def exitNextStatement(self, ctx:ToyParser.NextStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#readStatement.
    def enterReadStatement(self, ctx:ToyParser.ReadStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#readStatement.
    def exitReadStatement(self, ctx:ToyParser.ReadStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#printfStatement.
    def enterPrintfStatement(self, ctx:ToyParser.PrintfStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#printfStatement.
    def exitPrintfStatement(self, ctx:ToyParser.PrintfStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#compoundStatement.
    def enterCompoundStatement(self, ctx:ToyParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#compoundStatement.
    def exitCompoundStatement(self, ctx:ToyParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#mainProcedure.
    def enterMainProcedure(self, ctx:ToyParser.MainProcedureContext):
        pass

    # Exit a parse tree produced by ToyParser#mainProcedure.
    def exitMainProcedure(self, ctx:ToyParser.MainProcedureContext):
        pass


    # Enter a parse tree produced by ToyParser#emptyStatement.
    def enterEmptyStatement(self, ctx:ToyParser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#emptyStatement.
    def exitEmptyStatement(self, ctx:ToyParser.EmptyStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#statementList.
    def enterStatementList(self, ctx:ToyParser.StatementListContext):
        pass

    # Exit a parse tree produced by ToyParser#statementList.
    def exitStatementList(self, ctx:ToyParser.StatementListContext):
        pass


    # Enter a parse tree produced by ToyParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:ToyParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:ToyParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#lhs.
    def enterLhs(self, ctx:ToyParser.LhsContext):
        pass

    # Exit a parse tree produced by ToyParser#lhs.
    def exitLhs(self, ctx:ToyParser.LhsContext):
        pass


    # Enter a parse tree produced by ToyParser#rhs.
    def enterRhs(self, ctx:ToyParser.RhsContext):
        pass

    # Exit a parse tree produced by ToyParser#rhs.
    def exitRhs(self, ctx:ToyParser.RhsContext):
        pass


    # Enter a parse tree produced by ToyParser#ifStatement.
    def enterIfStatement(self, ctx:ToyParser.IfStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#ifStatement.
    def exitIfStatement(self, ctx:ToyParser.IfStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#trueStatement.
    def enterTrueStatement(self, ctx:ToyParser.TrueStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#trueStatement.
    def exitTrueStatement(self, ctx:ToyParser.TrueStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#falseStatement.
    def enterFalseStatement(self, ctx:ToyParser.FalseStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#falseStatement.
    def exitFalseStatement(self, ctx:ToyParser.FalseStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#whileStatement.
    def enterWhileStatement(self, ctx:ToyParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#whileStatement.
    def exitWhileStatement(self, ctx:ToyParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#procedureCallStatement.
    def enterProcedureCallStatement(self, ctx:ToyParser.ProcedureCallStatementContext):
        pass

    # Exit a parse tree produced by ToyParser#procedureCallStatement.
    def exitProcedureCallStatement(self, ctx:ToyParser.ProcedureCallStatementContext):
        pass


    # Enter a parse tree produced by ToyParser#procedureName.
    def enterProcedureName(self, ctx:ToyParser.ProcedureNameContext):
        pass

    # Exit a parse tree produced by ToyParser#procedureName.
    def exitProcedureName(self, ctx:ToyParser.ProcedureNameContext):
        pass


    # Enter a parse tree produced by ToyParser#argumentList.
    def enterArgumentList(self, ctx:ToyParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by ToyParser#argumentList.
    def exitArgumentList(self, ctx:ToyParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by ToyParser#argument.
    def enterArgument(self, ctx:ToyParser.ArgumentContext):
        pass

    # Exit a parse tree produced by ToyParser#argument.
    def exitArgument(self, ctx:ToyParser.ArgumentContext):
        pass


    # Enter a parse tree produced by ToyParser#expression.
    def enterExpression(self, ctx:ToyParser.ExpressionContext):
        pass

    # Exit a parse tree produced by ToyParser#expression.
    def exitExpression(self, ctx:ToyParser.ExpressionContext):
        pass


    # Enter a parse tree produced by ToyParser#simpleExpression.
    def enterSimpleExpression(self, ctx:ToyParser.SimpleExpressionContext):
        pass

    # Exit a parse tree produced by ToyParser#simpleExpression.
    def exitSimpleExpression(self, ctx:ToyParser.SimpleExpressionContext):
        pass


    # Enter a parse tree produced by ToyParser#term.
    def enterTerm(self, ctx:ToyParser.TermContext):
        pass

    # Exit a parse tree produced by ToyParser#term.
    def exitTerm(self, ctx:ToyParser.TermContext):
        pass


    # Enter a parse tree produced by ToyParser#variableFactor.
    def enterVariableFactor(self, ctx:ToyParser.VariableFactorContext):
        pass

    # Exit a parse tree produced by ToyParser#variableFactor.
    def exitVariableFactor(self, ctx:ToyParser.VariableFactorContext):
        pass


    # Enter a parse tree produced by ToyParser#numberFactor.
    def enterNumberFactor(self, ctx:ToyParser.NumberFactorContext):
        pass

    # Exit a parse tree produced by ToyParser#numberFactor.
    def exitNumberFactor(self, ctx:ToyParser.NumberFactorContext):
        pass


    # Enter a parse tree produced by ToyParser#characterFactor.
    def enterCharacterFactor(self, ctx:ToyParser.CharacterFactorContext):
        pass

    # Exit a parse tree produced by ToyParser#characterFactor.
    def exitCharacterFactor(self, ctx:ToyParser.CharacterFactorContext):
        pass


    # Enter a parse tree produced by ToyParser#stringFactor.
    def enterStringFactor(self, ctx:ToyParser.StringFactorContext):
        pass

    # Exit a parse tree produced by ToyParser#stringFactor.
    def exitStringFactor(self, ctx:ToyParser.StringFactorContext):
        pass


    # Enter a parse tree produced by ToyParser#booleanFactor.
    def enterBooleanFactor(self, ctx:ToyParser.BooleanFactorContext):
        pass

    # Exit a parse tree produced by ToyParser#booleanFactor.
    def exitBooleanFactor(self, ctx:ToyParser.BooleanFactorContext):
        pass


    # Enter a parse tree produced by ToyParser#functionCallFactor.
    def enterFunctionCallFactor(self, ctx:ToyParser.FunctionCallFactorContext):
        pass

    # Exit a parse tree produced by ToyParser#functionCallFactor.
    def exitFunctionCallFactor(self, ctx:ToyParser.FunctionCallFactorContext):
        pass


    # Enter a parse tree produced by ToyParser#getArgCallFactor.
    def enterGetArgCallFactor(self, ctx:ToyParser.GetArgCallFactorContext):
        pass

    # Exit a parse tree produced by ToyParser#getArgCallFactor.
    def exitGetArgCallFactor(self, ctx:ToyParser.GetArgCallFactorContext):
        pass


    # Enter a parse tree produced by ToyParser#notFactor.
    def enterNotFactor(self, ctx:ToyParser.NotFactorContext):
        pass

    # Exit a parse tree produced by ToyParser#notFactor.
    def exitNotFactor(self, ctx:ToyParser.NotFactorContext):
        pass


    # Enter a parse tree produced by ToyParser#parenthesizedFactor.
    def enterParenthesizedFactor(self, ctx:ToyParser.ParenthesizedFactorContext):
        pass

    # Exit a parse tree produced by ToyParser#parenthesizedFactor.
    def exitParenthesizedFactor(self, ctx:ToyParser.ParenthesizedFactorContext):
        pass


    # Enter a parse tree produced by ToyParser#getArgCall.
    def enterGetArgCall(self, ctx:ToyParser.GetArgCallContext):
        pass

    # Exit a parse tree produced by ToyParser#getArgCall.
    def exitGetArgCall(self, ctx:ToyParser.GetArgCallContext):
        pass


    # Enter a parse tree produced by ToyParser#booleanConstant.
    def enterBooleanConstant(self, ctx:ToyParser.BooleanConstantContext):
        pass

    # Exit a parse tree produced by ToyParser#booleanConstant.
    def exitBooleanConstant(self, ctx:ToyParser.BooleanConstantContext):
        pass


    # Enter a parse tree produced by ToyParser#variable.
    def enterVariable(self, ctx:ToyParser.VariableContext):
        pass

    # Exit a parse tree produced by ToyParser#variable.
    def exitVariable(self, ctx:ToyParser.VariableContext):
        pass


    # Enter a parse tree produced by ToyParser#modifier.
    def enterModifier(self, ctx:ToyParser.ModifierContext):
        pass

    # Exit a parse tree produced by ToyParser#modifier.
    def exitModifier(self, ctx:ToyParser.ModifierContext):
        pass


    # Enter a parse tree produced by ToyParser#indexList.
    def enterIndexList(self, ctx:ToyParser.IndexListContext):
        pass

    # Exit a parse tree produced by ToyParser#indexList.
    def exitIndexList(self, ctx:ToyParser.IndexListContext):
        pass


    # Enter a parse tree produced by ToyParser#index.
    def enterIndex(self, ctx:ToyParser.IndexContext):
        pass

    # Exit a parse tree produced by ToyParser#index.
    def exitIndex(self, ctx:ToyParser.IndexContext):
        pass


    # Enter a parse tree produced by ToyParser#field.
    def enterField(self, ctx:ToyParser.FieldContext):
        pass

    # Exit a parse tree produced by ToyParser#field.
    def exitField(self, ctx:ToyParser.FieldContext):
        pass


    # Enter a parse tree produced by ToyParser#functionCall.
    def enterFunctionCall(self, ctx:ToyParser.FunctionCallContext):
        pass

    # Exit a parse tree produced by ToyParser#functionCall.
    def exitFunctionCall(self, ctx:ToyParser.FunctionCallContext):
        pass


    # Enter a parse tree produced by ToyParser#functionName.
    def enterFunctionName(self, ctx:ToyParser.FunctionNameContext):
        pass

    # Exit a parse tree produced by ToyParser#functionName.
    def exitFunctionName(self, ctx:ToyParser.FunctionNameContext):
        pass


    # Enter a parse tree produced by ToyParser#number.
    def enterNumber(self, ctx:ToyParser.NumberContext):
        pass

    # Exit a parse tree produced by ToyParser#number.
    def exitNumber(self, ctx:ToyParser.NumberContext):
        pass


    # Enter a parse tree produced by ToyParser#unsignedNumber.
    def enterUnsignedNumber(self, ctx:ToyParser.UnsignedNumberContext):
        pass

    # Exit a parse tree produced by ToyParser#unsignedNumber.
    def exitUnsignedNumber(self, ctx:ToyParser.UnsignedNumberContext):
        pass


    # Enter a parse tree produced by ToyParser#integerConstant.
    def enterIntegerConstant(self, ctx:ToyParser.IntegerConstantContext):
        pass

    # Exit a parse tree produced by ToyParser#integerConstant.
    def exitIntegerConstant(self, ctx:ToyParser.IntegerConstantContext):
        pass


    # Enter a parse tree produced by ToyParser#realConstant.
    def enterRealConstant(self, ctx:ToyParser.RealConstantContext):
        pass

    # Exit a parse tree produced by ToyParser#realConstant.
    def exitRealConstant(self, ctx:ToyParser.RealConstantContext):
        pass


    # Enter a parse tree produced by ToyParser#characterConstant.
    def enterCharacterConstant(self, ctx:ToyParser.CharacterConstantContext):
        pass

    # Exit a parse tree produced by ToyParser#characterConstant.
    def exitCharacterConstant(self, ctx:ToyParser.CharacterConstantContext):
        pass


    # Enter a parse tree produced by ToyParser#stringConstant.
    def enterStringConstant(self, ctx:ToyParser.StringConstantContext):
        pass

    # Exit a parse tree produced by ToyParser#stringConstant.
    def exitStringConstant(self, ctx:ToyParser.StringConstantContext):
        pass


    # Enter a parse tree produced by ToyParser#relOp.
    def enterRelOp(self, ctx:ToyParser.RelOpContext):
        pass

    # Exit a parse tree produced by ToyParser#relOp.
    def exitRelOp(self, ctx:ToyParser.RelOpContext):
        pass


    # Enter a parse tree produced by ToyParser#addOp.
    def enterAddOp(self, ctx:ToyParser.AddOpContext):
        pass

    # Exit a parse tree produced by ToyParser#addOp.
    def exitAddOp(self, ctx:ToyParser.AddOpContext):
        pass


    # Enter a parse tree produced by ToyParser#mulOp.
    def enterMulOp(self, ctx:ToyParser.MulOpContext):
        pass

    # Exit a parse tree produced by ToyParser#mulOp.
    def exitMulOp(self, ctx:ToyParser.MulOpContext):
        pass



del ToyParser