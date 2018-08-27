# IMPORTS

# pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# models
from client.models import *

# VIEWS

# list view
def news(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 1)  # show 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'news/news_list.html', {
        "posts" : posts,
    })

# item view
def news_item(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request, 'news/news_item.html', {
        "post" : post,
    })
