from django.db import models

class LeafSample(models.Model):
    image_path = models.CharField(max_length=255)  # Increased length for flexibility
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Leaf Sample - {self.image_path}"

    class Meta:
        verbose_name_plural = "Leaf Samples"


class SoilSample(models.Model):
    nitrogen_value = models.FloatField()
    phosphorus_value = models.FloatField()
    potassium_value = models.FloatField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Soil Sample - N:{self.nitrogen_value}, P:{self.phosphorus_value}, K:{self.potassium_value}"

    class Meta:
        verbose_name_plural = "Soil Samples"


class Prediction(models.Model):
    leaf = models.ForeignKey(
        LeafSample, on_delete=models.CASCADE, null=True, blank=True, related_name="predictions"
    )
    soil = models.ForeignKey(
        SoilSample, on_delete=models.CASCADE, null=True, blank=True, related_name="predictions"
    )
    result = models.CharField(max_length=255)
    confidence = models.FloatField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction - {self.result} ({self.confidence*100:.2f}%)"

    class Meta:
        verbose_name_plural = "Predictions"
