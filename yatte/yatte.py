from nodes import Text, Var, Block, Node
from lexer import each_fragment, TEXT_FRAGMENT, VAR_FRAGMENT, OPEN_BLOCK_FRAGMENT, CLOSE_BLOCK_FRAGMENT
from errors import StackOverflowError, StackUnderflowError


class Template(object):

    def __init__(self, src):
        self.src = src
        self.root = Node()
        stack = [self.root]

        for f in each_fragment(src):
            if f.type == TEXT_FRAGMENT:
                try:
                    stack[-1].add_child(Text(f.clean))
                except IndexError:
                    raise StackOverflowError(f)
            elif f.type == VAR_FRAGMENT:
                stack[-1].add_child(Var(f.clean))
            elif f.type == OPEN_BLOCK_FRAGMENT:
                block = Block(content=f.clean)
                stack[-1].add_child(block)
                stack.append(block)
            elif f.type == CLOSE_BLOCK_FRAGMENT:
                try:
                    stack.pop()
                except IndexError:
                    raise StackUnderflowError(f)

    def render(self, context):
        res = ''
        for child in self.root.children:
            res += child.render(context)
        return res


if __name__ == '__main__':
    context = {'var': '__var__', 'list': range(5)}
    tmpl = Template("""{% each list %}
        {% if _ < 3 %}
            sup {{ _ }}
        {% end %}
    {% end %}""")
    print tmpl.render(context)
