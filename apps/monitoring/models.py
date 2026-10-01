from django.db import models
class Sensor(models.Model):
 sensor_id=models.CharField(max_length=64,unique=True); location=models.CharField(max_length=120,default='Cold room'); product_type=models.CharField(max_length=40,default='Food'); active=models.BooleanField(default=True)
class SensorReading(models.Model):
 sensor=models.ForeignKey(Sensor,on_delete=models.CASCADE,related_name='readings'); timestamp=models.DateTimeField(db_index=True); temperature=models.FloatField(); humidity=models.FloatField(null=True); ambient_temperature=models.FloatField(null=True); power_kw=models.FloatField(null=True); compressor_state=models.BooleanField(default=False); door_open=models.BooleanField(default=False)
 class Meta: ordering=['timestamp']; constraints=[models.UniqueConstraint(fields=['sensor','timestamp'],name='sensor_time')]
