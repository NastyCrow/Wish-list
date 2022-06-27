import bcrypt
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
# Create your views here.
def index(request):
    if 'signedIn' not in request.session:
        request.session['signedIn'] =False
    elif request.session['signedIn'] ==True:
        return redirect('/dashboard')
    return render(request, 'main.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
            request.session["signedIn"] = False
        return redirect("/")
    else:
        if request.method == 'POST':
            password_hash = bcrypt.hashpw(request.POST.get(
                'password').encode(), bcrypt.gensalt()).decode()
            User.objects.create(name=request.POST.get(
                'name'), username=request.POST.get('username'), hired_date=request.POST.get('hired_date'), password=password_hash)
            
            request.session["username"]=request.POST.get('username')
            request.session["signedIn"] = True
            return redirect("/dashboard")
    return redirect("/")

def dashboard(request):
    if request.method == 'POST' or request.session.get('signedIn')==True:
        user= User.objects.get(username=request.session["username"])
        context={
            "user":user,
            "all_items":Item.objects.exclude(user_who_wish=user),
        }
        return render(request,'dashboard.html',context)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        request.POST.get('username')
        try:
            user = User.objects.filter(username= request.POST.get('username'))[0]
        except IndexError:
            messages.error(request, "Sorry, the username is not registered")
            return redirect('/')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session["username"] = user.username
            request.session["signedIn"] = True
            return redirect("/dashboard")
    return redirect("/")

def logout(request):
    request.session.flush()
    return redirect('/')

def create_item(request):
    if request.method == 'POST':
        errors = Item.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/wish_items/create")
        else:
            user= User.objects.get(username=request.session["username"])
            Item.objects.create(name=request.POST.get("item_name"),created_by=user)
            user.whish_list.add(Item.objects.last())
            return redirect('/dashboard')
    elif request.session.get('signedIn')==True:
        return render(request, 'create_item.html')
    else:
        return redirect('/')

def add_item(request,id):
    user = User.objects.get(username=request.session["username"])
    user.whish_list.add(Item.objects.get(id=int(id)))
    return redirect('/dashboard')
    
def remove_item(request,id):
    user = User.objects.get(username=request.session["username"])
    user.whish_list.remove(Item.objects.get(id=int(id)))
    return redirect('/dashboard')

def delete_item(request,id):
    item_to_delete=Item.objects.get(id=int(id))
    item_to_delete.delete()
    item_to_delete=None
    return redirect('/dashboard')

def show_item(request,id):
    context={
        "item":Item.objects.get(id=int(id))
    }
    return render(request, 'item.html',context)

