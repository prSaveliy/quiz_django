from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('core:index')
    else:
        form = UserCreationForm()
    return render(
        request,
        'users/register.html',
        {'form': form}
    )

def logging_out(request):
    return render(request, 'users/logging_out.html')