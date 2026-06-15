from django.views.generic import DetailView, ListView

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    context_object_name = "posts"
    template_name = "blog/post_list.html"


class BlogPostDetailView(DetailView):
    model = BlogPost
    context_object_name = "post"
    template_name = "blog/post_detail.html"
