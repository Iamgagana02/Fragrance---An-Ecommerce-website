from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import re                                                                    #-------------------- messages---------------------
from django.contrib import messages
                                                                    #--------------------- forgot------------------------
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
import random
import datetime
from .models import *
import razorpay
# import connection
from django.utils import timezone
from datetime import timedelta
from .models import *
from django.contrib import messages

                                                                         #--------- Create your views here.------------

#--------- INDEX PAGE.------------

def index(r):
    if 'id' in r.session:
        logged_in = True
        my_order=True
        user = register.objects.get(username=r.session['id'])
        datas = c_rt.objects.filter(user_det=user)
        wdata = Wishlist.objects.filter(user_details=user)
        # d = c_rt.objects.filter(user_det_id=r.session['id'])
        print(datas)
        # x=c_rt.objects.filter(user_det=r.session['id'])
        # d=c_rt.objects.filter(r.session['id'])
    else:
        logged_in = False
        my_order = False
        datas=None
        wdata=None
    obj = pro.objects.all()
    l = []
    for i in obj:
        if i.category == 'Best seller':
            l.append(i)
            print(l)
    return render(r,'index.html',{'data':logged_in,'l':l,'myod':my_order,'d':datas,'w':wdata})

                                                                             #--------- PATH FUNCTIONS PAGE.------------

def login(r):
    return render(r,'login.html')
def reg(r):
    return render(r,'registerr.html')
def o(r):
    a = Join.objects.get(username=r.session['emp'])

    return render(r,'employee_home.html',{'a':a})
def iid(r):
    return render(r,'employee_id.html')
def joini(r):
    return render(r,'join.html')
def adm(r):
    return redirect(view_details)
def a(r):
    return render(r,'admin-add_product.html')
def plog(r):
    return render(r,'please log in.html')
def ai(r):
    return render(r,'product_view.html')

def contact(r):
    return render(r,'contactus.html')


                                                                        # --------- FORGOT RESET PASSWORD.------------

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = register.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)
        det = register.objects.filter(email=email)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password',
                                             f'Hi user,'
                                             f'You recently requested to reset your password for your Fragrance Perfume account. Use the button below to reset it. This password reset is only valid for the next 24 hours.'
                                             f'If you did not request a password reset, please ignore this email.: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            # return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)
    return render(request, 'frgt.html')

