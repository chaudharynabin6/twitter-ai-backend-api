"""sentimental_analysis_on_celibrity_tweets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.documentation import include_docs_urls

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.schemas.openapi import SchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="Twitter AI API",
        default_version="v1",
        contact=openapi.Contact(email="chaudharynabin6@gmail.com")
        )
        ,
    public=True
    


)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweet-manager/',include('tweet_manager.urls')),
    path('search/',include('UserManager.urls')),
    path('docs/',include_docs_urls(title="docs")),
    path("api.json",schema_view.without_ui()),
    path("schema/",schema_view.with_ui()),
     path('redoc/', schema_view.with_ui('redoc',
                                       cache_timeout=0), name='schema-redoc'),

]

