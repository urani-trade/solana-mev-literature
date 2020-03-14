import json
import django

import implementations.forms as forms
import implementations.models as models
import implementations.utils as utils
from .utils import send_email_admin

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    """
    Process index.html page, including the main search.

    Arguments:
        request {<WSGIRequest>}: The request object (GET/POST)

    Returns:
        index.html rendered data.
    """

    computers = models.QuantumComputer.objects.all()
    algorithms = models.Algorithm.objects.all()
    qubit_types = models.QubitType.objects.all()
    qubit_subtypes = models.QubitSubtype.objects.all()

    try:
        min_year = utils.get_year_span()[0]
        max_year = utils.get_year_span()[1]

    except TypeError as e:
        min_year = None
        max_year = None
        print(f'Could not get year span: {e}. Setting data to None.')

    context = {
        'implementations': None,
        'computers': computers,
        'algorithms': algorithms,
        'qubit_types': qubit_types,
        'qubit_subtypes': qubit_subtypes,
        'min_year': min_year,
        'max_year': max_year,
        'current_page': None,
        'is_paginated': None,
        'is_searched': False,
    }

    if 'nisq_search' in request.GET:

        qs = models.NISQImplementation.objects.order_by('-id')
        qs_count = qs.count()

        description_contains_query = request.GET.get('description_contains')
        ref_url_exact_query = request.GET.get('ref_url_exact')
        qubit_min_count_query = request.GET.get('qubit_min_count')
        qubit_max_count_query = request.GET.get('qubit_max_count')
        min_year_query = request.GET.get('min_year')
        max_year_query = request.GET.get('max_year')
        algorithms_query = request.GET.getlist('algorithms')
        computers_query = request.GET.getlist('computers')
        qubit_types_query = request.GET.getlist('qubit_types')
        qubit_subtypes_query = request.GET.getlist('qubit_subtypes')

        try:

            if utils.is_valid_queryparam(description_contains_query):
                qs = qs.filter(description__icontains=description_contains_query).distinct()

            if utils.is_valid_queryparam(ref_url_exact_query):
                qs = qs.filter(reference_url__iexact=ref_url_exact_query)

            if utils.is_valid_queryparam(qubit_min_count_query):
                qs = qs.filter(qubit_number__gte=qubit_min_count_query)

            if utils.is_valid_queryparam(qubit_max_count_query):
                qs = qs.filter(qubit_number__lte=qubit_max_count_query)

            if utils.is_valid_queryparam(min_year_query):
                qs = qs.filter(year_int__gte=min_year_query)

            if utils.is_valid_queryparam(max_year_query):
                qs = qs.filter(year_int__lte=max_year_query)

            if utils.is_valid_queryparam(algorithms_query):
                for alg in algorithms_query:
                    qs = qs.filter(algorithm__type__iexact=alg)

            if utils.is_valid_queryparam(computers_query):
                for comp in computers_query:
                    qs = qs.filter(computer__computer_type__iexact=comp)

            if utils.is_valid_queryparam(qubit_types_query):
                for qtype in qubit_types_query:
                    qs = qs.filter(qubit_type__type__iexact=qtype)

            if utils.is_valid_queryparam(qubit_subtypes_query):
                for subtype in qubit_subtypes_query:
                    qs = qs.filter(qubit_subtype__type__iexact=subtype)
            
        except django.core.exceptions.FieldError as e:
            print(f'Error: {e}')

        # Pagination
        if qs_count == qs.count():
            paginator = Paginator(qs, 14)
            page = request.GET.get('page')
            implementations = paginator.get_page(page)
            is_paginated = True

        else:
            implementations = qs
            page = None
            is_paginated = False

            context = {
                'implementations': implementations,
                'computers': computers,
                'algorithms': algorithms,
                'qubit_types': qubit_types,
                'qubit_subtypes': qubit_subtypes,
                'min_year': min_year,
                'max_year': max_year,
                'current_page': page,
                'is_paginated': is_paginated,
                'is_searched': True,
            }
    
    return render(request, 'index.html', context=context) 


