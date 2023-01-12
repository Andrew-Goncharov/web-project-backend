import uuid

from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework import authentication, permissions, status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from django.http import JsonResponse

from .serializers import NodeSerializer, ImportSerializer
from .models import Node
from .helpers import rearrange_data, create_get_node_result,\
    is_valid_uuid, delete_node, get_nodes, create_result

from django.db import connection
from django.core import serializers
from rest_framework.permissions import IsAuthenticated
import json


class GetAllView(APIView):
    """
    Get all elements by recursively traversing child elements.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        all_nodes = Node.objects.all()

        data_str = serializers.serialize("json", all_nodes)
        data_json = json.loads(data_str)

        roots = []
        final_data = []

        for node in data_json:
            if node["fields"]["parent_id"] is None:
                roots.append(node["pk"])

        for root in roots:
            nodes = get_nodes(node_id=root)

            data_str = serializers.serialize("json", nodes)
            data_json = json.loads(data_str)

            r_data = rearrange_data(data_json)
            data = create_result(r_data, root)
            final_data.extend(data)

        return JsonResponse(final_data, safe=False, status=200)


class ImportView(APIView):
    """
    Imports new products and/or categories.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # print("Request received: ", request.data)
        serializer = ImportSerializer(data=request.data)

        if not serializer.is_valid():

            # print("Errors: ", serializer.errors)

            return JsonResponse({
                "code": 400,
                "message": "Validation failed"
            })

        serializer.save()
        return Response(status=200)


class DeleteView(APIView):
    """
    Delete element by id.
    """
    permission_classes = (IsAuthenticated,)

    def delete(self, request, node_id):
        if not is_valid_uuid(node_id):
            return JsonResponse({
                "code": 400,
                "message": "Validation failed"
            })

        try:
            delete_node(node_id)
        except Exception:
            return JsonResponse({
                "code": 400,
                "message": "Validation failed"
            })

        return Response(status=200)


class GetView(APIView):
    """
    Get element by id by recursively traversing child elements.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, node_id):

        if not is_valid_uuid(node_id):
            return JsonResponse({
                "code": 400,
                "message": "Validation failed"
            })

        nodes = get_nodes(node_id)

        data_str = serializers.serialize("json", nodes)
        data_json = json.loads(data_str)

        r_data = rearrange_data(data_json)
        # print(r_data)

        data = create_get_node_result(r_data, node_id)
        # print(data)

        return JsonResponse(data, safe=False, status=200)

