from pkg_resources import resource_string

from twisted.web.template import renderer, XMLString

from diamondash.widgets.widget.widget import Widget, WidgetConfig


class TextWidgetConfig(WidgetConfig):
    TYPE_NAME = 'text'
    MIN_COLUMN_SPAN = 2


class TextWidget(Widget):
    """A widget that simply displays static text."""

    loader = XMLString(resource_string(__name__, 'template.xml'))

   
    STYLESHEETS = ('text/style.css',)

    def __init__(self, text, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text = text

    @renderer
    def text_renderer(self, request, tag):
        return tag(self.text)
