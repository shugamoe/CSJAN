import datetime
from haystack import indexes
from user_forms.models import File


class FileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    heading = indexes.CharField(model_attr='heading')
    description = indexes.CharField(model_attr='description')
    body = indexes.CharField(model_attr='body')
    path = indexes.CharField(model_attr='path')

    def get_model(self):
        return File

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()