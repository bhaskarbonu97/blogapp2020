from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.models import User
from django.views.generic import ListView
from .models import Profile,FollowUser
from blogapp.models import Post
from django.db.models import Q
from django.contrib import messages
from .forms import SignUpForm,ProfileUpdateForm,UserUpdateForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, f'Your Accounts Successfully Register.Thank You to join--{username}!')
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your Profile Update successfuly Thank You.')
            return redirect('profile_list')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
    'u_form':u_form,
    'p_form':p_form
    }
    return render(request,'registration/profile_edite.html',context)

@method_decorator(login_required, name="dispatch")
class ProfileListView(ListView):
    model = Profile
    redirect_field_name = 'registration/profile_list.html'
    paginate_by = 4
    def get_queryset(self):
        si = self.request.GET.get("si")
        if si == None:
            si = ""
        profilelist = Profile.objects.filter(Q(user__username__icontains = si) | Q(address__icontains = si) | Q(gender__icontains = si) | Q(status__icontains = si)).order_by("-id");
        for pl in profilelist:
            pl.followed = False
            ob = FollowUser.objects.filter(profile = pl,followed_by=self.request.user.profile)
            if ob:
                pl.followed = True
            obList = FollowUser.objects.filter(profile = pl)
            pl.followno = obList.count()
        return profilelist

def getprofile(request, pk):
    post_author = get_object_or_404(User, pk=pk)
    profile = get_object_or_404(Profile, pk=post_author.id)
    post = Post.objects.filter(author=profile.id).order_by('-id')
    context = {
        "profile": profile,
        "post": post
    }
    profileuser = render(request, "registration/profile_detail.html", context)
    return profileuser

@login_required
def follow(req, pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, followed_by = req.user.profile)
    return redirect("profile_list")

@login_required
def unfollow(req, pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, followed_by = req.user.profile).delete()
    return redirect("profile_list")
