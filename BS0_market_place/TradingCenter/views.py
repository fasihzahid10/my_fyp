from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from datetime import date
import TradingCenter.models as m
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.forms import ModelForm, Form
from django import forms
import TradingCenter.component as c
from TradingCenter.MLAlgo import BuildRelations as b
from django.db.models import Q
from django.db.models import Sum
import TradingCenter.easypaisa_integration as eas
# Create your views here.
componentListView = "pages/DisplayManagers.html"
componentDetailView = "pages/DisplayDetailManager.html"
componentFormView = "pages/DisplayForm.html"
loginRegistrationForm = "registration/login.html"
admin_handle = "ibtisam"


def get_inventory_business_product_rank(ppk):
    total = m.inventory_managment.objects.all().aggregate(
        Sum('total_rating'))['total_rating__sum']
    if total > 0:
        business = m.inventory_managment.objects.get(pk=ppk).total_rating
        return (business/total)
    return 0


def get_software_business_product_rank(ppk):
    total = m.software_manager.objects.all().aggregate(
        Sum('total_rating'))['total_rating__sum']
    if total > 0:
        business = m.software_manager.objects.get(pk=ppk).total_rating
        return (business/total)
    return 0


def get_service_business_product_rank(ppk):
    total = m.services_manager.objects.all().aggregate(
        Sum('total_rating'))['total_rating__sum']
    if total > 0:
        business = m.services_manager.objects.get(pk=ppk).total_rating
        return (business/total)
    return 0


def get_inventory_trans_product_rank(ppk):
    total = m.inventory_orders.objects.filter(manager_id=ppk).count()
    if total > 0:
        business = total - \
            m.inventory_orders.objects.filter(
                Q(manager_id=ppk) & Q(is_reported=True)).count()
        return (business/total)
    return 0


def get_software_trans_product_rank(ppk):
    total = m.software_orders.objects.filter(manager_id=ppk).count()
    if total > 0:
        business = total - \
            m.software_orders.objects.filter(
                Q(manager_id=ppk) & Q(is_reported=True)).count()
        return (business/total)
    return 0


def get_service_trans_product_rank(ppk):
    total = m.service_order.objects.filter(request_id__service_id=ppk).count()
    if total > 0:
        business = total - m.service_order.objects.filter(
            Q(request_id__service_id=ppk) & Q(is_reported=True)).count()
        return (business/total)
    return 0


def get_inventory_happiness_product_rank(ppk):
    total = m.comment_on_inventory_order.objects.filter(
        order__manager_id=ppk).count()*5
    if total > 0:
        business = m.comment_on_inventory_order.objects.filter(
            order__manager_id=ppk).aggregate(Sum('rating'))['rating__sum']
        return (business/total)
    return 0


def get_software_happiness_product_rank(ppk):
    total = m.comment_on_software_order.objects.filter(
        order__manager_id=ppk).count()*5
    if total > 0:
        business = m.comment_on_software_order.objects.filter(
            order__manager_id=ppk).aggregate(Sum('rating'))['rating__sum']
        return (business/total)
    return 0


def get_service_happiness_product_rank(ppk):
    total = m.comment_on_service.objects.filter(
        order__request_id__service_id=ppk).count()*5
    if total > 0:
        business = m.comment_on_service.objects.filter(
            order__request_id__service_id=ppk).aggregate(Sum('rating'))['rating__sum']
        return (business/total)
    return 0


def get_total_inventory_product_rank(ppk):
    return get_inventory_happiness_product_rank(ppk) + get_inventory_trans_product_rank(ppk) + get_inventory_business_product_rank(ppk)


def get_total_software_product_rank(ppk):
    return get_software_happiness_product_rank(ppk) + get_software_trans_product_rank(ppk) + get_software_business_product_rank(ppk)


def get_total_service_product_rank(ppk):
    return get_service_happiness_product_rank(ppk) + get_service_trans_product_rank(ppk) + get_service_business_product_rank(ppk)


def get_inventory_complete_total(ppk):
    # business rank
    total = 0
    business = 0
    temp = m.inventory_managment.objects.all().aggregate(
        Sum('total_rating'))['total_rating__sum']
    if temp:
        total = temp
    temp = m.inventory_managment.objects.get(pk=ppk).total_rating
    if temp:
        business = temp
    temp = m.comment_on_inventory_order.objects.filter(
        order__manager_id=ppk).count()*5
    if temp:
        total += temp
    temp = m.comment_on_inventory_order.objects.filter(
        order__manager_id=ppk).aggregate(Sum('rating'))['rating__sum']
    if temp:
        business += temp
    if total > 0:
        return (business/total)
    return 0


def get_software_complete_total(ppk):
    # business rank
    total = 0
    business = 0
    temp = m.software_manager.objects.all().aggregate(
        Sum('total_rating'))['total_rating__sum']
    if temp:
        total = temp
    temp = m.software_manager.objects.get(pk=ppk).total_rating
    if temp:
        business = temp
    temp = m.comment_on_software_order.objects.filter(
        order__manager_id=ppk).aggregate(Sum('rating'))['rating__sum']
    if temp:
        business += temp
    temp = m.comment_on_software_order.objects.filter(
        order__manager_id=ppk).count()*5
    if temp:
        total += temp
    if total > 0:
        return (business/total)
    return 0


def get_service_complete_total(ppk):
    # business rank
    total = 0
    business = 0
    temp = m.services_manager.objects.all().aggregate(
        Sum('total_rating'))['total_rating__sum']
    if temp:
        total = temp
    temp = m.services_manager.objects.get(pk=ppk).total_rating
    if temp:
        business = temp
    temp = m.comment_on_service.objects.filter(
        order__request_id__service_id=ppk).count()*5
    if temp:
        total += temp
    temp = m.comment_on_service.objects.filter(
        order__request_id__service_id=ppk).aggregate(Sum('rating'))['rating__sum']
    if temp:
        business += temp
    if total > 0:
        return (business/total)
    return 0


def log_in_inventory(request, pk):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(f'/inventory/list/detail/{pk}')
    return render(request, loginRegistrationForm, {'form': AuthenticationForm()})


def log_in_software(request, pk):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(f'/software/list/detail/{pk}')
    return render(request, loginRegistrationForm, {'form': AuthenticationForm()})


def log_in_services(request, pk):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(f'/services/list/detail/{pk}')
    return render(request, loginRegistrationForm, {'form': AuthenticationForm()})


class MarketView(ListView):
    template_name = "pages/market.html"
    model = m.sector

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sectors'] = []
        si = self.request.GET.get("si")
        context['component'] = []
        counter = 0
        if self.request.user.is_authenticated:
            inv_num = 0
            serv = 0
            cust = self.request.user.customer
            lis = m.brand.objects.filter(owner=cust)
            if lis:
                for obj in lis:
                    inv_num += m.inventory_orders.objects.filter(
                        Q(manager_id__brands_product=obj) & Q(is_commited_by_owner=False)).count()
                    serv += m.service_order.objects.filter(
                        Q(request_id__service_id__brands_product=obj) & Q(is_commited_by_owner=False)).count()
            value = inv_num + serv
            context['component'].append(c.InfoButtons(name1="msg", name2="orders", value1=m.message.objects.filter(
                Q(reciver=self.request.user.customer) & Q(revived=False)).count(), value2=value, url1="/send/message/", url2="/brands/cart/"))
        for sec in context['object_list']:
            dic = {}
            dic['name'] = c.TextBodyCard(sec.name)
            obj = m.brand.objects.filter(Q(brand_sector=sec.pk) & Q(
                is_active=True)).order_by("-total_rating")
            if si:
                obj = obj.filter((Q(name__icontains=si) | Q(description__icontains=si) | Q(location__icontains=si) | Q(long_description__icontains=si) | Q(brand_sector__profit_on_brand__icontains=si) | Q(
                    brand_sector__location__icontains=si) | Q(brand_sector__name__icontains=si) | Q(brand_sector__description__icontains=si)) & Q(is_active=True))

            context['component'].append(c.brand_sliders(
                sec.name, obj, counter, sec.total_rating))
            counter += 1
        return context


class SectorListView(ListView):
    template_name = componentListView
    model = m.sector

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = " Register Brand In Sectors to Sell "
        context['component'] = []
        for obj in context['object_list']:
            context['component'].append(c.InformationCard(
                obj.name, obj.description, f"profit taken by Us {obj.profit_on_brand}%", f"Product Manager Offers {obj.type_of_manager_allowed}", f"/brand/create/{obj.pk}", obj.commit_allowed))
        return context


class MyBrandsList(ListView):
    template_name = componentListView
    model = m.brand

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['component'] = []
        if (self.request.user.is_authenticated):
            obj = m.brand.objects.filter(
                Q(owner=self.request.user.customer) & Q(is_active=True))
            for obj in obj:
                context['component'].append(c.CardsWithTwoButton(
                    f"/media/{obj.logo}", obj.name, obj.description, f"/brands/detail/{obj.pk}", " more information ", "show details", f"/brand/remove/{obj.pk}", " delete ", "Remove"))
        return context


