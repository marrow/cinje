
# Some samples.

class Transform(object):
    """Convert a value between Python-native and web-friendly datatypes."""
    
    def __call__(self, value):
        """Get the web-friendly version of this Python-native value."""
        return value
    
    def native(self, value):
        """Get the Python-native version of this web-friendly value."""
        return value


class Widget(DataAttribute):
    title = DataAttribute(defualt=None)
    
    transform = DataAttribute(default=Transform())

    def decode(self, value):
        return self.default if value is None else self.transform.native(value)
    
    def encode(self, value):
        return self.transform(self.default if value is None else value)


class Container(Widget):
    children = DeclarativeAttributes(only=Widget)
    
    def decode(self, value):
        pass
    
    def encode(self, value):
        pass


class SampleContainer(Container):
    test = Widget(default=True, title="Testing!")
