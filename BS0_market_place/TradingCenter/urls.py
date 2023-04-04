"""BS0_market_place URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
import TradingCenter.views as v
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from BS0_market_place import settings
urlpatterns = [
    path("market_page/",v.MarketView.as_view()),
    path("brands/list/",v.MyBrandsList.as_view()),
    path("brands/detail/<int:pk>",v.BrandsDetailView.as_view()),
    path("brand/create/<int:sector_pk>",v.create_brand),
    path("brand/update/<int:pk>",v.BrandUpdateView.as_view(success_url="/market_page/")),
    path("inventory/list/",v.InventoryManagerListView.as_view()),
    path("inventory/list/detail/<int:pk>",v.InventoryDetailView.as_view()),
    path("software/list/",v.SoftwareManagerListView.as_view()),
    path("software/list/detail/<int:pk>",v.SoftwareDetailView.as_view()),
    path("services/list/",v.ServicesManagerListView.as_view()),
    path("services/list/detail/<int:pk>",v.ServicesDetailView.as_view()),
    path("services/list/detail/create/portfolio/<int:ser_id>",v.create_portfolio),
    path("services/list/detail/delete/portfolio/<int:serv_id>/<int:port_id>",v.delete_portfolio),
    path("inventory/update/<int:pk>",v.InventoryManagerUpdateView.as_view(success_url="/market_page/")),
    path("software/update/<int:pk>",v.SofwareManagerUpdateView.as_view(success_url="/market_page/")),
    path("service/update/<int:pk>",v.ServiceManagerUpdateView.as_view(success_url="/market_page/")),
    path("inventory/create/<int:brand_pk>",v.create_inventory_product),
    path("software/create/<int:brand_pk>",v.create_software_product),
    path("service/create/<int:brand_pk>",v.create_services),
    path("inventory/remove/<int:pk>/<int:bk>",v.remove_inventory),
    path("software/remove/<int:pk>/<int:bk>",v.remove_software),
    path("service/remove/<int:pk>/<int:bk>",v.remove_services),
    path("brand/remove/<int:pk>",v.remove_brand),

    path("sector/list/",v.SectorListView.as_view()),
    path("send/message/",v.MessagesView.as_view()),
    path("recived/message/",v.MessagesRecivedView.as_view()),
    path("detail/message/<int:pk>",v.MessageDetailView.as_view()),
    path("compose/message/",v.compose_message),
    path("customers/cart/",v.ClientCartOrdersView.as_view()),
    path("customer/cancel/cart",v.ClientCancelOrdersView.as_view()),
    path("brands/cart/",v.BrandsCartOrderView.as_view()),
    path("brand/cart/detail/<int:pk>",v.BrandsCartDetailView.as_view()),
    path("customers/cart/complete",v.ClientCartCompleteView.as_view()),
    path("brands/cart/complete",v.BrandsCartCompleteView.as_view()),
    path("brand/cart/complete/detail/<int:pk>",v.BrandsCompletCartDetailView.as_view()),
    path("service/order/detail/cust/<int:pk>",v.ServiceOrderDetailViewByCart.as_view()),
    path("service/order/detail/own/<int:pk>",v.ServiceOrderDetailViewByOwner.as_view()),
    path("user/cart/inventory/commit/<int:pk>",v.inventory_user_commit),
    path("user/cart/software/commit/<int:pk>",v.software_user_commit),
    path("user/cart/service/commit/<int:pk>",v.service_user_commit),
    path("user/cart/inventory/delete/<int:pk>",v.inventory_cart_delete),
    path("user/cart/software/delete/<int:pk>",v.software_cart_delete),
    path("user/cart/service/delete/<int:pk>",v.services_cart_delete),

    path("owner/order/inventory/commit/<int:pk>",v.inventory_owner_commit),
    path("owner/order/service/commit/<int:pk>",v.service_owner_commit),
    path("owner/order/inventory/simple/commit/<int:pk>",v.inventory_owner_simple_commit),
    path("owner/order/service/simple/commit/<int:pk>",v.service_owner_simple_commit),

    path("owner/order/inventory/delete/<int:pk>",v.inventory_order_delete),
    path("owner/order/service/delete/<int:pk>",v.services_order_delete),
    path("customer/finantial/",v.FinantialListView.as_view()),
    path("customer/finantial/ledger/<int:pk>",v.DetailLedgerUrl.as_view()),
    path("customer/finantial/ledger/cashin/<int:turn_id>",v.enter_cashin),
    path("customer/finantial/ledger/cashout/<int:turn_id>",v.enter_cashout),
    path("customer/finantial/ledger/turn/start",v.start_new_turn),
    path("customer/finantial/ledger/turn/remove/<int:turn_id>",v.remove_turn),
    path("customer/finantial/ledger/turn/complete/<int:turn_id>",v.complete_turn),
    path("admins/rollback/inventory/<int:pk>",v.inventory_order_rollback),
    path("admins/rollback/software/<int:pk>",v.software_order_rollback),
    path("admins/rollback/services/<int:pk>",v.service_order_rollback),

    path("create/inventory/comments/<int:pk>",v.create_inventory_comments),
    path("create/software/comments/<int:pk>",v.create_software_comments),
    path("create/services/comments/<int:pk>",v.create_services_comments),

    path("create/inventory/report/<int:pk>",v.create_inventory_report),
    path("create/software/report/<int:pk>",v.create_software_report),
    path("create/services/report/<int:pk>",v.create_services_report),

    path("checkoutform/<int:amount>/<int:bill>/",v.check_out_form),
    path("otp/<int:amount>/<int:bill>/<int:phone_number>/<str:username>/<str:email>/<str:password>/",v.one_time_password_form),
    path("make/relations/",v.MLView.as_view()),
    path("request/on/service/<int:service_pk>",v.create_request_on_service),
    path("login/inventory/<int:pk>",v.log_in_inventory),
    path("login/software/<int:pk>",v.log_in_software),
    path("login/services/<int:pk>",v.log_in_services),


    path('', RedirectView.as_view(url="market_page/")), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)