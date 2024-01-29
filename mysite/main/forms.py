from cloudinary.forms import CloudinaryFileField
from django import forms
from .models import Post, PostImage
# from users import CustomUser


class PostCreateForm(forms.ModelForm):
    # image = forms.ImageField(label='Post Image', required=False)
    tag = forms.CharField(max_length=10)

    class Meta:
        model = Post

        fields = [
            "title",
            "body",
        ]


class PostUpdateForm(forms.ModelForm):
    # image = forms.ImageField(label='Post Image', required=False)
    tag = forms.CharField(max_length=10)

    class Meta:
        model = Post

        fields = [
            "title",
            "body",
        ]
