"""The program converts pydoc to html."""
import argparse
import importlib
import os
import inspect
import jinja2


class DocContainer:
    """Class-container that renders object with data for html"""
    def __init__(self, name, desc, cls, func, pattern):
        self.name = name
        self.desc = desc
        self.cls = cls
        self.func = func
        self.pattern = pattern

    def prep(self):

        if self.desc:
            self.desc = self.desc.replace('\n', '<br/>')

        res = []
        for x in self.cls:
            if x[1] is None:
                res.append((x[0], 'no information'))
            else:
                res.append((x[0], x[1].replace('\n', '<br/>')
                            .replace('    ', '&emsp;&emsp;')))

        self.cls = res

        res = []
        for x in self.func:

            if x[1] is None:
                res.append((x[0], 'no information'))
            else:
                res.append((x[0], x[1].replace('\n', '<br/>')
                            .replace('    ', '&emsp;&emsp;')))

        self.func = res

    def __str__(self):
        self.prep()
        fname = 't{}.html'.format(self.pattern)
        with open(fname, 'r') as MyTemplate:
            res_template = MyTemplate.read()

        res_patt = jinja2.Template(res_template)

        return res_patt.render(name=self.name, classes=self.cls,
                               ff=self.func, desc=self.desc)


def find_classes(module):
    """The function that finds classes in module"""
    d = module.__dict__
    return [d[x] for x in d if inspect.isclass(d[x])]


def find_func(module):
    """The function that finds functions in module"""
    d = module.__dict__
    return [d[x] for x in d if inspect.isfunction(d[x])
            or inspect.isbuiltin(d[x]) or inspect.isgeneratorfunction(d[x])]


def parse_docs(module, template):
    """The function that handles docstring of module"""
    classes = find_classes(module)
    func = find_func(module)

    cls = sorted([(x.__name__, x.__doc__) for x in classes],
                 key=lambda x: x[0])
    fn = sorted([(x.__name__, x.__doc__) for x in func], key=lambda x: x[0])

    return DocContainer(module.__name__, module.__doc__, cls, fn, template)


def main():

    args = argparse.ArgumentParser(description="""A programm that converts
                                   pydoc to html.""")
    args.add_argument('object',
                      help='name of object for that you want to recieve doc')
    args.add_argument(
        'template', help='the number of template for html: 1,2,3,4,5',
        nargs='?', default=1, type=int)
    prog_args = args.parse_args()
    object = prog_args.object
    filename = "{}_help.htm".format(object)
    template = prog_args.template
    try:
        module = eval(object)
    except NameError:
        try:
            module = importlib.__import__(object)
        except ImportError:
            print('Sorry, there was an error')
            os._exit(0)
        pass

    container = parse_docs(module, template)

    with open(filename, 'w') as file:
        file.write(container.__str__())


if __name__ == '__main__':
    main()
