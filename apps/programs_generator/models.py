from django.db import models
from meals.models import FoodItem


class ClientData(models.Model):
    subscription_id = models.CharField(max_length=10, verbose_name="Subscription ID")
    fullname = models.CharField(max_length=350, verbose_name="User full name")
    weight = models.IntegerField(verbose_name="Weight")
    height = models.IntegerField(verbose_name="Height")
    age = models.IntegerField(verbose_name="Age")
    body_fat = models.IntegerField(verbose_name="Body fat percentage")
    body_fat_calc_method = models.CharField(
        verbose_name="Body fat calculation method", max_length=350
    )
    training_volume = models.CharField(verbose_name="Training volume", max_length=150)
    activity_per_day = models.CharField(verbose_name="Activity per day", max_length=100)
    goal = models.CharField(max_length=100, verbose_name="User goal")
    excluded_food_items = models.ManyToManyField(
        FoodItem,
        verbose_name="User excluded food items",
        related_name="excluded_food_items",
    )
    prefered_food_items = models.ManyToManyField(
        FoodItem, verbose_name="Prefered food item", related_name="prefered_food_items"
    )
    can_take_protein_supplement = models.BooleanField(
        default=False, verbose_name="Can take protein supplement"
    )
    number_of_meals = models.IntegerField(verbose_name="Prefered number of meals")

    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "User data"
        verbose_name_plural = "Users data"

    def __str__(self):
        return f"{self.subscription_id} - {self.fullname}"


class ClientMacros(models.Model):
    client = models.ForeignKey(
        ClientData,
        verbose_name="Related user",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    lean_body_mass = models.IntegerField(verbose_name="Lean body mass")
    bmr = models.IntegerField(verbose_name="BMR")
    total_calories = models.IntegerField(verbose_name="Total calories")
    calories_deficit = models.IntegerField(verbose_name="Calories deficit")
    protein_grams = models.IntegerField(verbose_name="Protein grams")
    fat_grams = models.IntegerField(verbose_name="Fat grams")
    carb_grams = models.IntegerField(verbose_name="Carb grams")
    computed_at = models.DateTimeField(auto_now_add=True, verbose_name="Computed at")

    class Meta:
        verbose_name = "User calories calculation"
        verbose_name_plural = "Users calories calculations"
