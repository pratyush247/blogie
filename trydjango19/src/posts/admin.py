from django.contrib import admin

# Register your models here.
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
	list_display=["title","lastupdated","timestamp"]
	list_display_links=["lastupdated"]
	list_filter=["lastupdated","timestamp"]
	
	search_fields=["title","content"]
	list_editable=["title"]
	class Meta:
		model=Post

admin.site.register(Post,PostModelAdmin)