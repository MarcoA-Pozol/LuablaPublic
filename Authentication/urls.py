from django.urls import path
from . import views

urlpatterns = [
    # path('', views.authentication_home, name="authentication-home"),
    path('/usersList', views.UsersListView.as_view(), name='usersList'),
    path('/protectedCardsList', views.ProtectedCardsView.as_view(), name='protectedCardsList'),
    path('/signUp', views.SignUpView.as_view(), name='signUp'),
    path('/signIn', views.SignInView.as_view(), name='signIn'),
    path('/signOut', views.SignOutView.as_view(), name='signOut'),
    path('/checkAuth', views.CheckAuthView.as_view(), name='checkAuth'),
    path('/checkUserHasPickedLanguage', views.CheckUserHasPickedLanguage.as_view(), name='checkUserHasPickedLanguage'),
    # path('signIn/', views.SignInView.as_view(), name="signIn"),
    # path('logout/', views.logout.as_view(), name="logout")
]
