from django.db import models
from cloudinary.models import CloudinaryField


class MuscleGroup(models.Model):
    name = models.CharField(max_length=350, verbose_name="Muscle group name")

    class Meta:
        verbose_name = "Muscle group"
        verbose_name_plural = "Muscle groups"

    def __str__(self):
        return self.name


class Muscle(models.Model):
    related_muscle_group = models.ForeignKey(
        MuscleGroup, on_delete=models.CASCADE, verbose_name="Related muscle group"
    )
    name = models.CharField(max_length=350, verbose_name="Muscle name")
    img = CloudinaryField(verbose_name="Muscle image", null=True, blank=True)
    img_link = models.URLField(verbose_name="Muscle image link")

    class Meta:
        verbose_name = "Muscle"
        verbose_name_plural = "Muscles"

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=350, verbose_name="Equipment name")
    related_muscle = models.ForeignKey(
        Muscle, on_delete=models.CASCADE, verbose_name="Related muscle"
    )
    img = CloudinaryField(verbose_name="Equipment image", null=True, blank=True)
    img_link = models.URLField(verbose_name="Equipment image link", null=True, blank=True)

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"

    def __str__(self):
        return self.name


class Excercise(models.Model):
    name = models.CharField(max_length=350, verbose_name="Excercise name")
    related_muscle = models.ForeignKey(
        Muscle, on_delete=models.CASCADE, verbose_name="Related muscle"
    )
    related_accessory_muscle = models.ManyToManyField(Muscle,  verbose_name="Accessory muscle", related_name="related_accessory_muscle_muscle")
    related_equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="Related equipment", null=True, blank=True, related_name="related_equipment")
    workout_thumbnail  = CloudinaryField(verbose_name = "Excercise thumbnail", null=True, blank=True)
    video = CloudinaryField(verbose_name="Excercise video", null=True, blank=True)
    video_link = models.URLField(verbose_name="Excercise video", null=True, blank=True)
    is_home_workout = models.BooleanField(default=False, verbose_name="Is home excercise ?")

    class Meta:
        verbose_name = "Excercise"
        verbose_name_plural = "Excercises"

    def __str__(self):
        return self.name
    
class Injury(models.Model):
    name = models.CharField(max_length=350, verbose_name="Injury name")
    excluded_workouts = models.ManyToManyField(Excercise, verbose_name="Excluded excercises")
    level = models.CharField(max_length=350, verbose_name="Level")
    explaination_video  = CloudinaryField(verbose_name ="Injury Explaination video", null=True, blank=True)
    explaination_video_link  = CloudinaryField(verbose_name ="Injury Explaination video", null=True, blank=True)
    description = models.TextField(verbose_name="Injury explaination video")

    class Meta:
        verbose_name = "Injury"
        verbose_name_plural = "Injuries"

    def __str__(self):
        return self.name
    
