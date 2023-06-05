


from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('user/post/', views.CreateUser.as_view(), name='user_post'),
    path('user/update/<int:pk>', views.RetrieveUpdate.as_view(), name='user_update'),
    path('user/delete/<int:pk>', views.RetrieveDelete.as_view(), name='user_delete'),
    path('user/list/<int:pk>', views.UserList.as_view(), name='user_list'),
    path('user/login/', views.Login.as_view(), name='user_login'),
    path('user/logout/', views.Logout.as_view(), name='user_logout'),
    path('user/forget/', views.ForgetPassword.as_view(), name='user_forget_password'),
    path('activate/<uidb64>/<token>/', views.activate, name= 'activate'),
    path('reset/<int:user_id>/<str:token>/', views.ChangePassword.as_view(), name= 'reset'),


]

