from django.shortcuts import render
from datacenter.models import Visit


def storage_information_view(request):
    non_closed_visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits_serialized = []

    for visitor in non_closed_visits:
        duration = Visit.get_duration(visitor)
        non_closed_visits_serialized.append(
            {
                'who_entered': visitor.passcard.owner_name,
                'entered_at': visitor.entered_at,
                'duration': Visit.format_duration(duration),
                'is_strange': Visit.is_visit_long(visitor),
            }
        )

    context = {
        'non_closed_visits': non_closed_visits_serialized,
    }
    return render(request, 'storage_information.html', context)
