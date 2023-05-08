from django.shortcuts import render, HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
def home(request):
    return render(request,'home/home.html')

def about(request):
    return render(request,'home/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request,'Please Fill Foam Correctly')
        else:
            contact = Contact(name=name,email=email,phone=phone,content=content)
            contact.save()
            messages.success(request,'Your Messeage is Sent')
    return render(request,'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78 or query == "":
        allPosts = []
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    
    if len(allPosts) == 0:
       messages.warning(request,'No search Result Found')

    params = {'allPosts':allPosts,'query':query}
    return render(request,'home/search.html',params)

def handleSignup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 10:
            messages.error(request,'Username must be under 10 character')
            return redirect('home')
        if not username.isalnum():
            messages.error(request,'Username must be alpha numeric')
            return redirect('home')
        if pass1 != pass2:
            messages.error(request,'Password do not match')
            return redirect('home')
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,'Your Account has Created')
        return redirect('home')

    else:
        return HttpResponse('404 Not Found')

def handleLogin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername,password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully Logged In')
            return redirect('home')
        else:
            messages.error(request,'Invalid Username or Password')
            return redirect('home')
       
    return HttpResponse('404 not Found')

def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully Logged Out')
    return redirect('home')