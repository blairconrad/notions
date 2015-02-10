# http://blogs.msdn.com/b/ericlippert/archive/2010/09/09/old-school-tree-display.aspx
# a
# ├─b
# │ ├─c
# │ │ └─d
# │ └─e
# │   └─f
# └─g
#   ├─h
#   │ └─i
#   └─j

class Node:
    public Text as string
    public Children = []

    def constructor(text):
        self.Text = text

    def constructor(text, *children):
        self.Text = text
        if children:
            self.Children.Extend(children)


class Dumper:
    static def Dump(root as Node):
        print root.Text
        DumpChildren('', root)


    static def DumpChildren(prefix, root as Node):
        for child in root.Children[:-1]:
            DumpSubTree(prefix, true, child)
        if len(root.Children):
            DumpSubTree(prefix, false, root.Children[-1])

    private static def DumpSubTree(prefix, moreSiblings, root as Node):
        if moreSiblings:
            print prefix + '├─' + root.Text
            prefix += '│ '
        else:
            print prefix + '└─' + root.Text
            prefix += '  '

        DumpChildren(prefix, root)


root = Node("a",
            Node("b",
                 Node("c", 
                      Node("d")),
                 Node("e",
                      Node("f"))),
            Node("g",     
                 Node("h",
                      Node("i")),
                 Node("j")))

Dumper.Dump(root)