class BrandsDetailView(DetailView):
    template_name = componentDetailView
    model = m.brand
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        canupdate = False
        update_url = ""
        context['component'] = []
        try:
            if (self.request.user.customer == context['object'].owner):
                update_url = f"/brand/update/{context['object'].pk}"
                self.add_drop_down_button(context)
                canupdate = True
        except Exception:
            pass
        context['name'] = context['object'].name
        context['component'].append(c.SliderCard(
            f"/media/{context['object'].bannar}", context['object'].name))
        context['component'].append(c.HeaderAndFooterCard(
            context['object'].name, context['object'].description, update_url))
        context['component'].append(c.LongDescription(
            context['object'].long_description))
        self.add_inventory_component(context, canupdate)
        self.add_software_component(context, canupdate)
        self.add_service_component(context, canupdate)

        return context

    def add_service_component(self, context, canupdate):
        lis = m.services_manager.objects.filter(Q(brands_product=context['object'].pk) & Q(
            is_active=True) & Q(brands_product__is_active=True))
        if lis:
            context['component'].append(c.TextBodyCard("Brands Services"))
            for obj in lis:
                if canupdate:
                    update_url = f"/service/update/{obj.pk}"
                    context['component'].append(c.RemoveBth(
                        f"/service/remove/{obj.pk}/{context['object'].pk}"))
                else:
                    update_url = ""
                context['component'].append(c.HorizontalImageCard(
                    f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.package_price}PKR ", f"/services/list/detail/{obj.pk}", "see more details", "detail", update_url))

    def add_inventory_component(self, context, canupdate):
        lis = m.inventory_managment.objects.filter(Q(brands_product=context['object'].pk) & Q(
            is_active=True) & Q(brands_product__is_active=True))
        if lis:
            context['component'].append(c.TextBodyCard("Inventory Products"))
            for obj in lis:
                if canupdate:
                    update_url = f"/inventory/update/{obj.pk}"
                    context['component'].append(c.RemoveBth(
                        f"/inventory/remove/{obj.pk}/{context['object'].pk}"))
                else:
                    update_url = ""
                context['component'].append(c.HorizontalImageCard(
                    f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.selling_price}PKR ", f"/inventory/list/detail/{obj.pk}", "see more details", "detail", update_url))

    def add_software_component(self, context, canupdate):
        lis = m.software_manager.objects.filter(Q(brands_product=context['object'].pk) & Q(
            is_active=True) & Q(brands_product__is_active=True))
        if lis:
            context['component'].append(c.TextBodyCard("Software Products"))
            for obj in lis:
                if canupdate:
                    update_url = f"/software/update/{obj.pk}"
                    context['component'].append(c.RemoveBth(
                        f"/software/remove/{obj.pk}/{context['object'].pk}"))
                else:
                    update_url = ""
                context['component'].append(c.HorizontalImageCard(
                    f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.selling_price}PKR ", f"/software/list/detail/{obj.pk}", "see more details", "detail", update_url))

    def add_drop_down_button(self, context):
        sec = context['object'].brand_sector
        types = sec.type_of_manager_allowed
        link_list = {}
        if types == "all":
            link_list['&plus; add inventory'] = f"/inventory/create/{context['object'].pk}"
            link_list['&plus; add software'] = f"/software/create/{context['object'].pk}"
            link_list['&plus; add service'] = f"/service/create/{context['object'].pk}"
        else:
            link_list[f'&plus; add {types}'] = f"/{types}/create/{context['object'].pk}"
        context['component'].append(c.DropDownButton(link_list))


def remove_brand(request, pk):
    obj = m.brand.objects.get(pk=pk)
    obj.is_active = False
    obj.save()
    return HttpResponseRedirect(f"/brands/list/")


def remove_software(request, pk, bk):
    obj = m.software_manager.objects.get(pk=pk)
    obj.is_active = False
    obj.save()
    return HttpResponseRedirect(f"/brands/detail/{bk}")


def remove_inventory(request, pk, bk):
    obj = m.inventory_managment.objects.get(pk=pk)
    obj.is_active = False
    obj.save()
    return HttpResponseRedirect(f"/brands/detail/{bk}")


def remove_services(request, pk, bk):
    obj = m.services_manager.objects.get(pk=pk)
    obj.is_active = False
    obj.save()
    return HttpResponseRedirect(f"/brands/detail/{bk}")


class InventoryManagerListView(ListView):
    template_name = componentListView
    model = m.inventory_managment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        si = self.request.GET.get("si")
        if si:
            context['object_list'] = m.inventory_managment.objects.filter(Q(name__icontains=si) | Q(description__icontains=si) | Q(long_description__icontains=si) | Q(selling_price__icontains=si) | Q(brands_product__name__icontains=si) | Q(
                brands_product__description__icontains=si) | Q(brands_product__location__icontains=si) & (Q(brands_product=context['object'].pk) & Q(is_active=True) & Q(brands_product__is_active=True))).order_by("selling_price")
        context['name'] = "Inventory Products"
        context['component'] = []
        for obj in context['object_list'].order_by("selling_price"):
            if obj.is_active and obj.brands_product.is_active:
                context['component'].append(c.CardsWithButton(f"/media/{obj.pic}", obj.name, obj.description, f"detail/{obj.pk}",
                                            f"price {obj.selling_price}PKR", get_inventory_complete_total(obj.pk), "see more details", "detail"))
        print()
        return context


class SoftwareManagerListView(ListView):
    template_name = componentListView
    model = m.software_manager

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        si = self.request.GET.get("si")
        if si:
            context['object_list'] = m.software_manager.objects.filter(Q(name__icontains=si) | Q(description__icontains=si) | Q(long_description__icontains=si) | Q(selling_price__icontains=si) | Q(brands_product__name__icontains=si) | Q(
                brands_product__description__icontains=si) | Q(brands_product__location__icontains=si) & (Q(brands_product=context['object'].pk) & Q(is_active=True) & Q(brands_product__is_active=True))).order_by("selling_price")
        context['name'] = "Softwares Products"
        context['component'] = []
        for obj in context['object_list'].order_by("selling_price"):
            if obj.is_active and obj.brands_product.is_active:
                context['component'].append(c.CardsWithButton(f"/media/{obj.pic}", obj.name, obj.description, f"detail/{obj.pk}",
                                            f"price {obj.selling_price}PKR", get_software_complete_total(obj.pk), "see more details", "detail"))
        return context


class ServicesManagerListView(ListView):
    template_name = componentListView
    model = m.services_manager

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        si = self.request.GET.get("si")
        if si:
            context['object_list'] = m.services_manager.objects.filter(Q(name__icontains=si) | Q(description__icontains=si) | Q(long_description__icontains=si) | Q(package_price__icontains=si) | Q(brands_product__name__icontains=si) | Q(
                brands_product__description__icontains=si) | Q(brands_product__location__icontains=si) & (Q(brands_product=context['object'].pk) & Q(is_active=True) & Q(brands_product__is_active=True))).order_by("package_price")
        context['name'] = "Services Offers"
        context['component'] = []
        for obj in context['object_list'].order_by("package_price"):
            if obj.is_active and obj.brands_product.is_active:
                context['component'].append(c.CardsWithButton(f"/media/{obj.pic}", obj.name, obj.description, f"detail/{obj.pk}",
                                            f"price {obj.package_price}PKR ", get_service_complete_total(obj.pk), "see more details", "detail"))
        return context


class InventoryDetailView(DetailView):
    template_name = componentDetailView
    model = m.inventory_managment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.name = "but"
        self.full_view = "full"
        self.less_view = "less"
        context['component'] = []
        obj = context['object']
        context['name'] = obj.name

        try:
            if (self.request.user.customer == context['object'].brands_product.owner):
                context['component'].append(c.HorizontalImageCardWidoutButtons(
                    f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.selling_price}PKR "))
                context['component'].append(self.owner_features_description(
                    context['object'], context['object'].brands_product.owner))
            else:
                context['component'].append(c.HorizontalImageCardWithForInventory(
                    f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.selling_price}PKR ", obj.amount, self.request.GET.get("dir"), self.request.GET.get("amo")))
                context['component'].append(
                    self.cust_features_description(context['object']))
        except Exception as e:
            print(e)
            context['component'].append(c.HorizontalImageCardWithForInventory(
                f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.selling_price}PKR ", obj.amount, self.request.GET.get("dir"), self.request.GET.get("amo")))
            context['component'].append(
                self.cust_features_description(context['object']))
        context['component'].append(c.LongDescription(
            context['object'].long_description))
        context['component'].append(c.RanKingCard(get_inventory_business_product_rank(context['object'].pk), get_inventory_happiness_product_rank(
            context['object'].pk), get_inventory_trans_product_rank(context['object'].pk)))
        self.add_inventory_relations(context)

        for comt in m.comment_on_inventory_order.objects.filter(order__manager_id=obj):
            context['component'].append(c.CommentsCard(
                comt.order.buyers_id.user.username, comt.rating, comt.comment))
        return context

    def cust_features_description(self, obj):
        inv_fea = m.inventory_items_featurers.objects.filter(manager_id=obj)
        features = c.cust_features(inv_fea)
        return c.features_bar(features.html)

    def owner_description_check(self):
        obj = self.object
        m.inventory_items_featurers.objects.create(manager_id=obj, description=self.request.GET.get(
            "feature"), ref_url=self.process_ref_value(self.request.GET.get("own_ref")))
        return HttpResponseRedirect(f"/inventory/list/detail/{obj.pk}")

    def process_ref_value(self, value):
        vallis = value.split("_")
        print("value lis", vallis)
        if vallis[0] != '-1':
            if vallis[1] == "inv":
                return f"/inventory/list/detail/{vallis[0]}"
            elif vallis[1] == "sof":
                return f"/software/list/detail/{vallis[0]}"
            elif vallis[1] == "ser":
                return f"/services/list/detail/{vallis[0]}"
        return None

    def owner_del_desc_check(self):
        print("p => ", self.request.GET.get("del_fea_btn"))
        m.inventory_items_featurers.objects.get(
            pk=self.request.GET.get("del_fea_btn")).delete()
        return HttpResponseRedirect(f"/inventory/list/detail/{self.object.pk}")

    def owner_features_description(self, obj, own):
        inv_fea = m.inventory_items_featurers.objects.filter(manager_id=obj)
        features = c.owner_features(inv_fea, m.inventory_managment.objects.filter(brands_product__owner=own), m.software_manager.objects.filter(
            brands_product__owner=own), m.services_manager.objects.filter(brands_product__owner=own))
        return c.features_bar(features.html)

    def get(self, request, pk):
        context = {'object': self.get_object()}
        self.object = self.get_object()
        try:
            amo = self.request.GET.get("amounts")
            if amo:
                print(amo, "have some thing")
                if amo.isdigit():
                    if self.request.user.is_authenticated:
                        amo = int(self.request.GET.get("amounts"))
                        if amo <= context['object'].amount and amo > 0:
                            print(amo, "order created")
                            saved_amount = context['object'].amount
                            context['object'].amount = saved_amount - amo
                            context['object'].save()
                            m.inventory_orders.objects.create(
                                manager_id=context['object'], buyers_id=self.request.user.customer, commited_amount=amo*context['object'].selling_price, amount_buy=amo)
                    else:
                        return redirect(f"/login/inventory/{pk}")
                if self.request.GET.get("insert_btn"):
                    return self.owner_description_check()
                if self.request.GET.get("del_fea_btn"):
                    return self.owner_del_desc_check()
        except Exception:
            pass
        return render(request, InventoryDetailView.template_name, self.get_context_data())

    def return_inventory_object_list(self, val, context):
        if val == self.full_view:
            return m.inventory_relations.objects.filter(Q(first=context['object']) | Q(second=context['object'])).order_by('-id')
        return m.inventory_relations.objects.filter(Q(first=context['object']) | Q(second=context['object'])).order_by('-id')[0:4]

    def add_inventory_relations(self, context):
        val = self.request.GET.get(self.name+"inv")
        lis = self.return_inventory_object_list(val, context)
        if lis:
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    f"Inventory Relations ", "show less", self.name+"inv", self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    f"Inventory Relations ", "show all", self.name+"inv", self.full_view))
            comp = []
            for objl in lis:
                if context['object'] == objl.first:
                    obj = objl.second
                else:
                    obj = objl.first
                comp.append(c.CardsWithButton(f"/media/{obj.pic}", obj.name, obj.description, f"{obj.pk}",
                            f"price {obj.selling_price}PKR", get_inventory_complete_total(obj.pk), "see more details", "detail"))
            context['component'].append(c.RelatedCards("Related Items", comp))


class SoftwareDetailView(DetailView):
    template_name = componentDetailView
    model = m.software_manager

    def get_context_data(self, **kwargs):
        self.name = "but"
        self.full_view = "full"
        self.less_view = "less"
        context = super().get_context_data(**kwargs)
        context['component'] = []
        obj = context['object']
        context['name'] = obj.name
        try:
            if (self.request.user.customer == context['object'].brands_product.owner):
                context['component'].append(c.HorizontalImageCardWidoutButtons(
                    f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.selling_price}PKR "))
                context['component'].append(self.owner_features_description(
                    context['object'], context['object'].brands_product.owner))
            else:
                context['component'].append(c.HorizontalImageCardWithForSoftware(
                    f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.selling_price}PKR "))
                context['component'].append(
                    self.cust_features_description(context['object']))
        except Exception:
            context['component'].append(c.HorizontalImageCardWithForSoftware(
                f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.selling_price}PKR "))
            context['component'].append(
                self.cust_features_description(context['object']))
        context['component'].append(c.LongDescription(
            context['object'].long_description))
        context['component'].append(c.RanKingCard(get_software_business_product_rank(context['object'].pk), get_software_happiness_product_rank(
            context['object'].pk), get_software_trans_product_rank(context['object'].pk)))
        self.add_software_relations(context)
        for comt in m.comment_on_software_order.objects.filter(order__manager_id=obj):
            context['component'].append(c.CommentsCard(
                comt.order.buyers_id.user.username, comt.rating, comt.comment))
        return context

    def cust_features_description(self, obj):
        inv_fea = m.software_featurers.objects.filter(manager_id=obj)
        features = c.cust_features(inv_fea)
        return c.features_bar(features.html)

    def owner_description_check(self):
        obj = self.object
        m.software_featurers.objects.create(manager_id=obj, description=self.request.GET.get(
            "feature"), ref_url=self.process_ref_value(self.request.GET.get("own_ref")))
        return HttpResponseRedirect(f"/software/list/detail/{obj.pk}")

    def process_ref_value(self, value):
        vallis = value.split("_")
        if vallis[0] != '-1':
            if vallis[1] == "inv":
                return f"/inventory/list/detail/{vallis[0]}"
            elif vallis[1] == "sof":
                return f"/software/list/detail/{vallis[0]}"
            elif vallis[1] == "ser":
                return f"/services/list/detail/{vallis[0]}"
        return None

    def owner_del_desc_check(self):
        m.software_featurers.get(
            pk=self.request.GET.get("del_fea_btn")).delete()
        return HttpResponseRedirect(f"/software/list/detail/{self.object.pk}")

    def owner_features_description(self, obj, own):
        inv_fea = m.software_featurers.objects.filter(manager_id=obj)
        features = c.owner_features(inv_fea, m.inventory_managment.objects.filter(brands_product__owner=own), m.software_manager.objects.filter(brands_product__owner=own),
                                    m.services_manager.objects.filter(brands_product__owner=own))
        return c.features_bar(features.html)

    def get(self, request, pk):
        context = {'object': self.get_object()}
        self.object = self.get_object()
        try:
            if self.request.GET.get("software"):
                if self.request.user.is_authenticated:
                    m.software_orders.objects.create(manager_id=context['object'], buyers_id=self.request.user.customer,
                                                     commited_amount=context['object'].selling_price, url=context['object'].product_url)
                else:
                    return redirect(f"/login/software/{pk}")
            if self.request.GET.get("insert_btn"):
                return self.owner_description_check()
            if self.request.GET.get("del_fea_btn"):
                return self.owner_del_desc_check()
        except Exception:
            pass
        return render(request, InventoryDetailView.template_name, self.get_context_data())

    def return_software_object_list(self, val, context):
        if val == self.full_view:
            return m.software_relations.objects.filter(Q(first=context['object']) | Q(second=context['object'])).order_by('-id')
        return m.software_relations.objects.filter(Q(first=context['object']) | Q(second=context['object'])).order_by('-id')[0:4]

    def add_software_relations(self, context):
        val = self.request.GET.get(self.name+"inv")
        lis = self.return_software_object_list(val, context)
        if lis:
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    f"Software Relations ", "show less", self.name+"inv", self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    f"Software Relations ", "show all", self.name+"inv", self.full_view))
            comp = []
            for objl in lis:
                if context['object'] == objl.first:
                    obj = objl.second
                else:
                    obj = objl.first
                comp.append(c.CardsWithButton(f"/media/{obj.pic}", obj.name, obj.description, f"{obj.pk}",
                            f"price {obj.selling_price}PKR", get_software_complete_total(obj.pk), "see more details", "detail"))
            context['component'].append(c.RelatedCards("Related Items", comp))


def delete_portfolio(request, serv_id, port_id):
    obj = m.service_portfolio.objects.get(pk=port_id)
    obj.delete()
    return redirect(f"/services/list/detail/{serv_id}")


class PortfolioCreateForm(ModelForm):
    class Meta:
        model = m.service_portfolio
        fields = ['project_name', "project_short_description",
                  "starting_date", "ending_date", "project_url_link"]


def create_portfolio(request, ser_id):
    obj = m.services_manager.objects.get(pk=ser_id)
    if request.method == 'POST':
        form = PortfolioCreateForm(request.POST)
        if form.is_valid():
            request_form = form.instance
            request_form.manager = obj
            request_form.save()
            return redirect(f'/services/list/detail/{ser_id}')
        else:
            return render(request, componentFormView, {'form': form, "name": f"Add Portfolio delails "})
    return render(request, componentFormView, {'form': PortfolioCreateForm, "name": f" Add Portfolio delails "})


class ServicesDetailView(DetailView):
    template_name = componentDetailView
    model = m.services_manager

    def get_context_data(self, **kwargs):
        self.name = "but"
        self.full_view = "full"
        self.less_view = "less"
        context = super().get_context_data(**kwargs)
        context['component'] = []
        obj = context['object']
        context['name'] = obj.name
        try:
            if (self.request.user.customer == context['object'].brands_product.owner):
                context['component'].append(c.HorizontalImageCardWidoutButtons(
                    f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.package_price}PKR "))
                context['component'].append(self.owner_features_description(
                    context['object'], context['object'].brands_product.owner))
                context['component'].append(c.PortfolioBar(m.service_portfolio.objects.filter(
                    manager=obj), f"/services/list/detail/create/portfolio/{obj.pk}", f"/services/list/detail/delete/portfolio/{obj.pk}/"))
            elif self.request.user.is_authenticated:
                context['component'].append(c.HorizontalImageCard(
                    f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.package_price}PKR ", f"/request/on/service/{obj.pk}", "send request", "Send Request"))
                context['component'].append(
                    self.cust_features_description(context['object']))
                context['component'].append(c.PortfolioBar(
                    m.service_portfolio.objects.filter(manager=obj)))
            else:
                context['component'].append(c.HorizontalImageCard(
                    f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.package_price}PKR ", f"/login/services/{obj.pk}", "to send request login first", "Login"))
                context['component'].append(
                    self.cust_features_description(context['object']))
                context['component'].append(c.PortfolioBar(
                    m.service_portfolio.objects.filter(manager=obj)))
        except Exception:
            print(" exceptions ")
            context['component'].append(c.HorizontalImageCard(
                f"/media/{obj.pic}", obj.name, obj.description, f"price {obj.package_price}PKR ", f"/login/services/{obj.pk}", "to send request login first", "Login"))
            context['component'].append(
                self.cust_features_description(context['object']))
            context['component'].append(c.PortfolioBar(
                m.service_portfolio.objects.filter(manager=obj)))
        context['component'].append(c.LongDescription(
            context['object'].long_description))
        context['component'].append(c.RanKingCard(get_service_business_product_rank(context['object'].pk), get_service_happiness_product_rank(
            context['object'].pk), get_service_trans_product_rank(context['object'].pk)))
        self.add_services_relations(context)
        for comt in m.comment_on_service.objects.filter(order__request_id__service_id=obj):
            context['component'].append(c.CommentsCard(
                comt.order.request_id.customer_id.user.username, comt.rating, comt.comment))
        return context

    def cust_features_description(self, obj):
        inv_fea = m.service_featurers.objects.filter(manager_id=obj)
        features = c.cust_features(inv_fea)
        return c.features_bar(features.html)

    def owner_description_check(self):
        obj = self.object
        m.service_featurers.objects.create(manager_id=obj, description=self.request.GET.get(
            "feature"), ref_url=self.process_ref_value(self.request.GET.get("own_ref")))
        return HttpResponseRedirect(f"/services/list/detail/{obj.pk}")

    def process_ref_value(self, value):
        vallis = value.split("_")
        if vallis[0] != '-1':
            if vallis[1] == "inv":
                return f"/inventory/list/detail/{vallis[0]}"
            elif vallis[1] == "sof":
                return f"/software/list/detail/{vallis[0]}"
            elif vallis[1] == "ser":
                return f"/services/list/detail/{vallis[0]}"
        return None

    def owner_del_desc_check(self):
        m.service_featurers.delete(pk=self.request.GET.get("del_fea_btn"))
        return HttpResponseRedirect(f"/services/list/detail/{self.object.pk}")

    def owner_features_description(self, obj, own):
        inv_fea = m.service_featurers.objects.filter(manager_id=obj)
        features = c.owner_features(inv_fea, m.inventory_managment.objects.filter(brands_product__owner=own), m.software_manager.objects.filter(brands_product__owner=own),
                                    m.services_manager.objects.filter(brands_product__owner=own))
        return c.features_bar(features.html)

    def get(self, request, pk):
        context = {'object': self.get_object()}
        self.object = self.get_object()
        try:
            if self.request.GET.get("software"):
                if self.request.user.is_authenticated:
                    m.software_orders.objects.create(manager_id=context['object'], buyers_id=self.request.user.customer,
                                                     commited_amount=context['object'].selling_price, url=context['object'].product_url)
                else:
                    return redirect("/accounts/login")
            if self.request.GET.get("insert_btn"):
                return self.owner_description_check()
            if self.request.GET.get("del_fea_btn"):
                return self.owner_del_desc_check()

        except Exception as e:
            print(e)
        return render(request, InventoryDetailView.template_name, self.get_context_data())

    def return_services_object_list(self, val, context):
        if val == self.full_view:
            return m.service_relations.objects.filter(Q(first=context['object']) | Q(second=context['object'])).order_by('-id')
        return m.service_relations.objects.filter(Q(first=context['object']) | Q(second=context['object'])).order_by('-id')[0:4]

    def add_services_relations(self, context):
        val = self.request.GET.get(self.name+"inv")
        lis = self.return_services_object_list(val, context)
        if lis:
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    f"services Relations ", "show less", self.name+"inv", self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    f"services Relations ", "show all", self.name+"inv", self.full_view))
            comp = []
            for objl in lis:
                if context['object'] == objl.first:
                    obj = objl.second
                else:
                    obj = objl.first
                comp.append(c.CardsWithButton(f"/media/{obj.pic}", obj.name, obj.description, f"{obj.pk}",
                            f"price {obj.package_price}PKR", get_service_complete_total(obj.pk), "see more details", "detail"))
            context['component'].append(c.RelatedCards("Related Items", comp))


class MessagesView(TemplateView):
    template_name = componentDetailView

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['component'] = []
        context['name'] = "messages"
        context['component'].append(c.CreateMessageButton(
            "/compose/message/", "/send/message/", "/recived/message/"))
        objlis = m.message.objects.filter(
            reciver=self.request.user.customer).order_by('-pk')
        for obj in objlis:
            if obj.revived:
                context['component'].append(c.MessageCard(
                    obj.sender.user.username, obj.subject, f"/detail/message/{obj.pk}", "btn-success"))
            else:
                context['component'].append(c.MessageCard(
                    obj.sender.user.username, obj.subject, f"/detail/message/{obj.pk}", "btn-secondary"))
        return context


class MessagesRecivedView(TemplateView):
    template_name = componentDetailView

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['component'] = []
        context['name'] = "messages"
        context['component'].append(c.CreateMessageButton(
            "/compose/message/", "/send/message/", "/recived/message/"))
        objlis = m.message.objects.filter(
            sender=self.request.user.customer).order_by('-pk')
        for obj in objlis:
            context['component'].append(c.HeaderAndFooterCard(
                f"recived by {obj.reciver.user.username}", f"{obj.subject} <br/> {obj.msg}"))
        return context


class MessageDetailView(DetailView):
    template_name = componentDetailView
    model = m.message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['component'] = []
        context['name'] = "messages"
        obj = context['object']
        context['component'].append(c.MessageDetailCard(
            obj.sender.user.username, obj.subject, obj.msg, obj.reciver.user.username))
        context['component'].append(c.CreateMessageButton(
            "/send/message/", firts_name="Back"))
        obj.revived = True
        obj.save()
        return context


class ServiceOrderDetailViewByCart(DetailView):
    template_name = componentDetailView
    model = m.service_order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['component'] = []
        context['name'] = "messages"
        obj = context['object']
        context['component'].append(c.MessageDetailCard(obj.request_id.customer_id.user.username, obj.request_id.form.problem_title,
                                    f"<p><strong>BackGround</strong></p><p>{obj.request_id.form.background}</p> <p><strong>Demands</strong></p><p>{obj.request_id.form.demands}</p> <p><strong>Links Of Inspiration</strong></p><p>{obj.request_id.form.first_link_of_inspiration}</p><p>{obj.request_id.form.second_link_of_inspiration}</p> <p>{obj.request_id.form.third_link_of_inspiration}</p> <p><strong> Project Complition Date {obj.request_id.form.completion_date} </strong></p> ", obj.request_id.service_id.brands_product.owner.user.username))
        context['component'].append(c.CreateMessageButton(
            "/customers/cart/", firts_name="Back"))
        return context


class ServiceOrderDetailViewByOwner(DetailView):
    template_name = componentDetailView
    model = m.service_order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['component'] = []
        context['name'] = "messages"
        obj = context['object']
        context['component'].append(c.MessageDetailCard(obj.request_id.customer_id.user.username, obj.request_id.form.problem_title,
                                    f"<p><strong>BackGround</strong></p><p>{obj.request_id.form.background}</p> <p><strong>Demands</strong></p><p>{obj.request_id.form.demands}</p> <p><strong>Links Of Inspiration</strong></p><p>{obj.request_id.form.first_link_of_inspiration}</p><p>{obj.request_id.form.second_link_of_inspiration}</p> <p>{obj.request_id.form.third_link_of_inspiration}</p> <p><strong> Project Complition Date {obj.request_id.form.completion_date} </strong></p> ", obj.request_id.service_id.brands_product.owner.user.username))
        context['component'].append(c.CreateMessageButton(
            "/brands/cart/", firts_name="Back"))
        return context


class ClientCartCompleteView(TemplateView):
    template_name = componentListView

    def get_context_data(self, **kwargs):
        self.name = "but"
        self.full_view = "full"
        self.less_view = "less"
        self.complete_ness = Q(is_commited_by_customer=True) & Q(is_commited_by_owner=True) & Q(
            is_finantial_transaction=True) & Q(buyers_id=self.request.user.customer)
        self.complete_ness1 = Q(is_commited_by_customer=True) & Q(is_commited_by_owner=True) & Q(
            is_finantial_transaction=True) & Q(request_id__customer_id=self.request.user.customer)
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['component'] = []
            context['name'] = f"{self.request.user.username}'s Cart"
            val = self.request.GET.get(self.name)
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    "Completed Orders History", "show less", self.name, self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    "Completed Orders History", "show all", self.name, self.full_view))

            inv = self.return_inventory_object_list()
            soft = self.return_software_object_list()
            serv = self.return_service_object_list()
            self.add_all_orders(context, inv, soft, serv)
            # self.add_inventory_orders(context)
            # self.add_software_orders(context)
            # self.add_service_orders(context)
        return context

    def add_all_orders(self, context, inv, soft, serv):
        inv_counter = 0
        soft_counter = 0
        serv_counter = 0
        lis = []
        while True:
            lis.clear()
            if len(inv) > inv_counter:
                lis.append([inv[inv_counter], self.add_inventory_orders])
                inv_counter += 1
            if len(soft) > soft_counter:
                lis.append([soft[soft_counter], self.add_software_orders])
                soft_counter += 1
            if len(serv) > serv_counter:
                lis.append([serv[serv_counter], self.add_service_orders])
                serv_counter += 1
            lis = self.sort_list(lis)
            for i in lis:
                i[1](context, i[0])
            if len(inv) <= inv_counter and len(soft) <= soft_counter and len(serv) <= serv_counter:
                break

    def sort_list(self, lis):
        def swap_positions(pos1, pos2):
            lis[pos1], lis[pos2] = lis[pos2], lis[pos1]
        for i in range(len(lis)):
            nex = i + 1
            if len(lis) > nex:
                if lis[nex][0].date_of_order > lis[i][0].date_of_order:
                    swap_positions(nex, i)
            else:
                return lis
        return lis

    def return_inventory_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.inventory_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_complete=True) | self.complete_ness).order_by('-id')
        return m.inventory_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_complete=True) | self.complete_ness).order_by('-id')[0:4]

    def return_software_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.software_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_complete=True) | self.complete_ness).order_by('-id')
        return m.software_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_complete=True) | self.complete_ness).order_by('-id')[0:4]

    def return_service_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.service_order.objects.filter(Q(request_id__customer_id=self.request.user.customer) & Q(is_complete=True) | self.complete_ness1).order_by('-id')
        return m.service_order.objects.filter(Q(request_id__customer_id=self.request.user.customer) & Q(is_complete=True) | self.complete_ness1).order_by('-id')[0:4]

    def add_inventory_orders(self, context, obj):
        if admin_auto_commit(obj, obj.manager_id, obj.buyers_id.customers_account, obj.manager_id.brands_product.owner.customers_account):
            if obj.is_reviewed == False:
                context['component'].append(c.OrdersCardWithTwoButtons(obj.manager_id.name, "inventory", f' unit Price {obj.manager_id.selling_price}', f" amount bought {obj.amount_buy} ",
                                            f"total bill {obj.commited_amount}PKR", f"/create/inventory/report/{obj.pk}", "report", f"/create/inventory/comments/{obj.pk}", "comment"))
            else:
                rep = m.report_on_inventory.objects.filter(order=obj)
                if rep:
                    print(" rollback ")
                    if admin_auto_rollback(rep, obj, obj.manager_id, obj.buyers_id.customers_account,  obj.manager_id.brands_product.owner.customers_account):
                        context['component'].append(c.OrdersCardWithOutButtons(
                            obj.manager_id.name, "inventory", f' unit Price {obj.manager_id.selling_price}', f" amount bought {obj.amount_buy} ", f"total bill {obj.commited_amount}PKR", "RollBacked"))
                    else:
                        context['component'].append(c.OrdersCardWithOutButtons(
                            obj.manager_id.name, "inventory", f' unit Price {obj.manager_id.selling_price}', f" amount bought {obj.amount_buy} ", f"total bill {obj.commited_amount}PKR", "Report under discussion"))
                else:
                    context['component'].append(c.OrdersCardWithOutButtons(
                        obj.manager_id.name, "inventory", f' unit Price {obj.manager_id.selling_price}', f" amount bought {obj.amount_buy} ", f"total bill {obj.commited_amount}PKR", "Completed"))

    def add_software_orders(self, context, obj):
        if admin_auto_commit(obj, obj.manager_id, obj.buyers_id.customers_account, obj.manager_id.brands_product.owner.customers_account):

            if obj.is_reviewed == False:
                context['component'].append(c.OrdersCardWithTwoButtons(
                    obj.manager_id.name, "software",
                    f' unit Price {obj.manager_id.selling_price}',
                    f" url: {obj.url} ",
                    f"total bill {obj.commited_amount}PKR",
                    f"/create/software/report/{obj.pk}",
                    "report",
                    f"/create/software/comments/{obj.pk}",
                    "comment"))
            else:
                rep = m.report_on_software.objects.filter(order=obj)
                if rep:
                    if admin_auto_rollback(rep, obj, obj.manager_id, obj.buyers_id.customers_account, obj.manager_id.brands_product.owner.customers_account):
                        context['component'].append(c.OrdersCardWithOutButtons(
                            obj.manager_id.name, "software",
                            f' unit Price {obj.manager_id.selling_price}',
                            f" url: {obj.url} ",
                            f"total bill {obj.commited_amount}PKR", "Roll Backed"))
                    else:
                        context['component'].append(c.OrdersCardWithOutButtons(
                            obj.manager_id.name, "software",
                            f' unit Price {obj.manager_id.selling_price}',
                            f" url: {obj.url} ",
                            f"total bill {obj.commited_amount}PKR", "Report under discussion"))
                else:
                    context['component'].append(c.OrdersCardWithOutButtons(
                        obj.manager_id.name, "software",
                        f' unit Price {obj.manager_id.selling_price}',
                        f" url: {obj.url} ",
                        f"total bill {obj.commited_amount}PKR", "Completed"))

    def add_service_orders(self, context, obj):
        if admin_auto_commit(obj, obj.request_id.service_id, obj.request_id.customer_id.customers_account, obj.request_id.service_id.brands_product.owner.customers_account):
            if obj.is_reviewed == False:
                context['component'].append(c.OrdersCardWithTwoButtons(obj.request_id.service_id.name, "service", f' unit Price {obj.request_id.service_id.package_price}',
                                            f"see Details: <a class = 'btn btn-primary' href='/service/order/detail/cust/{obj.pk}'>detail</a>", f"total bill {obj.commited_amount}PKR", f"/create/services/report/{obj.pk}", "report", f"/create/services/comments/{obj.pk}", "comment"))
            else:
                rep = m.report_on_service.objects.filter(order=obj)
                if rep:
                    if admin_auto_rollback(rep, obj, obj.request_id.service_id, obj.request_id.customer_id.customers_account, obj.request_id.service_id.brands_product.owner.customers_account):
                        context['component'].append(c.OrdersCardWithOutButtons(obj.request_id.service_id.name, "service", f' unit Price {obj.request_id.service_id.package_price}',
                                                    f"see Details: <a class = 'btn btn-primary' href='/service/order/detail/cust/{obj.pk}'>detail</a>", f"total bill {obj.commited_amount}PKR", "RollBacked"))
                    else:
                        context['component'].append(c.OrdersCardWithOutButtons(obj.request_id.service_id.name, "service", f' unit Price {obj.request_id.service_id.package_price}',
                                                    f"see Details: <a class = 'btn btn-primary' href='/service/order/detail/cust/{obj.pk}'>detail</a>", f"total bill {obj.commited_amount}PKR", "Report under discussion"))
                else:
                    context['component'].append(c.OrdersCardWithOutButtons(obj.request_id.service_id.name, "service",
                                                f' unit Price {obj.request_id.service_id.package_price}', f"see Details: <a class = 'btn btn-primary' href='/service/order/detail/cust/{obj.pk}'>detail</a>", f"total bill {obj.commited_amount}PKR", "Completed"))


