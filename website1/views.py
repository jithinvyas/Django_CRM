from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()

    # To Login...
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authintication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You have been logged in Successfully")
            return redirect('home')
        
        else:
            messages.success(request, "There was an Error while Logging. Try Again!!!")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "You have been Loggedout Successfully")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have been registerd Successfully")
        
    else:
        form = SignupForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # fetch that record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be Loggedin to view that Page")
        return redirect('home')
    

def delete_customer(request,pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record(s) deleted Successfully!!!")
        return redirect('home')
    else:
        messages.success(request, "You must be Loggedin to do that!!!")
        return redirect('home')
    

def add_customer(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method=='POST':
            if form.is_valid():
                add_customer = form.save()
                messages.success(request, 'Record added Successfully!!!')
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be Loggedin!!!")
        return redirect('home')
    
def update_customer(request,pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been Updated!')
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You must be Loggedin to Update...")
        return redirect('home')