"""
Vues du portfolio professionnel.
"""

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages
from django.core.paginator import Paginator
from .models import SiteSettings, Category, Service, Project, GalleryImage, Testimonial
from .forms import TestimonialForm


def home(request):
    """Page d'accueil."""
    settings = SiteSettings.load()

    # Hero & presentation
    hero_text = settings.hero_text if settings else "Des solutions pensées pour vos projets."
    hero_subtext = settings.hero_subtext if settings else ""

    # Services actifs
    services = Service.objects.filter(is_active=True)[:6]

    # Catégories actives avec compteur
    categories = Category.objects.filter(is_active=True)[:8]

    # Réalisations à la une
    featured_projects = Project.objects.filter(is_published=True, is_featured=True)[:6]

    # Dernières réalisations
    latest_projects = Project.objects.filter(is_published=True)[:6]

    # Témoignages approuvés à la une
    featured_testimonials = Testimonial.objects.filter(
        status='approved',
        is_featured=True
    )[:6]

    # Tous les témoignages approuvés
    testimonials = Testimonial.objects.filter(status='approved')[:6]

    # Statistiques
    stats = {
        'projects_count': Project.objects.filter(is_published=True).count(),
        'categories_count': Category.objects.filter(is_active=True).count(),
        'testimonials_count': Testimonial.objects.filter(status='approved').count(),
        'services_count': Service.objects.filter(is_active=True).count(),
    }

    context = {
        'hero_text': hero_text,
        'hero_subtext': hero_subtext,
        'services': services,
        'categories': categories,
        'featured_projects': featured_projects,
        'latest_projects': latest_projects,
        'featured_testimonials': featured_testimonials,
        'testimonials': testimonials,
        'stats': stats,
        'meta_title': settings.seo_title if settings else "Bilyamine — Ingénieur Civil & Bâtiment",
        'meta_description': settings.seo_description if settings else "",
    }
    return render(request, 'portfolio/home.html', context)


def about(request):
    """Page À propos."""
    settings = SiteSettings.load()

    context = {
        'meta_title': f"À propos — {settings.professional_name if settings else 'Bilyamine'}",
        'meta_description': settings.short_presentation if settings else "",
    }
    return render(request, 'portfolio/about.html', context)


def services(request):
    """Page Services."""
    settings = SiteSettings.load()
    services_list = Service.objects.filter(is_active=True)

    context = {
        'services': services_list,
        'meta_title': f"Nos Services — {settings.professional_name if settings else 'Bilyamine'}",
        'meta_description': "Découvrez nos services de conception, construction, rénovation et aménagement.",
    }
    return render(request, 'portfolio/services.html', context)


def projects(request):
    """Page Réalisations avec filtre par catégorie."""
    settings = SiteSettings.load()

    # Toutes les catégories avec compteur pour le filtre
    categories = Category.objects.filter(is_active=True)

    # Filtrage
    category_slug = request.GET.get('categorie')
    projects_qs = Project.objects.filter(is_published=True).select_related('category')

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        projects_qs = projects_qs.filter(category=active_category)

    # Pagination
    paginator = Paginator(projects_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'projects': page_obj,
        'active_category': active_category,
        'meta_title': f"Nos Réalisations — {settings.professional_name if settings else 'Bilyamine'}",
        'meta_description': "Découvrez nos projets de construction, conception, rénovation et aménagement à Douala et au Cameroun.",
    }
    return render(request, 'portfolio/projects.html', context)


def project_detail(request, slug):
    """Détail d'une réalisation."""
    settings = SiteSettings.load()
    project = get_object_or_404(Project, slug=slug, is_published=True)

    # Galerie
    gallery = project.gallery_images.filter(is_published=True)

    # Témoignages liés
    testimonials = Testimonial.objects.filter(
        project=project,
        status='approved'
    )

    # Projets similaires (même catégorie)
    similar_projects = Project.objects.filter(
        is_published=True,
        category=project.category
    ).exclude(id=project.id)[:3]

    context = {
        'project': project,
        'gallery': gallery,
        'testimonials': testimonials,
        'similar_projects': similar_projects,
        'meta_title': project.meta_title or f"{project.title} — Réalisation",
        'meta_description': project.meta_description or project.short_description,
    }
    return render(request, 'portfolio/project_detail.html', context)


def testimonials(request):
    """Page Témoignages avec formulaire."""
    settings = SiteSettings.load()

    # Témoignages approuvés
    testimonials_list = Testimonial.objects.filter(status='approved').select_related('project')

    # Formulaire
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Merci pour votre témoignage. Il a bien été envoyé et sera vérifié avant publication."
            )
            return redirect('portfolio:testimonials')
    else:
        form = TestimonialForm()

    context = {
        'testimonials': testimonials_list,
        'form': form,
        'meta_title': f"Témoignages — {settings.professional_name if settings else 'Bilyamine'}",
        'meta_description': "Découvrez les témoignages de nos clients et partagez votre expérience.",
    }
    return render(request, 'portfolio/testimonials.html', context)


def contact(request):
    """Page Contact."""
    settings = SiteSettings.load()

    # Lien WhatsApp dynamique
    whatsapp_number = "+237693149222"
    if settings and settings.whatsapp_number:
        whatsapp_number = settings.whatsapp_number.replace(" ", "").replace("+", "")

    whatsapp_link = f"https://wa.me/{whatsapp_number}?text=Bonjour%2C%20je%20souhaite%20avoir%20des%20informations%20concernant%20un%20projet."

    context = {
        'whatsapp_link': whatsapp_link,
        'meta_title': f"Contact — {settings.professional_name if settings else 'Bilyamine'}",
        'meta_description': "Contactez Bilyamine pour vos projets de construction, conception et rénovation à Douala, Cameroun.",
    }
    return render(request, 'portfolio/contact.html', context)
