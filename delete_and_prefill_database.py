import os
import django
import json
import random

# Django-Umgebung konfigurieren
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coderr.settings')
django.setup()

from reviews_app.models import Review
from offers_app.models import Offer, OfferDetail
from profiles_app.models import UserProfile
from django.contrib.auth.models import User

# Pfad für Profilbilder
PROFILE_IMAGE_PATH = "uploads/profiles/"  


def delete_all_data():
    """ Löscht ALLE User, Profile, Angebote und Reviews in der Datenbank """
    print("🚨 Lösche alle User, Profile, Angebote und Reviews...")
    Review.objects.all().delete()
    Offer.objects.all().delete()
    User.objects.all().delete()  
    print("✅ Alle Daten wurden erfolgreich gelöscht!")


def get_profile_image(username):
    """ Gibt den Dateipfad des Profilbildes zurück oder `default.jpg`, falls keins existiert """
    return f"{PROFILE_IMAGE_PATH}{username}.jpg"


def create_user(username, email, password, user_type):
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists!")
        return None

    if User.objects.filter(email=email).exists():
        print(f"Email '{email}' is already in use!")
        return None

    user = User.objects.create_user(username=username, email=email, password=password)

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.type = user_type
    user_profile.file = get_profile_image(username)  
    user_profile.save()

    print(f"User '{username}' created successfully with type '{user_type}' and profile image '{user_profile.file}'!")

    if user_type == "business":
        create_offer_for_business(user)

    return user


def create_offer_for_business(user):
    """ Erstellt automatisch ein IT-relevantes Angebot für jeden Business-User """
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
        },
        {
            "title": "Cybersecurity Beratung",
            "description": "Expertenberatung für Sicherheitsstrategien und IT-Sicherheit.",
            "details": [
                {
                    "title": "Basic Audit",
                    "revisions": 1,
                    "delivery_time_in_days": 7,
                    "price": 500,
                    "features": ["Grundlegendes Security Audit", "Bericht mit Empfehlungen"],
                    "offer_type": "basic"
                },
                {
                    "title": "Standard Audit",
                    "revisions": 3,
                    "delivery_time_in_days": 14,
                    "price": 1200,
                    "features": ["Umfassendes Security Audit", "Bericht mit detaillierten Handlungsempfehlungen", "Firewall-Check"],
                    "offer_type": "standard"
                },
                {
                    "title": "Premium Audit",
                    "revisions": 5,
                    "delivery_time_in_days": 21,
                    "price": 3000,
                    "features": ["Tiefgehende Sicherheitsanalyse", "Penetrationstests", "Schwachstellenbehebung"],
                    "offer_type": "premium"
                }
            ]
        }
    ]

    # Weise jedem Business-User ein Angebot basierend auf der Reihenfolge zu
    business_users = list(User.objects.filter(userprofile__type="business"))
    assigned_offer = offers_data[business_users.index(user) % len(offers_data)]

    offer = Offer.objects.create(
        title=assigned_offer["title"],
        description=assigned_offer["description"],
        creator=user
    )

    for detail in assigned_offer["details"]:
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
        business_user = random.choice(business_users)

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
    delete_all_data()

    users_to_create = [
        {"username": "andrey", "email": "customer@example.com", "password": "asdasd", "user_type": "customer"},
        {"username": "peter", "email": "peter@example.com", "password": "customer1", "user_type": "customer"},
        {"username": "sophia", "email": "sophia@example.com", "password": "customer2", "user_type": "customer"},
        {"username": "kevin", "email": "business@example.com", "password": "asdasd24", "user_type": "business"},
        {"username": "christoph", "email": "christoph@example.com", "password": "dsaggda", "user_type": "business"},
        {"username": "helga", "email": "helga@example.com", "password": "business2", "user_type": "business"},
    ]

    for user_data in users_to_create:
        create_user(**user_data)

    create_reviews()

    print("\n🎉 Datenbank-Reset abgeschlossen & neue User + Angebote + Reviews erstellt! 🚀")
