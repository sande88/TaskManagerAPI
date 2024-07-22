from rest_framework import viewsets
from .models import tasks
from .serializers import TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.

class  tasksviewset(viewsets.ModelViewSet):
    queryset = tasks.objects.all()
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'])
    def by_priority(self, request):
        priority = (request.query_params.get('priority',None))
        if priority is not None:
            filtered = tasks.objects.filter(priority=priority)
            serializer = self.get_serializer(filtered, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Priority parameter is required."},status=400)