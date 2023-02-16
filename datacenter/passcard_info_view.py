from django.shortcuts import render, get_object_or_404
from datacenter.models import Passcard, Visit


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    this_passcard_visits = Visit.objects.filter(passcard__passcode=passcode)

    this_passcard_visits_serialized = []
    for visit in this_passcard_visits:
        duration = Visit.get_duration(visit)
        is_strange = Visit.is_visit_long(visit)
        this_passcard_visits_serialized.append({
            'entered_at': visit.entered_at,
            'duration': Visit.format_duration(duration),
            'is_strange': is_strange,
        })

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits_serialized
    }
    return render(request, 'passcard_info.html', context)
