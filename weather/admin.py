from django.contrib import admin
from .models import City, CurrentWeather, CityStats, StatsSummary
from django.db.models import Count, Sum, Min, Max, DateTimeField

# admin.site.register(City)
# admin.site.register(CurrentWeather)
# admin.site.register(CityStats)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("russian_name", "name", "openweather_id",)
    search_fields = ("russian_name__icontains", "name__icontains")


@admin.register(CurrentWeather)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city", "temp", "description",)
    list_filter = ("description",)
    search_fields = ("city__russian_name", "description__icontains",)


@admin.register(CityStats)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city", "views",)
    search_fields = ("city__russian_name",)


# TODO broken af
@admin.register(StatsSummary)
class StatsSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/stats_summary_change_list.html'
    # date_hierarchy = 'created'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total_cities': Count('city'),
            'total_views': Sum('views'),
        }

        response.context_data['summary'] = list(
            qs
            .values('views')
            .annotate(**metrics)
            .order_by('-views')
        )

        return response
