from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, PostLike, PostUnlike
from .serializer import RegisterSerializer, UserSerializer, PostSerializer, UserActivitySerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication


class RegisterApiView(generics.GenericAPIView):
    """ API for registration user """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'message': "User Created Successfully. Now perform Login to get your token",
        })


class UserActivityView(generics.ListAPIView):
    """ API for getting users activities """
    permission_classes = [permissions.AllowAny]

    queryset = User.objects.all()
    serializer_class = UserActivitySerializer


class PostListApiView(generics.ListAPIView):
    """ API for returning all posts """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostLikesAnalyticsView(APIView):
    """ API for returning analytics """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *arg, **kwargs):
        likes = PostLike.objects.filter(published_at__range=[kwargs.get('date_from'), kwargs.get('date_to')])
        unlikes = PostUnlike.objects.filter(published_at__range=[kwargs.get('date_from'), kwargs.get('date_to')])
        liked_posts, unliked_posts = {}, {}
        for liked_post in likes:
            liked_posts[liked_post.post.name] = 'liked'
        for unliked_post in unliked_posts:
            unliked_posts[unliked_post.post.name] = 'unliked'
        return Response(
            {f"Count of likes {likes.count()}, "
             f"count of unlikes {unlikes.count()}",
             f'{liked_posts} , '
             f'{unliked_posts}'},
            status.HTTP_200_OK
        )


class PostApiView(APIView):
    """ API for Post creation """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        author = request.user
        post = Post(author_id=author.id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):
    """ API for like """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        author = request.user
        post = Post.objects.get(id=pk)
        if PostLike.objects.filter(user_id=author.id, post_id=post.id).exists():
            return Response({"message": "You're already liked this post"}, status.HTTP_200_OK)
        else:
            PostLike.objects.create(post=post, user=author)
            if PostUnlike.objects.filter(user_id=author.id, post_id=post.id).exists():
                PostUnlike.objects.get(user_id=author.id, post_id=post.id).delete()
                print("Thank you for removing unlike")
            return Response({"message": "Thanks for your like"}, status.HTTP_201_CREATED)


class UnlikeView(APIView):
    """ API for like """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        author = request.user
        post = Post.objects.get(id=pk)
        if PostUnlike.objects.filter(user_id=author.id, post_id=post.id).exists():
            return Response({"message": "You're already unliked this post"}, status.HTTP_200_OK)
        else:
            PostUnlike.objects.create(post=post, user=author)
            if PostLike.objects.filter(user_id=author.id, post_id=post.id).exists():
                PostLike.objects.get(user_id=author.id, post_id=post.id).delete()
                print("Thank you for removing unlike")
            return Response({"message": "Thanks for your review"}, status.HTTP_201_CREATED)
