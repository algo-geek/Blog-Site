from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404
from . models import Post
from . models import Profile

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):

    profiles = Profile.objects.all().order_by("-time")
    posts = Post.objects.all().order_by("-time")
    context = {
        "posts":posts,
        "profiles":profiles,
    }
    print(posts)
    return render(request,'home.html', context)

@login_required(login_url='signup')    
def addpost(request):
    if request.method =="POST":
        title =  request.POST.get('title','')
        description = request.POST.get('description','')



        thumb =  request.FILES.get('thumbnail','')
        prof = Profile.objects.filter(prof_user=request.user)[0]

        post_blog = Post(title=title, description=description, image=thumb, author=prof)



        post_blog.save()
        messages.success(request,"Thanks For Posting")

    return render(request,"addpost.html")    

def single_post(request, pk):
    single_post=Post.objects.filter(pk=pk)[0]
    context={
        "post":single_post
    }
    return render(request,"single_post.html", context)

def search(request):
    if request.method =="POST":

        search_text=request.POST.get('search_text','')
        print(search_text)

        allpost_title = Post.objects.filter(title__icontains = search_text)
        allpost_content = Post.objects.filter(description__icontains = search_text)
        allposts = allpost_title.union(allpost_content)

        context={
            "txt":search_text,
            "search_post":allposts

        }


        return render(request, 'search.html', context)

    else:
        raise Http404()        

# def addprofile(request):
#     if request.method=="POST":
#         name = request.POST.get('name','')
#         about = request.POST.get('about','')
#         print(name)
#         print(about)

#         dp=request.FILES.get('dp','')
#         profl = Post(title=name, description=about, image=dp)
#         profl.save()
#         messages.success(request,"Account has been created")

#     return render(request,"addprofile.html")    

def signup(request):
    if request.method =="POST":
        name =  request.POST.get('name','')
        username = request.POST.get('username','')
        email =  request.POST.get('email','')
        password = request.POST.get('password','')
        confpassword = request.POST.get('confpassword','')
        userCheck = User.objects.filter(username=username)
        if len(username)>20:
            messages.warning(request,"Too Long Username!!")
        elif password != confpassword:
            messages.warning(request,"Passwords Don't Match!!")    
        elif userCheck:
            messages.warning(request,"Username Already Exist, Kindly Change!!")   
        else:
            user_obj = User.objects.create_user(first_name=name, email=email, password=password, username=username)
            user_obj.save()
            messages.success(request,"Account Created Successfully!!")

    return render(request,"signup.html")    

def login_(request):
    if request.method =="POST":

        username = request.POST.get('username','')
        password = request.POST.get('password','')
        print(username)
        print(password)
        user_obj = authenticate(username=username, password=password)
        user_obj2 = User.objects.filter(username=username)[0]
        if user_obj is not None:
            login(request, user_obj)
            # messages.success(request,"Logged In Successfully:^) ")
            return redirect('/profile/' + str(user_obj2.pk))
        else:
            messages.warning(request,"Invalid Credentials : ( ") 
            return redirect('/signup')
    else:
        return render(request, "signup.html")

@login_required(login_url='signup') 
def profile(request, pk):
    prof = Profile.objects.filter(pk=pk)[0]
    posts = Post.objects.filter(author=prof).order_by("-time")
    postno = len(posts)
    context={
        "prof":prof,
        "posts":posts,
        "postno":postno
        
    }
    return render(request,"profile.html", context)

def edit_post(request, pk): 
    pos=Post.objects.filter(pk=pk)[0]
    context={
        'i':pos
    }
    if pos.author.prof_user==request.user:
        if request.method=="POST":
            title = request.POST.get('title','') 
            description = request.POST.get('description','')
            image =  request.FILES.get('thumbnail','')
            if title:
               pos.title=title
            if description:   
               pos.description=description
            if image:
                pos.image=image   

            pos.save()
            return redirect('/profile/' + str(request.user.pk))
        return render(request,"edit_post.html", context) 
    else:
        raise Http404()

@login_required(login_url='signup')
def edit_profile(request, pk): 
    prf=Profile.objects.filter(pk=pk)[0]
    context={
        'i':prf
    }
    if prf.prof_user==request.user:
        if request.method=="POST":

            about = request.POST.get('about','')
            prfp =  request.FILES.get('prfp','')
            if about:
                prf.occupation=about
            
            if prfp:
                prf.dp=prfp
   
    

            prf.save()
            return redirect('/profile/' + str(request.user.pk))   
        return render(request,"edit_profile.html", context) 
    else:
        raise Http404()        

def log_out(request):
    logout(request)

    return redirect("/")

def delete(request):
    
    user = request.user
    user.delete()

    return redirect("/")    
  
# def forgot_pass(request):

def delete_post(request, pk):
    pos=Post.objects.filter(pk=pk)[0]

    context={
        'i':pos
    }
    if pos.author.prof_user==request.user:
        pos.delete()
        return redirect('/profile/' + str(request.user.pk))
 


