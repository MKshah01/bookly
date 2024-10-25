from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import authenticate, login ,get_user_model, logout
from django.contrib import messages
from django.conf import settings



User = get_user_model()  # Get the user model directly

def register_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("core:index")
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            # Save the new user
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your account was created successfully!")
            
            # Authenticate the user with the credentials provided during sign-up
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            
            if new_user is not None:
                login(request, new_user)  # Log the user in
                return redirect("core:index")  # Redirect to home page after sign-up and login
            else:
                messages.error(request, "There was an issue logging you in after registration.")
                return redirect('userauths:sign-in')  # If login fails, redirect to the sign-in page
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect("core:index")  # Redirect to home if already logged in

    if request.method == "POST":
        email = request.POST.get("email")  # Email input
        password = request.POST.get("password")  # Password input

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.warning(request, f"User with email {email} does not exist.")
            return redirect("userauths:sign-in")  # Redirect back to sign-in on failure

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You are logged in successfully.")
            return redirect("core:index")  # Redirect to home page after successful login
        else:
            messages.warning(request, "Invalid credentials.")
            return redirect("userauths:sign-in")  # Redirect back to sign-in on failure

    return render(request, "userauths/sign-in.html")



def logout_view(request):
    # Log out the user
    logout(request)
    # Redirect to the sign-in page (assuming 'sign-in' is defined in 'userauths' namespace)
    return redirect('userauths:sign-in')
