from django.urls import path


from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('login_handle/', views.login_handle, name='login_handle'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_page, name='register'),
    path('register_handle',views.register_handle,name="register_handle"),
    path('student/<int:id>',views.student_dashboard,name='student_dashboard'),
    path('teacher/<int:id>',views.teacher_dashboard,name='teacher_dashboard')
    
]