from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganisorAndLoginRequiredMixin
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm
from django.views import generic


class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')



class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

def landingPage(request):
    return render(request, 'landing.html')


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'lead_list.html'
    context_object_name= 'leads'

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for entire organization
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)   
            #filter leads for current agent
            queryset = queryset.filter(agent__user=user)
        return queryset



class LeadDetailView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'lead_detail.html'
    context_object_name= 'lead'

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for entire organization
        if user.is_organisor:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)   
            #filter leads for current agent
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = 'lead_create.html'
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse('leads:leadList')

    def form_valid(self, form):
        send_mail(
            subject='A lead has been created',
            message='Go to the site to see the new lead',
            from_email='test@test.com',
            recipient_list=['test2@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)

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


class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'lead_update.html'
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse('leads:leadDetail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for entire organization

        return Lead.objects.filter(organization=user.userprofile)
   
    


class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'lead_delete.html'

    def get_queryset(self):
        user = self.request.user
        #initial queryset of leads for entire organization

        return Lead.objects.filter(organization=user.userprofile)
    
    def get_success_url(self):
        return reverse('leads:leadList')



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