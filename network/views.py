from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from .models import User, Post, Following, Like
import json
from django.middleware.csrf import get_token


class NewPostForm(forms.Form):
    post = forms.CharField(label="", widget=forms.Textarea(attrs={
        "class": "form-control", 
        "required": True,
        "rows": 3,
        "cols": 200
        }))

class EditPostForm(forms.Form):
    post = forms.CharField(label="", widget=forms.Textarea(attrs={
        "class": "form-control", 
        "required": True,
        "rows": 3,
        "cols": 200
        }))

def index(request):
    username = request.user
    print(username)
    posts = Post.objects.all().order_by("-created_at")

    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:

        page_obj = p.page(1)
    except EmptyPage:

        page_obj = p.page(p.num_pages)
        

    return render(request, "network/index.html", 
                  {'posts': posts, 'page_obj': page_obj, 
                   'form': NewPostForm(), 'username': username, 'paginator': p})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")
    
       
def new_post(request):
    
    if request.method == "POST":
        
        try:
            newpost = request.POST["newpost"]
        except:
            pass
        
        form = NewPostForm(request.POST)
        
        if form.is_valid():
            post = form.cleaned_data["post"]
            print(post)
            
            date = timezone.now()
        
            username = request.user.username

            newpost = Post.objects.create(username=username, content=post, created_at=date)
            newpost.save()
    
            return HttpResponseRedirect(reverse('network:index'))
        
        else:
            return render(request, "network/index.html", {'form': form})
    
    return render(request, "network/index.html", {'form': NewPostForm()})

def profile(request):

    username = request.user.username
    posts = Post.objects.all().order_by("-created_at").filter(username=username)
    user = User.objects.filter(username=username)
    try:
        following = user.following.all()
        count = following.count() 
    except:
        count = 0
        
    p = Paginator(posts, 10)
    
    page_number = request.GET.get('page')
    
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:

        page_obj = p.page(1)
    except EmptyPage:

        page_obj = p.page(p.num_pages)  

    return render(request, "network/profile.html", {'username': username, 'profile': profile, 'page_obj': page_obj, 'posts': posts, 'count': count})
    



def following(request):
    username = request.user.username

    try:
        user = User.objects.get(username=username)
        following = user.following.all()
    except:
        following = ""
        
    posts = Post.objects.all().order_by("-created_at")
    posts_list = []
    
    for post in posts:
        for follow in following:
            if post.username == follow.username:
                posts_list.append(post)

    
    p = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:

        page_obj = p.page(1)
    except EmptyPage:

        page_obj = p.page(p.num_pages)
        
    return render(request, "network/following.html", {'page_obj': page_obj})


def edit(request):

    if request.method == 'POST':

        try:
            post_id = request.POST["post_id"]
            post = Post.objects.get(id=post_id)   
        except:
            pass

        form = EditPostForm(request.POST)
        
        if form.is_valid():
            p = form.cleaned_data["post"]
            post_id = request.POST["id"]
            post = Post.objects.get(id=post_id)
    
            post.content = p
            post.save()
            
            return HttpResponseRedirect(reverse('network:index'))
        else:
            return render(request, "network/edit.html", {'post': post, 'form': form})


    return render(request, "network/edit.html", {"form": EditPostForm()})


def fetch_data(request):
    data = Post.objects.all().values().order_by("-created_at")
    return JsonResponse(list(data), safe=False)


def post_data(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        user = request.user.username
        u = User.objects.get(username=user)
        print(u.id)
        post_id = body['post_id']
        print(post_id)
        post = Post.objects.get(id=post_id)
        post.likes = body['likes']
        post.is_liked = body['is_liked']
        post.save() 
        
        if post.is_liked:
            like = Like.objects.create(user=u, post=post)
            like.save()
        else:
            like = Like.objects.filter(user=u, post=post)
            like.delete()
        
        
        likes = Like.objects.all()
    
        print(likes)

        
    return JsonResponse("success", safe=False)


def get_csrf_token(request):
    csrf_token = get_token(request)
    return csrf_token


def user_profile(request, username):
    
    if request.user.username:
        
    
        posts = Post.objects.all().order_by("-created_at").filter(username=username)
        profile = User.objects.filter(username=username)
        user = request.user.username

        p = Paginator(posts, 10)
        page_number = request.GET.get('page')
        
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages) 
            
        if request.method == "POST":
            follow_button = request.POST["follow_button"]
            profilename = request.POST["user"]
                
                
            if follow_button == "Follow":
                        
                user1 = User.objects.get(username=username)
                user1.save()
                
                user2 = User.objects.get(username=profilename)
                user2.has_followers += 1
                user2.save()
                
                f = Following.objects.create(username=profilename)
                f.save()
                
                user1.following.add(f)
                user1.save()
                
                return HttpResponseRedirect(reverse("network:index"))      
            else:
                user1 = User.objects.get(username=username)
                user1.save()
                
                user2 = User.objects.get(username=profilename)
                user2.has_followers -= 1
                user2.save()
                
                user1.following.filter(username=profilename).delete()
    
                return HttpResponseRedirect(reverse("network:index")) 
            
        u = User.objects.get(username=request.user.username)
        
        try:
            following = u.following.all()
            count = following.count()
        except:
            count = 0
            
        is_followed = ""
        
        try:
            for follow in following:
                if profile[0].username == follow.username:
                    is_followed = follow.username
        except:
            pass
            
        return render(request, "network/user_profile.html", {'page_obj': page_obj, 'profile': profile, 'username': user, 'is_followed': is_followed, 'following': following, 'count': count})
    
    else:
        return render(request, "network/error.html")
    
    
def error(request):
    return render(request, "network/error.html")