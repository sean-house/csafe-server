from django.urls import path, include, reverse_lazy
from . import views

app_name = 'safe'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('keyholder/', views.SHListView.as_view(), name='keyholder'),
    path('keyholder/<pk>/', views.SafeKHDetailView.as_view(), name = 'kh_detail'),
    path('keyholder/update/<pk>', views.KH_SafeUpdateView.as_view(), name='kh_message'),
    path('safeholder/', views.SafeListView.as_view(), name='safeholder'),
    path('safeholder/<pk>/', views.SafeSHDetailView.as_view(), name ='sh_detail'),
    path('safeholder/update/<pk>/', views.SH_SafeUpdateView.as_view(), name='sh_message'),
    path('sh_claim_safe/', views.SH_ClaimSafeView.as_view(), name='sh_claim_safe'),
    path('sh_claim_safe/<pk>/', views.sh_confirm_safe, name='sh_confirm'),
    path('kh_claim_sh/', views.KH_ClaimSafeView.as_view(), name='kh_claim_safe'),
    path('kh_claim_sh/<pk>/', views.kh_confirm_safe, name='kh_confirm'),
    path('kh_release_sh/<pk>/', views.SafeKHReleaseView.as_view(), name='kh_release'),
    path('',views.IndexView.as_view(), name='index'),
]
