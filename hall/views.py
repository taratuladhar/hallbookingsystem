import datetime
from django import forms
from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as login_view, logout as logout_view
from .models import Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseForbidden, HttpResponseNotFound
from .forms import BookingStatusForm
from django.core.mail import send_mail
from django.db import IntegrityError
from django.core.validators import EmailValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import ValidationError

# from hall import models
# from .forms import FeedbackForm
# import re
from . import forms 

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
 
# def register(request):
    if request.method == "POST":
        uname=request.POST.get("name")
        email=request.POST.get("email")
        pass1=request.POST.get("password1")
        pass2=request.POST.get("password2")
        
        if pass1!=pass2:
            return HttpResponse("Your password and confirm password doesnot match !!")
        else:
            if User.objects.filter(username=uname).exists() or User.objects.filter(email=email).exists():
                messages.error(request, "A user with the same username or email address already exists. Please choose different credentials.")
                return redirect('register-page')
            else:
                try:
                    my_user = User.objects.create_user(uname, email, pass1)
                    my_user.save()
                    messages.success(request, 'New user registered successfully.')
                    return redirect('login-page')
                except IntegrityError:
                    messages.error(request, "An error occurred during registration.")
                    return redirect('register-page')
                
    return render(request, 'hall/register.html')
    
# def is_valid_username(username):
#     # Use regular expression to check if username contains only letters
#     return bool(re.match("^[a-zA-Z]+$", username))

# def register(request):
    if request.method == "POST":
        uname = request.POST.get("name")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password do not match!!")
        else:
            # Validate username format
            if not is_valid_username(uname):
                messages.error(request, "Username should only contain letters.")
                return redirect('register-page')

            if User.objects.filter(username=uname).exists() or User.objects.filter(email=email).exists():
                messages.error(request, "A user with the same username or email address already exists. Please choose different credentials.")
                return redirect('register-page')
            else:
                try:
                    my_user = User.objects.create_user(uname, email, pass1)
                    my_user.save()
                    messages.success(request, 'New user registered successfully.')
                    return redirect('login-page')
                except IntegrityError:
                    messages.error(request, "An error occurred during registration.")
                    return redirect('register-page')

    return render(request, 'hall/register.html')

def is_username_valid(username):
    try:
        ASCIIUsernameValidator()(username)
        if any(char.isdigit() for char in username):
            raise ValidationError("Username should not contain digits.")
        return True
    except ValidationError:
        return False

class CustomEmailValidator(EmailValidator):
    def __call__(self, value):
        super().__call__(value)
        if value and value[0].isdigit():
            raise ValidationError("Email addresses cannot start with a number.")

def is_email_valid(email):
    try:
        CustomEmailValidator()(email)
        return True
    except ValidationError:
        return False
    
def register(request):
    if request.method == "POST":
        uname = request.POST.get("name")
        email = request.POST.get("email")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")

        # Validate username
        if not is_username_valid(uname):
            messages.error(request, "Invalid username. Please use only alphabet letters and no digits.")
            return redirect('register-page')

        # Validate email
        if not is_email_valid(email):
            messages.error(request, "Invalid email address.")
            return redirect('register-page')
        
        try:
            User.objects.get(email=email)
            messages.error(request, "A user with the same email address already exists. Please choose a different email.")
            return redirect('register-page')
        except User.DoesNotExist:
            pass
        
        if len(pass1) < 8:
            messages.error(request, "Password should have at least 8 characters.")
            return redirect('register-page')
        
        if pass1 != pass2:
            messages.error(request, "Your password and confirm password do not match!")
            return redirect('register-page')
        else:
            try:
                my_user = User.objects.create_user(uname, email, pass1)
                my_user.save()
                messages.success(request, 'New user registered successfully.')
                return redirect('login-page')
            except IntegrityError:
                messages.error(request, "An error occurred during registration.")
                return redirect('register-page')

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
# def book_program(request):
#     if request.method == "POST":
#         program_title = request.POST.get("pname")
#         name = request.POST.get("name")
#         date = request.POST.get("date")
#         start_time = request.POST.get("start_time")
#         end_time = request.POST.get("end_time")
#         email = request.POST.get("email")
#         description = request.POST.get("description")

#         # Convert start_time and end_time to datetime objects
#         start_datetime = datetime.datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
#         end_datetime = datetime.datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

