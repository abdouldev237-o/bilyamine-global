"""
Modèles du portfolio professionnel d'Abdoulwahab Oumar.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils.html import format_html
from PIL import Image
import os


class SingletonModel(models.Model):
    """Modèle singleton pour garantir une seule instance."""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    """Configuration globale du site."""
    # Identité
    professional_name = models.CharField(
        "Nom du professionnel",
        max_length=200,
        default="Abdoulwahab Oumar"
    )
    slogan = models.CharField("Slogan", max_length=300, blank=True)
    short_presentation = models.TextField("Courte présentation", blank=True)
    full_description = models.TextField("Description complète", blank=True)

    # Contact
    phone_primary = models.CharField("Téléphone principal", max_length=50, default="+237 693 149 222")
    phone_secondary = models.CharField("Deuxième téléphone", max_length=50, blank=True, default="+237 690 892 646")
    phone_third = models.CharField("Troisième téléphone", max_length=50, blank=True, default="+237 689 874 206")
    whatsapp_number = models.CharField("Numéro WhatsApp", max_length=50, default="+237 693 149 222")
    email = models.EmailField("Email", blank=True)
    address = models.CharField("Adresse", max_length=300, blank=True)
    city = models.CharField("Ville", max_length=100, default="Douala")
    country = models.CharField("Pays", max_length=100, default="Cameroun")

    # Images
    profile_photo = models.ImageField("Photo de profil", upload_to='site/', blank=True)
    logo = models.ImageField("Logo", upload_to='site/', blank=True)
    hero_image = models.ImageField("Image hero", upload_to='site/', blank=True)

    # Hero text
    hero_text = models.CharField("Texte hero", max_length=300, default="Des solutions pensées pour vos projets.")
    hero_subtext = models.CharField("Sous-texte hero", max_length=500, blank=True)

    # SEO
    seo_title = models.CharField("Titre SEO", max_length=200, default="Abdoulwahab Oumar — Ingénieur Civil & Bâtiment | Douala, Cameroun")
    seo_description = models.TextField("Description SEO", blank=True)
    og_image = models.ImageField("Image Open Graph", upload_to='site/', blank=True)

    # Réseaux sociaux
    facebook_url = models.URLField("Facebook", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    linkedin_url = models.URLField("LinkedIn", blank=True)
    twitter_url = models.URLField("Twitter / X", blank=True)

    # Copyright
    copyright_year = models.PositiveIntegerField("Année de copyright", default=2026)

    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Configuration du site"
        verbose_name_plural = "Configuration du site"

    def __str__(self):
        return "Configuration du site"

    def thumbnail(self):
        if self.profile_photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', self.profile_photo.url)
        return "—"
    thumbnail.short_description = "Aperçu"


class Category(models.Model):
    """Catégorie de réalisations."""
    name = models.CharField("Nom", max_length=100)
    slug = models.SlugField("Slug", unique=True, blank=True)
    description = models.TextField("Description", blank=True)
    icon = models.CharField("Icône (classe SVG ou nom)", max_length=100, blank=True, help_text="Nom de l'icône ou classe CSS")
    image = models.ImageField("Image", upload_to='categories/', blank=True)
    is_active = models.BooleanField("Active", default=True)
    order = models.PositiveIntegerField("Ordre", default=0)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def project_count(self):
        return self.projects.filter(is_published=True).count()

    @property
    def total_project_count(self):
        return self.projects.count()

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;" />', self.image.url)
        return "—"
    thumbnail.short_description = "Aperçu"


class Service(models.Model):
    """Service proposé."""
    title = models.CharField("Titre", max_length=200)
    slug = models.SlugField("Slug", unique=True, blank=True)
    short_description = models.CharField("Courte description", max_length=300, blank=True)
    description = models.TextField("Description complète", blank=True)
    icon = models.CharField("Icône SVG / classe", max_length=200, blank=True, help_text="Code SVG inline ou classe CSS")
    image = models.ImageField("Image", upload_to='services/', blank=True)
    is_active = models.BooleanField("Actif", default=True)
    order = models.PositiveIntegerField("Ordre", default=0)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;" />', self.image.url)
        return "—"
    thumbnail.short_description = "Aperçu"


class Project(models.Model):
    """Réalisation / Projet."""
    title = models.CharField("Titre", max_length=200)
    slug = models.SlugField("Slug", unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Catégorie",
        related_name='projects'
    )
    short_description = models.CharField("Courte description", max_length=300, blank=True)
    description = models.TextField("Description complète", blank=True)
    location = models.CharField("Localisation", max_length=200, blank=True)
    client_name = models.CharField("Nom du client", max_length=200, blank=True)
    year = models.PositiveIntegerField("Année", blank=True, null=True)
    duration = models.CharField("Durée", max_length=100, blank=True)
    main_image = models.ImageField("Image principale", upload_to='projects/main/')
    is_featured = models.BooleanField("À la une", default=False)
    is_published = models.BooleanField("Publié", default=True)
    order = models.PositiveIntegerField("Ordre", default=0)

    # SEO
    meta_title = models.CharField("Meta titre", max_length=200, blank=True)
    meta_description = models.TextField("Meta description", blank=True)

    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Réalisation"
        verbose_name_plural = "Réalisations"
        ordering = ['-is_featured', 'order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def image_count(self):
        return self.gallery_images.filter(is_published=True).count()

    def thumbnail(self):
        if self.main_image:
            return format_html('<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 4px;" />', self.main_image.url)
        return "—"
    thumbnail.short_description = "Aperçu"

    def preview(self):
        if self.main_image:
            return format_html('<img src="{}" style="width: 200px; height: 150px; object-fit: cover; border-radius: 6px;" />', self.main_image.url)
        return "—"
    preview.short_description = "Prévisualisation"

    def large_preview(self):
        if self.main_image:
            return format_html('<img src="{}" style="max-width: 400px; max-height: 300px; object-fit: cover; border-radius: 8px;" />', self.main_image.url)
        return "—"
    large_preview.short_description = "Grande prévisualisation"


class GalleryImage(models.Model):
    """Image de la galerie d'un projet."""
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name="Projet",
        related_name='gallery_images'
    )
    image = models.ImageField("Image", upload_to='projects/gallery/')
    title = models.CharField("Titre", max_length=200, blank=True)
    caption = models.CharField("Légende", max_length=300, blank=True)
    alt_text = models.CharField("Texte alternatif", max_length=200, blank=True)
    order = models.PositiveIntegerField("Ordre", default=0)
    is_published = models.BooleanField("Publiée", default=True)
    created_at = models.DateTimeField("Créé le", auto_now_add=True)

    class Meta:
        verbose_name = "Image de galerie"
        verbose_name_plural = "Images de galerie"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.project.title} — {self.title or 'Image'}"

    def thumbnail(self):
        if self.image:
            return format_html('<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 4px;" />', self.image.url)
        return "—"
    thumbnail.short_description = "Aperçu"

    def preview(self):
        if self.image:
            return format_html('<img src="{}" style="width: 200px; height: 150px; object-fit: cover; border-radius: 6px;" />', self.image.url)
        return "—"
    preview.short_description = "Prévisualisation"

    def large_preview(self):
        if self.image:
            return format_html('<img src="{}" style="max-width: 400px; max-height: 300px; object-fit: cover; border-radius: 8px;" />', self.image.url)
        return "—"
    large_preview.short_description = "Grande prévisualisation"


class Testimonial(models.Model):
    """Témoignage client."""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Refusé'),
    ]

    name = models.CharField("Nom", max_length=200)
    profession = models.CharField("Profession", max_length=200, blank=True)
    company = models.CharField("Entreprise", max_length=200, blank=True)
    message = models.TextField("Message")
    rating = models.PositiveIntegerField(
        "Note",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Projet associé",
        related_name='testimonials'
    )
    status = models.CharField(
        "Statut",
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    is_featured = models.BooleanField("À la une", default=False)
    admin_note = models.TextField("Note admin", blank=True, help_text="Notes internes pour l'administrateur")
    created_at = models.DateTimeField("Créé le", auto_now_add=True)
    updated_at = models.DateTimeField("Modifié le", auto_now=True)

    class Meta:
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.name} — {self.get_status_display()}"

    def status_badge(self):
        colors = {
            'pending': '#F59E0B',
            'approved': '#10B981',
            'rejected': '#EF4444',
        }
        color = colors.get(self.status, '#64748B')
        label = self.get_status_display()
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600;">{}</span>',
            color, label
        )
    status_badge.short_description = "Statut"
