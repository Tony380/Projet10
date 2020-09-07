""" Contains database filler """
from django.core.management.base import BaseCommand
from core.models import Category, Product
from django.db.utils import IntegrityError
import requests
from django.db import transaction


class Command(BaseCommand):
    help = 'Fill the database with OpenFoodFacts data'

    def handle(self, *args, **options):
        # Chosen categories
        name = ["Pâtes à tartiner aux noisettes et au cacao",
                "Muffins", "Biscuits", "Tortellini", "Viennoiseries",
                "Taboulés", "Confitures", "Cassoulets", "Yaourts", "Sodas"]
        self.stdout.write('Réinitialisation de la base de données')
        Category.objects.all().delete()
        Product.objects.all().delete()
        self.stdout.write('Base de données réinitialisée avec succès')
        cat_id = 1
        prod_id = 1
        for element in name:
            self.stdout.write('Import de la catégorie {}'.format(element))
            cat = Category.objects.create(id=cat_id, name=element)
            cat_id += 1
            self.stdout.write(
                'Import des produits de la catégorie {}'.format(element))
            payload = {"search_terms": "{}".format(cat),
                       "page_size": 50, "json": 1}
            res = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                               params=payload)
            result = res.json()
            products = result["products"]
            for i in products:
                # avoid products with missing data
                try:
                    with transaction.atomic():
                        if i.get("product_name", False) and\
                                i.get("brands", False) and \
                                i.get("nutrition_grades", False) and\
                                i.get("image_front_url", False):
                            product = Product.objects.create(
                                id=prod_id,
                                name=i["product_name"],
                                brands=i["brands"],
                                link=i["url"],
                                nutriscore=i["nutrition_grades"],
                                image=i["image_front_url"],
                                fat=i["nutriments"]["fat_100g"],
                                saturated_fat=i["nutriments"]
                                ["saturated-fat_100g"],
                                sugars=i["nutriments"]["sugars_100g"],
                                salt=i["nutriments"]["salt_100g"], )
                            cat.products.add(product)
                            prod_id += 1

                except IntegrityError:
                    pass

        self.stdout.write('Base de données remplie avec succès')
