from django.db import models
from user.models import User
import datetime

# This model defines Cattle table in database with fields related to cattle information.
class Cattle(models.Model):

    cattleTagID = models.CharField(max_length=250)
    cattleTagPosition = models.CharField(max_length=250)
    cattleType = models.CharField(max_length=250)
    cattleStatus = models.CharField(max_length=250)
    cattleHornStatus = models.CharField(max_length=250)
    cattleBreed = models.CharField(max_length=250,null=True,)
    cattleComment = models.CharField(max_length=250,null=True,)
    cattleDateRecorded = models.DateField(default=datetime.date.today)
    cattleAttachment = models.ImageField(upload_to='animal/cattle/', null=True)
    cattleOfferPrice = models.FloatField(default=0,null=True,)
    cattleRaisedOrPurchased = models.CharField(max_length=250)
    cattleCommercialNote = models.CharField(max_length=250,null=True,)
    cattleBirthDate = models.DateField(null=True, blank=True)
    cattleBirthWeight = models.FloatField(null=True,)
    cattleWeaningStatus = models.CharField(max_length=250)
    cattleLastUpdatedBy = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    cattleDam = models.ForeignKey('Cattle',on_delete=models.SET_NULL, null=True, blank=True, related_name="cattle_Dam")
    cattleSire = models.ForeignKey('Cattle',on_delete=models.SET_NULL, null=True, blank=True, related_name="cattle_Sire")

    def save(self):
        super().save()
        return self.id

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'Cattle'


# This model defines CattleGroup table in database with fields related to cattle group information.
class CattleGroup(models.Model):
    cattleGroupName = models.CharField(max_length=250)

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'CattleGroup'


# This model defines CattleGrouping table in database with fields related to cattle grouping information.
class CattleGrouping(models.Model):
    c_cattleID = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    cg_cattleGroup = models.ForeignKey(CattleGroup, on_delete=models.CASCADE)

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'CattleGrouping'
        unique_together = [['c_cattleID', 'cg_cattleGroup']]


# This model defines Sheep table in database with fields related to sheep information.
class Sheep(models.Model):

    sheepTagID = models.CharField(max_length=250)
    sheepTagPosition = models.CharField(max_length=250)
    sheepType = models.CharField(max_length=250)
    sheepStatus = models.CharField(max_length=250)
    sheepHornStatus = models.CharField(max_length=250)
    sheepBreed = models.CharField(max_length=250,null=True)
    sheepComment = models.CharField(max_length=250,null=True)
    sheepDateRecorded = models.DateField(default=datetime.date.today)
    sheepAttachment = models.ImageField(upload_to='animal/sheep/', null=True)
    sheepOfferPrice = models.FloatField(default=0,null=True)
    sheepRaisedOrPurchased = models.CharField(max_length=250)
    sheepCommercialNote = models.CharField(max_length=250,null=True)
    sheepBirthDate = models.DateField(null=True, blank=True)
    sheepBirthWeight = models.FloatField(null=True)
    sheepWeaningStatus = models.CharField(max_length=250)
    sheepLastUpdatedBy = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    sheepDam = models.ForeignKey('Sheep',on_delete=models.SET_NULL, null=True, blank=True, related_name="sheep_Dam")
    sheepSire = models.ForeignKey('Sheep',on_delete=models.SET_NULL, null=True, blank=True, related_name="sheep_Sire")

    def save(self):
        super().save()
        return self.id

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'Sheep'


# This model defines SheepGroup table in database with fields related to sheep group information.
class SheepGroup(models.Model):
    sheepGroupName = models.CharField(max_length=250)

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'SheepGroup'


# This model defines SheepGrouping table in database with fields related to sheep grouping information.
class SheepGrouping(models.Model):
    s_sheepID = models.ForeignKey(Sheep, on_delete=models.CASCADE)
    sg_sheepGroup = models.ForeignKey(SheepGroup, on_delete=models.CASCADE)

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'SheepGrouping'
        unique_together = [['s_sheepID', 'sg_sheepGroup']]