from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField, CharField

class UploadSerializer(Serializer):
    data = serializers.ListField(
        min_length=1,
        child=serializers.ListField(
            child=serializers.CharField(
                help_text="The value of the cell.", allow_blank=True
            ),
            help_text="The row containing all the values.",
        ),
        default=None,
        help_text="A list of rows that needs to be created as initial table data. If "
        "not provided some example data is going to be created.",
    )
    name = CharField(max_length=30)
    exploit = CharField(max_length=30, default="")

    class Meta:
        fields = ("data")