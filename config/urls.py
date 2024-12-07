"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from account.views import RegistrationView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
from student_prof.views import StudentProfileViewSet, GradeViewSet, StudentTransferViewSet
from account.views import ListTeachers

router = DefaultRouter()
router.register(r'student-profiles', StudentProfileViewSet, basename='studentprofile')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'student-transfers', StudentTransferViewSet, basename='studenttransfer')



urlpatterns = router.urls


"""=============Swagger docs============="""
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

swagger_view = get_schema_view(
    openapi.Info(
        title="Auth API",
        default_version='v1',
        description="auth API"
    ),
    public=True
)
"""======================================"""



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('docs/', swagger_view.with_ui('swagger', cache_timeout=0)),
    path('account/register/', RegistrationView.as_view()),
    path('account/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('teachers/', ListTeachers.as_view(), name='list_teachers'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)