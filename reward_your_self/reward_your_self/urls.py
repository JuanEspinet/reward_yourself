"""reward_your_self URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from reward import views as rwviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^main/$', rwviews.main_page, name = 'main_page'),
    url(r'^login_page/$', rwviews.login_page, name='login_page'),
    url(r'^login/$', rwviews.login_attempt, name='login_attempt'),
    url(r'^register/$', rwviews.register_attempt, name='reg_attempt'),
    url(r'^logout_request/$', rwviews.logout_request, name='logout_req'),
    url(r'^profile/$', rwviews.profile_page, name='profile_page'),
]
