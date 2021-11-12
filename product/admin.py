import admin_thumbnails
from django.contrib import admin
from django.db import models
from product.models import Categorie,Product, Images, Setting, ReviewMessage, Comment_ReviewForm, Color, Size, Variants, ProductLang, CategoryLang
from mptt.admin import DraggableMPTTAdmin



# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = 'title'
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count', 'create_at', 'update_at')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    list_filter = ['status']

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        #Add cumulative product count
        qs = Categorie.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True
        )

        #Add non cumulative product count
        qs = Categorie.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_count',
            cumulative=False
        )
        return qs
    
   
    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'



#   /////////////// Start of Inlines \\\\\\\\\\\\\\\\#

@admin_thumbnails.thumbnail('image')
class ProductImageInLine(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1


class NewProductCaptionInline(admin.TabularInline):
    model = Setting


class ProductVariantInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True


class ProductLangInline(admin.TabularInline):
    model = ProductLang
    extra = 1
    show_change_link = True
    prepopulated_fields = {'slug': ('title',)}

#   /////////////// End of Inlines \\\\\\\\\\\\\\\\#

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'image_tag']
    list_filter = ['category']
    readonly_fields = ['image_tag']
    inlines = [ProductImageInLine, NewProductCaptionInline, ProductVariantInline, ProductLangInline]
    prepopulated_fields = {'slug': ('title',)}


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'title', 'image_thumbnail']


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    #inlines = [NewProductCaptionInline]


class Comment_Review(admin.ModelAdmin):
    list_display = ['name', 'subject', 'email', 'created_at', 'updated_at', 'status']
    readonly_fields = ('name', 'subject', 'email', 'comment', 'rate', 'ip')
    list_filter = ['status']
    #prepopulated_fields = {'title': ('subject',)}


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']


class Variants_Admin(admin.ModelAdmin):
    list_display = ['title', 'product', 'color', 'size', 'image_id', 'quantity', 'price', 'image_tag']


class ProductLangugaeAdmin(admin.ModelAdmin):
    list_display = ['title','lang','slug']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['lang']

class CategoryLangugaeAdmin(admin.ModelAdmin):
    list_display = ['title','lang','slug']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['lang']





admin.site.register(Color, ColorAdmin)
admin.site.register(Variants, Variants_Admin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Categorie, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Images, ImagesAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(ReviewMessage, Comment_Review)
admin.site.register(ProductLang,ProductLangugaeAdmin)
admin.site.register(CategoryLang,CategoryLangugaeAdmin)