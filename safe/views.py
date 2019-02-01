from django.shortcuts import render
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.utils.decorators import method_decorator

from safe import models
from safe.forms import UserForm, UserAttributeForm, SafeUpdateForm


# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
from safe.models import Safe, UserAttributes, Safe_Event


class IndexView(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'safe/index.html'

    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        #context['injectme'] = "Basic Injection!"
        return context


def top_level(request):
    # Default top-level - redirects to safe
    return HttpResponseRedirect(reverse('safe:index'))


@login_required
def keyholder(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/safe/user_login/'
    return render(request, 'safe/keyholder.html', {})


@login_required
def safeholder(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/safe/user_login/'
    return render(request, 'safe/safeholder.html', {})


@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('safe:index'))


def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        attribute_form = UserAttributeForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and attribute_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            attributes = attribute_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserAttributeForm
            attributes.user = user

            # # Check if they provided a profile picture
            # if 'profile_pic' in request.FILES:
            #     print('found it')
            #     # If yes, then grab it from the POST form reply
            #     profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            attributes.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,attribute_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        attribute_form = UserAttributeForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'safe/registration.html',
                          {'user_form':user_form,
                           'attribute_form':attribute_form,
                           'registered':registered})


def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                return HttpResponseRedirect(reverse('safe:index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'safe/login.html', {})


@method_decorator(login_required, name='dispatch')
class SafeListView(ListView):
    context_object_name = 'safe_list'
    model = models.Safe
    template_name = 'safe/safeholder.html'
    #queryset = Safe.objects.filter(safeholder=request.user)

    def get_queryset(self):
        return Safe.objects.filter(safeholder=self.request.user)


@method_decorator(login_required, name='dispatch')
class SafeSHDetailView(DetailView):
    context_object_name = 'safe'
    model = models.Safe
    template_name = 'safe/safe_sh_detail.html'

    # def get_context_data(self, **kwargs):
    #     # Add details from related models
    #     context = super(SafeDetailView, self).get_context_data(**kwargs)
    #     sh_displayname = self.request.user.userattributes.displayname
    #     context['sh_displayname'] = sh_displayname
    #     # Get KH attribute data
    #     kh =
    #     kh = models.Relationship.objects.get(safeholder=self.request.user.pk)
    #     kh_user = models.User.objects.get(username=kh.keyholder)
    #     kh_displayname = kh_user.userattributes.displayname
    #     context['kh_displayname'] = kh_displayname
    #     # Get KH message
    #     context['kh_message'] = kh.keyholder_msg
    #     context['kh_message_timestamp'] = kh.keyholder_msg_timestamp
    #     return context


@method_decorator(login_required, name='dispatch')
class SHListView(ListView):
    context_object_name = 'safe_list'
    model = models.Safe
    template_name = 'safe/keyholder.html'

    def get_queryset(self):
        return Safe.objects.filter(keyholder=self.request.user)


@method_decorator(login_required, name='dispatch')
class SH_ClaimSafeView(ListView):
    context_object_name = 'safe_list'
    model = models.Safe
    template_name = 'safe/sh_claim_safe.html'

    def get_queryset(self):
        return Safe.objects.filter(safeholder=None)


@method_decorator(login_required, name='dispatch')
class KH_ClaimSafeView(ListView):
    context_object_name = 'safe_list'
    model = models.Safe
    template_name = 'safe/kh_claim_safe.html'

    def get_queryset(self):
        return Safe.objects.filter(keyholder=None).exclude(safeholder=None)

@method_decorator(login_required, name='dispatch')
class SH_SafeUpdateView(UpdateView):
    fields = ('safeholder_msg',)
    model = models.Safe
    template_name = 'safe/sh_update_form.html'


    def form_valid(self, form):
        form.instance.safeholder_msg_timestamp = timezone.now()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SafeKHDetailView(DetailView):
    context_object_name = 'safe'
    model = models.Safe
    template_name = 'safe/safe_kh_detail.html'

    # Get recent Safe events and add to context object
    def get_context_data(self, **kwargs):
        # Add details from Safe Event model
        context = super(SafeKHDetailView, self).get_context_data(**kwargs)
        safe_events = list(Safe_Event.objects.filter(safe=context['safe'].hardware_id).order_by(
            '-timestamp'))
        context['events'] = safe_events[:20]
        return context



@method_decorator(login_required, name='dispatch')
class KH_SafeUpdateView(UpdateView):
    #fields = ('auth_to_unlock', 'unlock_time', 'scanfreq', 'reportfreq', 'proximityunit',
    #          'displayproximity', 'keyholder_msg',)
    model = models.Safe
    form_class = SafeUpdateForm
    template_name = 'safe/kh_update_form.html'

    def get_success_url(self, **kwargs):
        """
        Override the default success_url (which is intended for safeholder views, not keyholder
        """
        return '/safe/keyholder/' + self.kwargs['pk']

    def form_valid(self, form):
        form.instance.keyholder_msg_timestamp = timezone.now()
        return super().form_valid(form)

@login_required
def kh_confirm_safe(request, pk):
    print(request.user, pk)
    safe = Safe.objects.get(hardware_id=pk)
    safe.keyholder = request.user
    safe.save()
    return render(request, 'safe/kh_confirm.html')


@login_required
def sh_confirm_safe(request, pk):
    print(request.user, pk)
    safe = Safe.objects.get(hardware_id=pk)
    safe.safeholder = request.user
    safe.save()
    return render(request, 'safe/sh_confirm.html')


@method_decorator(login_required, name='dispatch')
class SafeKHReleaseView(DetailView):
    context_object_name = 'safe'
    model = models.Safe
    template_name = 'safe/safe_kh_release.html'

    # Use this methid to execute the release of the safeholder
    def get_context_data(self, **kwargs):
        data = super(SafeKHReleaseView, self).get_context_data(**kwargs)
        self.object.keyholder = None
        self.object.keyholder_msg = 'Your Keyholder has released you. You safe is now unlocked.'
        self.object.keyholder_msg_timestamp = timezone.now()
        self.object.auth_to_unlock = True
        self.object.unlock_time = timezone.now()
        self.object.save()
        return data



