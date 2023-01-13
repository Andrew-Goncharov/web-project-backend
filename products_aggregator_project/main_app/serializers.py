from rest_framework import serializers
from .models import Node
#from .helpers import is_valid_datetime, base64_file
from django.db import connections, connection
from django_base64field.fields import Base64Field


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ["id", "parent_id", "name", "price", "updated_dt", "type", "image"]


class ItemSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    price = serializers.IntegerField(allow_null=True)
    parentId = serializers.UUIDField(allow_null=True)
    type = serializers.CharField()
    image = serializers.CharField()


    def validate(self, attrs):
        print("price validation")
        print("price: ", attrs)

        if "type" not in attrs:
            print("validate_1")
            raise serializers.ValidationError("Type is missing.")

        if attrs["type"] == "OFFER" and attrs["price"] is None:
            print("validate_2")
            raise serializers.ValidationError("Unacceptable price value for offer: Null.")
        if attrs["type"] == "CATEGORY" and attrs["price"] is not None:
            print("validate_3")
            raise serializers.ValidationError("Unacceptable price value for category: not Null.")
        return attrs

    def create(self, validated_data, updateDate):

        print("parent_id: ", str(validated_data["parentId"]), "; type: ", type(validated_data["parentId"]))

        parentId = None
        if validated_data["parentId"]:
            parentId = str(validated_data["parentId"])

        data_to_insert = {
            "id": str(validated_data["id"]),
            "parent_id_id": parentId,
            "name": validated_data["name"],
            "price": validated_data["price"],
            "updated_dt": str(updateDate),
            "type": validated_data["type"],
            "image": validated_data["image"]
        }

        return Node.objects.create(**data_to_insert)


class ImportSerializer(serializers.Serializer):
    # TODO: implement additional validators in the validate method
    #  (requires getting all records from the database)

    items = serializers.ListField(child=ItemSerializer())
    updateDate = serializers.CharField()    # DateTimeField()

    def validate_items(self, items):
        print("Items validation")
        #print("Items: ", items)

        all_ids = set()
        category_ids = set()
        for item in items:
            if item["id"] not in all_ids:
                all_ids.add(item["id"])
                if item["type"] == "CATEGORY":
                    category_ids.add(item["id"])
            else:
                print("validate_items_1")
                raise serializers.ValidationError("Non-unique values exist.")
        offer_ids = all_ids - category_ids
        for item in items:
            if item["parentId"] in offer_ids:
                print("validate_items_2")
                raise serializers.ValidationError("parentId does not belong to category ids.")

        return items

    def validate_updateDate(self, updateDate):
        print("updateDate validation")
        #print("updateDate: ", updateDate)

        # if not isinstance(updateDate, str) or not is_valid_datetime(updateDate):
        # if not is_valid_datetime(updateDate):
        #     raise serializers.ValidationError("Invalid datetime value.")

        return updateDate

    # def validate(self, attrs):
    #     pass

    def create(self, validated_data):
        #print("Data: ", validated_data)

        for item in validated_data["items"]:
            s = ItemSerializer(data=item)
            s.create(item, validated_data["updateDate"])

        return self

    def update(self):
        pass
