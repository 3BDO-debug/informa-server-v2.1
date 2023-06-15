from django.db import models

# Create your models here.


class FoodItem(models.Model):
    en_name = models.CharField(max_length=350, verbose_name="Meal english name")
    ar_name = models.CharField(max_length=350, verbose_name="Meal arabic name")
    serving = models.IntegerField(verbose_name="Serving")
    protein = models.FloatField(verbose_name="Protein")
    fats = models.FloatField(verbose_name="Fats")
    carbs = models.FloatField(verbose_name="Carbs")
    total_kcal = models.FloatField(verbose_name="Total kcal")
    calc_per_piece = models.BooleanField(
        default=False, verbose_name="This food item should be calculated per piece ?"
    )
    per_piece_serving = models.FloatField(
        verbose_name="Per piece serving", default=0.00
    )
    per_piece_name = models.CharField(
        max_length=350, verbose_name="Per piece name", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Food item"
        verbose_name_plural = "Food items"

    def __str__(self):
        return self.en_name


class MealType(models.Model):
    name = models.CharField(max_length=350, verbose_name="Meal type name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Meal type"
        verbose_name_plural = "Meals types"

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=350, verbose_name="Meal name")

    meal_type = models.ForeignKey(
        MealType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Meal type",
    )
    recommendation_months = models.CharField(
        max_length=30, verbose_name="This meal recommended for", null=True
    )
    is_snack = models.BooleanField(default=False, verbose_name="Is snack ?")
    contain_protein_supplement = models.BooleanField(
        default=False, verbose_name="This meal contains protein supplement"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    is_refeed_snack = models.BooleanField(default=False)
    recommendation_indexes = models.CharField(
        max_length=350, verbose_name="Recommendation index", null=True
    )

    class Meta:
        verbose_name = "Meal"
        verbose_name_plural = "Meals"

    def __str__(self):
        return self.name


class MealItem(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, verbose_name="Meal")
    category = models.CharField(max_length=350, verbose_name="Category")

    food_item = models.ForeignKey(
        FoodItem, on_delete=models.CASCADE, verbose_name="Food Item"
    )
    video_link = models.CharField(
        max_length=350, verbose_name="Video link", default="Video Link Here"
    )
    preparation_description = models.TextField(
        verbose_name="Meal item preparation description",
        default="Meal item preparation description",
    )
    serving = models.IntegerField(verbose_name="Serving")
    protein = models.FloatField(verbose_name="Protein per serving")
    carbs = models.FloatField(verbose_name="Carbohydrates per serving")
    fats = models.FloatField(verbose_name="Fats per serving")
    total_kcal = models.FloatField(verbose_name="Total kcal")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Meal item"
        verbose_name_plural = "Meal items"

    def __str__(self):
        return f"{self.food_item.en_name} for {self.meal.name}"
