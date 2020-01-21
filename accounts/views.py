from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterationForm, LoginForm, UpdateAccountForm
from django.http import HttpResponse
from .models import Account

# Register page view.
def register_view(request):
    context = {

    }
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.POST:
        form = RegisterationForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            context['registeration_form'] = form
    else:
        form = RegisterationForm()
        context['registeration_form'] = form

    return render(request, 'accounts/register.html', context)

# Login Page view
def login_view(request):
    context = {

    }
    if request.user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
        else:
            context['login_form'] = form
    else:
        form = LoginForm()
        context['login_form'] = form

    return render(request, 'accounts/login.html', context)


# Logout Page view
def logout_view(request):
    logout(request)
    return redirect('home')


# Update Account view
def update_account_view(request):
    context = {
    }

    if not request.user.is_authenticated:
        return redirect('home')

    account = get_object_or_404(Account, email=request.user.email)
    
    if account != request.user:
        return HttpResponse("This is not your account")

    if request.POST:
        form = UpdateAccountForm(request.POST or None, request.FILES or None, instance=account)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            account = obj
            context['success_message'] = "Updated"
            return redirect('home')
        else:
            context['accountupdate_form'] = form
    else:
        form = UpdateAccountForm(instance=account)
            # initial = {
            #     "username": user.username,
            #     "first_name": user.first_name,
            #     "last_name": user.last_name,
            #     "description": user.description,
            #     "position": user.position,
            #     "department": user.department,
            #     "birth_date": user.birth_date,
            #     "on_leave": user.on_leave
            # }
        context['accountupdate_form'] = form

    return render(request, 'accounts/update_account.html', context)

# # Update user password
# def reset_password_view(request):
#     context = {

#     }
#     if request.POST:
#         form = PasswordResetForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)
#             messages.success(request, 'Your password was successfully changed')
#             return redirect('home')
#         else:
#             context['error'] = "Wrong credentials"
#             context['form'] = form
#     else:
#         form = PasswordResetForm(request.user)
#         context['form'] = form
#     return render(request, 'account/reset_password.html',context)