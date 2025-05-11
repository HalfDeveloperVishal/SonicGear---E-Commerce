from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import New_arrival, Featured_product, CustomUser, CartItem , Earphone , Headphone ,TechGadget , Address , ProductImage , AllProduct
from django.utils.html import mark_safe

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 4
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'display_image', 'type', 'stock_status', 'rating', 'price', 'created_at')
    list_filter = ('type', 'stock_status')
    search_fields = ('product_name', 'id', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    list_editable = ('price', 'rating', 'stock_status')
    list_per_page = 20
    inlines = [ProductImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'product_name', 'type', 'description')
        }),
        ('Stock & Pricing', {
            'fields': ('stock_status', 'price', 'rating')
        }),
        ('Media', {
            'fields': ('product_image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def display_image(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.product_image.url)
        return "No Image"
    
    display_image.short_description = 'Image Preview'


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('name', 'email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('name', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)

    fieldsets = (
        ("User Info", {"fields": ("name", "email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        ("New User", {
            "classes": ("wide",),
            "fields": ("name", "email", "password1", "password2", "is_staff", "is_superuser", "is_active"),
        }),
    )


# CartItem Admin
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'display_product', 
        'product_type', 
        'display_image', 
        'display_rating', 
        'display_price', 
        'quantity', 
        'added_at'
    )
    list_filter = ('product_type', 'added_at')
    search_fields = (
        'user__username', 
        'new_arrival__product_name', 
        'featured_product__product_name', 
        'earphone__product_name',
        'headphone__product_name',
        'techgadget__product_name',
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Dynamically filter product selection based on product type."""
        if db_field.name == "new_arrival":
            kwargs["queryset"] = New_arrival.objects.all()
        elif db_field.name == "featured_product":
            kwargs["queryset"] = Featured_product.objects.all()
        elif db_field.name == "earphone":
            kwargs["queryset"] = Earphone.objects.all()
        elif db_field.name == "headphone":
            kwargs["queryset"] = Headphone.objects.all()
        elif db_field.name == "techgadget":
            kwargs["queryset"] = TechGadget.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def display_product(self, obj):
        """ Show product name based on product type. """
        if obj.new_arrival:
            return obj.new_arrival.product_name
        elif obj.featured_product:
            return obj.featured_product.product_name
        elif obj.earphone:
            return obj.earphone.product_name
        elif obj.headphone:
            return obj.headphone.product_name
        elif obj.techgadget:
            return obj.techgadget.product_name
        return "Unknown Product"

    display_product.short_description = "Product Name"

    def display_image(self, obj):
        """ Show product image in admin. """
        image_url = None
        if obj.new_arrival and obj.new_arrival.product_image:
            image_url = obj.new_arrival.product_image.url
        elif obj.featured_product and obj.featured_product.product_image:
            image_url = obj.featured_product.product_image.url
        elif obj.earphone and obj.earphone.product_image:
            image_url = obj.earphone.product_image.url
        elif obj.headphone and obj.headphone.product_image:
            image_url = obj.headphone.product_image.url
        elif obj.techgadget and obj.techgadget.product_image:
            image_url = obj.techgadget.product_image.url

        if image_url:
            return mark_safe(f'<img src="{image_url}" width="50" height="50" />')
        return "No Image"

    display_image.allow_tags = True
    display_image.short_description = "Image"

    def display_rating(self, obj):
        """ Show product rating in admin. """
        if obj.new_arrival:
            return obj.new_arrival.rating
        elif obj.featured_product:
            return obj.featured_product.rating
        elif obj.earphone:
            return obj.earphone.rating
        elif obj.headphone:
            return obj.headphone.rating
        elif obj.techgadget:
            return obj.techgadget.rating
        return "N/A"

    display_rating.short_description = "Rating"

    def display_price(self, obj):
        """ Show product price in admin. """
        if obj.new_arrival:
            return f"${obj.new_arrival.price}"
        elif obj.featured_product:
            return f"${obj.featured_product.price}"
        elif obj.earphone:
            return f"${obj.earphone.price}"
        elif obj.headphone:
            return f"${obj.headphone.price}"
        elif obj.techgadget:
            return f"${obj.techgadget.price}"
        return "N/A"

    display_price.short_description = "Price"

    
class EarphoneAdmin(admin.ModelAdmin):
    list_display = ('product_name','product_image_tag', 'price', 'rating', 'created_at')
    search_fields = ('product_name',)
    list_filter = ('created_at',)
    inlines = [ProductImageInline]

    def product_image_tag(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" style="height: 50px;"/>', obj.product_image.url)
        return "-"
    
    product_image_tag.short_description = 'Image'


class HeadphoneAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_image_tag', 'price', 'rating', 'created_at')
    search_fields = ('product_name',)
    list_filter = ('created_at',)
    inlines = [ProductImageInline]

    def product_image_tag(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" style="height: 50px;"/>', obj.product_image.url)
        return "-"
    
    product_image_tag.short_description = 'Image'
    
class TechGadgetAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_image_tag', 'price', 'rating', 'created_at')
    search_fields = ('product_name',)
    list_filter = ('created_at',)
    inlines = [ProductImageInline]

    def product_image_tag(self, obj):
        if obj.product_image:
            return format_html('<img src="{}" style="height: 50px;"/>', obj.product_image.url)
        return "-"
    
    product_image_tag.short_description = 'Image'


class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'state', 'zip_code', 'country')
    
class AllProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'image')  # Display these fields in the list view
    list_filter = ('category',)  # Filter products by category in the admin panel
    search_fields = ('product_name', 'description')  # Allow searching by product name or description
    list_per_page = 20  # Show 20 products per page

# Register Models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(New_arrival, ProductAdmin)
admin.site.register(Featured_product, ProductAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Earphone, EarphoneAdmin)
admin.site.register(Headphone, HeadphoneAdmin)
admin.site.register(TechGadget, TechGadgetAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(AllProduct, AllProductAdmin)