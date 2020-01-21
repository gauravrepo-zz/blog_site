from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateBlogForm, UpdateBlogForm
from .models import Blog
from accounts.models import Account

# Create blog view.
def create_blog_view(request):
    context = {}

    if request.user.is_authenticated:

        form = CreateBlogForm(request.POST or None, request.FILES or None)
        if request.POST:
            if form.is_valid():
                obj = form.save(commit=False)
                author = Account.objects.filter(email=request.user.email).first()
                obj.author = author
                obj.save()
                return redirect('home')
            else:
                context['blog_form'] = form  
        else:
            context['blog_form'] = form
        return render(request, "blogs/create_blog.html", context)
    else:
        return redirect('home')


# Blog detail view
def detail_blog_view(request, slug):
    context = {}
    blog = get_object_or_404(Blog, slug=slug)
    if (blog.is_draft == False):
        context['blog'] = blog
    else:
        return redirect('home')
    return render(request, 'blogs/detail_blog.html', context)

# Blog List view
def list_blog_view(request):
    context = {}
    blogs = Blog.objects.filter(is_draft=False)
    context['blogs'] = blogs
    return render(request, 'blogs/list_blogs.html', context)


# Update blog view
def update_blog_view(request, slug):
    context = {}

    if request.user.is_authenticated:
        blog = get_object_or_404(Blog, slug=slug)
        context['blog'] = blog
        if(request.user == blog.author):
            form = UpdateBlogForm(request.POST or None, request.FILES or None, instance=blog)
            if request.POST:
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.save()
                    blog = obj
                    return redirect('home')
                else:
                    context['blog_form'] = form
            else:
                context['blog_form'] = form
            return render(request, "blogs/update_blog.html", context)
        else:
            return redirect('home')
    else:
        return redirect('home')


# Blog blogs view
def my_blogs_list_view(request):
    context = {}

    if request.user.is_authenticated:
        blogs = Blog.objects.filter(author=request.user)
        if blogs is not None:
            context['blogs'] = blogs
        else:
            context['message'] = "You do not have any posts yet"
    else:
        context['message'] = "You need to sign in to see your posts"
    
    return render(request, "blogs/my_blogs.html", context)


# Blog delete view
def delete_blog_view(request, slug):
    context = {}

    if request.user.is_authenticated:
        blog = get_object_or_404(Blog, slug=slug)
        if (blog.author == request.user):
            blog.delete()
            return redirect('my_blogs')
        else:
            return redirect('home')
    else:
        return redirect('home')
    
        
