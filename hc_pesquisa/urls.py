from django.urls import path, include
from django.contrib import admin
from busca.views_auth import logout_manual

urlpatterns = [
    path("", include("busca.urls")),
    path('admin/', admin.site.urls),

    # 🔥 logout 100% controlado por você
    path('logout/', logout_manual, name='logout'),

    # depois disso você pode incluir o resto
    path('accounts/', include('django.contrib.auth.urls')),
]
