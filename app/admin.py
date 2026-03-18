from django.contrib import admin
from .models import ZenithProfile, ZenithDeposit, ZenithTrade

@admin.register(ZenithProfile)
class ZenithProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance_display')
    search_fields = ('user__username', 'user__email')
    ordering = ('-balance',)

    def balance_display(self, obj):
        return f"KES {obj.balance}"
    balance_display.short_description = 'Available Balance'

@admin.register(ZenithDeposit)
class ZenithDepositAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount_display', 'phone_number', 'is_complete', 'mpesa_receipt_number', 'created_at')
    list_filter = ('is_complete', 'created_at')
    search_fields = ('user__username', 'phone_number', 'mpesa_receipt_number', 'checkout_request_id')
    readonly_fields = ('checkout_request_id', 'merchant_request_id', 'result_code', 'result_description', 'created_at')
    ordering = ('-created_at',)

    def amount_display(self, obj):
        return f"KES {obj.amount}"
    amount_display.short_description = 'Deposit Amount'

@admin.register(ZenithTrade)
class ZenithTradeAdmin(admin.ModelAdmin):
    list_display = ('user', 'trade_type', 'amount_display', 'outcome', 'timestamp')
    list_filter = ('trade_type', 'outcome', 'timestamp')
    search_fields = ('user__username',)
    readonly_fields = ('user', 'amount', 'trade_type', 'outcome', 'timestamp') # Make trades read-only so they can't be tampered with
    ordering = ('-timestamp',)

    def amount_display(self, obj):
        return f"KES {obj.amount}"
    amount_display.short_description = 'Investment'

# Rebrand the Django Admin interface
admin.site.site_header = "StakeZenith Administration"
admin.site.site_title = "StakeZenith Admin Portal"
admin.site.index_title = "Welcome to the StakeZenith Broker Dashboard"