@login_required
def submit_implementation_view(request):
    """
    Process submit_implementation_view.html page, 
    including the main search.

    Arguments:
        request {<WSGIRequest>}: The request object (GET/POST)

    Returns:
        submit_implementation_view.html rendered data.
    """

    form = forms.ImplementationCreateForm(request.POST or None)

    new_comp = None
    new_alg = None
    new_qtype = None
    new_qsubtype = None

    if request.method == 'POST':
    
        if not form.is_valid():
            e = form.errors.as_data()
            messages.error(request, 'Please fix the following error: {}'.format(e))

        else:
            if form.cleaned_data.get('new_computer'):
                nc = form.cleaned_data.get('new_computer')
                new_comp = models.QuantumComputer()
                new_comp.computer_type = nc
                new_comp.save()
            if form.cleaned_data.get('new_algorithm'):
                na = form.cleaned_data.get('new_algorithm')
                new_alg = models.Algorithm(type=na)
                new_alg.save()
            if form.cleaned_data.get('new_qubit_type'):
                nqt = form.cleaned_data.get('new_qubit_type')
                new_qtype = models.QubitType(type=nqt)
                new_qtype.save()
            if form.cleaned_data.get('new_qubit_subtype'):
                nqst = form.cleaned_data.get('new_qubit_subtype')
                new_qsubtype = models.QubitSubtype(type=nqst)
                new_qsubtype.save()

            if form.cleaned_data.get('computer'):
                computers = form.cleaned_data.get('computer')
                if new_comp:
                    computers.append(new_comp.computer_type)
                computers = models.QuantumComputer.objects.filter(computer_type__in=computers)

            if form.cleaned_data.get('algorithm'):
                algorithms = form.cleaned_data.get('algorithm')
                if new_alg:
                    algorithms.append(new_alg.type)
                algorithms = models.Algorithm.objects.filter(type__in=algorithms)

            if form.cleaned_data.get('qubit_type'):
                qtypes = form.cleaned_data.get('qubit_type')
                if new_qtype:
                    qtypes.append(new_qtype.type)
                qtypes = models.QubitType.objects.filter(type__in=qtypes)

            if form.cleaned_data.get('qubit_subtype'):
                qsubtypes = form.cleaned_data.get('qubit_subtype')
                if new_qsubtype:
                    qsubtypes.append(new_qsubtype.type)
                qsubtypes = models.QubitSubtype.objects.filter(type__in=qsubtypes)

            # Save the models.
            new_nisq_imp = models.NISQImplementation()
            new_nisq_imp = form.save(commit=False)
            new_nisq_imp.submitted_by = request.user
            new_nisq_imp.month = form.cleaned_data.get('month')
            new_nisq_imp.year_int = form.cleaned_data.get('year_int')
            new_nisq_imp.description = form.cleaned_data.get('description')
            new_nisq_imp.qubit_number = form.cleaned_data.get('qubit_number')
            new_nisq_imp.reference_url = form.cleaned_data.get('reference_url')

            if request.user.is_superuser:
                new_nisq_imp.approved = True

            new_nisq_imp.save()

            new_nisq_imp.algorithm.set(algorithms)
            new_nisq_imp.computer.set(computers)
            new_nisq_imp.qubit_type.set(qtypes)
            new_nisq_imp.qubit_subtype.set(qsubtypes)

            new_nisq_imp.save()

            # Notify user (onsite) and admin (email)
            messages.success(request, 'NISQ Algorithm successfully added and is pending administrator approval.')
            send_email_admin()

            return redirect(reverse('index'))

    computers = models.QuantumComputer.objects.all()
    algorithms = models.Algorithm.objects.all()
    qubit_types = models.QubitType.objects.all()
    qubit_subtypes = models.QubitSubtype.objects.all()

    context = {
        'computers': computers,
        'algorithms': algorithms,
        'qubit_types': qubit_types,
        'qubit_subtypes': qubit_subtypes,
        'form': form,
    }

    return render(request, 'implementations/submit_implementation.html', context=context)

def graph_view(request):
    """
    Process graph_view.html page, 
    including the main search.

    Arguments:
        request {<WSGIRequest>}: The request object (GET/POST)

    Returns:
        graph_view.html rendered data.
    """
    num_implementations = utils.count_nisq_implementations()
    min_year = utils.get_year_span()[0]
    max_year = utils.get_year_span()[1]

    # Setting graph type and winnowing data set
    graph_type = request.GET.get('graph_type')
    if graph_type is None:
        graph_type = 'bar'

    data_set = request.GET.get('data_set')
    earliest_date = request.GET.get('min_year')
    if earliest_date is not None:
        earliest_date = int(earliest_date)

    latest_date = request.GET.get('max_year')
    if latest_date is not None:
        latest_date = int(latest_date)

    lower_bound = request.GET.get('min_imp_id')
    if lower_bound is not None:
        lower_bound = int(lower_bound)

    upper_bound = request.GET.get('max_imp_id')
    if upper_bound is not None:
        upper_bound = int(upper_bound)

    if data_set == 'implementations_per_computer':
        json = utils.count_computers()
        graph_title = 'Implementations per Computer'
        graph_label = '# of instances'

    elif data_set == 'max_number_qubits':
        json = utils.get_max_qubits_per_year(min_year=earliest_date, max_year=latest_date)
        graph_title = 'Implementation qubit maximum per year'
        graph_label = '# of qubits'
        year_range = None

    elif data_set == 'total_number_qubits':
        json = utils.get_qubits_per_year(min_year=earliest_date, max_year=latest_date)
        graph_title = 'Total qubits per year'
        graph_label = '# of qubits'
        year_range = None

    elif data_set == 'imp_per_year':
        json = utils.get_imp_per_year(min_year=earliest_date, max_year=latest_date)
        graph_title = 'Implementations per year'
        graph_label = '# of implementations'

    elif data_set == 'qubits_per_implementation':
        json = utils.get_qubits_per_imp(min_id=lower_bound, max_id=upper_bound)
        graph_title = 'Qubits per implementaion'
        graph_label = '# of qubits'
    
    elif data_set == 'implementations_per_algorithm':
        json = utils.count_algorithms()
        graph_title = 'Implementations per algorithm'
        graph_label = '# of instances'
    
    elif data_set == 'implementations_per_qubit_type':
        json = utils.count_qubit_types()
        graph_title = 'Implementations per qubit type'
        graph_label = '# of instances'
    else:
        json = utils.get_max_qubits_per_year()
        graph_title = 'Implementation qubit maximum per year'
        graph_label = '# of qubits'

    max_qubits_per_year = utils.get_max_qubits_per_year()

    context = {
        'num_of_implementations': num_implementations,
        'min_year': min_year,
        'max_year': max_year,
        'graph_type': graph_type,
        'graph_title': graph_title,
        'graph_label': graph_label,
        'json': json,
        'max_qubits_per_year': max_qubits_per_year
    }
    return render(request, 'implementations/graphs.html', context)


def about_view(request):
    return render(request, 'implementations/about.html')


def privacy_view(request):
    return render(request, 'implementations/privacy.html')


def terms_view(request):
    return render(request, 'implementations/terms.html')


def cookies_policy_view(request):
    return render(request, 'implementations/cookies-policy.html')
