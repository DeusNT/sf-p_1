class HTML:
    def __init__(self, output):
        self.output = output
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.output == "print":
            print("<html>\n")
            if self.children:
                for child in self.children:
                    print(str(child))
            print("</html>\n")
        else:
            with open(self.output, "w") as f:
                f.write("<html>\n")
                if self.children:
                    for child in self.children:
                        f.write(str(child))
                f.write("</html>\n")


class TopLevelTag:
    def __init__(self, tag, klass=None, is_single=False, **kwargs):
        self.tag = tag
        self.attributes = {}
        self.children = []
        self.text = ""
        self.is_single = is_single
        if klass is not None:
            self.attributes["class"] = " ".join(klass)
        if kwargs:
            for key, value in kwargs.items():
                self.attributes[key] = value

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __str__(self):
        attrs = []
        if self.attributes:
            for key, value in self.attributes.items():
                attrs.append('{key}="{value}"'.format(key=key, value=value))
            attrs = " " + " ".join(attrs)
        else:
            attrs = ""

        if self.children:
            opening = "<%s%s>\n" % (self.tag, attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal += str(child)
            ending = "</%s>\n" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag}{attrs}>\n".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag}{attrs}>{text}</{tag}>\n".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )


class Tag(TopLevelTag):
    pass



if __name__ == "__main__":
    with HTML(output="test.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body
