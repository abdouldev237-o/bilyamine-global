from django.contrib.sitemaps import Sitemap

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    
    def items(self):
        return ['/', '/about/', '/services/', '/contact/', '/projects/', '/a-propos', '/realisations', '/temoignages']

    def location(self, item):
        return item