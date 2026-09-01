"""
Configuration personnalisée de l'administration Django.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, Category, Service, Project, GalleryImage, Testimonial


# Custom admin site
admin.site.site_header = "Portfolio — Bilyamine"
admin.site.site_title = "Administration Portfolio"
admin.site.index_title = "Tableau de bord"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identité", {
            'fields': ('professional_name', 'slogan', 'short_presentation', 'full_description')
        }),
        ("Contact", {
            'fields': ('phone_primary', 'phone_secondary', 'phone_third', 'whatsapp_number', 'email', 'address', 'city', 'country')
        }),
        ("Images", {
            'fields': ('profile_photo', 'logo', 'hero_image')
        }),
        ("Hero", {
            'fields': ('hero_text', 'hero_subtext')
        }),
        ("SEO", {
            'fields': ('seo_title', 'seo_description', 'og_image')
        }),
        ("Réseaux sociaux", {
            'fields': ('facebook_url', 'instagram_url', 'linkedin_url', 'twitter_url')
        }),
        ("Informations système", {
            'fields': ('copyright_year', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        if SiteSettings.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ('thumbnail', 'image', 'title', 'caption', 'alt_text', 'order', 'is_published')
    readonly_fields = ('thumbnail',)
    ordering = ['order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'project_count_display', 'published_count_display', 'is_active', 'order', 'created_at')
    list_display_links = ('thumbnail', 'name')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'thumbnail')
    fieldsets = (
        ("Informations générales", {
            'fields': ('name', 'slug', 'description', 'icon')
        }),
        ("Image", {
            'fields': ('image', 'thumbnail')
        }),
        ("Publication", {
            'fields': ('is_active', 'order')
        }),
        ("Informations système", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def project_count_display(self, obj):
        return obj.total_project_count
    project_count_display.short_description = "Total réalisations"

    def published_count_display(self, obj):
        return obj.project_count
    published_count_display.short_description = "Publiées"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'title', 'is_active', 'order', 'created_at')
    list_display_links = ('thumbnail', 'title')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'thumbnail')
    fieldsets = (
        ("Informations générales", {
            'fields': ('title', 'slug', 'short_description', 'description', 'icon')
        }),
        ("Image", {
            'fields': ('image', 'thumbnail')
        }),
        ("Publication", {
            'fields': ('is_active', 'order')
        }),
        ("Informations système", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'title', 'category', 'location', 'year', 'image_count_display', 'is_published', 'is_featured', 'created_at')
    list_display_links = ('thumbnail', 'title')
    list_editable = ('is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', 'category', 'year', 'created_at')
    search_fields = ('title', 'description', 'location', 'client_name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'thumbnail', 'preview', 'large_preview')
    actions = ['make_published', 'make_unpublished', 'make_featured', 'make_unfeatured']
    inlines = [GalleryImageInline]
    fieldsets = (
        ("Informations générales", {
            'fields': ('title', 'slug', 'category', 'short_description', 'description')
        }),
        ("Détails du projet", {
            'fields': ('location', 'client_name', 'year', 'duration')
        }),
        ("Image principale", {
            'fields': ('main_image', 'thumbnail', 'preview', 'large_preview')
        }),
        ("Publication", {
            'fields': ('is_featured', 'is_published', 'order')
        }),
        ("SEO", {
            'fields': ('meta_title', 'meta_description')
        }),
        ("Informations système", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_count_display(self, obj):
        return obj.image_count
    image_count_display.short_description = "Images"

    @admin.action(description="Publier les réalisations sélectionnées")
    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Dépublier les réalisations sélectionnées")
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    @admin.action(description="Mettre à la une")
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Retirer de la une")
    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'title', 'project', 'order', 'is_published', 'created_at')
    list_display_links = ('thumbnail', 'title')
    list_editable = ('order', 'is_published')
    list_filter = ('is_published', 'project', 'created_at')
    search_fields = ('title', 'caption', 'alt_text', 'project__title')
    readonly_fields = ('thumbnail', 'preview', 'large_preview', 'created_at')
    fieldsets = (
        ("Informations", {
            'fields': ('project', 'image', 'thumbnail', 'preview', 'large_preview', 'title', 'caption', 'alt_text')
        }),
        ("Publication", {
            'fields': ('order', 'is_published')
        }),
        ("Informations système", {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'profession', 'company', 'rating', 'project', 'status_badge', 'is_featured', 'created_at')
    list_display_links = ('name',)
    list_editable = ('is_featured',)
    list_filter = ('status', 'is_featured', 'rating', 'created_at')
    search_fields = ('name', 'profession', 'company', 'message')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_testimonials', 'reject_testimonials', 'pending_testimonials', 'feature_testimonials', 'unfeature_testimonials']
    fieldsets = (
        ("Informations", {
            'fields': ('name', 'profession', 'company', 'rating', 'project', 'message')
        }),
        ("Modération", {
            'fields': ('status', 'is_featured', 'admin_note')
        }),
        ("Informations système", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.action(description="Approuver les témoignages sélectionnés")
    def approve_testimonials(self, request, queryset):
        queryset.update(status='approved')

    @admin.action(description="Refuser les témoignages sélectionnés")
    def reject_testimonials(self, request, queryset):
        queryset.update(status='rejected')

    @admin.action(description="Remettre en attente")
    def pending_testimonials(self, request, queryset):
        queryset.update(status='pending')

    @admin.action(description="Mettre à la une")
    def feature_testimonials(self, request, queryset):
        queryset.update(is_featured=True)

    @admin.action(description="Retirer de la une")
    def unfeature_testimonials(self, request, queryset):
        queryset.update(is_featured=False)
