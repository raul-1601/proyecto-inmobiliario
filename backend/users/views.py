from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import login
from .utils import generar_username

# Create your views here.


def register_view(request, tipo_usuario):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.username = generar_username(form.cleaned_data['first_name'], form.cleaned_data['last_name'])
                user.tipo_usuario = tipo_usuario
                user.save()
                login(request, user)
                messages.success(request, f"¡Cuenta creada exitosamente!")
                return redirect("home")
                
            except Exception as e:
                messages.error(request, "Error al crear la cuenta. Por favor, intenta nuevamente.")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})