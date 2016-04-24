from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from urllib import quote_plus
from django.db.models import Q
from django.http import Http404
# Create your views here.
def post_create(request):
	if request.user.is_staff or request.user.is_superuser:
		form=PostForm(request.POST or None,request.FILES or None)
		if form.is_valid():
			instance =form.save(commit=False)
			#print form.cleaned_data.get("title")
			instance.user=request.user
			instance.save()
			return HttpResponseRedirect(instance.get_absolute_url())
		context={
			"form":form,}
		return render(request,"post_form.html",context)
	else:
		raise Http404

def post_detail(request,slug=None):#retrieve
	instance=get_object_or_404(Post,slug=slug)
	#return HttpResponse("<h1>detail</h1>")
	share_string=quote_plus(instance.content)
	context={
				"title":instance.title,
				"instance":instance,
				"share_string":share_string,
				}
	#return HttpResponse("<h1>list</h1>")
	return render(request,"post_detail.html",context)

def post_update(request,slug):#update
	instance=get_object_or_404(Post,slug=slug)
	#return HttpResponse("<h1>detail</h1>")
	form=PostForm(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
			instance=form.save(commit=False)
			instance.save()
			#success message
			return HttpResponseRedirect(instance.get_absolute_url())
	context={
				"form":form,
				}
	#return HttpResponse("<h1>list</h1>")
	return render(request,"post_form.html",context)

def post_list(request):
	#this query set is not working and not giving output however everything is running fine
		queryset_list= Post.objects.active()#.order_by("-timestamp")
		
		if request.user.is_staff or request.user.is_superuser:
			queryset_list=Post.objects.all()

		query = request.GET.get("q")
		if query:
			queryset_list=queryset_list.filter(Q(title__icontains =query)).distinct()		
			
		paginator = Paginator(queryset_list, 3) # Show 5 contacts per page
		page = request.GET.get('page')
		try:
			queryset = paginator.page(page)
		except PageNotAnInteger:
		# If page is not an integer, deliver first page.
			queryset = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			queryset= paginator.page(paginator.num_pages)

		context={
		"object_list": queryset,

		"title": "List",
		}
		return render(request,"post_list.html",context)
	
	#method for authentication 
	#if request.user.is_authenticated():
		#	context={"title":"list"}
		#return HttpResponse("<h1>my list is working</h1>")
	#else:
		#context={"title":"list for not logged in user"}
	#	return HttpResponse("<h1>my list is working</h1>")


def post_delete(request,slug=None):
	instance=get_object_or_404(Post,slug=slug)
	instance.delete()
	return redirect("Posts:list")