#         # Check if a booking already exists for the selected date and time range
#         conflicting_bookings = Booking.objects.filter(
#             date=date,
#             start_time__lte=end_datetime,
#             end_time__gte=start_datetime,
#         )

#         if conflicting_bookings.exists():
#             messages.error(request, 'This time slot is already booked. Please choose another time.')
#         else:
#             booking = Booking(
#                 program_title=program_title,
#                 name=name,
#                 date=date,
#                 start_time=start_time,
#                 end_time=end_time,
#                 email=email,
#                 description=description,
#                 user=request.user,
#             )
#             booking.save()
            
#             send_mail(
#                 'Booking Request Sent',
#                 'Dear User, Your booking request has been sent successfully.',
#                 'swetara88@gmail.com',
#                 [email],
#                 fail_silently=False,
#             )
            
#             messages.success(request, 'Hall booking request sent successfully.')
#             return redirect("home")

#     return render(request, "hall/book.html")
def book_program(request):
    if request.method == "POST":
        program_title = request.POST.get("pname")
        name = request.POST.get("name")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        email = request.POST.get("email")
        description = request.POST.get("description")

        # Convert start_time and end_time to datetime objects
        start_datetime = datetime.datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

        # Check if the selected time is between 7 am and 3 pm
        valid_start_time = datetime.datetime.strptime(f"{date} 07:00", "%Y-%m-%d %H:%M")
        valid_end_time = datetime.datetime.strptime(f"{date} 15:00", "%Y-%m-%d %H:%M")

        if not (valid_start_time <= start_datetime <= valid_end_time) or not (valid_start_time <= end_datetime <= valid_end_time):
            messages.error(request, 'Hall bookings are only allowed between 7 am and 3 pm.')
            return render(request, "hall/book.html")

        # Check if a booking already exists for the selected date and time range
        conflicting_bookings = Booking.objects.filter(
            date=date,
            start_time__lte=end_datetime,
            end_time__gte=start_datetime,
        )

        if conflicting_bookings.exists():
            messages.error(request, 'This time slot is already booked. Please choose another time.')
        else:
            booking = Booking(
                program_title=program_title,
                name=name,
                date=date,
                start_time=start_time,
                end_time=end_time,
                email=email,
                description=description,
                user=request.user,
            )
            booking.save()
            
            send_mail(
                'Booking Request Sent',
                'Dear User, Your booking request has been sent successfully.',
                'swetara88@gmail.com',
                [email],
                fail_silently=False,
            )
            
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

@login_required
def edit_user_success(request):
    return render(request,'hall/edit_user_success.html')

@login_required
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

@login_required
def display_user_booking(request):
    if request.method == "POST" and request.user.is_staff:
        form = BookingStatusForm(request.POST)
        if form.is_valid():
            booking_id = form.cleaned_data['booking_id']
            status = form.cleaned_data['status']
            booking = Booking.objects.get(id=booking_id)
            booking.status = status
            booking.save()
            messages.success(request, 'Booking status updated successfully.')
                 
    user_bookings = Booking.objects.filter(email=request.user.email)  # Assuming email is used for user identification
    return render(request, 'hall/user_booking.html', {'user_bookings': user_bookings})

@login_required
def user_delete_booking(request,pk):
    booking = get_object_or_404(Booking, id=pk)

    # Check if the logged-in user is the owner of the booking
    if booking.email != request.user.email:  # Replace 'email' with the appropriate user identification field
        # If not, return an error response or handle it as needed
        return HttpResponseForbidden("You do not have permission to delete this booking.")

    # Delete the booking
    booking.delete()

    # Redirect to a relevant page (e.g., user profile or booking history)
    return redirect('display-user-booking') 

@login_required
def all_bookings(request):
    approved_bookings = Booking.objects.filter(status='Approved')

    context = {
        'bookings': approved_bookings,
    }

    return render(request, 'hall/all_bookings.html', context)

@login_required
def feedbackPage(request):
    return render(request, 'hall/user_feedback.html')

@login_required
def user_feedback(request):
    user=request.user
    print("1")
    feedback=forms.FeedbackForm()
    print("2")
    if request.method=='POST':
        print("3")
        feedback=forms.FeedbackForm(request.POST)
        
        print("4")
        if feedback.is_valid():
            print("5")
            feedback.save()
            
        else:
            print("form is invalid")
            print(feedback.errors)
        return render(request,'hall/feedback_sent.html',{'user':user})
    return render(request,'hall/user_feedback.html',{'feedback':feedback,'user':user})