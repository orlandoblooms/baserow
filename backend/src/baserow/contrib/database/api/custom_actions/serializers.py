from rest_framework.serializers import Serializer, FileField

class UploadSerializer(Serializer):
    uploaded_file = FileField()

    class Meta:
        fields = ("data")