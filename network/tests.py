from django.test import Client, TestCase
from .models import Post, Like, User, Following
from django.utils import timezone


date = timezone.now()
    
# Create your tests here.
class TestPost(TestCase):
    
    def setUp(self):
        Post.objects.create(username="Sasha", content="test", created_at=date, likes=0, is_liked=False)
        
    def test_new_post(self):
        """New Post is created"""
        post = Post.objects.get(username="Sasha", content="test", created_at=date, likes=0, is_liked=False)
        self.assertEqual(post.username, "Sasha")
        self.assertEqual(post.content, "test")
        self.assertEqual(post.created_at, date)
        self.assertEqual(post.likes, 0)
        self.assertFalse(post.is_liked, False)
        
        
    def test_like_post(self):
        """Post is liked"""  
        post = Post.objects.get(username="Sasha", content="test", created_at=date, likes=0, is_liked=False)
        post.is_liked = True
        post.likes = 1
        post.save()
        self.assertTrue(post.is_liked, True)
        self.assertEqual(post.likes, 1)
        
    def test_dislike_post(self):
        """Post is disliked"""
        post = Post.objects.get(username="Sasha", content="test", created_at=date, likes=0, is_liked=False)
        post.is_liked = False
        post.likes = 0
        post.save()
        self.assertFalse(post.is_liked, False)
        self.assertEqual(post.likes, 0)
        
    def test_2_likes(self):
        """Post is liked"""
        Post.objects.create(username="Sasha", content="test", created_at=date, likes=1, is_liked=False)
        post = Post.objects.get(username="Sasha", content="test", created_at=date, likes=1, is_liked=False)
        post.is_liked = True
        post.likes += 1
        post.save()
        self.assertTrue(post.is_liked, True)
        self.assertEqual(post.likes, 2)
        
    def test_2_dislikes(self):
        """Post is disliked"""
        Post.objects.create(username="Sasha", content="test", created_at=date, likes=2, is_liked=True)
        post = Post.objects.get(username="Sasha", content="test", created_at=date, likes=2, is_liked=True)
        post.is_liked = False
        post.likes -= 1
        post.save()
        self.assertFalse(post.is_liked, False)
        self.assertEqual(post.likes, 1)
        

class TestFollowing(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="User", password="123")
        self.user2 = User.objects.create(username="User2", password="123")
        self.u = Following.objects.create(username=self.user2)
        
    def test_follow(self):
        self.user.following.add(self.u)
        self.user.save()
        self.assertEqual(self.user.following.count(), 1)
        
    def test_unfollow(self):
        self.user.following.remove(self.u)
        self.user.save()
        self.assertEqual(self.user.following.count(), 0)
        
        
class TestPages(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_index(self):
        response = self.client.get('/indexs')
        self.assertEqual(response.status_code, 200)
        
    def test_profile(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        
    def test_following(self):
        response = self.client.get('/following')
        self.assertEqual(response.status_code, 200)
        
    def test_login(self):
        c = Client()
        response = c.post("/login", {"username": "john", "password": "smith"})
        self.assertEqual(response.status_code, 200)
        
        
class TestEditPost(TestCase):
    def setUp(self):
        Post.objects.create(username="Sasha", content="test", created_at=date, likes=0, is_liked=False)
        
    def test_edit(self):
        """Post is edited"""
        post = Post.objects.get(username="Sasha", content="test", created_at=date, likes=0, is_liked=False)
        post.content = "edited"
        post.save()
        self.assertEqual(post.content, "edited")
    
class TestFetchData(TestCase):
    def setUp(self):
        Post.objects.create(username="Sasha", content="test", created_at=date, likes=0, is_liked=False)
        
    def test_fetch_data(self):
        """Post is fetched"""
        post = Post.objects.get(username="Sasha", content="test", created_at=date, likes=0, is_liked=False)
        self.assertEqual(post.username, "Sasha")
        self.assertEqual(post.content, "test")
        self.assertEqual(post.created_at, date)
        self.assertEqual(post.likes, 0)
        self.assertFalse(post.is_liked, False)

class TestUserProfile(TestCase):
    def setUp(self):
        Post.objects.create(username="Sasha", content="test", created_at=date, likes=0, is_liked=False)
        
    def test_user_profile(self):
        """User Profile Page"""
        post = Post.objects.get(username="Sasha", content="test", created_at=date, likes=0, is_liked=False)
        self.assertEqual(post.username, "Sasha")
        self.assertEqual(post.content, "test")
        self.assertEqual(post.created_at, date)
        self.assertEqual(post.likes, 0)
        self.assertFalse(post.is_liked, False)
         
    
