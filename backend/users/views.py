from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .utils import generar_username
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = generar_username(form.cleaned_data['first_name'], form.cleaned_data['last_name'])
                user.save()
                login(request, user)
                messages.success(request, f"¡Cuenta creada exitosamente!")
                return redirect("home")
                
            except Exception as e:
                messages.error(request, "Error al crear la cuenta. Por favor, intenta nuevamente.")
    else:
        form = RegisterForm()
    return render(request, "usuarios/register.html", {"form": form})


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, "Has iniciado sesión.")
        return redirect("home")

    return render(request, "usuarios/login.html", {"form": form})


@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("home")