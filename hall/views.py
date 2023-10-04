from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as login_view, logout as logout_view
from .models import Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# from . forms import RegistrationForm
# from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.hashers import make_password


# Create your views here.
def homePage(request):
    return render(request, 'hall/index.html')

def aboutPage(request):
    return render(request, 'hall/about.html')

def bookPage(request):
    return render(request, 'hall/book.html')

def registerPage(request):
    return render(request, 'hall/register.html')

def loginPage(request):
    return render(request, 'hall/login.html')


# ================================*************=======================================
 
def register(request):
    if request.method == "POST":
        uname=request.POST.get("name")
        email=request.POST.get("email")
        pass1=request.POST.get("password1")
        pass2=request.POST.get("password2")
        
        if pass1!=pass2:
            return HttpResponse("Your password and confirm password doesnot match !!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            messages.success(request, 'User registered successfully.')
            return redirect('login-page')
        
    return render(request, 'hall/register.html')
    
def login(request):
    if request.method == "POST":
        username=request.POST.get('name')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login_view(request,user)
            messages.success(request, 'User logged in successfully.')
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!!")
        
    return render(request,'hall/login.html')

def logout(request):
    logout_view(request)
    return redirect('home')

@login_required
def book_program(request):
    print("1")
    if request.method == "POST":
        print("11")
        program_title = request.POST.get("pname")
        name = request.POST.get("name")
        date = request.POST.get("date")
        time = request.POST.get("time")
        email = request.POST.get("email")
        description = request.POST.get("description")
        print("111")
        booking = Booking(
            program_title=program_title,
            name=name,
            date=date,
            time=time,
            email=email,
            description=description,
        )
        print("1111")
        booking.save()
        print("11111")
        # You can redirect to a success page or another view here
        messages.success(request, 'Hall booking request sent successfully.')
        return redirect("home")

    return render(request, "hall/book.html")

@login_required
def user_profile(request):
    # Get the currently logged-in user
    current_user = request.user

    # Now you can access the user's attributes, for example:
    user_id = current_user.id
    username = current_user.username
    email = current_user.email
    first_name = current_user.first_name
    last_name = current_user.last_name

    # Pass user attributes to the template for rendering
    context = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
    }

    return render(request, 'hall/user_profile.html', context)

def edit_user_success(request):
    return redirect('edit-user-success')

def edit_user_profile(request):
    if request.method == 'POST':
        new_name = request.POST['edit_name']
        new_email = request.POST['edit_email']
        request.user.username = new_name
        request.user.email = new_email
        request.user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('edit-user-success')  # Redirect to the profile editing page after successful update

    return render(request, 'hall/edit_user_profile.html') 