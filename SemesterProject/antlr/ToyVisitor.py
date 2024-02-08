# Generated from Toy.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ToyParser import ToyParser
else:
    from ToyParser import ToyParser



# This class defines a complete generic visitor for a parse tree produced by ToyParser.

class ToyVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ToyParser#classStart.
    def visitClassStart(self, ctx:ToyParser.ClassStartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#classHeader.
    def visitClassHeader(self, ctx:ToyParser.ClassHeaderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#classLevelBlock.
    def visitClassLevelBlock(self, ctx:ToyParser.ClassLevelBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#classIdentifier.
    def visitClassIdentifier(self, ctx:ToyParser.ClassIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#block.
    def visitBlock(self, ctx:ToyParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#declarations.
    def visitDeclarations(self, ctx:ToyParser.DeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#constantsPart.
    def visitConstantsPart(self, ctx:ToyParser.ConstantsPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#constantDefinitionsList.
    def visitConstantDefinitionsList(self, ctx:ToyParser.ConstantDefinitionsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#constantDefinition.
    def visitConstantDefinition(self, ctx:ToyParser.ConstantDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#constantIdentifier.
    def visitConstantIdentifier(self, ctx:ToyParser.ConstantIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#constant.
    def visitConstant(self, ctx:ToyParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#sign.
    def visitSign(self, ctx:ToyParser.SignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#typesPart.
    def visitTypesPart(self, ctx:ToyParser.TypesPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#typeDefinitionsList.
    def visitTypeDefinitionsList(self, ctx:ToyParser.TypeDefinitionsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#typeDefinition.
    def visitTypeDefinition(self, ctx:ToyParser.TypeDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#typeIdentifier.
    def visitTypeIdentifier(self, ctx:ToyParser.TypeIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#simpleTypespec.
    def visitSimpleTypespec(self, ctx:ToyParser.SimpleTypespecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#iteratorTypespec.
    def visitIteratorTypespec(self, ctx:ToyParser.IteratorTypespecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#arrayTypespec.
    def visitArrayTypespec(self, ctx:ToyParser.ArrayTypespecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#recordTypespec.
    def visitRecordTypespec(self, ctx:ToyParser.RecordTypespecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#iteratorType.
    def visitIteratorType(self, ctx:ToyParser.IteratorTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#typeIdentifierTypespec.
    def visitTypeIdentifierTypespec(self, ctx:ToyParser.TypeIdentifierTypespecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#arrayType.
    def visitArrayType(self, ctx:ToyParser.ArrayTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#arrayDimensionList.
    def visitArrayDimensionList(self, ctx:ToyParser.ArrayDimensionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#recordType.
    def visitRecordType(self, ctx:ToyParser.RecordTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#recordFields.
    def visitRecordFields(self, ctx:ToyParser.RecordFieldsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#variablesPart.
    def visitVariablesPart(self, ctx:ToyParser.VariablesPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#variableDeclarationsList.
    def visitVariableDeclarationsList(self, ctx:ToyParser.VariableDeclarationsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#variableDeclarations.
    def visitVariableDeclarations(self, ctx:ToyParser.VariableDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#variableIdentifierList.
    def visitVariableIdentifierList(self, ctx:ToyParser.VariableIdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#variableIdentifier.
    def visitVariableIdentifier(self, ctx:ToyParser.VariableIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#routinesPart.
    def visitRoutinesPart(self, ctx:ToyParser.RoutinesPartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#routineDefinition.
    def visitRoutineDefinition(self, ctx:ToyParser.RoutineDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#procedureHead.
    def visitProcedureHead(self, ctx:ToyParser.ProcedureHeadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#functionHead.
    def visitFunctionHead(self, ctx:ToyParser.FunctionHeadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#routineIdentifier.
    def visitRoutineIdentifier(self, ctx:ToyParser.RoutineIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#parameters.
    def visitParameters(self, ctx:ToyParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#parameterDeclarationsList.
    def visitParameterDeclarationsList(self, ctx:ToyParser.ParameterDeclarationsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#parameterDeclarations.
    def visitParameterDeclarations(self, ctx:ToyParser.ParameterDeclarationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#parameterIdentifierList.
    def visitParameterIdentifierList(self, ctx:ToyParser.ParameterIdentifierListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#parameterIdentifier.
    def visitParameterIdentifier(self, ctx:ToyParser.ParameterIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#statement.
    def visitStatement(self, ctx:ToyParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#hasNextStatement.
    def visitHasNextStatement(self, ctx:ToyParser.HasNextStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#nextStatement.
    def visitNextStatement(self, ctx:ToyParser.NextStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#readStatement.
    def visitReadStatement(self, ctx:ToyParser.ReadStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#printfStatement.
    def visitPrintfStatement(self, ctx:ToyParser.PrintfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#compoundStatement.
    def visitCompoundStatement(self, ctx:ToyParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#mainProcedure.
    def visitMainProcedure(self, ctx:ToyParser.MainProcedureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#emptyStatement.
    def visitEmptyStatement(self, ctx:ToyParser.EmptyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#statementList.
    def visitStatementList(self, ctx:ToyParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#assignmentStatement.
    def visitAssignmentStatement(self, ctx:ToyParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#lhs.
    def visitLhs(self, ctx:ToyParser.LhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#rhs.
    def visitRhs(self, ctx:ToyParser.RhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#ifStatement.
    def visitIfStatement(self, ctx:ToyParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#trueStatement.
    def visitTrueStatement(self, ctx:ToyParser.TrueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#falseStatement.
    def visitFalseStatement(self, ctx:ToyParser.FalseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#whileStatement.
    def visitWhileStatement(self, ctx:ToyParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#procedureCallStatement.
    def visitProcedureCallStatement(self, ctx:ToyParser.ProcedureCallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#procedureName.
    def visitProcedureName(self, ctx:ToyParser.ProcedureNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#argumentList.
    def visitArgumentList(self, ctx:ToyParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#argument.
    def visitArgument(self, ctx:ToyParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#expression.
    def visitExpression(self, ctx:ToyParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#simpleExpression.
    def visitSimpleExpression(self, ctx:ToyParser.SimpleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#term.
    def visitTerm(self, ctx:ToyParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#variableFactor.
    def visitVariableFactor(self, ctx:ToyParser.VariableFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#numberFactor.
    def visitNumberFactor(self, ctx:ToyParser.NumberFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#characterFactor.
    def visitCharacterFactor(self, ctx:ToyParser.CharacterFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#stringFactor.
    def visitStringFactor(self, ctx:ToyParser.StringFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#booleanFactor.
    def visitBooleanFactor(self, ctx:ToyParser.BooleanFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#functionCallFactor.
    def visitFunctionCallFactor(self, ctx:ToyParser.FunctionCallFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#getArgCallFactor.
    def visitGetArgCallFactor(self, ctx:ToyParser.GetArgCallFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#notFactor.
    def visitNotFactor(self, ctx:ToyParser.NotFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#parenthesizedFactor.
    def visitParenthesizedFactor(self, ctx:ToyParser.ParenthesizedFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#getArgCall.
    def visitGetArgCall(self, ctx:ToyParser.GetArgCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#booleanConstant.
    def visitBooleanConstant(self, ctx:ToyParser.BooleanConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#variable.
    def visitVariable(self, ctx:ToyParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#modifier.
    def visitModifier(self, ctx:ToyParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#indexList.
    def visitIndexList(self, ctx:ToyParser.IndexListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#index.
    def visitIndex(self, ctx:ToyParser.IndexContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#field.
    def visitField(self, ctx:ToyParser.FieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#functionCall.
    def visitFunctionCall(self, ctx:ToyParser.FunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#functionName.
    def visitFunctionName(self, ctx:ToyParser.FunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#number.
    def visitNumber(self, ctx:ToyParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#unsignedNumber.
    def visitUnsignedNumber(self, ctx:ToyParser.UnsignedNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#integerConstant.
    def visitIntegerConstant(self, ctx:ToyParser.IntegerConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#realConstant.
    def visitRealConstant(self, ctx:ToyParser.RealConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#characterConstant.
    def visitCharacterConstant(self, ctx:ToyParser.CharacterConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#stringConstant.
    def visitStringConstant(self, ctx:ToyParser.StringConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#relOp.
    def visitRelOp(self, ctx:ToyParser.RelOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#addOp.
    def visitAddOp(self, ctx:ToyParser.AddOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ToyParser#mulOp.
    def visitMulOp(self, ctx:ToyParser.MulOpContext):
        return self.visitChildren(ctx)



del ToyParser