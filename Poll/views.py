from django.shortcuts import render


from django.http import HttpResponse, Http404
from django.template import loader

from .models import Candidate, Vote, Voter


def index(request, token):
    try:
        voter = Voter.objects.get(token=token)
    except Voter.DoesNotExist:
        raise Http404()


    candidates = Candidate.objects.order_by('name')
    template = loader.get_template('vote.html')
    context = {
        'candidates': candidates,
    }

    if len(Vote.objects.filter(voter=voter)):
        context['error_message'] = 'شما قبلا رای داده اید.'
        return HttpResponse(template.render(context, request))

    if request.method == "GET":
        return HttpResponse(template.render(context, request))
    else:
        votes = request.POST.getlist('vote', [])
        if len(votes) == 0:
            context['error_message'] = 'لطفا حداقل یک کاندید را انتخاب کنید.'
        elif len(votes) > 5:
            context['error_message'] = 'حداکثر ۵ نفر را می‌توانید انتخاب کنید.'

        else:
            objs = []
            for vote in votes:
                try:
                    candidate = Candidate.objects.get(pk = vote)
                except Candidate.DoesNotExist:
                    context['error_message'] = 'کاندید انتخاب شده معتبر نیست.'
                    return HttpResponse(template.render(context, request))
                obj = Vote(voter=voter, candidate=candidate)
                objs.append(obj)
            Vote.objects.bulk_create(objs)
            context['success_message'] = 'رای شما ثبت شد.'
    return HttpResponse(template.render(context, request))
