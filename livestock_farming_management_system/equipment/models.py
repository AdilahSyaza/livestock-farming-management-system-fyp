from django.db import models

from user.models import User

# This model defines Equipment table in database with fields related to equipment information.
class Equipment(models.Model):

    equipmentName = models.CharField(max_length=150)
    equipmentMake = models.CharField(max_length=150, null=True)
    equipmentModel = models.CharField(max_length=150, null=True)
    equipmentYear = models.CharField(max_length=150, null=True)
    equipmentSerialID = models.CharField(max_length=150, unique=True, null=True, blank=True)
    equipmentAcquiredDate = models.DateField(null=True, blank=True)
    equipmentLastMaintenance = models.DateField(null=True, blank=True)
    equipmentColor = models.CharField(max_length=150, null=True)
    equipmentLocation = models.CharField(max_length=150)
    equipmentPrice = models.FloatField(max_length=150, null=True)
    equipmentPurchasedFrom = models.CharField(max_length=150, null=True)
    equipmentNotes = models.CharField(max_length=150, null=True)
    equipmentStatus = models.CharField(max_length=150, null=True)
    equipmentPhoto = models.ImageField(upload_to='equipment/',default="", null=True)

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'Equipment'


# This model defines EquipmentUsage table in database with fields related to equipmant usage information.
class EquipmentUsage(models.Model):

    dateUsed = models.DateField(null=True, blank=True)
    statusUsage = models.CharField(max_length=250)
    usageInfo = models.CharField(max_length=250)
    usedBy_user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipmentID_equip = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name="usedEquipment")

    def save(self):
        super().save()

    def delete(self):
        super().delete()

    class Meta:
        db_table = 'EquipmentUsage'