class ClientCartOrdersView(TemplateView):
    template_name = componentListView

    def get_context_data(self, **kwargs):
        self.name = "but"
        self.full_view = "full"
        self.less_view = "less"
        self.total_purchase = 0
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['component'] = []
            context['name'] = f"{self.request.user.username}'s Cart"
            val = self.request.GET.get(self.name)
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    "Orders History", "show less", self.name, self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    "Orders History", "show all", self.name, self.full_view))

            inv = self.return_inventory_object_list()
            soft = self.return_software_object_list()
            serv = self.return_service_object_list()
            self.add_all_orders(context, inv, soft, serv)
            # self.add_inventory_orders(context)
            # self.add_software_orders(context)
            # self.add_service_orders(context)
            if self.request.user.customer.customers_account.balance < self.total_purchase:
                have_to_pay = self.total_purchase - \
                    self.request.user.customer.customers_account.balance
                context['component'].insert(0, c.Bill(
                    self.total_purchase, self.request.user.customer.customers_account.balance, f"/checkoutform/{have_to_pay}/{self.total_purchase}/"))
            else:
                context['component'].insert(0, c.Bill_Form(
                    self.total_purchase, self.request.user.customer.customers_account.balance))
        return context

    def get(self, request):
        if request.GET.get("check_out_fin") == "checked_click":
            commit_check_out_orders(
                request, request.user.customer.customers_account, None)
            return HttpResponseRedirect("/customers/cart/")
        return render(request, componentListView, self.get_context_data())

    def add_all_orders(self, context, inv, soft, serv):
        inv_counter = 0
        soft_counter = 0
        serv_counter = 0
        lis = []
        while True:
            lis.clear()
            if len(inv) > inv_counter:
                lis.append([inv[inv_counter], self.add_inventory_orders])
                inv_counter += 1
            if len(soft) > soft_counter:
                lis.append([soft[soft_counter], self.add_software_orders])
                soft_counter += 1
            if len(serv) > serv_counter:
                lis.append([serv[serv_counter], self.add_service_orders])
                serv_counter += 1
            lis = self.sort_list(lis)
            for i in lis:
                i[1](context, i[0])
            if len(inv) <= inv_counter and len(soft) <= soft_counter and len(serv) <= serv_counter:
                break

    def sort_list(self, lis):
        def swap_positions(pos1, pos2):
            lis[pos1], lis[pos2] = lis[pos2], lis[pos1]
        for i in range(len(lis)):
            nex = i + 1
            if len(lis) > nex:
                if lis[nex][0].date_of_order > lis[i][0].date_of_order:
                    swap_positions(nex, i)
            else:
                return lis
        return lis

    def return_inventory_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.inventory_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=False)).order_by('-id')
        return m.inventory_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=False)).order_by('-id')[0:4]

    def return_software_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.software_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=False)).order_by('-id')
        return m.software_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=False)).order_by('-id')[0:4]

    def return_service_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.service_order.objects.filter(Q(request_id__customer_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=False)).order_by('-id')
        return m.service_order.objects.filter(Q(request_id__customer_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=False)).order_by('-id')[0:4]

    def add_inventory_orders(self, context, obj):
        self.total_purchase += obj.commited_amount
        context['component'].append(c.OrdersCardWithOneButtons(obj.manager_id.name, "inventory",
                                    f' unit Price {obj.manager_id.selling_price}', f" amount bought {obj.amount_buy} ", f"total bill {obj.commited_amount}PKR", f"/user/cart/inventory/delete/{obj.pk}", "delete"))

    def add_software_orders(self, context, obj):
        self.total_purchase += obj.commited_amount
        context['component'].append(c.OrdersCardWithOneButtons(obj.manager_id.name, "software",
                                    f' unit Price {obj.manager_id.selling_price}', f" url: after commit url appear ", f"total bill {obj.commited_amount}PKR", f"/user/cart/software/delete/{obj.pk}", "delete"))

    def add_service_orders(self, context, obj):
        self.total_purchase += obj.commited_amount
        context['component'].append(c.OrdersCardWithOneButtons(obj.request_id.service_id.name, "services", f' unit Price {obj.request_id.service_id.package_price}',
                                    f"see Details: <a class = 'btn btn-primary' href='/service/order/detail/cust/{obj.pk}'>detail</a>", f"total bill {obj.commited_amount}PKR", f"/user/cart/service/delete/{obj.pk}", "delete"))


