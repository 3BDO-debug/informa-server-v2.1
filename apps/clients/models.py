from django.db import models
from accounts.models import User
from meals.models import FoodItem

# Create your models here.
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_id = models.CharField(max_length=10, verbose_name="Subscription ID")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} -- {self.subscription_id}"


class ClientData(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name="Related Client", null=True
    )
    weight = models.IntegerField(verbose_name="Weight")
    height = models.IntegerField(verbose_name="Height")
    age = models.IntegerField(verbose_name="Age")
    body_fat = models.IntegerField(verbose_name="Body fat percentage")
    body_fat_calc_method = models.CharField(
        verbose_name="Body fat calculation method", max_length=350
    )
    training_volume = models.CharField(verbose_name="Training volume", max_length=150)
    activity_per_day = models.CharField(verbose_name="Activity per day", max_length=100)
    goal = models.CharField(max_length=100, verbose_name="Client goal")
    preferred_schema = models.CharField(
        max_length=350, verbose_name="Client Prefered Schema"
    )
    excluded_food_items = models.ManyToManyField(
        FoodItem,
        verbose_name="Client excluded food items",
        related_name="excluded_food_items",
    )
    can_take_protein_supplement = models.BooleanField(
        default=False, verbose_name="Can take protein supplement"
    )
    number_of_meals = models.IntegerField(verbose_name="Prefered number of meals")
    lean_body_mass = models.IntegerField(verbose_name="Lean body mass", default=100)
    bmr = models.IntegerField(verbose_name="BMR", default=100)
    total_calories = models.IntegerField(verbose_name="Total calories", default=100)
    calories_deficit = models.IntegerField(verbose_name="Calories deficit", default=100)
    protein_grams = models.IntegerField(verbose_name="Protein grams", default=100)
    fat_grams = models.IntegerField(verbose_name="Fat grams", default=100)
    carb_grams = models.IntegerField(verbose_name="Carb grams", default=100)
    generate_using_this_data = models.BooleanField(
        default=False, verbose_name="Generate program using this data"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "Client Data"
        verbose_name_plural = "Clients Data"

    def __str__(self):
        return (
            f"Data For {self.client.user.username} -- {self.generate_using_this_data}"
        )
