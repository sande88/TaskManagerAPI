from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import tasksviewset

router = DefaultRouter()
router.register(r'tasks',tasksviewset)

urlpatterns=[path('',include(router.urls)),
             path('by_priority/', tasksviewset.as_view({'get':'by_priority'}), name='by_priority'),
             path('edit_tasks/',tasksviewset.as_view({'get':'id'}),name='id'),
             path('get_task/',tasksviewset.as_view({'get':'by_task'},name='by_task'))     
             
        ]