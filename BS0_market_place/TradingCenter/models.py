from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class finantial_account(models.Model):
    balance = models.IntegerField(default = 0)
    commited_balance = models.IntegerField(default = 0)
    def __str__(self):
        return str(self.pk)

class customer(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)
    customers_account = models.OneToOneField(to=finantial_account,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)


class message(models.Model):
    sender = models.ForeignKey(to=customer,on_delete=models.CASCADE,related_name="sender")
    reciver = models.ForeignKey(to=customer,on_delete=models.CASCADE,related_name="reciver")
    revived = models.BooleanField(default=False)
    msg = models.TextField()
    subject = models.CharField(max_length=100,null=True)
    def __str__(self):
        return " sender "+str(self.sender)+" reciver "+str(self.reciver)

class sector(models.Model):
    name = models.CharField(max_length = 35,unique = True)
    location = models.TextField()
    description = models.TextField()
    profit_on_brand = models.FloatField()
    type_of_manager_allowed = models.CharField(max_length=20, default="all", choices=(("all","all"), ("inventory","inventory"),("software","software"),("service","service")))
    total_rating = models.IntegerField(default=0)
    commit_allowed = models.BooleanField(default=True)
    def __str__(self):
        return str(self.name)

class brand(models.Model):
    name = models.CharField(max_length = 35,unique = True)
    owner = models.ForeignKey(to=customer,on_delete=models.CASCADE)
    brand_sector = models.ForeignKey(to=sector,on_delete=models.CASCADE)
    location = models.TextField()
    description = models.TextField()
    long_description = models.TextField(null=True)
    bannar = models.ImageField(upload_to="image")
    total_rating = models.IntegerField(default=0)
    logo = models.ImageField(upload_to="image")
    is_active = models.BooleanField(default = True)
    def __str__(self):
        return str(self.name)

class check_out(models.Model):
    cust = models.ForeignKey(to=customer,on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now=True)
    amount_pay = models.IntegerField()
    total_bill = models.IntegerField()
    mssid = models.IntegerField()
    email = models.EmailField()


class inventory_managment(models.Model):
    description = models.TextField()
    long_description = models.TextField(null=True)
    pic = models.ImageField(upload_to="image")
    name = models.CharField(max_length = 30)
    amount = models.IntegerField()
    selling_price = models.IntegerField()
    brands_product = models.ForeignKey(to=brand,on_delete=models.CASCADE)
    total_rating = models.IntegerField(default=0)
    seconds_spends_on_product = models.IntegerField(default=0)
    is_active = models.BooleanField(default = True)
    def __str__(self):
        return "brand "+str(self.brands_product)+" inv product "+str(self.name)

class inventory_relations(models.Model):
    first = models.ForeignKey(to=inventory_managment,on_delete=models.CASCADE,related_name="first")
    second = models.ForeignKey(to=inventory_managment,on_delete=models.CASCADE,related_name="second")

class inventory_items_featurers(models.Model):
    manager_id = models.ForeignKey(to=inventory_managment,on_delete=models.CASCADE)    
    description = models.CharField(max_length=100)
    ref_url =  models.URLField(null=True)

class inventory_orders(models.Model):
    date_of_order = models.DateTimeField(auto_now=True)
    manager_id = models.ForeignKey(to=inventory_managment,on_delete=models.CASCADE)
    buyers_id = models.ForeignKey(to=customer,on_delete=models.CASCADE)
    check_out = models.ForeignKey(to=check_out,on_delete=models.CASCADE,null=True)
    commited_amount = models.IntegerField()
    amount_buy = models.IntegerField()
    is_complete = models.BooleanField(default=False)
    is_commited_by_customer = models.BooleanField(default = False)
    is_commited_by_owner = models.BooleanField(default= False)
    is_commited_by_admin = models.BooleanField(default= False)
    is_active = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    is_finantial_transaction = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    def __str__(self):
        return " buyer "+str(self.buyers_id)+" inv-order "+str(self.manager_id)




class comment_on_inventory_order(models.Model):
    order = models.OneToOneField(to=inventory_orders,on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((5,5), (4,4),(3,3),(2,2),(1,1),(0,0)))
    comment = models.TextField()
    def __str__(self):
        return " inv rating "+str(self.rating)+" on inv product "+str(self.order)

