from nodes import Text, Var, Block, Root
from lexer import each_fragment, TEXT_FRAGMENT, VAR_FRAGMENT, OPEN_BLOCK_FRAGMENT, CLOSE_BLOCK_FRAGMENT


class Template:

    def __init__(self, src):
        self.src = src

        root = Root()
        stack = [root]

        # build AST

        for f in each_fragment(src):
            if f.type == TEXT_FRAGMENT:
                # TODO: handle stack overflow
                stack[-1].add_child(Text(f.clean))
            elif f.type == VAR_FRAGMENT:
                stack[-1].add_child(Var(f.clean))
            elif f.type == OPEN_BLOCK_FRAGMENT:
                block = Block(content=f.clean)
                stack[-1].add_child(block)
                stack.append(block)
            elif f.type == CLOSE_BLOCK_FRAGMENT:
                # TODO: handle stack underflow
                stack.pop()

        self.root = root

    def render(self, context):
        res = ''
        for child in self.root.children:
            res += child.render(context)
        return res

if __name__ == '__main__':

    context = {'var': '__var__', 'list': range(5)}
    tmpl = Template("""
Start {{var}}
{% if 2 < 5 %}
    Test inner
    {% if 5 < 10 %}
        Test inner-inner
    {% end %}

    {% each list %}
        {% if _ < 3 %}
            sup {{ _ }}
        {% end %}
    {% end %}
{% end %}
Test outer
""")

    print tmpl.render(context)
