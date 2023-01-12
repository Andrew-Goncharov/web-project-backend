from django.shortcuts import render
from rest_framework.views import APIView

from rest_framework import authentication, permissions, status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from django.http import JsonResponse

from .serializers import NodeSerializer, ImportSerializer
from .models import Node
from .helpers import rearrange_data, create_get_node_result

from django.db import connection
from django.core import serializers

import json


def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM main_app_node')
        row = cursor.fetchone()
    return row

class GetAllView(APIView):
    def get(self, request):

        '''nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)'''
        # row = my_custom_sql()
        # serializer = GetSerializer(row, many=True)
        # print(row)

        data = request.data
        nodes = Node.objects.raw('SELECT * FROM main_app_node')
        serializer = NodeSerializer(nodes, many=True)
        data = serializers.serialize('json', nodes)
        print(data)

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
    """
    Get element by id by recursively traversing child elements.
    """

    def get(self, request, node_id):

        nodes = Node.objects.raw('''WITH RECURSIVE recursive_nodes AS (
            SELECT * FROM main_app_node WHERE main_app_node.id = %s
        
            UNION
        
            SELECT main_app_node.* FROM main_app_node
            JOIN recursive_nodes ON main_app_node.parent_id_id = recursive_nodes.id
        )
        
        SELECT * FROM recursive_nodes;''', [node_id])

        data_str = serializers.serialize('json', nodes)
        data_json = json.loads(data_str)

        r_data = rearrange_data(data_json)
        print(r_data)

        data = create_get_node_result(r_data, node_id)
        print(data)

        return JsonResponse(data, safe=False, status=200)

