from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Post, PostImage, Like, Tag, NewsFeedItem
from users.models import CustomUser
from .decorators import user_is_auth
from .forms import PostCreateForm, PostUpdateForm
from django.contrib.auth import get_user_model
from PIL import Image
from io import BytesIO


def create_news_feed_item(user, post=None, like=None, follow=None, unfollowed_by=None, activity_type=None):
    NewsFeedItem.objects.create(
        user=user, post=post, like=like, followed_by=follow, unfollowed_by=unfollowed_by, activity_type=activity_type)



def homepage(request):
    post = Post.objects.all()

    return render(request=request,
                  template_name='main/home.html',
                  context={
                      "objects": post,
                      "user:": request.user
                  }
                  )


def post_view(request, post_id):
    post = Post.objects.filter(id=post_id).first()

    return render(request=request,
                  template_name='main/post.html',
                  context={"object": post}
                  )


@user_is_auth
def post_create(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user

            post.save()

            tag_name = form.cleaned_data['tag']
            post.tags.create(name=tag_name, user=post.user, post=post)

            # Process the post images
            images = request.FILES.getlist('images')  # Retrieve all uploaded images
            for image in images:
                PostImage.objects.create(image=image, post=post)

            create_news_feed_item(user=request.user, post=post, activity_type='post')

            return redirect('/')
    else:
        form = PostCreateForm()
    return render(request, 'main/new_record.html', {'form': form})


@user_is_auth
def post_update(request, post_id: int):
    post = Post.objects.filter(id=post_id).first()

    if request.method == "POST":
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()

            tag_name = form.cleaned_data['tag']
            post.tags.create(name=tag_name, user=post.user, post=post)

            images = request.FILES.getlist('images')  # Retrieve all uploaded images
            for image in images:
                PostImage.objects.create(image=image, post=post)

            return redirect(f'/{post.id}')

    else:
        form = PostUpdateForm(instance=post)

        return render(
            request=request,
            template_name='main/new_record.html',
            context={
                "form": form
            }
        )



@csrf_exempt
@user_is_auth
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    try:
        # check
        like = Like.objects.get(user=user, post=post)
        like.delete()  # delete
        liked = False
    except Like.DoesNotExist:
        like = Like.objects.create(user=user, post=post)  # add
        liked = True
        create_news_feed_item(user=user, like=like, activity_type='like')

    # Get the updated like count
    like_count = post.likes.count()

    return JsonResponse({'liked': liked, 'like_count': like_count})


@user_is_auth
def post_delete(request, post_id: int):
    post = Post.objects.filter(id=post_id).first()

    if request.method == 'POST':
        post.delete()
        return redirect('/')
    else:
        return render(request, 'main/confirm_delete.html', {'object': post})


def news_feed(request):
    following_users = request.user.following.all()
    followers_users = request.user.followers.all()

    feed_items_user = NewsFeedItem.objects.filter(Q(user=request.user))
    q1 = NewsFeedItem.objects.filter(user__in=following_users)
    q2 = NewsFeedItem.objects.filter(user__in=followers_users)

    feed_items = feed_items_user.union(q1, q2).order_by('-timestamp')
    context = {
        'feed_items': feed_items,
    }
    return render(request, 'main/feed.html', context)



