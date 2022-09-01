from api.views import GetAuthTokenView, SignupView
from django.urls import path

app_name = 'api'


urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('token/', GetAuthTokenView.as_view()),
]
