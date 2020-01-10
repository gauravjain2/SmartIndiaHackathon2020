from django.shortcuts import render,redirect
from .forms import UserForm,BuyerSignupForm
from django.contrib import messages
from django.contrib.auth import authenticate,login

# Create your views here.



def register(request):
    if request.method=="POST":
        form=UserForm(data=request.POST)
        bform=BuyerSignupForm(data=request.POST)
        if form.is_valid() and bform.is_valid():
            user=form.save(commit=False)
            user.username=form.cleaned_data['email']
            user.save()
            profile=bform.save(commit=False)
            profile.user=user
            profile.save()
            messages.success(request,'Your account has been created !')
            return redirect('home')

        else:
            print(form.errors)
            print(bform.errors)
            messages.warning(request,form.errors)
            messages.warning(request,bform.errors)
            return redirect('buyer:buyersignup')

    else:
        form=UserForm()
        bform=BuyerSignupForm()

    return render(request,'buyer/buyer_signup.html',{'form':form,'bform':bform})


def user_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        print(email,password)
        user = authenticate(username=email, password=password)
        if user:
            if user.is_active and user.buyerprofile.is_buyer:
                login(request, user)
                messages.success(request, f'You are logged in successfully!')
                return redirect('home')

        else:
            messages.error(request,'Please Check your username and password !')
    return render(request,'buyer/buyer_login.html')
