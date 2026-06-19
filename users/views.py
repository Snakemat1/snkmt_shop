from django.shortcuts import redirect, render
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("catalog:product_list")
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})


