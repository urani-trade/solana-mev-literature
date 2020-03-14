import json
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from .views import index, submit_implementation_view, graph_view
from .models import Algorithm, QubitType, QubitSubtype, QuantumComputer, NISQImplementation
from .forms import ImplementationCreateForm
from .utils import (
    count_nisq_implementations,
    get_year_span,
    is_valid_queryparam,
    count_computers,
    count_algorithms,
    count_qubit_types,
    count_qubit_subtypes,
    get_imp_per_year,
    get_qubits_per_year,
    get_max_qubits_per_year,
    get_qubits_per_imp,
    get_computer_tuples,
    get_algorithm_tuples,
    get_qubit_type_tuples,
    get_qubit_subtype_tuples
)

# Create your tests here.

User = get_user_model()

# Testing url patterns
class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)

    def test_submit_implementation_view_resolves(self):
        url = reverse('submit')
        self.assertEquals(resolve(url).func, submit_implementation_view)

    def test_graph_view_resolves(self):
        url = reverse('graphs')
        self.assertEquals(resolve(url).func, graph_view)

# Testing views
class TestViews(TestCase):
    # Adding test database
    fixtures = ['test_db.json']

    # Tests for index view
    def test_index_GET(self):
        client = Client()
        response = client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_description_contains_search(self):
        client = Client()
        response = client.get(reverse('index'), data={'description_contains': 'implementations'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_ref_url_exact_search(self):
        client = Client()
        response = client.get(reverse('index'), data={'ref_url_exact': 'https://arxiv.org/abs/quant-ph/9709001'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_qubit_min_count_search(self):
        client = Client()
        response = client.get(reverse('index'), data={'qubit_min_count': 4})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_qubit_max_count_search(self):
        client = Client()
        response = client.get(reverse('index'), data={'qubit_max_count': 10})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_min_year_search(self):
        client = Client()
        response = client.get(reverse('index'), data={'min_year': 2000})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_max_year_search(self):
        client = Client()
        response = client.get(reverse('index'), data={'min_year': 2015})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_algorithms_search(self):
        client = Client()
        response = client.get(reverse('index'), data={'algorithms': ['BV', 'HS']})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_computers_search(self):
        client = Client()
        response = client.get(reverse('index'), data={'computers': ['Rigetti 19Q-Acorn', 'IBMQX5']})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_qubit_types_search(self):
        client = Client()
        response = client.get(reverse('index'), data={'qubit_types': ['atom', 'Photon']})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_qubit_subtypes_search(self):
        client = Client()
        response = client.get(reverse('index'), data={'qubit_subtypes': ['9Be+']})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    # Tests for graph_view
    def test_graphs_GET(self):
        client = Client()
        response = client.get(reverse('graphs'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'implementations/graphs.html')

    def test_graphs_max_num_qubits_filter(self):
        data = {
            'graph_type': 'line',
            'data_set': 'max_number_qubits',
            'min_year': 1997,
            'max_year': 2019,
            'min_imp_id': 1,
            'max_imp_id': 109
        }

        client = Client()
        response = client.get(reverse('graphs'), data=data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'implementations/graphs.html')

    def test_graphs_total_num_qubits_filter(self):
        data = {
            'graph_type': 'bar',
            'data_set': 'total_number_qubits',
            'min_year': 1997,
            'max_year': 2019,
            'min_imp_id': 1,
            'max_imp_id': 109
        }

        client = Client()
        response = client.get(reverse('graphs'), data=data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'implementations/graphs.html')

    def test_graphs_imp_per_year_filter(self):
        data = {
            'graph_type': 'doughnut',
            'data_set': 'imp_per_year',
            'min_year': 1997,
            'max_year': 2019,
            'min_imp_id': 1,
            'max_imp_id': 109
        }

        client = Client()
        response = client.get(reverse('graphs'), data=data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'implementations/graphs.html')

    def test_graphs_qubits_per_implementation_filter(self):
        data = {
            'graph_type': 'pie',
            'data_set': 'qubits_per_implementation',
            'min_year': 1997,
            'max_year': 2019,
            'min_imp_id': 1,
            'max_imp_id': 109
        }

        client = Client()
        response = client.get(reverse('graphs'), data=data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'implementations/graphs.html')

    def test_graphs_implementations_per_computer_filter(self):
        data = {
            'graph_type': 'polarArea',
            'data_set': 'implementations_per_computer',
            'min_year': 1997,
            'max_year': 2019,
            'min_imp_id': 1,
            'max_imp_id': 109
        }

        client = Client()
        response = client.get(reverse('graphs'), data=data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'implementations/graphs.html')

    def test_graphs_implementations_per_algorithm_filter(self):
        data = {
            'graph_type': 'bar',
            'data_set': 'implementations_per_algorithm',
            'min_year': 1997,
            'max_year': 2019,
            'min_imp_id': 1,
            'max_imp_id': 109
        }

        client = Client()
        response = client.get(reverse('graphs'), data=data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'implementations/graphs.html')

    def test_graphs_implementations_per_qubit_type_filter(self):
        data = {
            'graph_type': 'bar',
            'data_set': 'implementations_per_qubit_type',
            'min_year': 1997,
            'max_year': 2019,
            'min_imp_id': 1,
            'max_imp_id': 109
        }

        client = Client()
        response = client.get(reverse('graphs'), data=data)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'implementations/graphs.html')

    # Tests for submit_implementation_view
    def test_submit_implementation_unauthenticated_GET(self):
        client = Client()
        response = client.get(reverse('submit'))
        self.assertEquals(response.status_code, 302)

    def test_submit_implementation_authenticated_GET(self):
        client = Client()
        user = User.objects.create_user('newuser',
                                        'newuser@example.com',
                                        'testing321')
        client.login(username='newuser', password='testing321')
        response = client.get(reverse('submit'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'implementations/submit_implementation.html')

    def test_submit_implementation_POST(self):
        client = Client()
        user = User.objects.create_user('newuser',
                                        'newuser@example.com',
                                        'testing321')
        client.login(username='newuser', password='testing321')

        data = {
            'month': 'Jan',
            'year_int': 2000,
            'reference_url': 'https://arxiv.org/abs/quant-ph/9709001',
            'qubit_number': 4,
            'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sunt, sapiente.',
            'computer': [
                'Rigetti 19Q-Acorn',
                'IBMQX1'
            ],
            'algorithm': [
                'HS',
                'SVM'
            ],
            'qubit_type': [
                'NMR',
                'atom'
            ],
            'qubit_subtype': [
                '9Be+',
                '40Ca+'
            ],
            'new_computer': 'IMBX5000',
            'new_algorithm': 'Shxor',
            'new_qubit_type': 'ETC',
            'new_qubit_subtype': '6NaCl-'
        }

        response = client.post(reverse('submit'), data=data, follow=True)
        messages = list(response.context['messages'])

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'NISQ Implementation successfully added and is pending administrator approval')

# Testing forms
class TestForms(TestCase):

    def test_submit_form(self):
        # valid form data
        form_data = {
            'month': 'Jan',
            'year_int': 2000,
            'reference_url': 'https://arxiv.org/abs/quant-ph/9709001',
            'qubit_number': 4,
            'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sunt, sapiente.',
            'computer': [
                'Rigetti 19Q-Acorn',
                'IBMQX1'
            ],
            'algorithm': [
                'HS',
                'SVM'
            ],
            'qubit_type': [
                'NMR',
                'atom'
            ],
            'qubit_subtype': [
                '9Be+',
                '40Ca+'
            ]
        }

        # invalid data for form
        no_description = {
            'month': 'Jan',
            'year_int': 2000,
            'reference_url': 'https://arxiv.org/abs/quant-ph/9709001',
            'qubit_number': 4,
            'computer': [
                'Rigetti 19Q-Acorn',
                'IBMQX1'
            ],
            'algorithm': [
                'HS',
                'SVM'
            ],
            'qubit_type': [
                'NMR',
                'atom'
            ],
            'qubit_subtype': [
                '9Be+',
                '40Ca+'
            ]
        }

        # invalid data for form
        no_month = {
            'year_int': 2000,
            'reference_url': 'https://arxiv.org/abs/quant-ph/9709001',
            'qubit_number': 4,
            'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sunt, sapiente.',
            'computer': [
                'Rigetti 19Q-Acorn',
                'IBMQX1'
            ],
            'algorithm': [
                'HS',
                'SVM'
            ],
            'qubit_type': [
                'NMR',
                'atom'
            ],
            'qubit_subtype': [
                '9Be+',
                '40Ca+'
            ]
        }

        # invalid data for form
        no_year = {
            'month': 'Jan',
            'reference_url': 'https://arxiv.org/abs/quant-ph/9709001',
            'qubit_number': 4,
            'description': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sunt, sapiente.',
            'computer': [
                'Rigetti 19Q-Acorn',
                'IBMQX1'
            ],
            'algorithm': [
                'HS',
                'SVM'
            ],
            'qubit_type': [
                'NMR',
                'atom'
            ],
            'qubit_subtype': [
                '9Be+',
                '40Ca+'
            ]
        }

        form = ImplementationCreateForm(data=form_data)
        no_descrip_form = ImplementationCreateForm(data=no_description)
        no_month_form = ImplementationCreateForm(data=no_month)
        no_year_form = ImplementationCreateForm(data=no_year)


        self.assertTrue(form.is_valid())
        self.assertFalse(no_descrip_form.is_valid())
        self.assertFalse(no_month_form.is_valid())
        self.assertFalse(no_year_form.is_valid())


class TestUtils(TestCase):
    # Adding test database
    fixtures = ['test_db.json']

    # I'm pretty sure these tests are pointless.
    # Since they make database calls dynamically, the test and function are identical.
    def test_count_nisq_implementations(self):
        count = NISQImplementation.objects.filter(approved=True).count()
        self.assertEqual(count_nisq_implementations(), count)

    def test_get_year_span(self):
        qs = NISQImplementation.objects.all()
        qs = qs.filter(approved=True)
        years = [implementation.year_int for implementation in qs]
        years = set(years)
        year_span = (min(years), max(years))
        self.assertEqual(get_year_span(), year_span)

    def test_is_valid_queryparam(self):
        param = 'param'
        null_param = None
        empty_param = ''
        self.assertEqual(is_valid_queryparam(param), True)
        self.assertEqual(is_valid_queryparam(null_param), False)
        self.assertEqual(is_valid_queryparam(empty_param), False)

    def test_count_computers(self):
        computer_list = QuantumComputer.objects.all()
        qs = NISQImplementation.objects.filter(approved=True)

        comp_dict = {}
        for computer in computer_list:
            comp_dict[computer.computer_type] = {"count": 0}

        for item in qs:
           for computer in item.computer.all():
               comp_dict[computer.computer_type]['count'] += 1

        result = json.dumps(comp_dict)

        self.assertEqual(count_computers(), result)

    def test_count_algorithms(self):
        algorithm_list = Algorithm.objects.all()
        qs = NISQImplementation.objects.filter(approved=True)

        alg_dict = {}
        for alg in algorithm_list:
            alg_dict[alg.type] = {"count": 0}

        for item in qs:
           for alg in item.algorithm.all():
               alg_dict[alg.type]['count'] += 1

        result = json.dumps(alg_dict)
        self.assertEqual(count_algorithms(), result)

    def test_count_qubit_types(self):
        type_list = QubitType.objects.all()
        qs = NISQImplementation.objects.filter(approved=True)

        type_dict = {}
        for type in type_list:
            type_dict[type.type] = {"count": 0}

        for item in qs:
           for type in item.qubit_type.all():
               type_dict[type.type]['count'] += 1

        result = json.dumps(type_dict)

        self.assertEqual(count_qubit_types(), result)

    def test_count_qubit_subtypes(self):
        subtype_list = QubitSubtype.objects.all()
        qs = NISQImplementation.objects.filter(approved=True)

        subtype_dict = {}
        for subtype in subtype_list:
            subtype_dict[subtype.type] = {"count": 0}

        for item in qs:
           for subtype in item.qubit_subtype.all():
               subtype_dict[subtype.type]['count'] += 1

        result = json.dumps(subtype_dict)

        self.assertEqual(count_qubit_subtypes(), result)

    def test_get_imp_per_year(self):
        min_year = 2000
        max_year = 2015

        qs = NISQImplementation.objects.filter(year_int__range=(min_year, max_year))

        qs = qs.filter(approved=True)

        year_dict = dict()
        for imp in qs:
            year_dict[imp.year_int] = {'count': 0}

        for imp in qs:
            year_dict[imp.year_int]['count'] += 1

        result = json.dumps(year_dict)

        self.assertEqual(get_imp_per_year(min_year=2000, max_year=2015), result)

    def test_get_qubits_per_year(self):
        min_year = 2000
        max_year = 2015

        qs = NISQImplementation.objects.filter(year_int__range=(min_year, max_year))

        qs = qs.filter(approved=True)

        year_dict = dict()
        for imp in qs:
            year_dict[imp.year_int] = {'count': 0}

        for imp in qs:
            year_dict[imp.year_int]['count'] += 1

        result = json.dumps(year_dict)

        self.assertEqual(get_imp_per_year(min_year=2000, max_year=2015), result)

    def test_get_max_qubits_per_year(self):
        min_year = 2000
        max_year = 2015

        qs = NISQImplementation.objects.filter(year_int__range=(min_year, max_year))

        qs = qs.filter(approved=True)

        year_dict = dict()
        for imp in qs:
            year_dict[imp.year_int] = {'count': 0}

        for imp in qs:
            if imp.qubit_number is not None:
                if imp.qubit_number > year_dict[imp.year_int]['count']:
                    year_dict[imp.year_int]['count'] = imp.qubit_number

        result = json.dumps(year_dict)

        self.assertEqual(get_max_qubits_per_year(min_year=2000, max_year=2015), result)

    def test_get_qubits_per_imp(self):
        min_id = 10
        max_id = 60
        qs = NISQImplementation.objects.filter(id__range=(min_id, max_id))

        qs = qs.filter(approved=True)

        qubit_dict = dict()
        for imp in qs:
            if imp.qubit_number is not None:
                qubit_dict[f'({imp.id}) {imp.month} {imp.year_int}'] = {'count': imp.qubit_number }

        result = json.dumps(qubit_dict)

        self.assertEqual(get_qubits_per_imp(min_id=10, max_id=60), result)

    def test_get_computer_tuples(self):
        computers = set()
        qs = QuantumComputer.objects.all()
        for computer in qs:
            computers.add((computer.computer_type, computer.computer_type))

        computers = list(computers)
        result = computers

        self.assertEqual(get_computer_tuples(), result)

    def test_get_algorithm_tuples(self):
        algorithms = set()
        qs = Algorithm.objects.all()
        for alg in qs:
            algorithms.add((alg.type, alg.type))

        algorithms = list(algorithms)
        result = algorithms

        self.assertEqual(get_algorithm_tuples(), result)

    def test_get_qubit_type_tuples(self):
        qubit_types = set()
        qs = QubitType.objects.all()
        for type in qs:
            qubit_types.add((type.type, type.type))

        qubit_types = list(qubit_types)
        result = qubit_types

        self.assertEqual(get_qubit_type_tuples(), result)

    def test_get_qubit_subtype_tuples(self):
        qubit_subtypes = set()
        qs = QubitSubtype.objects.all()
        for subtype in qs:
            qubit_subtypes.add((subtype.type, subtype.type))

        qubit_subtypes = list(qubit_subtypes)

        result = qubit_subtypes

        self.assertEqual(get_qubit_subtype_tuples(), result)
