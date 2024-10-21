"""
URL configuration for perfume project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views

from django.conf import settings
from django.conf.urls.static import static






urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('contact', views.contact),
    path('log', views.login),
    path('plog', views.plog),
    path('l', views.adm),
    path('p', views.reg),
    path('r', views.r1),
    path('a', views.a),
    path('reg', views.regi),
    path('login', views.loginn),
    path('join', views.joini),
    path('jo', views.joins),
    path('logout', views.logout),
    path('add', views.add),
    path('s', views.view_details),

    path('delete/<int:id>',views.delete),

    path('upd/<int:id>', views.upd),
    path('update/<int:id>', views.updatas),
    # path('updis', views.updis),
    path('w', views.women),
    path('men',views.Men,name="Men"),
    path('women',views.Women,name="Women"),
    path('unisex',views.Unisex,name="unisex"),
    path('gift',views.Gift,name="Gift"),

    # forgotpassword------------------------------------------------------------------
    # path("forgot", views.forgot_password, name="forgot"),
    # path("reset/<token>", views.reset_password, name="reset"),
    # path("reset/reset2/<token>", views.reset_password2, name="reset2"),
    # path('emailsent', views.emailsent),


    # path('pa', views.p),
    path('ai', views.ai),
    path('o/<int:id>', views.product_view),

    path('wish/<int:id>', views.wish_list),

    path('view_wslt', views.display_product),
    path('delete_wish/<int:id>', views.delete_wish),


    path('cart/', views.viewcart),
    path('bill/', views.pr_update),
    path('addcart/<int:id>', views.addcart),
    path('cart/inc/<int:d>', views.pluscart),
    path('cart/dec/<int:d>', views.minuscart),
    path('cart/delete_c/<int:d>', views.delete_c),
    path('r6/<int:d>', views.r6,name='r6'),
    path('r8/<int:d>', views.r8,name='r8'),
    # path('single/<int:d>', views.single_pro_booking),
    # path('m/<int:d>', views.multiple_pro_booking),
    # path('mbook', views.multiple_pro_booking,name='mbook'),
    # path('sbook/<int:d>', views.single_pro_booking,name='sbook'),
    path('myorder', views.myorder),
    path('cancel/<int:d>', views.order_cancel),
    # path('od/', views.order_items, name='order_items'),
    # path('order-items1/', views.order_items1, name='order_items1'),

    # path('proceed-to-pay', views.razorpaycheck, name='proceed-to-pay'),
    path('place-order', views.placeorder, name='placeorder'),
    path('place-order2', views.placeorder2, name='placeorder2'),
    path('single_payment', views.single_payment, name='single_payment'),
    path('razor/<int:totq>', views.razor, name='razor'),
    # path('payments/', views.payments, name='payments'),
    # path('success', views.payments),
    path('proceed-to-pay', views.razorpaycheck, name='proceed-to-pay'),
    path('proceed-to-pay2', views.razorpaycheck2, name='proceed-to-pay2'),
    path('myorder', views.myorder, name='myorder'),


    #profile

    path('create/<int:id>', views.create_prof),
    path('pr_update/<int:id>', views.pr_update),
    path('profile_updated/<int:id>', views.profile_updated),
    path('profcreate/<int:id>', views.profview),
    path('profupdate/<int:id>', views.update),

    path('create/<int:id>', views.create),
    #password_reset
    path('forgot', views.forgot_password, name="forgot"),
    path('reset/<token>', views.reset_password, name='reset_password'),

    # path('empty_cart', views.empty_cart, name='empty_cart'),
    path('empty_wish', views.empty_wish, name='empty_wish'),

    path('myaccound',views.myaccound),


    path('use', views.registerd_d),
    path('cus', views.customerss),
    path('joi', views.joind_d),
    path('joi2', views.joiemp),
    path('joi3', views.joidassi),
    path('rej/<int:id>', views.joind_rej),
    path('acp/<int:d>', views.accept_request),
    path('o', views.o),
    path('iii', views.iid),
    path('iu', views.id_update),
    path('eiu', views.em_id_updated),
    path('deli', views.delivery),
    # path('www', views.checkout12),
    # path('ww', views.razor_pay_callback),
    path('dv', views.delivery_update),
    path('status/<int:id>', views.status_update),
    path('ad_order_status/<int:id>', views.distribute),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)