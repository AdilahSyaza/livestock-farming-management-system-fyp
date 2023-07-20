from django.db import models
from user.models import User
from animal.models import Cattle,Sheep
import datetime


# This model defines Expense table in database with fields related to expense information.
class Expense(models.Model):

    expenseName = models.CharField(max_length=250)
    expenseAmount = models.FloatField(default=0,null=True)
    expenseCategory = models.CharField(max_length=250,null=True)
    expenseNote = models.TextField(blank=True, null=True)
    expenseMadeDate = models.DateField(null=True, blank=True)
    expenseRecordDate = models.DateField(default=datetime.date.today)
    expenseAttachment = models.FileField(upload_to='financial/expense/', null=True)
    expenseMadeBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="expenseMadeBy", null=True)
    expenseLastUpdatedBy = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="expenseLastUpdatedBy", null=True)

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'Expense'


# This model defines Income table in database with fields related to income information.
class Income(models.Model):

    incomeItem = models.CharField(max_length=250)
    incomeAmount = models.FloatField(default=0,null=True)
    incomeCategory = models.CharField(max_length=250,null=True)
    incomeCustomer = models.CharField(max_length=255,blank=True, null=True)
    incomeInvoice = models.CharField(max_length=250,null=True)
    incomeMadeDate = models.DateField(null=True, blank=True)
    incomeRecordDate = models.DateField(default=datetime.date.today)
    incomeAttachment = models.FileField(upload_to='financial/income/', null=True)
    incomeRecordedBy = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="incomeRecordedBy", null=True)
    incomeLastUpdatedBy = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="incomeLastUpdatedBy", null=True)

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'Income'


# This model defines SaleTicket table in database with fields related to sale ticket information.
class SaleTicket(models.Model):

    saleTicketInvoice = models.CharField(max_length=250, null=True)
    saleTotalAmount = models.FloatField(default=0,null=True)
    saleMarketingCost = models.FloatField(default=0,null=True)
    soldToCustomer = models.CharField(max_length=255,)
    saleComment = models.TextField(blank=True, null=True)
    saleDate = models.DateField(null=True, blank=True)
    saleRecordedDate = models.DateField(default=datetime.date.today)
    saleAttachment = models.FileField(upload_to='financial/saleTicket/', null=True)
    saleTicketInvoiceStatus = models.CharField(max_length=255,null=True)
    saleRecordedBy = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="saleTicketRecordedBy", null=True)
    saleLastUpdatedBy = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="saleTicketLastUpdatedBy", null=True)

    def save(self):
        super().save()
        return self.id

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'SaleTicket'


# This model defines SoldCattle table in database with fields related to sold cattle information.
class SoldCattle(models.Model):

    sc_pricePerKg = models.FloatField(default=0,null=True)
    sc_salePrice = models.FloatField(default=0,null=True)
    sc_saleWeight = models.FloatField(default=0,null=True)
    sc_cattle = models.ForeignKey(Cattle,on_delete=models.SET_NULL,related_name="cattleSold", null=True)
    sc_saleTicket = models.ForeignKey(SaleTicket,on_delete=models.SET_NULL,related_name="cattleSaleTicket", null=True)

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'SoldCattle'


# This model defines SoldSheep table in database with fields related to sold sheep information.
class SoldSheep(models.Model):

    ss_pricePerKg = models.FloatField(default=0,null=True)
    ss_salePrice = models.FloatField(default=0,null=True)
    ss_saleWeight = models.FloatField(default=0,null=True)
    ss_sheep = models.ForeignKey(Sheep,on_delete=models.SET_NULL,related_name="sheepSold", null=True)
    ss_saleTicket = models.ForeignKey(SaleTicket,on_delete=models.SET_NULL,related_name="sheepSaleTicket", null=True)

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'SoldSheep'