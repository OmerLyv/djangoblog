from django.contrib import admin

# Register your models here.

from .models import Article,Comment

admin.site.register(Comment)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title","author","created_date"] #Admin panelindeki makalenin sütun başlıklarını ekledik
    list_display_links=["title","author"] #Admin panelindeki makaledeki başlığa ve yazara tıklayınca onun makalesine gidiyoruz

    search_fields=["title"] #admin panelinde başlığa göre makale arama yeri ekledik

    list_filter = ["created_date"] # Oluşturulan makaleyi tarihe göre filtreliyor mesela son 7 gün

    class Meta:
        model = Article