class ClientCancelOrdersView(TemplateView):
    template_name = componentListView

    def get_context_data(self, **kwargs):
        self.name = "but"
        self.full_view = "full"
        self.less_view = "less"
        self.total_purchase = 0
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['component'] = []
            context['name'] = f"{self.request.user.username}'s Cancel Orders"
            val = self.request.GET.get(self.name)
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    "Orders History", "show less", self.name, self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    "Orders History", "show all", self.name, self.full_view))

            inv = self.return_inventory_object_list()
            soft = self.return_software_object_list()
            serv = self.return_service_object_list()
            self.add_all_orders(context, inv, soft, serv)
            # self.add_inventory_orders(context)
            # self.add_software_orders(context)
            # self.add_service_orders(context)
        return context

    def get(self, request):
        if request.GET.get("check_out_fin") == "checked_click":
            commit_check_out_orders(
                request, request.user.customer.customers_account, None)
            return HttpResponseRedirect("/customers/cart/")
        return render(request, componentListView, self.get_context_data())

    def add_all_orders(self, context, inv, soft, serv):
        inv_counter = 0
        soft_counter = 0
        serv_counter = 0
        lis = []
        while True:
            lis.clear()
            if len(inv) > inv_counter:
                lis.append([inv[inv_counter], self.add_inventory_orders])
                inv_counter += 1
            if len(soft) > soft_counter:
                lis.append([soft[soft_counter], self.add_software_orders])
                soft_counter += 1
            if len(serv) > serv_counter:
                lis.append([serv[serv_counter], self.add_service_orders])
                serv_counter += 1
            lis = self.sort_list(lis)
            for i in lis:
                i[1](context, i[0])
            if len(inv) <= inv_counter and len(soft) <= soft_counter and len(serv) <= serv_counter:
                break

    def sort_list(self, lis):
        def swap_positions(pos1, pos2):
            lis[pos1], lis[pos2] = lis[pos2], lis[pos1]
        for i in range(len(lis)):
            nex = i + 1
            if len(lis) > nex:
                if lis[nex][0].date_of_order > lis[i][0].date_of_order:
                    swap_positions(nex, i)
            else:
                return lis
        return lis

    def return_inventory_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.inventory_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=True) | Q(is_reported=True)).order_by('-id')
        return m.inventory_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=True) | Q(is_reported=True)).order_by('-id')[0:4]

    def return_software_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.software_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=True) | Q(is_reported=True)).order_by('-id')
        return m.software_orders.objects.filter(Q(buyers_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=True) | Q(is_reported=True)).order_by('-id')[0:4]

    def return_service_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.service_order.objects.filter(Q(request_id__customer_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=True) | Q(is_reported=True)).order_by('-id')
        return m.service_order.objects.filter(Q(request_id__customer_id=self.request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=True) | Q(is_reported=True)).order_by('-id')[0:4]

    def add_inventory_orders(self, context, obj):
        self.total_purchase += obj.commited_amount
        context['component'].append(c.OrdersCardWithOneButtons(obj.manager_id.name, "inventory",
                                    f' unit Price {obj.manager_id.selling_price}', f" amount bought {obj.amount_buy} ", f"total bill {obj.commited_amount}PKR", f"/user/cart/inventory/delete/{obj.pk}", "delete"))

    def add_software_orders(self, context, obj):
        self.total_purchase += obj.commited_amount
        context['component'].append(c.OrdersCardWithOneButtons(obj.manager_id.name, "software",
                                    f' unit Price {obj.manager_id.selling_price}', f" url: after commit url appear ", f"total bill {obj.commited_amount}PKR", f"/user/cart/software/delete/{obj.pk}", "delete"))

    def add_service_orders(self, context, obj):
        self.total_purchase += obj.commited_amount
        context['component'].append(c.OrdersCardWithOneButtons(obj.request_id.service_id.name, "services", f' unit Price {obj.request_id.service_id.package_price}',
                                    f"see Details: <a class = 'btn btn-primary' href='/service/order/detail/cust/{obj.pk}'>detail</a>", f"total bill {obj.commited_amount}PKR", f"/user/cart/service/delete/{obj.pk}", "delete"))


