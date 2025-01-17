
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





# from django.contrib import admin
# from django.urls import path, include, re_path
# from django.conf import settings
# from django.conf.urls.static import static
# from django.views.static import serve as mediaserve

# urlpatterns = [
#     # re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
#     # re_path(r'^statics/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
#     path('admin/', admin.site.urls),
#     path('', include('base.urls'))
# ]

# urlpatterns.append(re_path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
#                      mediaserve, {'document_root': settings.MEDIA_ROOT}))
