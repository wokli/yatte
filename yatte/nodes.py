from errors import TmplSyntaxError
import operator

ops = {
    '<': operator.lt,
    '>': operator.gt,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge
}


def resolve(name, *args):
    for context in args:
        resolved_var = context.get(name, None)
        if resolved_var is not None:
            break
    return resolved_var


def condition_eval(expr, *args):
    # TODO: handle &&, ||
    # TODO: add string comparsion
    # TODO: speed it up
    tokens = expr.split()
    arg1, op, arg2 = tokens
    op = ops.get(op, None)

    if op is None:
        raise TmplSyntaxError()

    try:
        arg1 = int(arg1)
    except ValueError:
        arg1 = resolve(arg1, *(args))

    # TODO: handle not found
    try:
        arg2 = int(arg2)
    except ValueError:
        arg2 = int(resolve(arg2, *(args)))

    # TODO: handle not found
    return op(arg1, arg2)


class Node(object):

    def __init__(self, content=None):
        self.content = content
        self.children = []

    def add_child(self, child): 
        self.children.append(child)

    def render(self, *args):
        pass

    def __repr__(self):
        return str(self.content)


class Text(Node):

    def render(self, *args):
        return self.content


class Var(Node):

    def render(self, *args):
        resolved_var = resolve(self.content, *args)
        return str(resolved_var)


class Block(Node):

    def __init__(self, content=None):
        super(Block, self).__init__(content)
        self.type, self.expr = content.split(' ', 1)

    def render(self, *args):

        if self.type == 'if':
            if (condition_eval(self.expr, *(args))):
                return ''.join(map(lambda x: x.render(*(args)), self.children))
            return ''

        if self.type == 'each':
            res = ''
            for item in args[0].get(self.expr, []):
                res += ''.join(map(lambda x: x.render(*(args + ({'_': item},))), self.children))

            return res