class CashInCreateForm(ModelForm):
    class Meta:
        model = m.cash_in
        fields = ['description', "amount"]


def enter_cashin(request, turn_id):
    obj = m.accounts_turn.objects.get(pk=turn_id)
    if request.method == 'POST':
        form = CashInCreateForm(request.POST)
        if form.is_valid():
            request_form = form.instance
            request_form.turn = obj
            request_form.save()
            return redirect(f'/customer/finantial/ledger/{turn_id}')
        else:
            return render(request, componentFormView, {'form': form, "name": "Enter Income Details "})
    return render(request, componentFormView, {'form': CashInCreateForm, "name": "Enter Income Details "})


class CashOutCreateForm(ModelForm):
    class Meta:
        model = m.cash_out
        fields = ['description', "amount"]


def enter_cashout(request, turn_id):
    obj = m.accounts_turn.objects.get(pk=turn_id)
    if request.method == 'POST':
        form = CashOutCreateForm(request.POST)
        if form.is_valid():
            request_form = form.instance
            request_form.turn = obj
            request_form.save()
            return redirect(f'/customer/finantial/ledger/{turn_id}')
        else:
            return render(request, componentFormView, {'form': form, "name": "Enter Investment Details "})
    return render(request, componentFormView, {'form': CashOutCreateForm, "name": " Enter Investment Details "})


def remove_turn(request, turn_id):
    obj = m.accounts_turn.objects.get(pk=turn_id)
    obj.activate = False
    obj.save()
    return redirect("/customer/finantial/")


def start_new_turn(request):
    m.accounts_turn.objects.create(user=request.user.customer)
    return redirect("/customer/finantial/")

def complete_turn(request,turn_id):
    obj = m.accounts_turn.objects.get(pk = turn_id)
    obj.ending_date = str(date.today())
    total_in = m.cash_in.objects.filter(turn=obj).aggregate(Sum('amount'))['amount__sum']
    total_out = m.cash_out.objects.filter(turn=obj).aggregate(Sum('amount'))['amount__sum']
    obj.total_gain = total_in - total_out
    obj.is_complete = True
    obj.save()
    return redirect("/customer/finantial/")

class DetailLedgerUrl(DetailView):
    template_name = componentDetailView
    model = m.accounts_turn

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['component'] = []
            context['name'] = f"{self.request.user.username}'s Ledger"
            if context['object'].is_complete == False:
                context['component'].append(c.EnterCashBar(
                    f"/customer/finantial/ledger/cashin/{context['object'].pk}",
                    f"/customer/finantial/ledger/cashout/{context['object'].pk}",
                    f"/customer/finantial/ledger/turn/complete/{context['object'].pk}"))
            context['component'].append(c.LedgerDetail(m.cash_in.objects.filter(
                turn=context['object']), m.cash_out.objects.filter(turn=context['object'])))
        return context


class FinantialListView(TemplateView):
    template_name = componentDetailView

    def get_context_data(self, **kwargs):
        error = ""
        context = super().get_context_data(**kwargs)
        if self.request.GET.get("recive_btn") and self.request.GET.get("widthraw_amount"):
            amo = int(self.request.GET.get("widthraw_amount"))
            if amo <= self.request.user.customer.customers_account.balance:
                resp = eas.p2p_transfer(amo, self.request.GET.get("msid"))
                if resp["responce"]["responseCode"] != "0000":
                    error = f" Oops Their might be some problem contect admin at {admin_handle} handle"
            else:
                error = " You Can Not Widraw That Much Amount Of Money "
        if self.request.user.is_authenticated:
            context['component'] = []
            context['name'] = f"{self.request.user.username}'s Accounts"
            context['component'].append(c.CreateFinnantialForm(error))
            context['component'].append(c.FinantialTableBalance(
                self.request.user.customer.customers_account.balance, self.request.user.customer.customers_account.commited_balance))
            context['component'].append(c.LedgerAddButton(
                "/customer/finantial/ledger/turn/start"))
            cards = ""
            for inc in m.accounts_turn.objects.filter(user=self.request.user.customer):
                cashin = m.cash_in.objects.filter(
                    turn=inc).aggregate(Sum('amount'))['amount__sum']
                cashout = m.cash_out.objects.filter(
                    turn=inc).aggregate(Sum('amount'))['amount__sum']
                if cashin == None:
                    cashin = 0
                if cashout == None:
                    cashout = 0
                cards += c.IncomeLedger(inc, f"/customer/finantial/ledger/{inc.pk}",
                                        f"/customer/finantial/ledger/turn/remove/{inc.pk}", cashin, cashout).html
            context['component'].append(c.FlexBox(cards))
            # context['component'].append(c.IncomeLedger())
            # self.add_inventory_orders(context)
            # self.add_software_orders(context)
            # self.add_service_orders(context)
        return context