class report_on_inventory(models.Model):
    order = models.OneToOneField(to=inventory_orders,on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    report = models.TextField()
    is_accepted = models.BooleanField(default=False)
    def __str__(self):
        return " inv report "+str(self.title)+" on inv product "+str(self.order)


class software_manager(models.Model):
    description = models.TextField()
    long_description = models.TextField(null=True)
    pic = models.ImageField(upload_to="image")
    name = models.CharField(max_length = 30)
    selling_price = models.IntegerField()
    brands_product = models.ForeignKey(to=brand,on_delete=models.CASCADE)
    product_url = models.URLField()
    total_rating = models.IntegerField(default=0)
    seconds_spends_on_product = models.IntegerField(default=0)
    is_active = models.BooleanField(default = True)
    def __str__(self):
        return "brand "+str(self.brands_product)+" soft product "+str(self.name)

class software_relations(models.Model):
    first = models.ForeignKey(to=software_manager,on_delete=models.CASCADE,related_name="first")
    second = models.ForeignKey(to=software_manager,on_delete=models.CASCADE,related_name="second")

class software_orders(models.Model):
    date_of_order = models.DateTimeField(auto_now=True)
    manager_id = models.ForeignKey(to=software_manager,on_delete=models.CASCADE)
    buyers_id = models.ForeignKey(to=customer,on_delete=models.CASCADE)
    commited_amount = models.IntegerField()
    check_out = models.ForeignKey(to=check_out,on_delete=models.CASCADE,null=True)
    url = models.URLField()
    is_complete = models.BooleanField(default=False)
    is_commited_by_customer = models.BooleanField(default = False)
    is_commited_by_owner = models.BooleanField(default= False)
    is_commited_by_admin = models.BooleanField(default= False)
    is_active = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    is_finantial_transaction = models.BooleanField(default=False)
    def __str__(self):
        return " buyer "+str(self.buyers_id)+" soft-order "+str(self.manager_id)


class software_featurers(models.Model):
    manager_id = models.ForeignKey(to=software_manager,on_delete=models.CASCADE)    
    description = models.CharField(max_length=100)
    ref_url =  models.URLField(null=True)



class comment_on_software_order(models.Model):
    order = models.OneToOneField(to=software_orders,on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((5,5), (4,4),(3,3),(2,2),(1,1),(0,0)))
    comment = models.TextField()
    def __str__(self):
        return " soft rating "+str(self.rating)+" on soft product "+str(self.order)

class report_on_software(models.Model):
    order = models.OneToOneField(to=software_orders,on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    report = models.TextField()
    rollback_url = models.URLField(null=True)
    is_accepted = models.BooleanField(default=False)
    def __str__(self):
        return " soft report "+str(self.title)+" on soft product "+str(self.order)


class services_manager(models.Model):
    description = models.TextField()
    long_description = models.TextField(null=True)
    pic = models.ImageField(upload_to="image")
    name = models.CharField(max_length = 30)
    package_price = models.IntegerField()
    brands_product = models.ForeignKey(to=brand,on_delete=models.CASCADE)
    total_rating = models.IntegerField(default=0)
    seconds_spends_on_product = models.IntegerField(default=0)
    is_active = models.BooleanField(default = True)
    def __str__(self):
        return "brand "+str(self.brands_product)+" service product "+str(self.name)

class service_relations(models.Model):
    first = models.ForeignKey(to=services_manager,on_delete=models.CASCADE,related_name="first")
    second = models.ForeignKey(to=services_manager,on_delete=models.CASCADE,related_name="second")


class service_portfolio(models.Model):
    manager = models.ForeignKey(to = services_manager,on_delete=models.CASCADE)
    project_name = models.CharField(max_length = 100)
    project_short_description = models.TextField()
    starting_date = models.DateField()
    ending_date = models.DateField()
    project_url_link = models.URLField()


class services_form(models.Model):
    problem_title = models.CharField(max_length = 100)
    background = models.TextField()
    demands = models.TextField()
    first_link_of_inspiration = models.URLField(null = True)
    second_link_of_inspiration = models.URLField(null = True)
    third_link_of_inspiration = models.URLField(null = True)
    completion_date = models.DateField()
    def __str__(self):
        return " problem "+str(self.problem_title)


class request_on_sevice(models.Model):
    form = models.OneToOneField(to=services_form,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(to=customer,on_delete=models.CASCADE)
    service_id = models.ForeignKey(to=services_manager,on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    def __str__(self):
        return " request by "+str(self.customer_id)+" on problem "+str(self.form)


class service_order(models.Model):
    date_of_order = models.DateTimeField(auto_now=True)
    request_id = models.OneToOneField(to=request_on_sevice,on_delete=models.CASCADE)
    commited_amount = models.IntegerField()
    check_out = models.ForeignKey(to=check_out,on_delete=models.CASCADE,null=True)
    is_complete = models.BooleanField(default=False)
    is_commited_by_customer = models.BooleanField(default = False)
    is_commited_by_owner = models.BooleanField(default= False)
    is_commited_by_admin = models.BooleanField(default= False)
    is_active = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    is_finantial_transaction = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    def __str__(self):
        return str(self.request_id)+" commited amount "+str(self.commited_amount)

class service_featurers(models.Model):
    manager_id = models.ForeignKey(to=services_manager,on_delete=models.CASCADE)    
    description = models.CharField(max_length=100)
    ref_url =  models.URLField(null=True)


class comment_on_service(models.Model):
    order = models.OneToOneField(to=service_order,on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((5,5), (4,4),(3,3),(2,2),(1,1),(0,0)))
    comment = models.TextField()
    def __str__(self):
        return " ser rating "+str(self.rating)+" on service product "+str(self.order)

class report_on_service(models.Model):
    order = models.OneToOneField(to=service_order,on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    report = models.TextField()
    rollback_url = models.URLField(null=True)
    is_accepted = models.BooleanField(default=False)
    def __str__(self):
        return " ser title "+str(self.title)+" on service product "+str(self.order)


class accounts_turn(models.Model):
    user = models.ForeignKey(to = customer,on_delete=models.CASCADE)
    starting_date = models.DateTimeField(auto_now=True)
    ending_date = models.DateTimeField(null = True)
    total_gain = models.IntegerField(null = True)
    is_complete = models.BooleanField(default = False)
    activate = models.BooleanField(default = True)

class cash_in(models.Model):
    turn = models.ForeignKey(to = accounts_turn,on_delete=models.CASCADE)
    description = models.CharField(max_length = 30,null = True)
    date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField()

class cash_out(models.Model):
    turn = models.ForeignKey(to = accounts_turn,on_delete=models.CASCADE)
    description = models.CharField(max_length = 30,null = True)
    date = models.DateTimeField(auto_now=True)
    amount = models.IntegerField()
