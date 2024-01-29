from django.db import models
from users.models import CustomUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_resized import ResizedImageField
import os
import shutil
from cloudinary.models import CloudinaryField


def post_image_upload_to(instance, filename):
    # Get the post title
    post_title = instance.post.title

    # Generate a unique filename
    base_filename, file_extension = os.path.splitext(filename)
    unique_filename = f"{base_filename}_{instance.id}{file_extension}"

    # Generate the path for the image
    directory_path = f"mysite/files/postimages/{post_title}"
    image_path = os.path.join(directory_path, unique_filename)

    return image_path


class PostImage(models.Model):
    image = ResizedImageField(size=[640, 360], upload_to=post_image_upload_to, blank=True, null=True)
    # image = CloudinaryField('image', blank=True, null=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name='images')


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, default=None, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username} on post {self.post.title}"


class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, default=None, related_name='tags')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=55, unique=True, blank=False)
    body = models.TextField()
    user = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT, blank=False)
    published = models.DateTimeField('Date published', default=timezone.now)
    modified = models.DateTimeField('Date modified', default=timezone.now)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the post images directory
        post_images_directory = os.path.join('mysite/files/postimages', self.title)
        shutil.rmtree(post_images_directory, ignore_errors=True)

        # Call the parent delete() method to delete the post
        super().delete(*args, **kwargs)


class NewsFeedItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    followed_by = models.ForeignKey(
        CustomUser, related_name='followed_by', on_delete=models.CASCADE, blank=True, null=True)
    unfollowed_by = models.ForeignKey(
        CustomUser, related_name='unfollowed_by', on_delete=models.CASCADE, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    like = models.ForeignKey(Like, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    ACTIVITY_CHOICES = [
        ('like', 'Like'),
        ('unfollow', 'Unfollow'),
        ('post', 'New Post'),
        ('follow', 'Follow'),
    ]
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_CHOICES, blank=True, null=True)

    def __str__(self):
        if self.post:
            return f"{self.user.username} posted: {self.post.title}"
        elif self.like:
            return f"{self.user.username} liked: {self.like.post.title}"
        elif self.followed_by:
            return f"{self.user.username} followed: {self.followed_by.username}"
        elif self.unfollowed_by:
            return f"{self.user.username} unfollowed: {self.unfollowed_by.username}"