class BrandsCompletCartDetailView(DetailView):
    template_name = componentListView
    model = m.brand

    def get_context_data(self, **kwargs):
        self.name = "but"
        self.full_view = "full"
        self.less_view = "less"
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            self.brn = context['object']
            context['component'] = []
            context['name'] = f"{self.request.user.username}'s Orders"
            val = self.request.GET.get(self.name)
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    f"{self.brn} Orders ", "show less", self.name, self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    f"{self.brn} Orders ", "show all", self.name, self.full_view))

            inv = self.return_inventory_object_list()
            soft = self.return_software_object_list()
            serv = self.return_service_object_list()
            self.add_all_orders(context, inv, soft, serv)
            # self.add_inventory_orders(context)
            # self.add_software_orders(context)
            # self.add_service_orders(context)
        return context

    def add_all_orders(self, context, inv, soft, serv):
        inv_counter = 0
        soft_counter = 0
        serv_counter = 0
        lis = []
        while True:
            lis.clear()
            if len(inv) > inv_counter:
                lis.append([inv[inv_counter], self.add_inventory_orders])
                inv_counter += 1
            if len(soft) > soft_counter:
                lis.append([soft[soft_counter], self.add_software_orders])
                soft_counter += 1
            if len(serv) > serv_counter:
                lis.append([serv[serv_counter], self.add_service_orders])
                serv_counter += 1
            lis = self.sort_list(lis)
            for i in lis:
                i[1](context, i[0])
            if len(inv) <= inv_counter and len(soft) <= soft_counter and len(serv) <= serv_counter:
                break

    def sort_list(self, lis):
        def swap_positions(pos1, pos2):
            lis[pos1], lis[pos2] = lis[pos2], lis[pos1]
        for i in range(len(lis)):
            nex = i + 1
            if len(lis) > nex:
                if lis[nex][0].date_of_order > lis[i][0].date_of_order:
                    swap_positions(nex, i)
            else:
                return lis
        return lis

    def return_inventory_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.inv
            entory_orders.objects.filter(
                Q(manager_id__brands_product=self.brn) & Q(is_complete=True)).order_by('-id')
        return m.inventory_orders.objects.filter(Q(manager_id__brands_product=self.brn) & Q(is_complete=True)).order_by('-id')[0:4]

    def return_software_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.software_orders.objects.filter(Q(manager_id__brands_product=self.brn) & Q(is_complete=True)).order_by('-id')
        return m.software_orders.objects.filter(Q(manager_id__brands_product=self.brn) & Q(is_complete=True)).order_by('-id')[0:4]

    def return_service_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.service_order.objects.filter(Q(request_id__service_id__brands_product=self.brn) & Q(is_complete=True)).order_by('-id')
        return m.service_order.objects.filter(Q(request_id__service_id__brands_product=self.brn) & Q(is_complete=True)).order_by('-id')[0:4]

    def add_inventory_orders(self, context, obj):
        context['component'].append(c.OrdersCardWithOutButtons(obj.manager_id.name, "inventory",
                                    f' unit Price {obj.manager_id.selling_price}', f" amount bought {obj.amount_buy} ", f"total bill {obj.commited_amount}PKR", ""))

    def add_software_orders(self, context, obj):
        context['component'].append(c.OrdersCardWithOutButtons(
            obj.manager_id.name, "software",
            f' unit Price {obj.manager_id.selling_price}',
            f" url: {obj.url} ",
            f"total bill {obj.commited_amount}PKR", ""))

    def add_service_orders(self, context, obj):
        context['component'].append(c.OrdersCardWithOutButtons(obj.request_id.service_id.name, "service",
                                    f' unit Price {obj.request_id.service_id.package_price}', f"see Details: <a class = 'btn btn-primary' href='/service/order/detail/cust/{obj.pk}'>detail</a>", f"total bill {obj.commited_amount}PKR", ""))


class BrandsCartCompleteView(TemplateView):
    template_name = componentListView

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['component'] = []
            context['name'] = f"{self.request.user.username}'s Completed Orders"
        for obj in m.brand.objects.filter(owner=self.request.user.customer):
            self.add_brand(obj, context)
        return context

    def add_brand(self, obj, context):
        soft_num = m.software_orders.objects.filter(
            Q(manager_id__brands_product=obj) & Q(is_complete=True)).count()
        inv_num = m.inventory_orders.objects.filter(
            Q(manager_id__brands_product=obj) & Q(is_complete=True)).count()
        serv = m.service_order.objects.filter(
            Q(request_id__service_id__brands_product=obj) & Q(is_complete=True)).count()
        context['component'].append(c.OrdersCardWithOutButtons(
            obj.name, "orders detail", f' inevntory orders {inv_num}', f" software orders {soft_num} ", f"services request {serv}", f"see Details: <a class = 'btn btn-primary' href='/brand/cart/complete/detail/{obj.pk}'>detail</a>"))

# BrandsCompletCartDetailView


class BrandsCartDetailView(DetailView):
    template_name = componentListView
    model = m.brand

    def get_context_data(self, **kwargs):
        self.name = "but"
        self.full_view = "full"
        self.less_view = "less"
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            self.brn = context['object']
            context['component'] = []
            context['name'] = f"{self.request.user.username}'s Orders"
            val = self.request.GET.get(self.name)
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    "Completed Orders History", "show less", self.name, self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    "Completed Orders History", "show all", self.name, self.full_view))

            inv = self.return_inventory_object_list()
            serv = self.return_service_object_list()
            self.add_all_orders(context, inv, serv)
            # self.add_inventory_orders(context)
            # self.add_software_orders(context)
            # self.add_service_orders(context)
        return context

    def add_all_orders(self, context, inv, serv):
        inv_counter = 0

        serv_counter = 0
        lis = []
        while True:
            lis.clear()
            if len(inv) > inv_counter:
                lis.append([inv[inv_counter], self.add_inventory_orders])
                inv_counter += 1

            if len(serv) > serv_counter:
                lis.append([serv[serv_counter], self.add_service_orders])
                serv_counter += 1
            lis = self.sort_list(lis)
            for i in lis:
                i[1](context, i[0])
            if len(inv) <= inv_counter and len(serv) <= serv_counter:
                break

    def sort_list(self, lis):
        def swap_positions(pos1, pos2):
            lis[pos1], lis[pos2] = lis[pos2], lis[pos1]
        for i in range(len(lis)):
            nex = i + 1
            if len(lis) > nex:
                if lis[nex][0].date_of_order > lis[i][0].date_of_order:
                    swap_positions(nex, i)
            else:
                return lis
        return lis

    def return_inventory_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.inventory_orders.objects.filter(Q(manager_id__brands_product=self.brn) & Q(is_commited_by_owner=False)).order_by('-id')
        return m.inventory_orders.objects.filter(Q(manager_id__brands_product=self.brn) & Q(is_commited_by_owner=False)).order_by('-id')[0:4]

    def return_service_object_list(self):
        val = self.request.GET.get(self.name)
        if val == self.full_view:
            return m.service_order.objects.filter(Q(request_id__service_id__brands_product=self.brn) & Q(is_commited_by_owner=False)).order_by('-id')
        return m.service_order.objects.filter(Q(request_id__service_id__brands_product=self.brn) & Q(is_commited_by_owner=False)).order_by('-id')[0:4]

    def add_inventory_orders(self, context, obj):
        if obj.manager_id.brands_product.brand_sector.commit_allowed == False:
            context['component'].append(c.OrdersCardWithTwoButtons(obj.manager_id.name, "inventory", f' unit Price {obj.manager_id.selling_price}', f" amount bought {obj.amount_buy} ",
                                        f"total bill {obj.commited_amount}PKR", f"/owner/order/inventory/delete/{obj.pk}", "delete", f"/owner/order/inventory/simple/commit/{obj.pk}", "commit"))
        else:
            context['component'].append(c.OrdersCardWithTwoButtons(obj.manager_id.name, "inventory", f' unit Price {obj.manager_id.selling_price}', f" amount bought {obj.amount_buy} ",
                                        f"total bill {obj.commited_amount}PKR", f"/owner/order/inventory/delete/{obj.pk}", "delete", f"/owner/order/inventory/commit/{obj.pk}", "commit"))

    def add_service_orders(self, context, obj):
        if obj.request_id.service_id.brands_product.brand_sector.commit_allowed == False:
            context['component'].append(c.OrdersCardWithTwoButtons(obj.request_id.service_id.name, "service", f' unit Price {obj.request_id.service_id.package_price}', f"see Details: <a class = 'btn btn-primary' href='/service/order/detail/cust/{obj.pk}'>detail</a>",
                                        f"total bill {obj.commited_amount}PKR", f"/owner/order/service/delete/{obj.pk}", "delete", f"/owner/order/service/simple/commit/{obj.pk}", "commit"))
        else:
            context['component'].append(c.OrdersCardWithTwoButtons(obj.request_id.service_id.name, "service", f' unit Price {obj.request_id.service_id.package_price}',
                                        f"see Details: <a class = 'btn btn-primary' href='/service/order/detail/cust/{obj.pk}'>detail</a>", f"total bill {obj.commited_amount}PKR", f"/owner/order/service/delete/{obj.pk}", "delete", f"/owner/order/service/commit/{obj.pk}", "commit"))


class BrandsCartOrderView(TemplateView):
    template_name = componentListView

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['component'] = []
            context['name'] = f"{self.request.user.username}'s business's Orders"
        for obj in m.brand.objects.filter(owner=self.request.user.customer):
            self.add_brand(obj, context)
        return context

    def add_brand(self, obj, context):
        inv_num = m.inventory_orders.objects.filter(
            Q(manager_id__brands_product=obj) & Q(is_commited_by_owner=False)).count()
        serv = m.service_order.objects.filter(
            Q(request_id__service_id__brands_product=obj) & Q(is_commited_by_owner=False)).count()
        context['component'].append(c.OrdersCardWithOutButtons(
            obj.name, "orders detail", f' inventory orders {inv_num}', f"services request {serv}", "", f"see Details: <a class = 'btn btn-primary' href='/brand/cart/detail/{obj.pk}'>detail</a>"))


