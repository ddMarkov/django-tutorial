from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'all_questions_list'

    def get_queryset(self):
        return Question.objects.all()


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model = Question


def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
