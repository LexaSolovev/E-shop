from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import BlogPost

class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        return queryset

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров при каждом открытии записи."""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj

class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:post_list')

class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
