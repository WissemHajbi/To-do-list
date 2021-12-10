from django.urls import path
from .views import GoalDelete, GoalDetail, GoalList, GoalCreate, GoalUpdate, Login, Register
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', GoalList.as_view(), name='goal_list'),
    path('goal/<int:pk>/', GoalDetail.as_view(), name='goal_detail'),
    path('create/POST/', GoalCreate.as_view(), name='goal_create'),
    path('update/<int:pk>/', GoalUpdate.as_view(), name="goal_update"),
    path('delete/<int:pk>/', GoalDelete.as_view(), name="goal_delete"),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', Register.as_view(), name='register')
]
