# search_indexes.py
from haystack import indexes
from django.contrib.auth.models import User

class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    username = indexes.CharField(model_attr='username')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
