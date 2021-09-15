from rest_framework import serializers
from PhotoRepoApp.models import Images

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Images 
        fields=(
            'Id',
            'Filename',
            'InsertedAt',
            'LocalPath',
            'S3Path',
            'Tag'
        )