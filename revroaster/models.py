from django.db import models
import ast

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

# Create your models here.
class SavedUrl(models.Model):
    url = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    image = models.CharField(max_length=300)
    positive = models.TextField(null=True)
    negative = models.TextField(null=True)
    def __str__(self):
		return self.url