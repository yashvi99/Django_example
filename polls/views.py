from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question,Choice
import requests


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
        
		return render(request, 'polls/detail.html', {
        	'question': question,
        	'error_message': "You didn't select a choice.",
        	})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def movie(request, movieName):
    key="546c6742"
    baseurl= "http://www.omdbapi.com/"
    params_d = {}
    params_d["t"]= movieName
    params_d["apikey"]= key
    params_d["r"]= "json"
    resp = requests.get(baseurl, params=params_d)
    respDic = resp.json()
    return render(request, 'polls/movie.html', {
        'name' : respDic['Title'],
        'year' : respDic['Year'],
        'genre' : respDic['Genre'],
        'actors' : respDic['Actors']

        })
