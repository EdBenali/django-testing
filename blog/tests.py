from datetime import timedelta

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import BlogPost


class BlogPostModelTests(TestCase):
    def test_str_returns_title(self):
        post = BlogPost(title="Hello", text="World")
        self.assertEqual(str(post), "Hello")

    def test_default_ordering_newest_first(self):
        older = timezone.now() - timedelta(days=1)
        newer = timezone.now()
        BlogPost.objects.create(title="Old", text="Old post", published_at=older)
        BlogPost.objects.create(title="New", text="New post", published_at=newer)

        titles = list(BlogPost.objects.values_list("title", flat=True))
        self.assertEqual(titles, ["New", "Old"])

    def test_create_post_persists_fields(self):
        published_at = timezone.now()
        post = BlogPost.objects.create(
            title="Test title",
            text="Test body",
            published_at=published_at,
        )
        reloaded = BlogPost.objects.get(pk=post.pk)
        self.assertEqual(reloaded.title, "Test title")
        self.assertEqual(reloaded.text, "Test body")
        self.assertEqual(reloaded.published_at, published_at)


class BlogPostAdminTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )
        self.client.force_login(self.user)

    def test_blog_post_registered_in_admin(self):
        self.assertIn(BlogPost, admin.site._registry)

    def test_changelist_loads(self):
        response = self.client.get(reverse("admin:blog_blogpost_changelist"))
        self.assertEqual(response.status_code, 200)

    def test_add_page_loads(self):
        response = self.client.get(reverse("admin:blog_blogpost_add"))
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_create_post_via_admin(self):
        response = self.client.post(
            reverse("admin:blog_blogpost_add"),
            {
                "title": "Admin post",
                "text": "Created via admin",
                "published_at_0": "2026-06-15",
                "published_at_1": "12:00:00",
            },
        )
        self.assertEqual(BlogPost.objects.count(), 1)
        self.assertEqual(BlogPost.objects.get().title, "Admin post")
        self.assertEqual(response.status_code, 302)


class BlogPostListViewTests(TestCase):
    def test_list_view_returns_200(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertEqual(response.status_code, 200)

    def test_list_view_shows_empty_message(self):
        response = self.client.get(reverse("blog:post_list"))
        self.assertContains(response, "No posts yet.")

    def test_list_view_shows_post_titles(self):
        BlogPost.objects.create(title="First post", text="Body one")
        BlogPost.objects.create(title="Second post", text="Body two")

        response = self.client.get(reverse("blog:post_list"))
        self.assertContains(response, "First post")
        self.assertContains(response, "Second post")

    def test_list_view_orders_newest_first(self):
        older = timezone.now() - timedelta(days=1)
        newer = timezone.now()
        BlogPost.objects.create(title="Older post", text="Old", published_at=older)
        BlogPost.objects.create(title="Newer post", text="New", published_at=newer)

        response = self.client.get(reverse("blog:post_list"))
        content = response.content.decode()
        self.assertLess(content.index("Newer post"), content.index("Older post"))


class BlogPostDetailViewTests(TestCase):
    def setUp(self):
        self.post = BlogPost.objects.create(title="Detail post", text="Full body text")

    def test_detail_view_returns_200(self):
        response = self.client.get(
            reverse("blog:post_detail", args=[self.post.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_view_shows_title_and_text(self):
        response = self.client.get(
            reverse("blog:post_detail", args=[self.post.pk])
        )
        self.assertContains(response, "Detail post")
        self.assertContains(response, "Full body text")

    def test_detail_view_returns_404_for_missing_post(self):
        response = self.client.get(reverse("blog:post_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)
