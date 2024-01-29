import random
import requests
import os
import tempfile
from users.models import CustomUser
from main.models import Post, PostImage, Like, Tag
from django.conf import settings
from django.contrib.auth.hashers import make_password
from faker import Faker
from django.core.management.base import BaseCommand, CommandError


def fill_fake_data_user(number_of_records=1):
    fake = Faker()
    password = 'qqq'
    for _ in range(number_of_records):
        user = CustomUser.objects.create(
            username=fake.name().split(' ')[0],
            email=fake.email(),
            bio=fake.text(),
            password=make_password(password)

        )
        user.save()
        random_avatar(user)


def fill_fake_data_post(number_of_records=1):
    fake = Faker()
    for _ in range(number_of_records):
        users = CustomUser.objects.all()
        post = Post.objects.create(
            title=f"{fake.name().split(' ')[0]}{fake.pystr(min_chars=None, max_chars=1)}",
            body=fake.text(),
            user=random.choice(users),
        )
        post.save()

        post_image = PostImage.objects.create(post=post)
        post_image.save()
        random_image(post_image)

        for _ in range(random.randint(1, 10)):
            like = Like.objects.create(post=post, user=random.choice(users))
            like.save()
            tag = Tag.objects.create(name=f'#{fake.pystr(min_chars=None, max_chars=5)}',
                                     post=post, user=random.choice(users))
            tag.save()


def random_avatar(custom_model):
    api_url = 'https://api.api-ninjas.com/v1/randomimage'
    response = requests.get(api_url, headers={'X-Api-Key': 'Yj+RENMPEtWlOdTaT2wpTw==fV57yhHCAiHfSyRY', 'Accept': 'image/jpg'}, stream=True)
    if response.status_code == requests.codes.ok:
        # Create a temporary file to save the image data
        custom_directory = os.path.join(settings.BASE_DIR, 'bin', 'fake_data', 'avatars')
        with tempfile.NamedTemporaryFile(delete=True, suffix='.jpg', dir=custom_directory) as temp_file:
            for chunk in response.iter_content(chunk_size=128):
                temp_file.write(chunk)
            # save tempfile to models field
            print(temp_file.read())
            custom_model.avatar.save(os.path.basename(temp_file.name), temp_file.file)
    else:
        print("Error:", response.status_code, response.text)
        return None


def random_image(custom_model):
    api_url = 'https://api.api-ninjas.com/v1/randomimage'
    response = requests.get(api_url, headers={'X-Api-Key': 'Yj+RENMPEtWlOdTaT2wpTw==fV57yhHCAiHfSyRY', 'Accept': 'image/jpg'}, stream=True)
    if response.status_code == requests.codes.ok:
        # Create a temporary file to save the image data
        custom_directory = os.path.join(settings.BASE_DIR, 'bin', 'fake_data', 'post_images')
        with tempfile.NamedTemporaryFile(delete=True, suffix='.jpg', dir=custom_directory) as temp_file:
            for chunk in response.iter_content(chunk_size=128):
                temp_file.write(chunk)
            # save tempfile to models field
            custom_model.image.save(os.path.basename(temp_file.name), temp_file)
    else:
        print("Error:", response.status_code, response.text)
        return None


class Command(BaseCommand):
    help = "Fill an app a fake data"

    def add_arguments(self, parser):
        parser.add_argument("model_types", nargs="+", type=str)
        parser.add_argument("number_of_records", nargs="+", type=int)

    def handle(self, *args, **options):
        for model_type in options["model_types"]:
            if model_type == 'user':
                fill_fake_data_user(options["number_of_records"][0])
                self.stdout.write(
                    self.style.SUCCESS('database was filled with users.')
                )
            elif model_type == 'post':
                fill_fake_data_post(options["number_of_records"][0])
                self.stdout.write(
                    self.style.SUCCESS('database was filled with posts.')
                )

