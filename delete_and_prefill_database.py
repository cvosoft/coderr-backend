import os
import django
import json
from django.utils.timezone import now

# Django-Umgebung konfigurieren
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coderr.settings')
django.setup()

# Models importieren
from django.contrib.auth import get_user_model
from profiles_app.models import UserProfile
from offers_app.models import Offer, OfferDetails
from orders_app.models import Order
from reviews_app.models import Reviews

User = get_user_model()
PROFILE_IMAGE_PATH = "uploads/profiles/"

def delete_all_data():
    print("🚨 Lösche Datenbankeinträge...")

    Order.objects.all().delete()
    Reviews.objects.all().delete()
    OfferDetails.objects.all().delete()
    Offer.objects.all().delete()
    UserProfile.objects.all().delete()
    User.objects.all().delete()

    print("✅ Alle Daten wurden gelöscht!")


def create_user_with_profile(username, email, password, user_type):
    if User.objects.filter(username=username).exists():
        print(f"⚠️  User '{username}' existiert bereits – wird übersprungen.")
        return

    user = User.objects.create_user(username=username, email=email, password=password)

    profile = UserProfile.objects.create(
        user=user,
        username=username,
        first_name=username.capitalize(),
        last_name=user_type.capitalize(),
        file=f"{PROFILE_IMAGE_PATH}{username}.jpg",
        location="Homeoffice",
        tel="123456789",
        description=f"Ich bin {username} und nutze Coderr als {user_type}.",
        working_hours="9-17 Uhr",
        type=user_type,
        email=email,
        created_at=now()
    )

    print(f"✅ User '{username}' ({user_type}) erstellt!")

    return user


def create_users():
    users_to_create = [
        {"username": "andrey", "email": "customer@example.com", "password": "asdasd", "user_type": "customer"},
        {"username": "peter", "email": "peter@example.com", "password": "customer1", "user_type": "customer"},
        {"username": "sophia", "email": "sophia@example.com", "password": "customer2", "user_type": "customer"},
        {"username": "kevin", "email": "business@example.com", "password": "asdasd24", "user_type": "business"},
        {"username": "christoph", "email": "christoph@example.com", "password": "dsaggda", "user_type": "business"},
        {"username": "helga", "email": "helga@example.com", "password": "business2", "user_type": "business"},
    ]

    created_users = []
    for user_data in users_to_create:
        user = create_user_with_profile(**user_data)
        if user:
            created_users.append(user)

    return created_users


def create_offers_for_business_users(business_users):
    offer_templates = [
        {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium"
                }
            ]
        },
        {
            "title": "Webentwicklung Starter-Paket",
            "image": None,
            "description": "Professionelle Webentwicklung für kleine und mittlere Unternehmen.",
            "details": [
                {
                    "title": "Basic Website",
                    "revisions": 2,
                    "delivery_time_in_days": 7,
                    "price": 500,
                    "features": ["OnePager", "Responsive Design"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Website",
                    "revisions": 5,
                    "delivery_time_in_days": 14,
                    "price": 1200,
                    "features": ["Mehrseitige Website", "Kontaktformular", "Responsive Design"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Website",
                    "revisions": 10,
                    "delivery_time_in_days": 21,
                    "price": 2500,
                    "features": ["CMS-Integration", "Blog-Bereich", "SEO-Optimierung"],
                    "offer_type": "premium"
                }
            ]
        },
        {
            "title": "App-Entwicklung Komplettlösung",
            "image": None,
            "description": "Von der Idee zur App: native & cross-platform Lösungen.",
            "details": [
                {
                    "title": "Basic App",
                    "revisions": 2,
                    "delivery_time_in_days": 10,
                    "price": 1500,
                    "features": ["iOS oder Android", "Startbildschirm", "Kontaktformular"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard App",
                    "revisions": 5,
                    "delivery_time_in_days": 20,
                    "price": 3000,
                    "features": ["iOS & Android", "User-Login", "Backend-Anbindung"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium App",
                    "revisions": 10,
                    "delivery_time_in_days": 30,
                    "price": 7000,
                    "features": ["Offline-Modus", "Push-Benachrichtigungen", "Admin-Panel"],
                    "offer_type": "premium"
                }
            ]
        },
    ]

    for index, user in enumerate(business_users):
        template = offer_templates[index % len(offer_templates)]

        offer = Offer.objects.create(
            user=user,
            title=template["title"],
            description=template["description"],
            image=template["image"]
        )

        for detail in template["details"]:
            OfferDetails.objects.create(
                offer=offer,
                title=detail["title"],
                revisions=detail["revisions"],
                delivery_time_in_days=detail["delivery_time_in_days"],
                price=detail["price"],
                features=detail["features"],
                offer_type=detail["offer_type"]
            )

        print(f"📦 Angebot '{template['title']}' für {user.username} erstellt!")


def create_reviews(customers, business_users):
    reviews_data = [
        {"rating": 5, "description": "Fantastische Zusammenarbeit – alles top!"},
        {"rating": 4, "description": "Sehr gute Leistung, schnelle Umsetzung."},
        {"rating": 5, "description": "Tolles Ergebnis, jederzeit wieder!"},
        {"rating": 3, "description": "Okay, aber nicht ganz wie erwartet."},
        {"rating": 4, "description": "Gute Arbeit, freundlicher Kontakt."},
        {"rating": 5, "description": "Alles lief reibungslos, super Service!"}
    ]

    for business_user in business_users:
        for i, customer in enumerate(customers):
            review_data = reviews_data[(i + business_users.index(business_user)) % len(reviews_data)]
            Reviews.objects.create(
                reviewer=customer,
                business_user=business_user,
                rating=review_data["rating"],
                description=review_data["description"]
            )
            print(f"⭐ {customer.username} hat {business_user.username} mit {review_data['rating']} Sternen bewertet.")


if __name__ == "__main__":
    delete_all_data()
    users = create_users()
    business_users = [user for user in users if user.profile.type == "business"]
    customers = [user for user in users if user.profile.type == "customer"]
    create_offers_for_business_users(business_users)
    create_reviews(customers, business_users)
    print("\n🎉 Alles bereit: Datenbank gefüllt mit Usern, Angeboten & Bewertungen! 🚀")


