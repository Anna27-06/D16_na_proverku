from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter, UserResponseFilter
from .forms import PostForm, EditForm, UserResponseForm
from .models import Post, UserResponse


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'
    # paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post_detail'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['userresponse_form'] = UserResponseForm()
        context['userresponses'] = UserResponse.objects.filter(post__id=self.kwargs.get('id'))
        return context



    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if UserResponse.objects.filter(author_id=self.request.user.id).filter(post_id=self.kwargs.get('pk')):
    #         context['respond'] = "Отклик"
    #     elif self.request.user == Post.objects.get(pk=self.kwargs.get('pk')).author:
    #         context['respond'] = "Мое сообщение"
    #     return context


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('app.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_create.html'
    # success_url = reverse_lazy('post')
    context_object_name = 'post_create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('app.change_post',)
    form_class = EditForm
    model = Post
    template_name = 'flatpages/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, DeleteView):
    # permission_required = ('app.delete_post',)
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('posts')


class UserResponseView(CreateView):
    # permission_required = ('app.view_userresponse',)
    model = UserResponse
    form_class = UserResponseForm
    template_name = 'flatpages/userresponse.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']

        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        cat_menu = Post.get_categories()
        context = super(CreateView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


class UserResponseList(ListView):
    permission_required = ('app.view_userresponses',)
    model = UserResponse
    template_name = 'flatpages/userresponses.html'
    context_object_name = 'userresponses'
    ordering = '-dateCreation'
    paginate_by = 10

    # def get_queryset(self):
    #     queryset = UserResponse.objects.filter(post__author=self.request.user)
    #     return queryset

    def get_queryset(self):
        queryset = UserResponse.objects.filter(post__author=self.request.user)
        self.filterset = UserResponseFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userresponsefilterset'] = self.filterset
        return context


class UserresponseDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('app.delete_userresponse',)
    model = UserResponse
    template_name = 'flatpages/userresponse_delete.html'
    success_url = reverse_lazy('userresponses')



def response_status_update(request, pk):
    resp = UserResponse.objects.get(pk=pk)
    resp.status = True
    resp.save()
    return HttpResponseRedirect(reverse_lazy('userresponses'))


