from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User

#blog code

from blogapp.models import Post, Comment,PostLike
from django.utils import timezone
from blogapp.forms import PostForm, CommentForm,ContactForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,RedirectView)

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


from django.core.mail import EmailMessage
from django.template.loader import get_template


def AboutView(request):
    return render(request,'blogapp/about.html')


@method_decorator(login_required, name="dispatch")
class PostListView(ListView):
    model = Post
    paginate_by = 2
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        postlist = Post.objects.filter(Q(title__icontains = si) | Q(text__icontains = si)).order_by("-id");
        for p1 in postlist:
            p1.liked = False
            ob = PostLike.objects.filter(post = p1,liked_by=self.request.user.profile)
            if ob:
                p1.liked = True
            obList = PostLike.objects.filter(post = p1)
            p1.likedno = obList.count()
        return postlist


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blogapp/post_detail.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user.profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blogapp/post_detail.html'

    form_class = PostForm

    model = Post


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blogapp/post_draft_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

@login_required
def like(request, pk):
    post = Post.objects.get(pk=pk)
    PostLike.objects.create(post=post, liked_by = request.user.profile)
    return redirect('post_list')
@login_required
def unlike(request, pk):
    post = Post.objects.get(pk=pk)
    PostLike.objects.filter(post=post, liked_by = request.user.profile).delete()
    return redirect('post_list')

#######################################
## Functions that require a pk match ##
#######################################
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user.profile
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blogapp/comment_form.html', {'form': form})



@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


@login_required
def contact(request):
    form_class = ContactForm
    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')
            # Email the profile with the
            # contact information
            template = get_template('blogapp/contact_template.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            }
            content = template.render(context)
            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['bhaskarbonu183@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            messages.success(request, f'Your Email Send Successfully.')
            return redirect('contact')

    return render(request, 'blogapp/contact.html', {
        'form': form_class,
    })
