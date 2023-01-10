from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework import authentication, permissions, status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from django.http import JsonResponse

from .serializers import NodeSerializer, ImportSerializer
from .models import Node


class GetAllView(APIView):
    def get(self, request):
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)


class ImportView(APIView):
    """
    Imports new products and/or categories.
    """

    def post(self, request):
        print("Request received: ", request.data)
        serializer = ImportSerializer(data=request.data)

        if not serializer.is_valid():

            print("Errors: ", serializer.errors)

            # return JsonResponse({
            #     "code": 400,
            #     "message": "Validation failed"
            # })

        serializer.save()
        return Response(status=200)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteView(APIView):
    """
    Delete element by id.
    """
    def delete(self, request, node_id):
        # TODO: add record existence check

        try:
            node = Node.objects.get(pk=node_id)
            node.delete()
        except Exception:
            return JsonResponse({
                "code": 400,
                "message": "Validation failed"
            })

        return Response(status=200)


class GetView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, node_id):
        data = request.data
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
