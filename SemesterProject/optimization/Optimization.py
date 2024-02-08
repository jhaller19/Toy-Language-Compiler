from antlr.ToyParser import ToyParser
from antlr.ToyVisitor import ToyVisitor


class Optimization(ToyVisitor):

    def visitSimpleExpression(self, ctx: ToyParser.SimpleExpressionContext):
        self.andFolding(ctx)
        self.orFolding(ctx)

        self.multFolding(ctx)
        self.addFolding(ctx)

    def multFolding(self, ctx: ToyParser.SimpleExpressionContext):
        for term in ctx.term():
            if len(term.children) > 1:
                i = 0
                size = term.getChildCount()
                while i < size:
                    c = term.children[i]
                    if isinstance(c, ToyParser.MulOpContext):
                        if c.getText() != '*':
                            l = term.children[i - 1]
                            r = term.children[i + 1]
                            if len(l.children) == 1 and len(r.children) == 1 and not isinstance(l,
                                                                                                ToyParser.BooleanFactorContext) and not isinstance(
                                    r, ToyParser.VariableFactorContext) and not isinstance(l,
                                                                                                       ToyParser.VariableFactorContext):
                                left = ''
                                right = ''
                                if l.children[0].sign() is not None:
                                    left += '-'
                                if r.children[0].sign() is not None:
                                    right += '-'
                                left += l.children[0].children[0].getText()
                                right += r.children[0].children[0].getText()
                                if c.getText() == '/':
                                    if isinstance(l.children[0].children[0].children[0],ToyParser.IntegerConstantContext) and isinstance(r.children[0].children[0].children[0],ToyParser.IntegerConstantContext):
                                        total = int(int(left) / int(right))
                                        term.children[i - 1].children[0].children[0].children[0].children[
                                            0].symbol.text = str(total)
                                        term.children.remove(term.children[i])
                                        term.children.remove(term.children[i])
                                        i -= 2
                                        size -= 2
                                    elif isinstance(l.children[0].children[0].children[0],ToyParser.RealConstantContext) and isinstance(r.children[0].children[0].children[0],ToyParser.IntegerConstantContext):
                                            total = float(float(left) / int(right))
                                            term.children[i - 1].children[0].children[0].children[0].children[
                                                0].symbol.text = str(total)
                                            term.children.remove(term.children[i])
                                            term.children.remove(term.children[i])
                                            i -= 2
                                            size -= 2
                                    elif isinstance(l.children[0].children[0].children[0],ToyParser.IntegerConstantContext) and isinstance(r.children[0].children[0].children[0],ToyParser.RealConstantContext):
                                            total = float(int(left) / float(right))
                                            term.children[i + 1].children[0].children[0].children[0].children[
                                                0].symbol.text = str(total)
                                            term.children.remove(term.children[i-1])
                                            term.children.remove(term.children[i-1])
                                            i -= 2
                                            size -= 2
                                    else:
                                        total = float(float(left) / float(right))
                                        term.children[i - 1].children[0].children[0].children[0].children[
                                            0].symbol.text = str(total)
                                        term.children.remove(term.children[i])
                                        term.children.remove(term.children[i])
                                        i -= 2
                                        size -= 2

                        else:
                            l = term.children[i-1]
                            r = term.children[i+1]
                            if len(l.children) == 1 and len(r.children) == 1 and not isinstance(l,ToyParser.BooleanFactorContext) and not isinstance(
                                    r, ToyParser.VariableFactorContext) and not isinstance(l,ToyParser.VariableFactorContext):
                                left = ''
                                right = ''
                                if l.children[0].sign() is not None:
                                    left += '-'
                                if r.children[0].sign() is not None:
                                    right += '-'
                                left += l.children[0].children[0].getText()
                                right += r.children[0].children[0].getText()
                                if c.getText() == '*':
                                    if isinstance(l.children[0].children[0].children[0],
                                                  ToyParser.IntegerConstantContext) and isinstance(
                                            r.children[0].children[0].children[0], ToyParser.IntegerConstantContext):
                                        total = int(int(left) * int(right))
                                        term.children[i - 1].children[0].children[0].children[0].children[
                                            0].symbol.text = str(total)
                                        term.children.remove(term.children[i])
                                        term.children.remove(term.children[i])
                                        i -= 2
                                        size -= 2
                                    elif isinstance(l.children[0].children[0].children[0],
                                                    ToyParser.RealConstantContext) and isinstance(
                                            r.children[0].children[0].children[0], ToyParser.IntegerConstantContext):
                                        total = float(float(left) * int(right))
                                        term.children[i - 1].children[0].children[0].children[0].children[
                                            0].symbol.text = str(total)
                                        term.children.remove(term.children[i])
                                        term.children.remove(term.children[i])
                                        i -= 2
                                        size -= 2
                                    elif isinstance(l.children[0].children[0].children[0],
                                                    ToyParser.IntegerConstantContext) and isinstance(
                                            r.children[0].children[0].children[0], ToyParser.RealConstantContext):
                                        total = float(int(left) * float(right))
                                        term.children[i + 1].children[0].children[0].children[0].children[
                                            0].symbol.text = str(total)
                                        term.children.remove(term.children[i - 1])
                                        term.children.remove(term.children[i - 1])
                                        i -= 2
                                        size -= 2
                                    else:
                                        total = float(float(left) * float(right))
                                        term.children[i - 1].children[0].children[0].children[0].children[
                                            0].symbol.text = str(total)
                                        term.children.remove(term.children[i])
                                        term.children.remove(term.children[i])
                                        i -= 2
                                        size -= 2
                    i += 1

    def addFolding(self, ctx: ToyParser.SimpleExpressionContext):
        c: ToyParser.TermContext = None
        i = 0
        size = ctx.getChildCount()
        while i < size:
            c = ctx.children[i]
            if isinstance(c, ToyParser.AddOpContext):
                if c.getText() != '+':
                    l = ctx.children[i - 1]
                    r = ctx.children[i + 1]
                    if len(l.children) == 1 and len(r.children) == 1 and not isinstance(l.children[0], ToyParser.BooleanFactorContext) and not isinstance(r.children[0], ToyParser.VariableFactorContext) and not isinstance(l.children[0], ToyParser.VariableFactorContext) :
                        left = ''
                        right = ''
                        if l.children[0].children[0].sign() is not None:
                            left += '-'
                        if r.children[0].children[0].sign() is not None:
                            right += '-'
                        left += l.children[0].children[0].getText()
                        right += r.children[0].children[0].getText()
                        if c.getText() == '-':
                            if isinstance(l.children[0].children[0].children[0].children[0],
                                          ToyParser.IntegerConstantContext) and isinstance(
                                    r.children[0].children[0].children[0].children[0],
                                    ToyParser.IntegerConstantContext):
                                total = int(left) - int(right)
                                ctx.children[i - 1].children[0].children[0].children[0].children[0].children[
                                    0].symbol.text = str(total)
                                ctx.children.remove(ctx.children[i])
                                ctx.children.remove(ctx.children[i])
                                size -= 2
                                i -= 1
                            elif isinstance(l.children[0].children[0].children[0].children[0],
                                            ToyParser.RealConstantContext) and isinstance(
                                    r.children[0].children[0].children[0].children[0],
                                    ToyParser.IntegerConstantContext):
                                total = float(left) - int(right)
                                ctx.children[i - 1].children[0].children[0].children[0].children[0].children[
                                    0].symbol.text = str(total)
                                ctx.children.remove(ctx.children[i])
                                ctx.children.remove(ctx.children[i])
                                size -= 2
                                i -= 1
                            elif isinstance(l.children[0].children[0].children[0].children[0],
                                            ToyParser.IntegerConstantContext) and isinstance(
                                    r.children[0].children[0].children[0].children[0], ToyParser.RealConstantContext):
                                total = int(left) - float(right)
                                ctx.children[i + 1].children[0].children[0].children[0].children[0].children[
                                    0].symbol.text = str(total)
                                ctx.children.remove(ctx.children[i - 1])
                                ctx.children.remove(ctx.children[i - 1])
                                size -= 2
                                i -= 1
                            else:
                                total = float(left) - float(right)
                                ctx.children[i - 1].children[0].children[0].children[0].children[0].children[
                                    0].symbol.text = str(total)
                                ctx.children.remove(ctx.children[i])
                                ctx.children.remove(ctx.children[i])
                                size -= 2
                                i -= 1
                else:
                    l = ctx.children[i-1]
                    r = ctx.children[i+1]
                    if len(l.children) == 1 and len(r.children) == 1 and not isinstance(l.children[0], ToyParser.BooleanFactorContext) and not isinstance(r.children[0], ToyParser.VariableFactorContext) and not isinstance(l.children[0], ToyParser.VariableFactorContext) :
                        left = ''
                        right = ''
                        if l.children[0].children[0].sign() is not None:
                            left += '-'
                        if r.children[0].children[0].sign() is not None:
                            right += '-'
                        left += l.children[0].children[0].getText()
                        right += r.children[0].children[0].getText()
                        if c.getText() == '+':
                            if isinstance(l.children[0].children[0].children[0].children[0] , ToyParser.IntegerConstantContext) and isinstance(r.children[0].children[0].children[0].children[0] , ToyParser.IntegerConstantContext):
                                total = int(left) + int(right)
                                ctx.children[i-1].children[0].children[0].children[0].children[0].children[0].symbol.text = str(total)
                                ctx.children.remove(ctx.children[i])
                                ctx.children.remove(ctx.children[i])
                                size -= 2
                                i -= 1
                            elif isinstance(l.children[0].children[0].children[0].children[0], ToyParser.RealConstantContext) and isinstance(r.children[0].children[0].children[0].children[0],ToyParser.IntegerConstantContext):
                                total = float(left) + int(right)
                                ctx.children[i - 1].children[0].children[0].children[0].children[0].children[
                                    0].symbol.text = str(total)
                                ctx.children.remove(ctx.children[i])
                                ctx.children.remove(ctx.children[i])
                                size -= 2
                                i -= 1
                            elif isinstance(l.children[0].children[0].children[0].children[0], ToyParser.IntegerConstantContext) and isinstance(r.children[0].children[0].children[0].children[0],ToyParser.RealConstantContext):
                                total = int(left) + float(right)
                                ctx.children[i + 1].children[0].children[0].children[0].children[0].children[
                                    0].symbol.text = str(total)
                                ctx.children.remove(ctx.children[i-1])
                                ctx.children.remove(ctx.children[i-1])
                                size -= 2
                                i -= 1
                            else:
                                total = float(left) + float(right)
                                ctx.children[i - 1].children[0].children[0].children[0].children[0].children[
                                    0].symbol.text = str(total)
                                ctx.children.remove(ctx.children[i])
                                ctx.children.remove(ctx.children[i])
                                size -= 2
                                i -= 1

            i+=1

    def andFolding(self, ctx: ToyParser.SimpleExpressionContext):
        for term in ctx.term():
            if len(term.children) > 1:
                i = 0
                size = term.getChildCount()
                while i < size:
                    c = term.children[i]
                    if isinstance(c, ToyParser.MulOpContext):
                        if c.getText().lower() == 'and':
                            l = term.children[i - 1]
                            r = term.children[i + 1]
                            if len(l.children) == 1 and len(r.children) == 1:
                                left = l.children[0].children[0].getText()
                                right = r.children[0].children[0].getText()
                                if left == 'false':
                                    term.children.remove(term.children[i])
                                    term.children.remove(term.children[i])
                                    i -= 1
                                    size -= 2
                                elif right == 'false':
                                    term.children.remove(term.children[i - 1])
                                    term.children.remove(term.children[i - 1])
                                    i -= 1
                                    size -= 2
                    i += 1

    def orFolding(self, ctx):
            i = 0
            size = ctx.getChildCount()
            while i < size:
                c = ctx.children[i]
                if isinstance(c, ToyParser.AddOpContext):
                    if c.getText().lower() == 'or':
                        l = ctx.children[i - 1]
                        r = ctx.children[i + 1]
                        if len(l.children) == 1 and len(r.children) == 1:
                            left = l.children[0].children[0].getText()
                            right = r.children[0].children[0].getText()
                            if left == 'true':
                                ctx.children.remove(ctx.children[i])
                                ctx.children.remove(ctx.children[i])
                                i -= 1
                                size -= 2
                            elif right == 'true':
                                ctx.children.remove(ctx.children[i - 1])
                                ctx.children.remove(ctx.children[i - 1])
                                i -= 1
                                size -= 2
                i += 1

