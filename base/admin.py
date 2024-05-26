from django.contrib import admin
from .models import User, Plan, PaymentMethod, Transaction, Investment, Recommendation
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    list_display_links = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ['-date_joined']


class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'minimum_amount', 'maximum_amount', 'percentage', 'hours']
    ordering = ['-minimum_amount']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'payment_method', 'transaction_type', 'image','status', 'created']
    ordering = ['-created']

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'profit', 'plan', 'is_active', 'created']
    ordering = ['-created']


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'address_type', 'address']
    # ordering = ['-minimum_amount']

class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommended_by', 'created']
    ordering = ['-created']

admin.site.register(User, UserAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
