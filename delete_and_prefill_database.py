import os
import django
import json
import random

# Django-Umgebung konfigurieren
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coderr.settings')
django.setup()

# Django-Modelle importieren
from django.contrib.auth.models import User
from profiles_app.models import UserProfile
from offers_app.models import Offer, OfferDetail
from reviews_app.models import Review


def delete_all_data():
    """ Löscht ALLE User, Profile, Angebote und Reviews in der Datenbank """
    print("🚨 Lösche alle User, Profile, Angebote und Reviews...")
    Review.objects.all().delete()
    Offer.objects.all().delete()
    User.objects.all().delete()  # Löscht auch UserProfile durch on_delete=CASCADE
    print("✅ Alle Daten wurden erfolgreich gelöscht!")


def create_user(username, email, password, user_type):
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists!")
        return None

    if User.objects.filter(email=email).exists():
        print(f"Email '{email}' is already in use!")
        return None

    # Erstelle den User
    user = User.objects.create_user(username=username, email=email, password=password)

    # Stelle sicher, dass ein UserProfile existiert
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.type = user_type
    user_profile.save()

    print(f"User '{username}' created successfully with type '{user_type}'!")

    # Falls es ein Business-User ist, erstelle ein Offer für ihn
    if user_type == "business":
        create_offer_for_business(user)

    return user


def create_offer_for_business(user):
    """ Erstellt automatisch ein IT-relevantes Angebot für einen Business-User """
    offers_data = [
        {
            "title": "Webentwicklung Komplett-Paket",
            "description": "Ein maßgeschneidertes Webdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Webdesign",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 300,
                    "features": ["Landing Page", "Responsive Design"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Webdesign",
                    "revisions": 5,
                    "delivery_time_in_days": 10,
                    "price": 600,
                    "features": ["Landing Page", "Responsive Design", "Kontaktformular"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Webdesign",
                    "revisions": 10,
                    "delivery_time_in_days": 15,
                    "price": 1200,
                    "features": ["Landing Page", "Responsive Design", "Kontaktformular", "CMS-Anbindung"],
                    "offer_type": "premium"
                }
            ]
        },
        {
            "title": "App-Entwicklung",
            "description": "Native oder Hybrid-App-Lösungen für Ihr Business.",
            "details": [
                {
                    "title": "Basic App",
                    "revisions": 2,
                    "delivery_time_in_days": 10,
                    "price": 1000,
                    "features": ["iOS oder Android", "Basic UI"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard App",
                    "revisions": 5,
                    "delivery_time_in_days": 20,
                    "price": 2500,
                    "features": ["iOS & Android", "Moderne UI", "Push-Benachrichtigungen"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium App",
                    "revisions": 10,
                    "delivery_time_in_days": 30,
                    "price": 5000,
                    "features": ["iOS & Android", "Moderne UI", "Push-Benachrichtigungen", "Datenbank-Anbindung"],
                    "offer_type": "premium"
                }
            ]
        }
    ]

    # Zufälliges Angebot für diesen Business-User auswählen
    offer_data = offers_data[len(User.objects.filter(userprofile__type="business")) % len(offers_data)]

    offer = Offer.objects.create(
        title=offer_data["title"],
        description=offer_data["description"],
        creator=user
    )

    # Angebot-Details erstellen
    for detail in offer_data["details"]:
        OfferDetail.objects.create(
            offer=offer,
            title=detail["title"],
            revisions=detail["revisions"],
            delivery_time_in_days=detail["delivery_time_in_days"],
            price=detail["price"],
            features=json.dumps(detail["features"]),
            offer_type=detail["offer_type"]
        )

    print(f"✅ Offer '{offer.title}' created for Business-User '{user.username}'!")


def create_reviews():
    """ Kunden bewerten zufällig verschiedene Business-User mit sinnvollen Reviews """
    customers = list(User.objects.filter(userprofile__type="customer"))
    business_users = list(User.objects.filter(userprofile__type="business"))

    reviews_data = [
        {"rating": 5, "description": "Fantastische Arbeit! Die Website sieht professionell aus."},
        {"rating": 4, "description": "Gute Leistung, aber es gab kleine Verzögerungen."},
        {"rating": 5, "description": "Sehr professionell! Kommunikation war erstklassig."},
        {"rating": 3, "description": "Qualität war okay, aber es hätte besser sein können."},
        {"rating": 5, "description": "Perfekt! Alles wurde genau nach meinen Wünschen umgesetzt."},
        {"rating": 4, "description": "Guter Service, aber die Reaktionszeit könnte verbessert werden."}
    ]

    for customer in customers:
        business_user = random.choice(business_users)  # Zufälligen Business-User auswählen

        # Prüfen, ob diese Bewertung schon existiert
        if not Review.objects.filter(reviewer=customer, business_user=business_user).exists():
            review_data = random.choice(reviews_data)
            Review.objects.create(
                reviewer=customer,
                business_user=business_user,
                rating=review_data["rating"],
                description=review_data["description"]
            )
            print(f"✅ {customer.username} hat {business_user.username} mit {review_data['rating']} Sternen bewertet!")


if __name__ == "__main__":
    # Zuerst alle Daten löschen
    delete_all_data()

    users_to_create = [
        # Neue Kunden (Customer)
        {"username": "andrey", "email": "customer@example.com", "password": "asdasd", "user_type": "customer"},
        {"username": "emma", "email": "emma@example.com", "password": "customer1", "user_type": "customer"},
        {"username": "oliver", "email": "oliver@example.com", "password": "customer2", "user_type": "customer"},
        {"username": "mia", "email": "mia@example.com", "password": "customer3", "user_type": "customer"},
        {"username": "noah", "email": "noah@example.com", "password": "customer4", "user_type": "customer"},

        # Neue Geschäftsleute (Business)
        {"username": "kevin", "email": "business@example.com", "password": "asdasd24", "user_type": "business"},
        {"username": "sophia", "email": "sophia@example.com", "password": "business1", "user_type": "business"},
        {"username": "liam", "email": "liam@example.com", "password": "business2", "user_type": "business"},
        {"username": "ava", "email": "ava@example.com", "password": "business3", "user_type": "business"},
        {"username": "ethan", "email": "ethan@example.com", "password": "business4", "user_type": "business"},
    ]

    for user_data in users_to_create:
        create_user(**user_data)

    create_reviews()

    print("\n🎉 Datenbank-Reset abgeschlossen & neue User + Angebote + Reviews erstellt! 🚀")
