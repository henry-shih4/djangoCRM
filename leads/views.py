from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm
from django.views import generic


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

def landingPage(request):
    return render(request, 'landing.html')


class LeadListView(generic.ListView):
    template_name = 'lead_list.html'
    queryset = Lead.objects.all()
    context_object_name= 'leads'

def leadList(request):
    leads = Lead.objects.all()
    context={
        "leads":leads
    }
    return render(request, "lead_list.html", context)


class LeadDetailView(generic.DeleteView):
    template_name = 'lead_detail.html'
    queryset = Lead.objects.all()
    context_object_name= 'lead'


def leadDetail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead":lead
    }
    return render(request, "lead_detail.html", context)


class LeadCreateView(generic.CreateView):
    template_name = 'lead_create.html'
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse('leads:leadList')


def createLead(request):
    form = LeadModelForm()
    if request.method == 'POST':
        print('receiving post request')
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'form':LeadModelForm()
    }

    return render(request, "lead_create.html", context)


class LeadUpdateView(generic.UpdateView):
    template_name = 'lead_update.html'
    queryset = Lead.objects.all()
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse('leads:leadDetail', kwargs={'pk': self.object.pk})

def leadUpdate(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == 'POST':
        print('receiving post request')
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect(f'/leads/{pk}/')
    context = {
            'form':form, 
            'lead':lead
        }
    return render(request, 'lead_update.html',context)

class LeadDeleteView(generic.DeleteView):
    template_name = 'lead_delete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:leadList')


def leadDelete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

# def leadUpdate(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == 'POST':
#         print('receiving post request')
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print('form is valid')
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name=first_name
#             lead.last_name=last_name
#             lead.age = age
#             lead.save()
#             return redirect('/leads')
#     context = {
#         'form':form, 
#         'lead':lead
#     }

#     return render(request, "lead_update.html", context)



# def createLead(request):
    # form = LeadForm()
    # if request.method == 'POST':
    #     print('receiving post request')
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         print('form is valid')
    #         print(form.cleaned_data)
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = form.cleaned_data['agent']
    #         Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
    #         print('lead has been created')
    #         return redirect('/leads')
    # context = {
    #     'form':LeadForm()
    # }

    # return render(request, "lead_create.html", context)