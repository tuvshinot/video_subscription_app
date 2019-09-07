from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic import ListView
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

from .models import Membership, UserMemberShip, Subscription


def get_user_membership(request):
    """ Method getting user membership """
    user_membership_qs = UserMemberShip.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None


def get_user_subscription(request):
    """ Method getting user subscription """
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None


def get_selected_membership(request):
    """ Get selected membership type from session """
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(
        membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


class MembershipSelectView(ListView):
    """ Select membership view """
    model = Membership

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context

    def post(self, request, **kwargs):
        selected_membership_type = request.POST.get('membership_type')

        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)

        selected_membership_qs = Membership.objects.filter(
            membership_type=selected_membership_type)

        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()

        # VALIDATION
        if user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(request, 'You already have this membership. Your \
                        next payment is due')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # assign membership type to session
        request.session['selected_membership_type'] = selected_membership.membership_type

        return HttpResponseRedirect(reverse('memberships:payment'))


def PaymentView(request):
    """ View for stripe payment """
    user_membership = get_user_membership(request)

    try:
        selected_membership = get_selected_membership(request)
    except:
        return redirect(reverse("memberships:select"))

    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            subscription = stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[
                    {"plan": selected_membership.stripe_plan_id},
                ],
                source=token
            )

            return redirect(reverse('memberships:update-transactions',
                                    kwargs={
                                        'subscription_id': subscription.id
                                    }))
        except:
            messages.info(
                request, "An error has occurred, investigate it in the console")

    context = {
        'publishKey ': publishKey,
        'selected_membership': selected_membership
    }

    return render(request, 'memberships/membership_payment.html', context)


def UpdateTransactions(request, subscription_id):
    """ Update transaction view for updating our side despite stripe"""
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)

    # saving selected membership
    user_membership.membership = selected_membership
    user_membership.save()

    sub, created = Subscription.get_or_create(user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request, 'Succesfully created {} membership'.format(
        selected_membership))
    return redirect(reverse('courses:list'))