class BrandUpdateView(UpdateView):
    template_name = componentFormView
    model = m.brand
    fields = ["name", "bannar", "description",
              "logo", "location", "long_description"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = " Update Brand "
        return context


class InventoryManagerUpdateView(UpdateView):
    template_name = componentFormView
    model = m.inventory_managment
    fields = ["name", "pic", "description",
              "long_description", "amount", "selling_price"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = " Update Inventory Product "
        return context


class SofwareManagerUpdateView(UpdateView):
    template_name = componentFormView
    model = m.software_manager
    fields = ["name", "pic", "description",
              "long_description", "product_url", "selling_price"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = " Update Software Product "
        return context


class ServiceManagerUpdateView(UpdateView):
    template_name = componentFormView
    model = m.services_manager
    fields = ["name", "pic", "description",
              "long_description", "package_price"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = " Update Product "
        return context


class InventoryManagerCreateForm(ModelForm):
    class Meta:
        model = m.inventory_managment
        fields = ["name", "pic", "description",
                  "long_description", "amount", "selling_price"]


class SoftwareManagerCreateForm(ModelForm):
    class Meta:
        model = m.software_manager
        fields = ["name", "pic", "description",
                  "long_description", "product_url", "selling_price"]


class ServiceManagerCreateForm(ModelForm):
    class Meta:
        model = m.services_manager
        fields = ["name", "pic", "description",
                  "long_description", "package_price"]


class BrandCreateForm(ModelForm):
    class Meta:
        model = m.brand
        fields = ["name", "bannar", "description",
                  "logo", "location", "long_description"]


class ComposeMessageForm(Form):
    to = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=100)
    msg = forms.CharField(widget=forms.Textarea)


class CheckOutForm(Form):
    phone_number = forms.IntegerField()
    username = forms.CharField(max_length=200)
    password = forms.PasswordInput()
    email = forms.EmailField()


class OneTimePassword(Form):
    otp = forms.IntegerField()


def check_out_form(request, amount, bill):
    if request.method == "POST":
        # print(request.POST.get("to"))
        form = CheckOutForm(data=request.POST)
        if form.is_valid():
            value = form.clean()
            eas.generate_otp(value['phone_number'],
                             value['username'], value['password'])
            form = OneTimePassword(data=request.POST)
            return HttpResponseRedirect(f"/otp/{amount}/{bill}/{value['phone_number']}/{value['username']}/{value['email']}/{value['password']}/")
        return render(request, componentFormView, {'form': form, "name": "Enter EasyPaisa Credantials"})
    return render(request, componentFormView, {'form': CheckOutForm(), "name": "Enter EasyPaisa Credantials"})


def one_time_password_form(request, amount, bill, phone_number, username, email, password):
    form = OneTimePassword(data=request.POST)
    if form.is_valid():
        value = form.clean()
        chec = m.check_out(cust=request.user.customer, username=username,
                           amount_pay=amount, total_bill=bill, mssid=phone_number, email=email)
        resp = eas.pinless_connection(
            chec.pk, amount, phone_number, email, value['otp'], username, password)
        if resp['responce']['responseCode'] == "0000":
            rest = eas.pinless_transfer(
                chec.pk, amount, phone_number, email, resp["tokenNumber"], username, password)
            chec.save()
            commit_check_out_orders(
                request, request.user.customer.customers_account, chec)
            return render(request, componentDetailView, {"component": c.Check_Out_Transfer(rest['responce'], "/market_page/")})
        else:
            form.add_error(
                "otp", f" invalid one time password resending new one at mobile No {phone_number} ")
            eas.generate_otp(phone_number, username, password)
        return render(request, componentFormView, {'form': form, "name": "Enter One Time Password"})
    return render(request, componentFormView, {'form': OneTimePassword(), "name": "Enter One Time Password"})


def commit_check_out_orders(request, finantial_account, check_out_obj):
    def return_inventory_object_list():
        return m.inventory_orders.objects.filter(Q(buyers_id=request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=False)).order_by('-id')

    def return_software_object_list():
        return m.software_orders.objects.filter(Q(buyers_id=request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=False)).order_by('-id')

    def return_service_object_list():
        return m.service_order.objects.filter(Q(request_id__customer_id=request.user.customer) & Q(is_active=False) & Q(is_commited_by_customer=False)).order_by('-id')
    inv = return_inventory_object_list()
    soft = return_software_object_list()
    serv = return_service_object_list()
    for i in inv:
        if check_out_obj:
            i.check_out = check_out_obj
        partial_user_commit(i, finantial_account)
    for j in soft:
        if check_out_obj:
            j.check_out = check_out_obj
        full_commit(j, j.manager_id, finantial_account,
                    j.manager_id.brands_product.owner.customers_account)
    for k in serv:
        if check_out_obj:
            k.check_out = check_out_obj
        partial_user_commit(k, finantial_account)


class ServiceRequestForm(ModelForm):
    class Meta:
        model = m.services_form
        fields = ["problem_title", "background", "demands", "first_link_of_inspiration",
                  "second_link_of_inspiration", "third_link_of_inspiration", "completion_date"]


class InventoryCommentsCreateForm(ModelForm):
    class Meta:
        model = m.comment_on_inventory_order
        fields = ['rating', "comment"]


class SoftwareCommentsCreateForm(ModelForm):
    class Meta:
        model = m.comment_on_software_order
        fields = ['rating', "comment"]


class ServiceCommentsCreateForm(ModelForm):
    class Meta:
        model = m.comment_on_service
        fields = ['rating', "comment"]


def create_inventory_comments(request, pk):
    inv = m.inventory_orders.objects.get(pk=pk)
    if request.method == 'POST':
        form = InventoryCommentsCreateForm(request.POST)
        if form.is_valid():
            request_form = form.instance
            inv.is_reviewed = True
            inv.save()
            request_form.order = inv
            request_form.save()
            return redirect(f'/customers/cart/complete')
        else:
            return render(request, componentFormView, {'form': form, "name": f"Comment On {inv.manager_id.name} "})
    return render(request, componentFormView, {'form': InventoryCommentsCreateForm, "name": f"Comment On {inv.manager_id.name} "})


def create_software_comments(request, pk):
    inv = m.software_orders.objects.get(pk=pk)
    if request.method == 'POST':
        form = SoftwareCommentsCreateForm(request.POST)
        if form.is_valid():
            request_form = form.instance
            inv.is_reviewed = True
            inv.save()
            request_form.order = inv
            request_form.save()
            return redirect(f'/customers/cart/complete')
        else:
            return render(request, componentFormView, {'form': form, "name": f"Comment On {inv.manager_id.name} "})
    return render(request, componentFormView, {'form': SoftwareCommentsCreateForm, "name": f"Comment On {inv.manager_id.name} "})


def create_services_comments(request, pk):
    inv = m.service_order.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServiceCommentsCreateForm(request.POST)
        if form.is_valid():
            inv.is_reviewed = True
            inv.save()
            request_form = form.instance
            request_form.order = inv
            request_form.save()

            return redirect(f'/customers/cart/complete')
        else:
            return render(request, componentFormView, {'form': form, "name": f"Comment On {inv.request_id.service_id.name} "})
    return render(request, componentFormView, {'form': ServiceCommentsCreateForm, "name": f"Comment On {inv.request_id.service_id.name} "})


class InventoryReportCreateForm(ModelForm):
    class Meta:
        model = m.report_on_inventory
        fields = ['title', "report"]


class SoftwareReportCreateForm(ModelForm):
    class Meta:
        model = m.report_on_software
        fields = ['title', "report"]


class ServiceReportCreateForm(ModelForm):
    class Meta:
        model = m.report_on_service
        fields = ['title', "report"]


def create_inventory_report(request, pk):
    inv = m.inventory_orders.objects.get(pk=pk)
    if request.method == 'POST':
        form = InventoryReportCreateForm(request.POST)
        if form.is_valid():
            request_form = form.instance
            request_form.order = inv
            inv.is_reviewed = True
            inv.save()
            request_form.save()
            return redirect(f'/customers/cart/complete')
        else:
            return render(request, componentFormView, {'form': form, "name": f"Report On {inv.manager_id.name} "})
    return render(request, componentFormView, {'form': InventoryReportCreateForm, "name": f"Report On {inv.manager_id.name} "})


def create_software_report(request, pk):
    inv = m.software_orders.objects.get(pk=pk)
    if request.method == 'POST':
        form = SoftwareReportCreateForm(request.POST)
        if form.is_valid():
            request_form = form.instance
            request_form.order = inv
            inv.is_reviewed = True
            inv.save()
            request_form.save()
            return redirect(f'/customers/cart/complete')
        else:
            return render(request, componentFormView, {'form': form, "name": f"Report On {inv.manager_id.name} "})
    return render(request, componentFormView, {'form': SoftwareReportCreateForm, "name": f"Report On {inv.manager_id.name} "})


def create_services_report(request, pk):
    inv = m.service_order.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServiceReportCreateForm(request.POST)
        if form.is_valid():
            request_form = form.instance
            request_form.order = inv
            inv.is_reviewed = True
            inv.save()
            request_form.save()
            return redirect(f'/customers/cart/complete')
        else:
            return render(request, componentFormView, {'form': form, "name": f"Report On {inv.request_id.service_id.name} "})
    return render(request, componentFormView, {'form': ServiceReportCreateForm, "name": f"Report On {inv.request_id.service_id.name} "})


def create_request_on_service(request, service_pk):
    service = m.services_manager.objects.get(pk=service_pk)
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            request_form = form.save()
            request_on_service_obj = m.request_on_sevice(
                form=request_form, customer_id=request.user.customer, service_id=service)
            request_on_service_obj.save()
            m.service_order.objects.create(
                request_id=request_on_service_obj, commited_amount=service.package_price)
            return redirect(f'/services/list/detail/{service_pk}')
        else:
            return render(request, componentFormView, {'form': form, "name": f"Request On {service.name} Service"})
    return render(request, componentFormView, {'form': ServiceRequestForm(), "name": f"Request On {service.name} Service"})


def compose_message(request):
    if request.method == "POST":
        # print(request.POST.get("to"))
        form = ComposeMessageForm(data=request.POST)
        if form.is_valid():
            value = form.clean()
            rec = m.customer.objects.filter(user__username=value['to'])
            if rec:
                m.message.objects.create(
                    sender=request.user.customer, reciver=rec[0], subject=value['subject'], msg=value['msg'])
                return HttpResponseRedirect("/send/message/")
            else:
                form.add_error("to", " invalid handle ")
                return render(request, componentFormView, {'form': form, "name": "Compose Message"})
    return render(request, componentFormView, {'form': ComposeMessageForm(), "name": "Compose Message"})


def create_inventory_product(request, brand_pk):
    brand = m.brand.objects.get(pk=brand_pk)
    if request.method == 'POST':
        form = InventoryManagerCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.instance
            obj.brands_product = brand
            obj.save()
            return redirect(f'/brands/detail/{brand_pk}')
        else:
            return render(request, componentFormView, {'form': form, "name": f"create inventory product In {brand.name}"})
    return render(request, componentFormView, {'form': InventoryManagerCreateForm(), "name": f"create inventory product In {brand.name}"})


def create_software_product(request, brand_pk):
    brand = m.brand.objects.get(pk=brand_pk)
    if request.method == 'POST':
        form = SoftwareManagerCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.instance
            obj.brands_product = brand
            obj.save()
            return redirect(f'/brands/detail/{brand_pk}')
        else:
            return render(request, componentFormView, {'form': form, "name": f"create software product In {brand.name}"})
    return render(request, componentFormView, {'form': SoftwareManagerCreateForm(), "name": f"create software product In {brand.name}"})


def create_services(request, brand_pk):
    brand = m.brand.objects.get(pk=brand_pk)
    if request.method == 'POST':
        form = ServiceManagerCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.instance
            obj.brands_product = brand
            obj.save()
            return redirect(f'/brands/detail/{brand_pk}')
        else:
            return render(request, componentFormView, {'form': form, "name": f"Create Services In {brand.name}"})
    return render(request, componentFormView, {'form': ServiceManagerCreateForm(), "name": f"Create Services In {brand.name}"})


def create_brand(request, sector_pk):
    sector = m.sector.objects.get(pk=sector_pk)
    if request.method == 'POST':
        form = BrandCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.instance
            obj.brand_sector = sector
            obj.owner = request.user.customer
            obj.save()
            return redirect('/market_page/')
        else:
            return render(request, componentFormView, {'form': form, "name": f"Register Brand In {sector.name}"})

    return render(request, componentFormView, {'form': BrandCreateForm(), "name": f"Register Brand In {sector.name}"})


def admin_commit(order, manager, finantial_account, owner_finantial_account):
    if (order.is_complete == False) and order.is_commited_by_customer and order.is_commited_by_owner and ((manager.brands_product.brand_sector.commit_allowed == False) or order.is_commited_by_admin):
        finantial_account.commited_balance = finantial_account.commited_balance - \
            order.commited_amount
        admin_amount = int(
            order.commited_amount*(order.manager_id.brands_product.brand_sector.profit_on_brand/100))
        owner_amount = order.commited_amount - admin_amount
        owner_finantial_account.balance = owner_finantial_account.balance + owner_amount


def admin_auto_commit(order, manager, finantial_account, owner_finantial_account):
    "return answer whether an order is complete or not "
    if manager.brands_product.brand_sector.commit_allowed == False:
        if order.is_commited_by_admin == True and order.is_complete == False:
            full_commit(order, manager, finantial_account,
                        owner_finantial_account)
    return True


def admin_auto_rollback(report, order, manager, finantial_account, owner_finantial_account):
    "return answer whether an order is complete or not "
    if report:
        if report.is_accepted == True and order.is_reported == False:
            full_rollback(order, manager, finantial_account,
                          owner_finantial_account)
            return True
        elif report.is_accepted == True:
            return True
    return False


def full_commit(order, manager, finantial_account, owner_finantial_account):
    finantial_account.commited_balance = finantial_account.commited_balance - \
        order.commited_amount
    admin_amount = int(order.commited_amount *
                       (manager.brands_product.brand_sector.profit_on_brand/100))
    owner_amount = order.commited_amount - admin_amount
    owner_finantial_account.balance = owner_finantial_account.balance + owner_amount
    manager.total_rating = manager.total_rating + order.commited_amount
    manager.brands_product.total_rating = manager.brands_product.total_rating + \
        order.commited_amount
    manager.brands_product.brand_sector.total_rating = manager.brands_product.brand_sector.total_rating + \
        order.commited_amount
    order.is_complete = True
    order.is_active = True
    order.is_commited_by_customer = True
    order.is_commited_by_owner = True
    order.is_commited_by_admin = True
    order.is_finantial_transaction = True
    order.is_reported = False
    order.is_reviewed = False
    order.save()
    manager.save()
    manager.brands_product.save()
    manager.brands_product.brand_sector.save()
    finantial_account.save()
    owner_finantial_account.save()


def full_rollback(order, manager, finantial_account, owner_finantial_account):
    if order.is_complete == True and order.is_reported == False:
        finantial_account.balance = finantial_account.balance + order.commited_amount
        admin_amount = int(
            order.commited_amount*(manager.brands_product.brand_sector.profit_on_brand/100))
        owner_amount = order.commited_amount - admin_amount
        owner_finantial_account.balance = owner_finantial_account.balance - owner_amount
        manager.total_rating = manager.total_rating - order.commited_amount
        manager.brands_product.total_rating = manager.brands_product.total_rating - \
            order.commited_amount
        manager.brands_product.brand_sector.total_rating = manager.brands_product.brand_sector.total_rating - \
            order.commited_amount
        order.is_complete = True
        order.is_active = True
        order.is_commited_by_customer = True
        order.is_commited_by_owner = True
        order.is_commited_by_admin = True
        order.is_finantial_transaction = True
        order.is_reviewed = True
        order.is_reported = True
        order.save()
        manager.save()
        manager.brands_product.save()
        manager.brands_product.brand_sector.save()
        finantial_account.save()
        owner_finantial_account.save()


def partial_roll_back(order, finantial_account):
    if order.is_active == True and order.is_commited_by_owner == False:
        finantial_account.balance = finantial_account.balance + order.commited_amount
        finantial_account.commited_balance = finantial_account.commited_balance - \
            order.commited_amount
        order.is_active = False
        order.is_commited_by_customer = True
        order.save()
        finantial_account.save()


def partial_user_commit(order, finantial_account):
    finantial_account.balance = finantial_account.balance - order.commited_amount
    finantial_account.commited_balance = finantial_account.commited_balance + \
        order.commited_amount
    order.is_active = True
    order.is_commited_by_customer = True
    order.is_finantial_transaction = True
    order.save()
    finantial_account.save()


def partial_owner_commit(order):
    order.is_commited_by_owner = True
    order.save()


def inventory_user_commit(request, pk):
    obj = m.inventory_orders.objects.get(pk=pk)
    finantial_account = request.user.customer.customers_account
    if finantial_account.balance >= obj.commited_amount:
        partial_user_commit(obj, finantial_account)
        return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.manager_id.name, f" Your Order Has Been Commited Current Balance: {finantial_account.balance} Commited Balance: {finantial_account.commited_balance} ", "/customers/cart/", "Back to Cart")]})
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.manager_id.name, f" You donot have sufficient balance to Order this Product: {finantial_account.balance} Balance Needed: {obj.commited_amount - finantial_account.balance} ", "/customers/cart/", "Back to Cart")]})


