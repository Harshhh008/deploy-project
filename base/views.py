from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm,MyUserCreationForm

# Create your views here.
def loginuser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=="POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password') 
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,'User does not exist')
            
        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,'successfully login')
            return redirect('home')
        else:
            messages.error(request,'username or password does not exist')
             
    context = {'page':page}
    return render(request,'base/login-register.html',context) 

def userlogout(request):
    logout(request)
    return redirect('home')

def userregistration(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #commit works for dont immidatly save
            user.username = user.username.lower() #first convert username into lower case
            user.save() #finaly save
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'enter valid username or password')
            return redirect('register')
    else:
        return render(request,'base/login-register.html',{'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)                       
        ) 
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    recent_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'recent_messages':recent_messages}
    return render(request,'base/home.html',context)

@login_required(login_url="login")
def user_profile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    recent_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user,'rooms':rooms,'recent_messages':recent_messages,'topics':topics}
    return render(request,'base/user_profile.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    print(participants)
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room',pk=room.id)
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)

@login_required(login_url='login')
# for creating room
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        form = RoomForm(request.POST)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        ) 
        return redirect('home')
    context = {'form' : form , 'topics':topics}
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
#for updating room
def update_room(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('<h1>You are not allowed here</h1>')
    if request.method == "POST":
        form = RoomForm(request.POST,instance=room)
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form, 'topics':topics,'room':room} 
    return render(request,'base/room_form.html',context)

@login_required(login_url='login')
def delete_room(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})
                  
@login_required(login_url='login')
def delete_message(request,pk):
    messages = Message.objects.get(id=pk)
    
    if request.user != messages.user:
        return HttpResponse('You are not allowed here!')
    if request.method == "POST":
        messages.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})
                  
@login_required(login_url='login')
def UpdateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == "POST":
        form = UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    context = {'form':form}
    return render(request,'base/update-user.html',context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics' : topics}
    return render(request,'base/topics.html',context)

def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    return render(request,'base/activity.html',context)