import unittest
from yatte import Template as t
from nodes import resolve, condition_eval

class BasicTest(unittest.TestCase):

    def test_text_node(self):
        tmpl = t('123')
        self.assertEquals(tmpl.render({}), '123')

    def test_var_node(self):
        tmpl = t('{{var}}')
        self.assertEquals(tmpl.render({'var': 'test'}), 'test')


class BlockTest(unittest.TestCase):

    # TODO: test nested each

    def test_each_node(self):
        tmpl = t('{%each var%}{{_}}{%end%}')
        self.assertEquals(tmpl.render({'var': range(3)}), '012')

    def test_if_node(self):
        tmpl = t('{%if a < 5 %}1{%end%}')
        self.assertEquals(tmpl.render({'a': 3}), '1')
        self.assertEquals(tmpl.render({'a': 9}), '')

    def test_if_node_inside_each(self):
        tmpl = t('{% each var %}{% if _ < t %}{{_}}{%end%}{%end%}')
        self.assertEquals(
            tmpl.render({'t': 3, 'var': range(5)}),
            '012'
        )
        self.assertEquals(
            tmpl.render({'t': 0, 'var': range(5)}),
            ''
        )

    def test_each_node_inside_if(self):
        tmpl = t('{% if var < 5 %}{% each q %}{{_}}{%end%}{%end%}')
        self.assertEquals(
            tmpl.render({'var': 3, 'q': range(3)}),
            '012'
        )
        self.assertEqual(
            tmpl.render({'var': 9, 'q': range(3)}),
            ''
        )


class OtherTest(unittest.TestCase):

    def test_resolver(self):
        self.assertEquals(resolve('q', {'a':1}, {'q':2}), 2)

    def test_condition_eval(self):
        self.assertEquals(condition_eval('2 < 5'), True)
        self.assertEquals(condition_eval('3 > 6'), False)
        self.assertEquals(condition_eval('q > 8', {'q':9}), True)
        self.assertEquals(condition_eval('q > 8', {'q':2}), False)



class ErrorHandlingTest(unittest.TestCase):
    # TODO: test syntax error
    # TODO: stack overflow, underflow
    # TODO: error in if condition
    # TODO: variable not found
    pass


if __name__ == '__main__':
    unittest.main()