def software_user_commit(request, pk):
    obj = m.software_orders.objects.get(pk=pk)
    obj.manager_id.total_rating = obj.manager_id.total_rating + obj.commited_amount
    finantial_account = request.user.customer.customers_account
    owner_finantial_account = obj.manager_id.brands_product.owner.customers_account
    if finantial_account.balance >= obj.commited_amount and obj.manager_id.brands_product.brand_sector.commit_allowed == False:
        full_commit(obj, obj.manager_id, finantial_account,
                    owner_finantial_account)
        return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.manager_id.name, f" Your Order Has Been Commited Current Balance: {finantial_account.balance} Commited Balance: {finantial_account.commited_balance} ", "/customers/cart/", "Back to Cart")]})
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.manager_id.name, f" You donot have sufficient balance to Order this Product: {finantial_account.balance} Balance Needed: {obj.commited_amount - finantial_account.balance} ", "/customers/cart/", "Back to Cart")]})


def service_user_commit(request, pk):
    obj = m.service_order.objects.get(pk=pk)
    finantial_account = request.user.customer.customers_account
    if finantial_account.balance >= obj.commited_amount:
        finantial_account.balance = finantial_account.balance - obj.commited_amount
        finantial_account.commited_balance = finantial_account.commited_balance + \
            obj.commited_amount
        partial_user_commit(obj, finantial_account)
        return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.request_id.service_id.name, f" Your Order Has Been Commited Current Balance: {finantial_account.balance} Commited Balance: {finantial_account.commited_balance} ", "/customers/cart/", "Back to Cart")]})
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.request_id.service_id.name, f" You donot have sufficient balance to Order this Product: {finantial_account.balance} Balance Needed: {obj.commited_amount - finantial_account.balance} ", "/customers/cart/", "Back to Cart")]})


def inventory_owner_commit(request, pk):
    obj = m.inventory_orders.objects.get(pk=pk)
    full_commit(obj, obj.manager_id, obj.buyers_id.customers_account,
                obj.manager_id.brands_product.owner.customers_account)
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.manager_id.name, f" Your Order Has Been Commited  payment shall be transfer after soon ", "/brands/cart/", "Back to Cart")]})


def inventory_owner_simple_commit(request, pk):
    obj = m.inventory_orders.objects.get(pk=pk)
    partial_owner_commit(obj)
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.manager_id.name, f" Your Order Has Been Commited  payment shall be transfer after soon ", "/brands/cart/", "Back to Cart")]})
# def software_owner_commit(request,pk):
#     obj = m.software_orders.objects.get(pk = pk)
#     obj.is_commited_by_owner = True
#     obj.save()


def service_owner_commit(request, pk):
    obj = m.service_order.objects.get(pk=pk)
    full_commit(obj, obj.request_id.service_id, obj.request_id.customer_id,
                obj.request_id.service_id.brands_product.owner.customers_account)
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.request_id.service_id.name, f" Your Order Has Been Commited payment shall be transfer after soon ", "/brands/cart/", "Back to Cart")]})


def service_owner_simple_commit(request, pk):
    obj = m.service_order.objects.get(pk=pk)
    partial_owner_commit(obj)
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.request_id.service_id.name, f" Your Order Has Been Commited payment shall be transfer after soon ", "/brands/cart/", "Back to Cart")]})


def inventory_order_rollback(request, pk):
    obj = m.inventory_orders.objects.get(pk=pk)
    full_rollback(obj, obj.manager_id, obj.buyers_id.customers_account,
                  obj.manager_id.brands_product.owner.customers_account)


def software_order_rollback(request, pk):
    obj = m.inventory_orders.objects.get(pk=pk)
    full_rollback(obj, obj.manager_id, obj.buyers_id.customers_account,
                  obj.manager_id.brands_product.owner.customers_account)


def service_order_rollback(request, pk):
    obj = m.service_order.objects.get(pk=pk)
    full_rollback(obj, obj.request_id.service_id, obj.request_id.customer_id,
                  obj.request_id.service_id.brands_product.owner.customers_account)


def inventory_cart_delete(request, pk):
    obj = m.inventory_orders.objects.get(pk=pk)
    obj.is_active = True
    obj.is_commited_by_customer = False
    obj.save()
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.manager_id.name, f" Your Order Has Been Canceled ", "/customers/cart/", "Back to Cart")]})


def software_cart_delete(request, pk):
    obj = m.software_orders.objects.get(pk=pk)
    obj.is_active = True
    obj.is_commited_by_customer = False
    obj.save()
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.manager_id.name, f" Your Order Has Been Canceled ", "/customers/cart/", "Back to Cart")]})


def services_cart_delete(request, pk):
    obj = m.service_order.objects.get(pk=pk)
    obj.is_active = True
    obj.is_commited_by_customer = False
    obj.save()
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.request_id.service_id.name, f" Your Order Has Been Canceled ", "/customers/cart/", "Back to Cart")]})


def inventory_order_delete(request, pk):
    obj = m.inventory_orders.objects.get(pk=pk)
    partial_roll_back(obj, obj.buyers_id.customers_account)
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.manager_id.name, f" Your Order Has Been Canceled ", "/brands/cart/", "Back to Cart")]})


def services_order_delete(request, pk):
    obj = m.service_order.objects.get(pk=pk)
    partial_roll_back(obj, obj.request_id.customer_id.customers_account)
    return render(request, componentDetailView, {"component": [c.HeaderAndFooterCard(obj.request_id.service_id.name, f" Your Order Has Been Canceled ", "/brands/cart/", "Back to Cart")]})


class MLView(TemplateView):
    template_name = componentDetailView

    def get_context_data(self, **kwargs):
        self.name = "but"
        self.full_view = "full"
        self.less_view = "less"
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            if self.request.GET.get("amounts") != "Select Max Distance" and self.request.GET.get("amounts") != None:
                print(" running algo ")
                b(int(self.request.GET.get("amounts")))
            context['component'] = []
            context['name'] = f"Make Relations"
            context['component'].append(c.MlMaxDistance(100))
            self.add_inventory_relations(context)
            self.add_software_relations(context)
            self.add_service_relations(context)
        return context

    def return_inventory_object_list(self, val):
        if val == self.full_view:
            return m.inventory_relations.objects.all().order_by('-id')
        return m.inventory_relations.objects.all().order_by('-id')[0:4]

    def return_software_object_list(self, val):
        if val == self.full_view:
            return m.software_relations.objects.all().order_by('-id')
        return m.software_relations.objects.all().order_by('-id')[0:4]

    def return_service_object_list(self, val):
        if val == self.full_view:
            return m.service_relations.objects.all().order_by('-id')
        return m.service_relations.objects.all().order_by('-id')[0:4]

    def add_inventory_relations(self, context):
        val = self.request.GET.get(self.name+"inv")
        lis = self.return_inventory_object_list(val)
        if lis:
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    f"Inventory Relations ", "show less", self.name+"inv", self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    f"Inventory Relations ", "show all", self.name+"inv", self.full_view))
            context['component'].append(c.MLTables("inventory", lis))

    def add_software_relations(self, context):
        val = self.request.GET.get(self.name+"soft")
        lis = self.return_software_object_list(val)
        if lis:
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    f"Software Relations ", "show less", self.name+"soft", self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    f"Software Relations ", "show all", self.name+"soft", self.full_view))
            context['component'].append(c.MLTables("Software", lis))

    def add_service_relations(self, context):
        val = self.request.GET.get(self.name+"ser")
        lis = self.return_service_object_list(val)
        if lis:
            if val == self.full_view:
                context['component'].append(c.ShowAllOrders(
                    f"Service Relations ", "show less", self.name+"ser", self.less_view))
            else:
                context['component'].append(c.ShowAllOrders(
                    f"Service Relations ", "show all", self.name+"ser", self.full_view))
            context['component'].append(c.MLTables("service", lis))


# def generate_inventory_rating(inv,fina_lis):
#     su = m.inventory_finantial_complete.objects()
#     for inv_m in m.inventory_managment.objects.all():
#         ""
