# from rest_framework import serializers
# from .import models
#
# class ImageSerializers(serializers.ModelSerializer):
#
#     class Meta:
#         model = models.Image
#         field = '__all__'
#
#
# class CommentSerializers(serializers.ModelSerializer):
#
#     class Meta:
#         model = models.Comment
#         field = '__all__'
#
# class LikeSerializers(serializers.ModelSerializer):
#
#     class Meta:
#         model = models.Like
#         field = '__all__'
#

from rest_framework import serializers
from . import models


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = '__all__'


