from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdown_deux import markdown
# Create your models here.
#MVC model view controller


class PostManager(models.Manager):
	def active(self, *args,**kwargs):
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance,filename):
	return "%s/%s" %(instance.id,filename)

class Post(models.Model):
		title=models.CharField(max_length=120)
		slug=models.SlugField(unique=True)
		content = models.TextField()
		user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
		lastupdated=models.DateTimeField(auto_now=True,auto_now_add=False)
		timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
		image=models.FileField(upload_to=upload_location,null=True,blank=True)
		draft=models.BooleanField(default=False)
		publish=models.DateField(auto_now=False,auto_now_add=False)


		objects=PostManager()

		def __unicode__(self):
			return self.title

		def __str__(self):
			return self.title
		def get_absolute_url(self):
			return reverse("detail",kwargs={"slug":self.slug})
			#return reverse("Posts:detail",kwargs={"id":self.id}) Posts: used with namespace as described in urls.py of trydjango19
			#return 'details', (), {'slug': self.slug}
			#return "/post/%s/"(self.id)
		def get_markdown(self):
			return mark_safe(markdown(self.content))
		class Meta:
			ordering=["-timestamp","-lastupdated"]
			#either this or as in views use orderby with query

def create_slug(instance,new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug=new_slug
	qs=Post.objects.filter(slug=slug).order_by("-id")
	exists=qs.exists()
	if exists:
			new_slug="%s-%s" %(slug,qs.first().id)
			return create_slug(instance,new_slug=new_slug)
	return slug

def  reciver(sender,instance,*args,**kwargs):
		if not instance.slug:
			instance.slug=create_slug(instance)


pre_save.connect(reciver,sender=Post)
