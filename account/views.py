from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views import View
from .forms import UserRegisterationForm, UserLoginForm
from django.contrib.auth.models import  User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post


class UserRegisterView(View):
    
    form_class = UserRegisterationForm
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated: # stops logged users from manually entering account/register url
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'Registeration Sucessful!', 'success')
            return redirect('home:home')

        return render(request, self.template_name, {"form":form})


class UserLoginView(View):

    form_class = UserLoginForm
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated: # stops logged users from manually entering account/login url
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in Successfully!', 'success')
                return redirect('home:home')
                
            messages.error(request, 'username or password is wrong!', 'warning')
        return render(request, self.template_name, {'form':form})


class UserLogoutView(LoginRequiredMixin, View):

    # login_url = '/account/login'   added LOGIN_URL to settings.py instead.

    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out Successfully!', 'success')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id) # production mode
        # user = User.objects.get(id=user_id)

        # posts = get_list_or_404(Post, user=user) # production mode (problem: will 404 if user exists but has zero posts)
        posts = Post.objects.filter(user=user)
        
        return render(request, 'account/profile.html', {'user':user, 'posts':posts})


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView): # even if email doesn't exist, it will show this page to avoid email leakage
    template_name = 'account/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'