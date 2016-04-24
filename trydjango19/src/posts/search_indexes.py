import datetime
from haystack import indexes
from posts.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    content_auto=indexes.EdgeNgramField(model_attr='title')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        #"""Used when the entire index for model is updated."""
        return self.get_model().objects.all()#filter#(pub_date__lte=datetime.datetime.now())
