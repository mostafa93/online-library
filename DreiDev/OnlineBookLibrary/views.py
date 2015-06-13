from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm
from OnlineBookLibrary.forms import UserCreateForm
from django.contrib.auth import authenticate, login, views
from OnlineBookLibrary.models import Library, Book
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.forms.models import modelformset_factory
from OnlineBookLibrary.forms import create_Book
from django import forms


class LoginRequiredMixin(object):

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            messages.add_message(self.request, messages.INFO, 'Hello world.')
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class HomeView(TemplateView):
    template_name = "home.html"

    def post(self, request, *args, **kwargs):
        template_response = views.login(request, template_name="home.html")
        return template_response

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        lib = 0
        try:
            lib = Library.objects.get(library_owner_id=request.user.id)
        except:
            pass
        return render(request, 'home.html', {'form': form, 'lib': lib})

    # def books(self):
    #     return Book.objects.all()


class UserRegisteration(TemplateView):
    template_name = 'user-registeration.html'

    def get(self, request, *args, **kwargs):
        form = UserCreateForm()
        return render(request, 'user-registeration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password1'])
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        return render(
            request,
            'user-registeration.html', {'form': form})


class LibraryCreation(LoginRequiredMixin, CreateView):
    model = Library
    fields = ['library_name', 'library_owner']
    success_url = reverse_lazy('home')
    template_name = 'library_form.html'
    # fail_url = reverse_lazy('home')


class LibraryList(ListView):
    model = Library


class LibraryView(DetailView):
    model = Library

    def get_context_data(self, **kwargs):
        lib = Library.objects.get(slug=self.kwargs['slug'])
        context = super(DetailView, self).get_context_data(**kwargs)
        
        book_list = Book.objects.filter(library_id=lib.id)
        paginator = Paginator(book_list, 5)
        page = self.request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
                books = paginator.page(1)
        except EmptyPage:
                books = paginator.page(paginator.num_pages)
        context['books'] = books
        return context


class BookCreate(CreateView):
    model = Book
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        lib = Library.objects.get(slug=self.kwargs['slug'])
        context = super(BookCreate, self).get_context_data(**kwargs)
        context['library'] = lib
        return context

    def get(self, request, *args, **kwargs):
        lib = Library.objects.get(slug=self.kwargs['slug'])
        BookFormSet = modelformset_factory(Book, extra=2, form=create_Book)
        formset = BookFormSet(queryset=Book.objects.none())
        for form in formset.forms:
                form.initial['library'] = lib.id
                form.fields['library'].widget = forms.HiddenInput()
        return render(
            request, 'book_form.html', {'formset': formset, 'library': lib})

    def post(self, request, *args, **kwargs):
        lib = Library.objects.get(slug=self.kwargs['slug'])
        BookFormSet = modelformset_factory(Book, extra=2, form=create_Book)
        formset = BookFormSet(request.POST)
        if formset.is_valid():  
            formset.save()
            return HttpResponseRedirect(reverse('home'))
        return render(
            request, 'book_form.html', {'formset': formset})
