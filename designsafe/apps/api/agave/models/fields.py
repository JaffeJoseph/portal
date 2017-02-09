""" Base field classes  """
import six
import datetime
import dateutil.parser
import collections
from decimal import Decimal
from designsafe.apps.api.agave.models.base import register_lazy_rel

import logging

logger = logging.getLogger(__name__)

class NOT_PROVIDED(object):
    pass

class BaseField(object):
    """ Base field class """
    related_model = None

    def __init__(self, verbose_name=None, name=None,
                 max_length=None, blank=False, null=False,
                 related=None, default=NOT_PROVIDED, choices=None,
                 help_text='', validators=(), error_messages=None,
                 nested=None, related_name=None):
        self.verbose_name = verbose_name
        self.name = name
        self.max_length = max_length
        self.blank = blank
        self.null = null
        self.related = related
        self.default = default
        self.choices = choices
        self.help_text = help_text
        self.validators = validators
        self.error_messages = error_messages
        self.nested = nested
        self.attname = None
        self.related_name = related_name
        
        if not isinstance(self.choices, collections.Iterator):
            self.choices = []
        else:
            self.choices = list( self.choices)

        if not self.name and self.verbose_name:
            self.name = self.verbose_name.lower()
            self.name = self.name.replace(' ', '_')

        self.choices = self.choices or []

    def contribute_to_class(self, cls, name):
        """ Register the field with the model class it belongs to. """
        if not self.name:
            self.name = name

        self.attname = name
        if self.verbose_name is None:
            self.verbose_name = name.replace('_', ' ')
        self.model = cls
        cls._meta.add_field(self)

    def get_default(self):
        if not isinstance(self.default, NOT_PROVIDED):
            return self.default
        else:
            raise ValueError('No default set')

    def to_python(self, value):
        return value

    def clean(self, value):
            return self.to_python(value)            

class CharField(BaseField):
    """ Char Field """
    def __init__(self, *args, **kwargs):
        super(CharField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        return unicode(value)

class UuidField(CharField):
    """ Uuid Field """
    def __init__(self, *args, **kwargs):
        kwargs['schema_field'] = True
        super(UuidField, self).__init__(*args, **kwargs)

class DateTimeField(BaseField):
    """ Date Time Field """
    def __init__(self, *args, **kwargs):
        super(DateTimeField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not isinstance(value, datetime):
            return dateutil.parser.parse(value)

        return value

class IntField(BaseField):
    """ Int Field """
    def __init__(self, *args, **kwargs):
        super(IntField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        return int(value)

class DecimalField(BaseField):
    """ Decimal Field """
    def __init__(self, *args, **kwargs):
        super(DecimalField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        return Decimal(value)

class ListField(BaseField):
    """ List Field """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', [])
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        return list(value)

class NestedObjectField(BaseField):
    """ Nested Object Field """
    def __init__(self, nested, *args, **kwargs):
        kwargs['nested'] = nested
        kwargs['default'] = kwargs.get('default', {})
        super(NestedObjectField, self).__init__(*args, **kwargs)

class RelatedObjectField(BaseField):
    """ Related Object Field """
    def __init__(self, related, multiple=False, related_name=None, *args, **kwargs):
        kwargs['related_name'] = related_name
        kwargs['related'] = related
        super(RelatedObjectField, self).__init__(*args, **kwargs)
        self.multiple = multiple

    def contribute_to_class(self, cls, name):
        """ Register the field with the model class it belongs to. """
        super(RelatedObjectField, self).contribute_to_class(cls, name)
        related_name = self.related_name or '%s_set' % cls.__name__.lower()
        register_lazy_rel(self.related, related_name, cls.model_name, self.multiple)
