from django.shortcuts import render, get_object_or_404
from polls.models import Question, Choice
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
import logging

# Create your views here.

logger = logging.getLogger(__name__)
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """latest 5 question"""
        return Question.objects.order_by('-pub_date')[:5]

#def index(request):
#    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
#    context = {'latest_question_list': latest_question_list}
#    return render(request, 'polls/index.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

#def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/detail.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#def results(request, question_id):
#    question = get_object_or_404(Question, pk=question_id)
#    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    logger.debug("vote().question_id: %s" % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You did not select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

