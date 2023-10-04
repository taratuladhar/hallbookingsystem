from django.contrib import admin
from django.urls import path
from hall import views
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("",views.homePage, name='home'),
    path("about/",views.aboutPage,name='about'),
    path("login_page/",views.loginPage,name='login-page'),
    path("register_page/",views.registerPage,name='register-page'),
    path("book_page/",views.bookPage,name='book-page'),
    
    path("register/",views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("book/", views.book_program, name="book-program"),
    
    path("user_profile/",views.user_profile, name='user-profile'),
    path("edit_user_profile/",views.edit_user_profile, name='edit-user-profile'),
    path("edit_user_success/",views.edit_user_success, name='edit-user-success'),
    
    
]