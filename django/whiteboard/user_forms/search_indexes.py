import datetime
from haystack import indexes
from user_forms.models import File

# http://django-haystack.readthedocs.org/en/latest/tutorial.html
class FileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    heading = indexes.CharField(model_attr='heading')
    path = indexes.CharField(model_attr='path')
    classpk = indexes.CharField(model_attr='classpk')

    def get_model(self):
        return File


    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
<<<<<<< HEAD
        return self.get_model().objects.filter()


=======
        return self.get_model().objects.all()
>>>>>>> f384d0a7c655203404acd4b251544e64a9e05893
