"""
Various utility functions for filtering, counting querysets,
and formatting querysets as tuples
"""

import json

from main.utils import send_email
from main.settings import ADMIN_EMAIL
from .models import NISQImplementation, Algorithm, QuantumComputer, QubitType, QubitSubtype

# Utility functions for implementations.views
def count_nisq_implementations():
    return NISQImplementation.objects.filter(approved=True).count()


def get_year_span():
    """
    Retrieve years range from implementation data.
    """
    qs = NISQImplementation.objects.all()
    qs = qs.filter(approved=True)
    years = [implementation.year_int for implementation in qs]
    years = set(years)
    try:
        return min(years), max(years)
    except AttributeError as e:
        print(f'Could not access year span: {e}')

# helper function to check if query string is empty or none.
def is_valid_queryparam(param):
    return param != "" and param is not None


def count_computers():
    """
    Counts unique instances of computer type.
    Returns JSON formatted string
    """

    computer_list = QuantumComputer.objects.all()
    qs = NISQImplementation.objects.filter(approved=True)

    comp_dict = {}
    for computer in computer_list:
        comp_dict[computer.computer_type] = {"count": 0}

    for item in qs:
       for computer in item.computer.all():
           comp_dict[computer.computer_type]['count'] += 1

    return json.dumps(comp_dict)


def count_algorithms():
    """
    Counts unique instances of algorithm type.
    Returns JSON formatted string
    """

    algorithm_list = Algorithm.objects.all()
    qs = NISQImplementation.objects.filter(approved=True)

    alg_dict = {}
    for alg in algorithm_list:
        alg_dict[alg.type] = {"count": 0}

    for item in qs:
       for alg in item.algorithm.all():
           alg_dict[alg.type]['count'] += 1

    return json.dumps(alg_dict)


def count_qubit_types():
    """
    Counts unique instances of qubit type.
    Returns JSON formatted string
    """

    type_list = QubitType.objects.all()
    qs = NISQImplementation.objects.filter(approved=True)

    type_dict = {}
    for type in type_list:
        type_dict[type.type] = {"count": 0}

    for item in qs:
       for type in item.qubit_type.all():
           type_dict[type.type]['count'] += 1

    return json.dumps(type_dict)


def count_qubit_subtypes():
    """
    Counts unique instances of qubit subtype.
    Returns JSON formatted string
    """

    subtype_list = QubitSubtype.objects.all()
    qs = NISQImplementation.objects.filter(approved=True)

    subtype_dict = {}
    for subtype in subtype_list:
        subtype_dict[subtype.type] = {"count": 0}

    for item in qs:
       for subtype in item.qubit_subtype.all():
           subtype_dict[subtype.type]['count'] += 1

    return json.dumps(subtype_dict)


def get_imp_per_year(min_year=None, max_year=None):
    """
    Counts number of NISQ implemenations per year.
    Year range defaults to the total year range.
    Returns JSON formatted string
    """
    try:
        min_year = min_year or get_year_span()[0]
        max_year = max_year or get_year_span()[1]
    except KeyError as e:
        print(f'Could not access year span: {e}')

    qs = NISQImplementation.objects.filter(year_int__range=(min_year, max_year))

    qs = qs.filter(approved=True)

    year_dict = dict()
    for imp in qs:
        year_dict[imp.year_int] = {'count': 0}

    for imp in qs:
        year_dict[imp.year_int]['count'] += 1

    return json.dumps(year_dict)


def get_qubits_per_year(min_year=None, max_year=None):
    """
    Counts total number of qubits across all instances per year.
    Year range defaults to the total year range.
    Returns JSON formatted string
    """
    try:
        min_year = min_year or get_year_span()[0]
        max_year = max_year or get_year_span()[1]
    except KeyError as e:
        print(f'Could not access year span: {e}')

    qs = NISQImplementation.objects.filter(year_int__range=(min_year, max_year))

    qs = qs.filter(approved=True)

    year_dict = dict()
    for imp in qs:
        year_dict[imp.year_int] = {'count': 0}

    for imp in qs:
        if imp.qubit_number is not None:
            year_dict[imp.year_int]['count'] += imp.qubit_number

    return json.dumps(year_dict)


def get_max_qubits_per_year(min_year=None, max_year=None):
    """
    Locates the maximum number of qubits per year.
    Year range defaults to the total year range.
    Returns JSON formatted string
    """
    try:
        min_year = min_year or get_year_span()[0]
        max_year = max_year or get_year_span()[1]
    except KeyError as e:
        print(f'Could not access year span: {e}')

    qs = NISQImplementation.objects.filter(year_int__range=(min_year, max_year))

    qs = qs.filter(approved=True)

    year_dict = dict()
    for imp in qs:
        year_dict[imp.year_int] = {'count': 0}

    for imp in qs:
        if imp.qubit_number is not None:
            if imp.qubit_number > year_dict[imp.year_int]['count']:
                year_dict[imp.year_int]['count'] = imp.qubit_number

    return json.dumps(year_dict)


def get_qubits_per_imp(min_id=1, max_id=count_nisq_implementations()):
    """
    Counts qubits per implementation.
    Implementation range defaults to the total implementation range.
    Returns JSON formatted string
    """

    qs = NISQImplementation.objects.filter(id__range=(min_id, max_id))

    qs = qs.filter(approved=True)

    qubit_dict = dict()
    for imp in qs:
        if imp.qubit_number is not None:
            qubit_dict[f'({imp.id}) {imp.month} {imp.year_int}'] = {'count': imp.qubit_number }

    return json.dumps(qubit_dict)


# Utility functions for implementations.forms
def get_computer_tuples():
    """
    Returns name, value tuples for computer MultipleSelect
    widget option.
    """
    computers = set()
    qs = QuantumComputer.objects.all()
    for computer in qs:
        computers.add((computer.computer_type, computer.computer_type))

    computers = list(computers)

    return computers


def get_algorithm_tuples():
    """
    Returns name, value tuples for algorithm MultipleSelect
    widget option.
    """
    algorithms = set()
    qs = Algorithm.objects.all()
    for alg in qs:
        algorithms.add((alg.type, alg.type))

    algorithms = list(algorithms)
    return algorithms


def get_qubit_type_tuples():
    """
    Returns name, value tuples for qubit type MultipleSelect
    widget option.
    """
    qubit_types = set()
    qs = QubitType.objects.all()
    for type in qs:
        qubit_types.add((type.type, type.type))

    qubit_types = list(qubit_types)
    return qubit_types


def get_qubit_subtype_tuples():
    """
    Returns name, value tuples for qubit subtype MultipleSelect
    widget option.
    """
    qubit_subtypes = set()
    qs = QubitSubtype.objects.all()
    for subtype in qs:
        qubit_subtypes.add((subtype.type, subtype.type))

    qubit_subtypes = list(qubit_subtypes)

    return qubit_subtypes


def send_email_admin():
    """
    Sends an email to admin whenever someone submits a
    new implementation.
    """
    message = "There is a new paper submission waiting to be approved."
    send_email(message, ADMIN_EMAIL, message)
