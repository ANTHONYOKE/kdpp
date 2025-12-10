from django.contrib import admin
from .models import Report
from django.utils import timezone
from datetime import timedelta

# Custom filter: Last 24 hours
class Last24HoursFilter(admin.SimpleListFilter):
    title = 'Reports from last 24 hours'
    parameter_name = 'last_24_hours'

    def lookups(self, request, model_admin):
        return [('yes', 'Last 24 Hours')]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            cutoff = timezone.now() - timedelta(hours=24)
            return queryset.filter(date_submitted__gte=cutoff)
        return queryset


# Custom filter: Reports with evidence
class EvidenceFilter(admin.SimpleListFilter):
    title = 'Evidence Attached'
    parameter_name = 'evidence_attached'

    def lookups(self, request, model_admin):
        return [('yes', 'With Evidence'), ('no', 'Without Evidence')]

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(image='')
        if self.value() == 'no':
            return queryset.filter(image='')
        return queryset


# Main Admin
class ReportAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'region', 'county', 'case_type', 'date_submitted', 'anonymous')
    list_filter = (
        'case_type',
        'anonymous',
        EvidenceFilter,
        Last24HoursFilter,
        'date_submitted'
    )
    search_fields = ('name', 'region', 'county', 'case_type', 'description', 'keywords')

    def display_name(self, obj):
        return "Anonymous" if obj.anonymous else (obj.name or "No Name")
    display_name.short_description = "Reporter"


admin.site.register(Report, ReportAdmin)
