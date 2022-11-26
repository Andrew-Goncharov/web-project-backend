from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from django.http import JsonResponse

from .serializers import NodeSerializer
from .models import Node


class GetAllView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)


class ImportView(APIView):
    # permission_classes = [IsAuthenticated]
    pass


class DeleteView(APIView):
    # permission_classes = [IsAuthenticated]
    pass


class GetView(APIView):
    # permission_classes = [IsAuthenticated]

    print("Hello, world!")

    def get(self, request, node_id):
        data = request.data
        print(data)
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False, status=200)
