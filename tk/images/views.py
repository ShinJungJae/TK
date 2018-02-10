from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .import models, serializers

# class ListAllImages(APIView):
#
#     def get(self, request, format=None):
#
#         all_images = models.Image.objects.all()
#
#         serializer = serializers.ImageSerializer(all_images, many=True)
#
#         return Response(data=serializer.data)
#
#
# class ListAllComments(APIView):
#
#     def get(self, request, format=None):
#
#         all_comments = models.Comment.objects.all()
#
#         serializer = serializers.CommentSerializer(all_comments, many=True)
#
#         return Response(data=serializer.data)
#
#
# class ListAllLikes(APIView):
#
#     def get(self, request, format=None):
#
#         all_likes = models.Like.objects.all()
#
#         serializer = serializers.LikeSerializer(all_likes, many=True)
#
#         return Response(data=serializer.data)

class Feed(APIView):

    def get(self, request, format=None):

        user = request.user

        print("user : ", user)

        following_users = user.following.all()

        print("following_users : ", following_users)

        image_list = []

        for following_user in following_users:

            print("following_user.images.all() : ", following_user.images.all()[:2])

            user_images = following_user.images.all()[:2]

            for image in user_images:

                image_list.append(image)

        print("image_list : ", image_list)

        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)

        print("sorted_list : ", sorted_list)

        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)

# Line 63 에 함수를 이용하여 key 정렬을 할수도 있으나 lambda 함수를 이용함
# sorted_list = sorted(image_list, key=getkey, reverse=True)
# def getkey(image):
#     return image.created_at

class LikeImage(APIView):

    def post(self, request, image_id, format=None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisiting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)

        except models.Like.DoesNotExist:

            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )

            new_like.save()

            return Response(status=status.HTTP_201_CREATED)

class UnLikeImage(APIView):

    def delete(self, request, image_id, format=None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisiting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )

            preexisiting_like.delete()

            return Response(status=status.HTTP_202_ACCEPTED)

        except models.Like.DoesNotExist:

            return Response(status=status.HTTP_304_NOT_MODIFIED)



class CommentOnImage(APIView):

    def post(self, request, image_id, format=None):

        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)

        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(creator=user, image=found_image)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        else:

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):

    def delete(self, request, comment_id, format=None):

        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)

            comment.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Comment.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)















