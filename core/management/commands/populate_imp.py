""" A one time command to populate NISQImplementation model with existing data."""

import django

from main.utils import load_json

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from implementations.models import NISQImplementation, QuantumComputer, QubitType, QubitSubtype, Algorithm

admin = User.objects.filter(username="admin").first()

class Command(BaseCommand):

    help = """One time command to add data from cleaned_data.json to db.sqlite3; 

              Usage: make populate_imp
           """

    def __init__(self):
        self.data = None

    def add_arguments(self, parser):
        parser.add_argument('data_file', 
                            type=str, 
                            help='JSON data file to convert to SQL.')
    
    def handle(self, *args, **kwargs):
        '''
            Get a data JSON file as argument, parse it, and add 
            the info to the database.
        '''
        # Load data.
        print('[*] Starting populate_imp script...')
        data_file = kwargs.get('data_file')
        self.data = load_json(data_file)
    
        # Handle each implementation in the data.
        for implementation in self.data:
            self._handle_implementation(implementation)

    def _handle_implementation(self, implementation):
        '''
            Handles data in each implementation.
        '''
        new_implementation = NISQImplementation()
        new_implementation.submitted_by = admin
        new_implementation.approved = True

        try:
            new_implementation.year_int = implementation['year']
            new_implementation.month = implementation['month']
            new_implementation.description = implementation['description']
            if implementation['reference_url'] is not None:
                new_implementation.reference_url = implementation['reference_url']
            if implementation['num_qubits'] is not None:
                new_implementation.qubit_number = implementation['num_qubits']
            
        except KeyError as e:
            print(f'Could not access implementation data: {e}')

        try:
            new_implementation.save()
        except django.db.utils.IntegrityError as e:
            print(f'Could not save new implementation: {e}')

        if implementation['qubit_type'] is not None:
            if isinstance(implementation['qubit_type'], list):
                qubit_type = QubitType.objects.filter(type__in=implementation['qubit_type'])
            else:
                qubit_type = QubitType.objects.filter(type=implementation['qubit_type'])
            try:
                new_implementation.qubit_type.set(qubit_type)
            except ValueError as e:
                print(f'Could not update qubit set: {e}')

        if implementation['computer'] is not None:
            if isinstance(implementation['computer'], list):
                computer_type = QuantumComputer.objects.filter(computer_type__in=implementation['computer'])
            else:
                computer_type = QuantumComputer.objects.filter(computer_type=implementation['computer'])
            try:
                new_implementation.computer.set(computer_type)
            except ValueError as e:
                print(f'Could not update computer type: {e}')

        if implementation['qubit_subtype'] is not None:
            if isinstance(implementation['computer'], list):
                qubit_subtype = QubitSubtype.objects.filter(type__in=implementation['qubit_subtype'])
            else:
                qubit_subtype = QubitSubtype.objects.filter(type=implementation['qubit_subtype'])
            try:
                new_implementation.qubit_subtype.set(qubit_subtype)
            except ValueError as e:
                print(f'Could not update qubit subtype: {e}')

        if implementation['algorithm'] is not None:
            if isinstance(implementation['algorithm'], list):
                alg_type = Algorithm.objects.filter(type__in=implementation['algorithm'])
            else:
                alg_type = Algorithm.objects.filter(type=implementation['algorithm'])
            try:
                new_implementation.algorithm.set(alg_type)
            except ValueError as e:
                print(f'Could not update algorithm type: {e}')
