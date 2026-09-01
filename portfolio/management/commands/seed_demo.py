"""
Commande pour créer des données de démonstration.
"""

from django.core.management.base import BaseCommand
from portfolio.models import SiteSettings, Category, Service, Project, Testimonial


class Command(BaseCommand):
    help = 'Crée des données de démonstration pour le portfolio'

    def handle(self, *args, **kwargs):
        self.stdout.write("Création des données de démonstration...")

        # SiteSettings
        if not SiteSettings.objects.exists():
            SiteSettings.objects.create(
                professional_name="Abdoulwahab Oumar",
                slogan="Excellence et rigueur dans chaque projet",
                short_presentation="Ingénieur civil passionné, je conçois et réalise des projets de construction alliant technique, esthétique et durabilité.",
                full_description="Avec une approche rigoureuse et créative, j'accompagne mes clients de la conception à la réalisation de leurs projets de construction. Basé à Douala, j'interviens sur l'ensemble du territoire camerounais.",
                phone_primary="+237 693 149 222",
                phone_secondary="+237 690 892 646",
                phone_third="+237 689 874 206",
                whatsapp_number="+237 693 149 222",
                email="contact@abdoulwahaboumar.com",
                address="Douala, Cameroun",
                city="Douala",
                country="Cameroun",
                hero_text="Des solutions pensées pour vos projets.",
                hero_subtext="Conception, construction, rénovation et aménagement — de l'idée à la livraison.",
                seo_title="Abdoulwahab Oumar — Ingénieur Civil & Bâtiment | Douala, Cameroun",
                seo_description="Services de génie civil, construction, rénovation et conception architecturale à Douala et au Cameroun.",
                copyright_year=2026,
            )
            self.stdout.write(self.style.SUCCESS("✓ Configuration du site créée"))

        # Catégories
        categories_data = [
            {"name": "Maisons", "slug": "maisons", "description": "Conception et construction de maisons individuelles", "order": 1},
            {"name": "Bâtiments", "slug": "batiments", "description": "Bâtiments commerciaux et industriels", "order": 2},
            {"name": "Construction", "slug": "construction", "description": "Projets de construction divers", "order": 3},
            {"name": "Rénovation", "slug": "renovation", "description": "Rénovation et réhabilitation", "order": 4},
            {"name": "Aménagement", "slug": "amenagement", "description": "Aménagement intérieur et extérieur", "order": 5},
            {"name": "Décoration", "slug": "decoration", "description": "Décoration et finitions", "order": 6},
            {"name": "Plans et conception", "slug": "plans-et-conception", "description": "Études et plans architecturaux", "order": 7},
            {"name": "Autres", "slug": "autres", "description": "Autres projets", "order": 8},
        ]

        for cat_data in categories_data:
            Category.objects.get_or_create(slug=cat_data["slug"], defaults=cat_data)
        self.stdout.write(self.style.SUCCESS(f"✓ {len(categories_data)} catégories créées"))

        # Services
        services_data = [
            {
                "title": "Conception architecturale",
                "slug": "conception-architecturale",
                "short_description": "Plans et études personnalisés pour votre projet",
                "description": "De l'esquisse initiale aux plans d'exécution, nous concevons des espaces adaptés à vos besoins, votre terrain et votre budget. Chaque projet est unique et mérite une attention particulière.",
                "order": 1,
            },
            {
                "title": "Construction",
                "slug": "construction",
                "short_description": "Réalisation de bâtiments neufs avec rigueur",
                "description": "Nous assurons la construction de maisons, bâtiments commerciaux et industriels avec un suivi rigoureux de la qualité, des délais et du budget. Maîtrise d'œuvre complète.",
                "order": 2,
            },
            {
                "title": "Rénovation",
                "slug": "renovation",
                "short_description": "Transformation et modernisation d'espaces existants",
                "description": "Redonnez vie à vos bâtiments grâce à nos services de rénovation complète ou partielle. Structure, façades, intérieurs — nous modernisons tout en préservant l'âme du lieu.",
                "order": 3,
            },
            {
                "title": "Aménagement",
                "slug": "amenagement",
                "short_description": "Optimisation de vos espaces intérieurs et extérieurs",
                "description": "Nous optimisons l'agencement et l'utilisation de vos espaces pour créer des environnements fonctionnels, esthétiques et confortables. Intérieur comme extérieur.",
                "order": 4,
            },
            {
                "title": "Décoration",
                "slug": "decoration",
                "short_description": "Finitions et décoration sur mesure",
                "description": "Peinture, revêtements, éclairage, mobilier sur mesure — nous sublimons vos espaces avec des finitions de qualité et un sens aigu du détail.",
                "order": 5,
            },
            {
                "title": "Suivi de projet",
                "slug": "suivi-de-projet",
                "short_description": "Coordination et contrôle de vos chantiers",
                "description": "Nous assurons le suivi technique et administratif de votre chantier : coordination des corps de métier, contrôle qualité, respect des normes et des délais.",
                "order": 6,
            },
        ]

        for svc_data in services_data:
            Service.objects.get_or_create(slug=svc_data["slug"], defaults=svc_data)
        self.stdout.write(self.style.SUCCESS(f"✓ {len(services_data)} services créés"))

        # Projets de démonstration (sans images)
        projects_data = [
            {
                "title": "Villa contemporaine Bonapriso",
                "slug": "villa-contemporaine-bonapriso",
                "short_description": "Construction d'une villa moderne de 450 m² avec piscine et jardin paysager.",
                "description": "Ce projet de construction neuve comprenait la réalisation complète d'une villa contemporaine sur deux niveaux. Nous avons assuré la conception architecturale, le gros œuvre, les finitions haut de gamme et l'aménagement paysager.",
                "location": "Bonapriso, Douala",
                "client_name": "Particulier",
                "year": 2025,
                "duration": "18 mois",
                "is_featured": True,
                "order": 1,
                "category_slug": "maisons",
            },
            {
                "title": "Rénovation immeuble Akwa",
                "slug": "renovation-immeuble-akwa",
                "short_description": "Rénovation complète d'un immeuble de bureaux de 5 étages.",
                "description": "Rénovation structurelle et esthétique d'un immeuble de bureaux datant des années 90. Travaux de consolidation, nouvelles façades, réaménagement des espaces intérieurs et mise aux normes.",
                "location": "Akwa, Douala",
                "client_name": "Société immobilière",
                "year": 2024,
                "duration": "14 mois",
                "is_featured": True,
                "order": 2,
                "category_slug": "renovation",
            },
            {
                "title": "Complexe commercial Deido",
                "slug": "complexe-commercial-deido",
                "short_description": "Construction d'un complexe commercial de 1200 m².",
                "description": "Conception et construction d'un complexe commercial moderne comprenant 15 boutiques, un parking souterrain et des espaces communs. Gestion complète du projet de la fondation à la livraison.",
                "location": "Deido, Douala",
                "client_name": "Investisseur privé",
                "year": 2025,
                "duration": "24 mois",
                "is_featured": False,
                "order": 3,
                "category_slug": "batiments",
            },
            {
                "title": "Aménagement résidence Makepe",
                "slug": "amenagement-residence-makepe",
                "short_description": "Aménagement intérieur complet d'une résidence de luxe.",
                "description": "Aménagement intérieur sur mesure incluant cuisine équipée, dressings, salles de bain, salon et chambres. Sélection des matériaux, supervision des artisans et coordination des finitions.",
                "location": "Makepe, Douala",
                "client_name": "Particulier",
                "year": 2024,
                "duration": "8 mois",
                "is_featured": True,
                "order": 4,
                "category_slug": "amenagement",
            },
            {
                "title": "Plan de maison individuelle",
                "slug": "plan-maison-individuelle",
                "short_description": "Étude architecturale complète pour une maison de 300 m².",
                "description": "Réalisation des plans architecturaux, structuraux et techniques pour une maison individuelle. Étude de faisabilité, permis de construire, plans d'exécution et suivi de chantier.",
                "location": "Bonamoussadi, Douala",
                "client_name": "Particulier",
                "year": 2025,
                "duration": "3 mois",
                "is_featured": False,
                "order": 5,
                "category_slug": "plans-et-conception",
            },
            {
                "title": "Décoration bureau direction",
                "slug": "decoration-bureau-direction",
                "short_description": "Décoration et finitions d'un bureau de direction moderne.",
                "description": "Conception et réalisation de l'aménagement d'un bureau de direction incluant mobilier sur mesure, éclairage architectural, revêtements muraux et sols haut de gamme.",
                "location": "Bali, Douala",
                "client_name": "Entreprise",
                "year": 2024,
                "duration": "2 mois",
                "is_featured": False,
                "order": 6,
                "category_slug": "decoration",
            },
        ]

        for proj_data in projects_data:
            cat_slug = proj_data.pop("category_slug")
            category = Category.objects.filter(slug=cat_slug).first()
            proj_data["category"] = category
            Project.objects.get_or_create(slug=proj_data["slug"], defaults=proj_data)
        self.stdout.write(self.style.SUCCESS(f"✓ {len(projects_data)} projets créés"))

        # Témoignages approuvés
        testimonials_data = [
            {
                "name": "Jean-Pierre M.",
                "profession": "Entrepreneur",
                "company": "",
                "message": "Abdoulwahab a su transformer notre vision en réalité. La construction de notre villa s'est déroulée dans le respect des délais et du budget. Un professionnel sérieux et à l'écoute.",
                "rating": 5,
                "status": "approved",
                "is_featured": True,
            },
            {
                "name": "Marie K.",
                "profession": "Cadre bancaire",
                "company": "",
                "message": "Très satisfaite de la rénovation de mon appartement. Le travail est soigné, les finitions sont impeccables. Je recommande vivement ses services.",
                "rating": 5,
                "status": "approved",
                "is_featured": True,
            },
            {
                "name": "Alain T.",
                "profession": "Promoteur immobilier",
                "company": "AT Immobilier",
                "message": "Nous collaborons régulièrement avec Abdoulwahab sur nos projets. Sa rigueur technique et son sens du détail font de lui un partenaire de confiance.",
                "rating": 5,
                "status": "approved",
                "is_featured": False,
            },
            {
                "name": "Sophie N.",
                "profession": "Médecin",
                "company": "",
                "message": "L'aménagement de ma clinique a été réalisé avec professionnalisme. L'espace est fonctionnel, moderne et accueillant. Merci pour cette excellente réalisation.",
                "rating": 4,
                "status": "approved",
                "is_featured": False,
            },
        ]

        for test_data in testimonials_data:
            Testimonial.objects.get_or_create(
                name=test_data["name"],
                message=test_data["message"],
                defaults=test_data
            )
        self.stdout.write(self.style.SUCCESS(f"✓ {len(testimonials_data)} témoignages créés"))

        self.stdout.write(self.style.SUCCESS("\nDonnées de démonstration créées avec succès !"))
        self.stdout.write("Lancez le serveur : python manage.py runserver")
