from django.db import models
from accounts.models import User
from meals.models import FoodItem
from cloudinary.models import CloudinaryField


# Create your models here.
class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_id = models.CharField(max_length=10, verbose_name="Subscription ID")
    phone_number = models.CharField(max_length=350, verbose_name="Phone number")
    follow_up_package = models.CharField(
        max_length=350, verbose_name="Follow up package"
    )
    plan_type = models.CharField(max_length=350, verbose_name="Plan Type")
    plan_duration = models.IntegerField(verbose_name="Plan duration")

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
        blank=True,
    )
    can_take_protein_supplement = models.BooleanField(
        default=False, verbose_name="Can take protein supplement"
    )
    number_of_meals = models.IntegerField(verbose_name="Prefered number of meals")
    water_in_take = models.FloatField(verbose_name="Daily water in take")
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


class MealIntake(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    meal = models.ForeignKey(
        "nutrition_plan_algorithm.NutritionPlanMeal",
        on_delete=models.CASCADE,
        verbose_name="Related meal",
    )
    meal_image = CloudinaryField(verbose_name="Meal uploaded", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Time stamp")

    class Meta:
        verbose_name = "Meal in-take tracking"
        verbose_name_plural = "Meal in-take trackings"

    def __str__(self):
        return f"Meal tracking for {self.client.user.first_name} {self.client.user.last_name} | {self.meal.meal_category} - {self.meal.meal_index}"


class WaterInTake(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name="Related client"
    )
    in_take = models.FloatField(max_length=150, verbose_name="Water in-take")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "Water in-take tracking"
        verbose_name_plural = "Water in-take trackings"

    def __str__(self):
        return f"Water in-take for {self.client.user.first_name} {self.client.user.last_name}"


class ClientFollowUp(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Related client",
        related_name="related_client",
    )
    coach = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="related_coach",
        verbose_name="Related coach",
    )
    note = models.TextField(max_length=350, verbose_name="Follow up note")
    status = models.CharField(max_length=350, verbose_name="Follow-up status")
    scheduled_time = models.TimeField(verbose_name="Scheduled follow-up time")
    is_active = models.BooleanField(default=True, verbose_name="Follow-up is active")

    class Meta:
        verbose_name = "Client follow-up"
        verbose_name_plural = "Cliens follow-ups"

    def __str__(self):
        return f"Follow-up for {self.client.user.username} - {self.scheduled_time}"