def reset_password(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user.password=new_password
            password_reset.user.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_pass.html',{'token':token})


                                                                             # ---------  REGISTRATION. HERE------------

# --------- EMPLOYEE JOIN.HERE------------
def joins(request):
    if request.method =='POST':
        name =request.POST['name']
        email =request.POST['email']
        phone =request.POST['phone']
        location =request.POST['location']
        photo =request.FILES['pho']
        license =request.FILES['license']
        username =request.POST['username']
        password =request.POST['password']
        passwordc =request.POST['passwordc']
        biodata =request.FILES['biodata']
        accoundnumber =request.POST['accoundnumber']

        # Check if email or username already exists
        existing_email = Join.objects.filter(email=email).exists()
        existing_username = Join.objects.filter(username=username).exists()

        if existing_email:
            messages.error(request, 'Email ID is already registered. Please log in.')
        elif existing_username:
            messages.error(request, 'Username is already taken. Try with different username')
        else:
            if passwordc == password:
                request.session['emp'] = username
                data = Join.objects.create(name=name, email=email, phone=phone, location=location, photo=photo,
                                           license=license, username=username, password=password, biodata=biodata,
                                           accoundnumber=accoundnumber)
                data.save()
                messages.error(request, 'Thank you for registering. We will send you an email with further instructions.')

                z = 'fragranceperfumes98@gmail.com'
                # email_message = f"New employee request from: {data.name}"
                # send_mail('Request', f'{"Employes Waiting for  your Accept "}','settings.EMAIL_HOST_USER',[z],fail_silently=False)

                # z = data.user.email

                email_message = f"New employee request from: {data.name},{data.location},{data.email}"

                send_mail('Employes Waiting for  your Accept', email_message, settings.EMAIL_HOST_USER, [z],
                          fail_silently=False)
            else:
                messages.warning(request, 'oops..passwords doesnt match')


    return redirect(request.META.get('HTTP_REFERER', '/'))





# --------- USER REGISTER HERE------------
def regi(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        passwordc = request.POST['passwordc']

        try:
            # Check if email or username already exists
            existing_email = register.objects.filter(email=email).exists()
            existing_username = register.objects.filter(username=username).exists()

            if existing_email:
                messages.error(request, 'Email ID is already registered. Please log in.')
            elif existing_username:
                messages.error(request, 'Username is already taken. Try with different username')
            else:
                if password==passwordc:
                    # Create a new user if email and username are unique
                    data = register.objects.create(name=name, email=email, username=username, password=password)
                    z = data.email
                    send_mail('Congrats!!!', 'Successfully registered for Fragrance', 'settings.EMAIL_HOST_USER', [z], fail_silently=False)
                    messages.success(request, 'Registration successful!')
                    return redirect(login)  # Redirect to the login page
                else:
                    messages.warning(request, 'oops..passwords doesnt match')

        except Exception:
            return redirect(r1)
    return render(request, 'registerr.html')
def r1(re):
    return render(re,'registerr.html')


                                                                                # --------- LOGIN HERE.------------
def loginn(re):
    if re.method == 'POST':
        username = re.POST['username']
        password = re.POST['password']

        # Check for the register model
        try:
            data = register.objects.get(username=username)
            if data.password == password:
                re.session['id'] = username
                messages.success(re, 'Login successful')
                return redirect(index)
            else:
                messages.error(re, 'Invalid username or password')
                return redirect(login)
        except register.DoesNotExist:
            pass  # Username does not exist in register model

        # Check for the admin login
        if username == 'admin' and password == 'admin':
            re.session['id1'] = username
            return redirect(adm)

        # Check for the Join model
        try:
            datas = Join.objects.get(username=username)

            if datas.password == password:
                re.session['emp'] = username
                if datas.status==1:
                   return redirect(o)
                else:
                    return render(re,'Rejected.html')
            else:
# ______________________________________________________________________________________________________________________
                messages.error(re, 'Dear Employee, Check your username or password')
                return redirect(login)
        except Join.DoesNotExist:
            pass  # Username does not exist in Join model

        # If neither register nor Join has the username
        messages.error(re, 'Invalid username or password')
        return render(re, 'login.html')

    return render(re, 'login.html')


                                                                                 # --------- LOG-OUT HERE.------------
def logout(request):
    if 'id' in request.session or 'id2' in request.session :
        request.session.flush()
    return redirect(index)




                                                                                     # --------- ADMIN PANEL.------------
# --------- ADD-PRODUCTS.------------
def add(re):
    if re.method=="POST":

        name=re.POST['name']
        quantity=re.POST['quantity']
        price=re.POST['price']
        ingredients=re.POST['ingredients']
        netquantity=re.POST['netquantity']
        fragrance=re.POST['fragrance']
        category=re.POST['category']

        image = re.FILES['image']
        upload=pro.objects.create(name=name,quantity=quantity,price=price,ingredients=ingredients,
                                  netquantity=netquantity,fragrance=fragrance,image=image,category=category)
        upload.save()
        return render(re,'admin-add_product.html')

# --------- VIEW PRODUCTS.------------
def view_details(re):
    display=pro.objects.all()
    return render(re,'admin-added-all.html',{'data':display})

# --------- DELETE PRODUCT.------------
def delete(re,id):
    dele=pro.objects.get(id=id)
    dele.delete()
    return redirect(view_details)

                            # --------- UPDATE PRODUCTS.HERE------------
def upd(re,id):
    data=pro.objects.get(id=id)
    return render(re, 'update.html', {'updata': data})

def updatas(re,id):
    if re.method=='POST':
        name=re.POST['name']
        quantity=re.POST['quantity']
        price=re.POST['price']
        ingredients=re.POST['ingredients']
        netquantity=re.POST['netquantity']
        fragrance=re.POST['fragrance']
        category=re.POST['category']
        pro.objects.filter(id=id).update(name=name,quantity=quantity,price=price,ingredients=ingredients,netquantity=netquantity,category=category,fragrance=fragrance)
        return redirect(view_details)
    return render(re, 'admin-added-all.html')

                                                                    # --------- VIEW EMPLOYEE APPLICATIONS.------------
def registerd_d(re):
    r=register.objects.all()
    return render(re,'user_det.html',{'data':r})
def customerss(re):
    r=orderitem.objects.all()
    return render(re,'customer.html',{'data':r})
def joind_d(re):
    r=Join.objects.all()
    return render(re,'TRYS.html',{'data':r})


def joiemp(re):
    r=Join.objects.filter(status=1).all()

    return render(re,'TRYS2.html',{'data':r})

def joidassi(re):
    # r=Join.objects.all()
    # return render(re,'orderdistri.html')
    items=order.objects.all()
    datas=Join.objects.filter(status=1)
    l=[]
    z=[]
    for i in items:
        if i.status=='Shipped':
            l.append(i)

    for i in datas:
        z.append(i.id)
    return render(re,'orderdistri.html',{'items':l,'datas':z})

def distribute(re,id):
    print(id)
    print('this is id')
    a=Join.objects.get(id=id)


# --------- REJECTS APPLICATIONS.------------
def joind_rej(re,id):
    r=Join.objects.get(id=id)
    z = r.email
    # email_message = f"New employee request from: {data.name}"
    # send_mail('Request', f'{"Employes Waiting for  your Accept "}','settings.EMAIL_HOST_USER',[z],fail_silently=False)

    # z = data.user.email

    email_message = f"Dear applicant {r.name} Thank you for taking the time to Register as delivery patner position. We appreciate your interest in our company.After careful consideration, we regret to inform you that you have not been selected for the position"

    send_mail('Job Application Received- Fragrance Customer services', email_message, settings.EMAIL_HOST_USER, [z], fail_silently=False)
    r.delete()
    return redirect(joind_d)

# --------- ACCEPT APPLICATIONS.------------
def accept_request(request,d):
    Join.objects.filter(id=d).update(status=1)
    Join.objects.filter(id=d).update(employee_id=1)
    x = Join.objects.get(id=d)
    z=x.email
    print(z)
    # email_message = f"New employee request from: {data.name}"
    # send_mail('Request', f'{"Employes Waiting for  your Accept "}','settings.EMAIL_HOST_USER',[z],fail_silently=False)

    # z = data.user.email

    email_message = f"Dear applicant {x.name} We are Happy to inform that, Your application is Accepted from admin. Please join our team ASAP. Check out Contact details provided in our official website. "

    send_mail('Congrats..', email_message, settings.EMAIL_HOST_USER, [z], fail_silently=False)
    return redirect(joind_d)

                                                                             # ---------PERFUME CATEGORIES.------------
def women(re):
    return render(re,'women.html')


def Men(a1):
    obj = pro.objects.all()
    l = []
    for i in obj:
        if i.category == 'Men':
            l.append(i)

    if 'id' in a1.session:
        user = register.objects.get(username=a1.session['id'])
        datass = c_rt.objects.filter(user_det=user)
        ca = [i.pro_det.id for i in datass]
        return render(a1, 'men.html', {'l': l,'c':ca,'d':datass})
    else:
        return render(a1, 'men.html', {'l': l,})


def Women(a2):
    obj = pro.objects.all()

    l = []
    for i in obj:
        if i.category == 'Women':
            l.append(i)
    if 'id' in a2.session:
        user = register.objects.get(username=a2.session['id'])
        datass = c_rt.objects.filter(user_det=user)

        ca = [i.pro_det.id for i in datass]
        print(ca)

        return render(a2, 'women.html', {'l': l,'c':ca,'d':datass,})
    else:
        return render(a2, 'women.html', {'l': l,})




def Unisex(a4):
    obj = pro.objects.all()
    l = []
    for i in obj:
        if i.category == 'Unisex':
            l.append(i)
    if 'id' in a4.session:
        user = register.objects.get(username=a4.session['id'])
        datass = c_rt.objects.filter(user_det=user)
        ca = [i.pro_det.id for i in datass]
        print(ca)

        return render(a4, 'unisex.html', {'l': l, 'c': ca,'d':datass})
    else:
        return render(a4, 'unisex.html', {'l': l, })

def Bestseller(a5):
    obj = pro.objects.all()
    l = []
    for i in obj:
        if i.category == 'Best seller':
            l.append(i)
            print(l)
    return render(a5, 'index.html', {'l': l})

def Gift(a6):
    obj = pro.objects.all()
    l = []
    for i in obj:
        if i.category == 'Gift':
            l.append(i)
    if 'id' in a6.session:
        user = register.objects.get(username=a6.session['id'])
        datass = c_rt.objects.filter(user_det=user)
        ca = [i.pro_det.id for i in datass]
        print(ca)

        return render(a6, 'unisex.html', {'l': l, 'c': ca,'d':datass})
    else:
        return render(a6, 'unisex.html', {'l': l, })

                                                                        # --------- SINGLE PRODUCT DETAILS.------------
def product_view(request, id):
    data = pro.objects.filter(id=id)
    dat = pro.objects.get(id=id)
    print(dat.quantity)
    print("here")
    w = Wishlist.objects.none()
    if 'id' in request.session:
        user = register.objects.get(username=request.session['id'])
        datas = c_rt.objects.filter(user_det=user)
        wdata = Wishlist.objects.filter(user_details=user)

        # c=c_rt.objects.filter(user_det=user).count()
        l = [i.pro_det.id for i in datas]  # List of product IDs in the cart
        wish = [i.item_details.id for i in wdata]  # List of product IDs in the wishlist
        print('********************************')
        print(l)
        print(wish)
    else:
        l = []  # If user is not logged in, cart is empty
        wish = []  # If user is not logged in, cart is empty

    return render(request, 'product_view.html', {'data': data, 'l': l,'wish':wish,'datas':dat})


                                                                         # ---------CREATING WISH LIST HERE------------
def wish_list(request,id):
    if 'id' in request.session:
        u=register.objects.get(username=request.session['id'])
        # print(u.email)
        item=pro.objects.get(pk=id)
        data = Wishlist.objects.create(user_details=u,item_details=item)
        data.save()
        print(item.quantity)

        # l=Wishlist.objects.filter(user_details=u)
        # print(l)
        # print('..................................................................')
        print('add wishlist done')
        messages.success(request,'Wishlist added successfully')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(plog)

def display_product(request):
    if 'id' in request.session:
        u=register.objects.get(username=request.session['id'])
        b=Wishlist.objects.filter(user_details=u)
        datas = c_rt.objects.filter(user_det=u)
        l = [i.pro_det.id for i in datas]
        print(b)
        if b.count()==0:
            return redirect('empty_wish')
        return render(request,'wishlist.html',{'data':b,'l':l})
    return redirect(plog)

def delete_wish(request,id):
    if 'id' in request.session:
        data=Wishlist.objects.get(id=id)
        data.delete()
        return redirect(display_product)

                                                                         # --------- FILL YOUR CART HERE.------------
def addcart(request, id):

    if 'id' in request.session:
        u=register.objects.get(username=request.session['id'])
        item=pro.objects.get(pk=id)
        date_t = datetime.datetime.now()
        data=c_rt.objects.create(user_det=u,pro_det=item,date=date_t,price=item.price,total_price=item.price)
        data.save()
        messages.success(request,'Cart added successfully')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(plog)

def viewcart(request):
    if 'id' in request.session:
        details = register.objects.get(username=request.session['id'])  # single user details get
        ide = details.id
        datas2 = c_rt.objects.filter(user_det=details)

        t = 0
        sub = {}
        su = datas2
        for i in su:
            sub[i.pro_det] = [i.cart_quantity, i.pk,
                              i.pro_det.price * i.cart_quantity]  # { product1:[quantity, id, price* quantity], product2:[quantity, id, price* quantity] }
        for i in su:
            t = t + (i.pro_det.price * i.cart_quantity)

        if not sub:
            return redirect(index)  # Redirect to another HTML page if sum or sub are empty

        return render(request, 'cart.html', {'datas': datas2, 'total': t, 'sub': sub, 'cl': sub, 'ii': ide})
    else:

        return render(request, 'please log in.html')

def empty_wish(re):
    return render(re,'empty_wish.html')
def minuscart(d2, d):
    if 'id' in d2.session:
        c = c_rt.objects.get(id=d)
        if c.cart_quantity > 1:
            c.cart_quantity = c.cart_quantity - 1
            c.total_price = c.total_price-c.price
            c.save()
        else:
            c.delete()
    return redirect(viewcart)

def pluscart(re, d):
    if 'id' in re.session:
        c = c_rt.objects.get(id=d)
        if c.pro_det.quantity > c.cart_quantity:
            c.cart_quantity = c.cart_quantity + 1
            c.total_price = c.total_price+c.price
            c.save()
    return redirect(viewcart)

def delete_c(re,d):
    datas=c_rt.objects.get(pk=d)
    datas.delete()
    return redirect(viewcart)



#---------------------------------------------------------------------------------------------------------------
                                        # --------- USER PROFILE------------
def create_prof(re,id):
    if 'id' in re.session:
        u=register.objects.get(username=re.session['id'])
        try:
            if re.method == "POST":
                # name = re.POST['name']
                # email = re.POST['email']
                address = re.POST['address']
                phone = re.POST['phone']
                district = re.POST['district']
                state = re.POST['state']
                pincode = re.POST['pincode']

                upload = profile.objects.create(user_det=u, address=address, phone=phone, district=district,
                                                state=state, pincode=pincode)
                upload.save()
                return redirect(index)
        except:
            messages.info(re,"Please fill all fields, its mandatory")

def pr_update(re,id):
    data=profile.objects.get(id=id)
    return render(re, 'profile_update.html', {'updata': data})

def profile_updated(re,id):
    if re.method=='POST':
        phone=re.POST['phone']
        address=re.POST['address']
        state=re.POST['state']
        district=re.POST['district']
        pincode=re.POST['pincode']

        profile.objects.filter(id=id).update(phone=phone,address=address,state=state,district=district,pincode=pincode)
        return redirect(index)
    return render(re, 'index.html')


#__________________________________________________________________________________________________________________________________

from django.shortcuts import render, redirect
from .models import register, order, orderitem


def myorder(r):
    if 'id' in r.session:
        username = r.session['id']
        details = register.objects.get(username=username)
        orders = order.objects.filter(user=details)
        orders_list = []

        for ord in orders:
            order_dict = {
                'order': ord,
                'order_items': orderitem.objects.filter(orderdet=ord)
            }
            orders_list.append(order_dict)

        return render(r, 'view_order.html', {'orders_list': orders_list})
    return redirect(index)


# def myorder(re):
#     if 'id' in re.session:
#         username = re.session['id']
#         details = register.objects.get(username=username)
#         orders = order.objects.filter(user=details)
#         order_items = orderitem.objects.filter(orderdet__user=details)
#         if not orders:
#             return redirect('empty_cart')
#         return render(re, 'view_order.html', {'booking': orders, 'item': order_items, 'det': details})

#profile
def myaccound(request):
    try:
        mydet=register.objects.get(username=request.session['id'])
        return render(request,'myaccound.html', {'mydet': mydet})
    except:
        return render(request,'please log in.html')
def profview(re,id):
    try:
        r=register.objects.get(username=re.session['id'])
        pr=profile.objects.get(user_det=r)
        return render(re,'profile_up.html', {'dat1': pr})
        #edit
    except:
        mydet = register.objects.get(username=re.session['id'])
        return render(re,'profile.html',{'dat1': mydet})
        #create
def create(request,id):
    if request.method == 'POST':
        mydet = register.objects.get(username=request.session['id'])
        address = request.POST['address']
        phone = request.POST['phone']
        district = request.POST['district']
        state = request.POST['state']
        pincode = request.POST['pincode']
        data = profile.objects.create(user_det=mydet,address=address,phone=phone,district=district,state=state,pincode=pincode)
        data.save()
        return redirect(request.META.get('HTTP_REFERER', 'r6/<int:d>'))
def update(request,id):
    if request.method=='POST':
        mydet = register.objects.get(username=request.session['id'])
        address = request.POST['address']
        phone = request.POST['phone']
        district = request.POST['district']
        state = request.POST['state']
        pincode = request.POST['pincode']

        profile.objects.filter(id=id).update(user_det=mydet,address=address,phone=phone,district=district,state=state,pincode=pincode)

        return redirect(index)
    return render(request, 'women.html')


def id_update(re):
    data=Join.objects.get(username=re.session['emp'])
    print(data.name)
    return render(re, 'employee_id.html', {'data': data})

def em_id_updated(re):

    if re.method=='POST':
        phone=re.POST['phone']
        location=re.POST['location']
        accoundnumber=re.POST['accoundnumber']


        Join.objects.filter(username=re.session['emp']).update(phone=phone,accoundnumber=accoundnumber,location=location)
        return redirect(o)
    return render(re, 'index.html')

def delivery(re):
    if 'emp' in re.session:
        ord=order.objects.all()
        return render(re,'delivery.html',{'data':ord})





def order_cancel(re,d):
    l=order.objects.filter(id=d).first()
    track=l.tracking_no
    items=orderitem.objects.filter(orderdet__tracking_no=track)
    print('just')
    print(items)
    for i in items:
        product=i.product
        p=i.quantity
        pp = product.quantity + p
        print(pp)
        pro.objects.filter(name=product.name).update(quantity=pp)
        print('updated')
    z = l.user.email
    email_message = f"Dear {l.user.name},We hope this email finds you well.We regret to inform you that we have had to cancel your recent order {l.tracking_no}. We apologize for any inconvenience this may cause."
    send_mail('Order cancellation mail!!!', email_message, settings.EMAIL_HOST_USER, [z],
              fail_silently=False)

    # if canceled increase stock which they selected
    l.delete()
    messages.error(re, 'Order cancelled successfully')
    return redirect(re.META.get('HTTP_REFERER', '/'))
# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------



def r8(re,d):
    c=d
    sp = []
    t=0
    if 'id' in re.session:
        details=register.objects.get(username=re.session['id'])
        sp=c_rt.objects.filter(user_det=details)
        print('this')
        # print(sp.pro_det)
        for i in sp:
            if i.pro_det.quantity<=10:
                z = 'fragranceperfumes98@gmail.com'
                email_message = f" The product {i.pro_det.name} is falling out off stock. its only {i.pro_det.quantity}, updatae fastly "

                send_mail('ALERT...UPDATE STOCK...', email_message, settings.EMAIL_HOST_USER, [z], fail_silently=False)
        for i in sp:
            t = t+i.total_price
        try:
            pr = profile.objects.get(user_det=details)
            return render(re,'dem_cart.html',{'data':details,'pr':pr,'pdata':sp,'t':t})
        except profile.DoesNotExist:
            return render(re,'dem_cart.html',{'data':details,'pdata':sp,'t':t})
    return redirect(index)

def r6(re,d):
    c=d
    if 'id' in re.session:
        details=register.objects.get(username=re.session['id'])
        sp=pro.objects.get(id=d)
        # alerts
        if sp.quantity<=10:
            z = 'fragranceperfumes98@gmail.com'
            email_message = f" The product {sp.name} is falling out off stock. its only {sp.quantity}, updatae fastly , its high on demand."

            send_mail('ALERT...UPDATE STOCK...', email_message, settings.EMAIL_HOST_USER, [z], fail_silently=False)
        re.session['pr_id'] = sp.id
        #creates session id for quantity and total
        my = re.POST.get('total_l')
        myq = re.POST.get('singleqty')
        print(myq)
        re.session['paytotal'] = my
        re.session['total_quant'] = myq
        # print(re.session['pr_id'])
        # print(pro.objects.get(id=re.session['pr_id'] ))
        # print('ppppppp')
        try:
            pr = profile.objects.get(user_det=details)
            return render(re,'checkout_single.html',{'data':details,'pr':pr,'pdata':sp,'my':my,'myq':myq})
        except profile.DoesNotExist:
            return render(re,'checkout_single.html',{'data':details,'pdata':sp,'my':my,'myq':myq})
    # return redirect(index)
    # messages.info(re, "Please Login")
    return redirect(login)

def placeorder2(r):
    if 'id' in r.session:
        se = r.session.get('id')
        print('se',se)
        tot = r.session.get('paytotal')
        totq = r.session.get('total_quant')
        usr = register.objects.get(username=se)
        products = pro.objects.get(id=r.session['pr_id'])
        print('placeorder2')
        print(usr)
        if r.method == 'POST':
                neworder = order()
                neworder.user = usr
                neworder.nname = r.POST.get('name')
                neworder.sphone = r.POST.get('phone')
                neworder.saddress = r.POST.get('address')
                neworder.sstate = r.POST.get('state')
                neworder.sdistrict = r.POST.get('district')
                neworder.spincode = r.POST.get('pincode')
                neworder.payment_mode = r.POST.get('payment_mode')
                neworder.payment_id = r.POST.get('payment_id')
                neworder.tprice=tot
                neworder.quant=totq
                print("payment_mode",neworder.payment_mode)
                trackno = 'fragrance' + str(random.randint(1111111, 9999999))
                while order.objects.filter(tracking_no=trackno) is None:
                    trackno = 'fragrance' + str(random.randint(1111111, 9999999))
                neworder.tracking_no = trackno
                # x=r.POST.get('total_l')
                # r.session['track'] = trackno
                # print(r.session['track'])
                # print('trackingno')

                # Store the current item's total price in session
                r.session['t'] = neworder.tprice

                today_date = timezone.now().date()
                future_date = today_date + timedelta(days=6)
                print('today')
                print(today_date)
                print(future_date)
                neworder.updated_at = future_date
                neworder.save()
                # r.session['t'] = x
                products = pro.objects.get(id=r.session['pr_id'])
                #
                # singlee.objects.create(
                #     user=usr,
                #     oddr=neworder,
                #     sproduct=products,
                #     sprice=products.price,
                #     stotal=r.POST.get('total_l'),
                #     squantity=r.POST.get('singleqty'),
                #     tracking_no=trackno
                #     )

                # produc_t=pro.objects.get(id=r.session['pr_id'])
                # print('here')
                # print(produc_t)
                # for item in c:

                orderitem.objects.create(
                    orderdet=neworder,
                    product=products,
                    price=products.price,
                    quantity=neworder.quant
                    )

                p = pro.objects.get(name=products.name)
                quants=int(totq)
                print(type(products.quantity))
                pp = products.quantity - quants
                print(pp)
                pro.objects.filter(name=p.name).update(quantity=pp)
                # print(neworder.quant)
                # c_rt.objects.filter(user_det=usr).delete()

                messages.success(r, 'Your order has been placed successfully')

                return redirect(myorder)

                payMode = r.POST.get('payment_mode')
                if payMode == "Razorpay":
                    return JsonResponse({'status': 'Your order has been placed successfully'})
        return redirect('/')


def razorpaycheck2(r):
    if 'id' in r.session:
        se = r.session.get('id')
        # tt=r.session.get('t')
        # usr = register.objects.get(name=se)
        products=pro.objects.get(id=r.session['pr_id'])
        # price=r.session['paytotal']
        # print(price)
        print(products)
        # item_det=singlee.objects.get(tracking_no=r.session['track'])
        return JsonResponse({'total_price':100})


from django.http import JsonResponse
from django.contrib import messages

def placeorder(request):
    if 'id' in request.session:
        se = request.session.get('id')
        usr = register.objects.get(username=se)
        cart_items = c_rt.objects.filter(user_det=usr).all()

        # Calculate total quantity and total price
        total_quantity = sum(item.cart_quantity for item in cart_items)
        total_price = sum(item.price * item.cart_quantity for item in cart_items)
        request.session['am'] = total_price

        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            state = request.POST.get('state')
            district = request.POST.get('district')
            pincode = request.POST.get('pincode')
            payment_id = request.POST.get('payment_id')
            payment_mode = request.POST.get('payment_mode')

            if name and phone and address and state and district and pincode and payment_id and payment_mode:
                try:

                    today_date = timezone.now().date()
                    future_date = today_date + timedelta(days=6)
                    new_order = order.objects.create(
                        user=usr,
                        nname=name,
                        sphone=phone,
                        saddress=address,
                        sstate=state,
                        sdistrict=district,
                        spincode=pincode,
                        tprice=total_price,
                        quant=total_quantity,
                        payment_id=payment_id,
                        payment_mode=payment_mode,
                        tracking_no='fragrance' + str(random.randint(1111111, 9999999)),
                        updated_at=future_date,
                    )

                    # Create order items
                    for item in cart_items:
                        orderitem.objects.create(
                            orderdet=new_order,
                            product=item.pro_det,
                            price=item.price,
                            quantity=item.cart_quantity
                        )
                        p=pro.objects.get(name=item.pro_det.name)
                        pp=p.quantity-item.cart_quantity
                        print(pp)
                        pro.objects.filter(name=p.name).update(quantity=pp)
                    # pro.objects.filter(id=id).update(name=name, quantity=quantity, price=price, ingredients=ingredients,
                    #                                  netquantity=netquantity, category=category, fragrance=fragrance)

                    # Clear the user's cart
                    c_rt.objects.filter(user_det=usr).delete()

                    messages.success(request, 'Your order has been placed successfully')


                    if payment_mode == "Razorpay":
                        return JsonResponse({'status': 'Your order has been placed successfully'})
                    else:
                        return redirect('myorder')
                except Exception as e:
                    messages.error(request, 'Error placing order: {}'.format(str(e)))
                    return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                messages.error(request, 'Please fill in all the details')
                return redirect(request.META.get('HTTP_REFERER', '/'))

        return redirect(index)


def razorpaycheck(r):

    if 'id' in r.session:
        se = r.session.get('id')
        usr = register.objects.get(username=se)
        c = c_rt.objects.filter(user_det=usr).all()
        p = 0
        for i in c:
            p = i.cart_quantity + p
        # cart total qty
        print(p)
        t = 0
        for i in c:
            t = t + (i.price * i.cart_quantity)
        print(t)
        r.session['am'] = t

    return JsonResponse({
        'total_price': r.session['am']
    })
# def delivery_update(re):
#     s=order.objects.all()
#
#     return render(re,'order_status_change.html',{"data":s})


        # return redirect(checkout)

def status_update(re,id):

    if re.method=='POST':
        category=re.POST['order_status']
        print(category)
        order.objects.filter(id=id).update(status=category)
        p=order.objects.get(id=id)
        print(p.status)
        return redirect(delivery_update)

def delivery_update(re):
    s=order.objects.all()
    orders_list = []

    for ord in s:
        order_dict = {
            'order': ord,
            'order_items': orderitem.objects.filter(orderdet=ord)
        }
        orders_list.append(order_dict)
        print(orders_list)

    return render(re,'order_status_change.html',{"data":orders_list})


def single_payment(r):
    if 'id' in r.session:
        se = r.session.get('id')
        print('serrr',se)
        tot = r.session.get('paytotal')
        totq = r.session.get('total_quant')
        print("qnty",totq)
        print("price",tot)
        usr = register.objects.get(username=se)
        products = pro.objects.get(id=r.session['pr_id'])
        print('placeorder2')
        print(usr)
        try:
            if r.method == 'POST':
                    neworder = order()
                    neworder.user = usr
                    neworder.nname = r.POST.get('name')
                    neworder.sphone = r.POST.get('phone')
                    neworder.saddress = r.POST.get('address')
                    neworder.sstate = r.POST.get('state')
                    neworder.sdistrict = r.POST.get('district')
                    neworder.spincode =r.POST['pincode']
                    neworder.payment_mode = r.POST.get('payment_mode')
                    print('all ok')
                    neworder.payment_id = r.POST.get('payment_id')
                    neworder.tprice=tot
                    neworder.quant=totq
                    print("payment_mode",neworder.payment_mode)
                    trackno = 'fragrance' + str(random.randint(1111111, 9999999))
                    while order.objects.filter(tracking_no=trackno) is None:
                        trackno = 'fragrance' + str(random.randint(1111111, 9999999))
                    neworder.tracking_no = trackno
                    # x=r.POST.get('total_l')
                    # r.session['track'] = trackno
                    # print(r.session['track'])
                    # print('trackingno')

                    # Store the current item's total price in session
                    r.session['t'] = neworder.tprice

                    today_date = timezone.now().date()
                    future_date = today_date + timedelta(days=6)
                    print('today')
                    print(today_date)
                    print(future_date)
                    neworder.updated_at = future_date
                    neworder.save()

                    # r.session['t'] = x
                    products = pro.objects.get(id=r.session['pr_id'])
                    #
                    # singlee.objects.create(
                    #     user=usr,
                    #     oddr=neworder,
                    #     sproduct=products,
                    #     sprice=products.price,
                    #     stotal=r.POST.get('total_l'),
                    #     squantity=r.POST.get('singleqty'),
                    #     tracking_no=trackno
                    #     )

                    # produc_t=pro.objects.get(id=r.session['pr_id'])
                    # print('here')
                    # print(produc_t)
                    # for item in c:

                    orderitem.objects.create(
                        orderdet=neworder,
                        product=products,
                        price=products.price,
                        quantity=neworder.quant
                        )

                    p = pro.objects.get(name=products.name)
                    quants=int(totq)
                    print(type(products.quantity))
                    pp = products.quantity - quants
                    print(pp)
                    pro.objects.filter(name=p.name).update(quantity=pp)
                    # print(neworder.quant)
                    # c_rt.objects.filter(user_det=usr).delete()

                    messages.success(r, 'Your order has been placed successfully')
                    print("total===",tot)
                    return redirect(razor,tot)

                    payMode = r.POST.get('payment_mode')
                    if payMode == "Razorpay":
                        return JsonResponse({'status': 'Your order has been placed successfully'})

            return redirect('/')
        except:
            messages.info(re,"Please fill all fields, its mandatory")


def razor(request,totq):
        amount = totq * 100
        order_currency = 'INR'
        client = razorpay.Client(
            auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        return render(request, "razor.html",{'amount':amount})
