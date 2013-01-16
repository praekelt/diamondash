from os import path

from twisted.web.template import Element

from diamondash.utils import slugify
from diamondash.exceptions import ConfigError


class Widget(Element):
    """Abstract class for dashboard widgets."""

    loader = None
    MAX_COLUMN_SPAN = 4
    STYLESHEETS = ()

    # (js_module_path, class_name)
    MODEL = ('widget/widget', 'WidgetModel')
    VIEW = ('widget/widget', 'WidgetView')

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.title = kwargs['title']
        self.client_config = kwargs['client_config']
        self.width = kwargs['width']

    @classmethod
    def parse_width(cls, width):
        """
        Wraps the passed in width as an int and clamps the value to the width
        range.
        """
        width = int(width)
        width = max(1, min(width, cls.MAX_COLUMN_SPAN))
        return width

    @classmethod
    def parse_config(cls, config):
        """Parses a widget config, altering it where necessary."""

        name = config.get('name', None)
        if name is None:
            raise ConfigError('Widget name not specified.')

        name = config['name']
        config.setdefault('title', name)
        name = slugify(name)
        config['name'] = name

        width = config.get('width', None)
        config['width'] = 1 if width is None else cls.parse_width(width)

        model_module, model_class_name = cls.MODEL
        view_module, view_class_name = cls.VIEW

        config['client_config'] = {
            'name': name,
            'model': {
                'modulePath': path.join('widgets', model_module),
                'className': model_class_name,
            },
            'view': {
                'modulePath': path.join('widgets', view_module),
                'className': view_class_name,
            },
        }

        return config

    @classmethod
    def from_config(cls, config, defaults):
        """Parses a widget config, then returns the constructed widget."""
        config = cls.parse_config(config)
        return cls(**config)

    def handle_render_request(self, **params):
        """
        Handles a 'render' request from the client, where `params` are the
        request parameters.
        """
        return {}
