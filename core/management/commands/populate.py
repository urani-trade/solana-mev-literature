"""
One-time command for populating the ManyToManyFields on the NISQImplementation 
model; i.e., Algorithm, QuantumComputer, QubitSubtype, and QubitType.
"""

from main.utils import load_json

from django.core.management.base import BaseCommand
from implementations.models import Algorithm, QuantumComputer, QubitType, QubitSubtype

class Command(BaseCommand):
    help = """Populates Django database with QuantumComputer, QubitType, 
              QubitSubtype, and Algorithm fields after preparing them 
              for migration.
              
              Usage: make populate
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
        print('[*] Starting populate script...')
        data_file = kwargs.get('data_file')
        self.data = load_json(data_file)

        # Declare variables.
        algorithms = set()
        qubit_types = set()
        qubit_subtypes = set()
        computers = set()
        
        # Handle the data
        for obj in self.data:
            algorithms.update(self._handle_algorithm(obj))
            qt, qst = self._handle_qubit_type(obj)
            qubit_types.update(qt)
            qubit_subtypes.update(qst)
            computers.update(self._handle_computer(obj))
        
        computers_cleaned_and = self._get_computers_cleaned(computers)

        # Print results
        print(f'[*] Populated algorithms: {algorithms}')
        print(f'[*] Populated computers: {computers_cleaned_and}')
        print(f'[*] Populated Qubit Type: {qubit_types}')
        print(f'[*] Populated Qubit subtypes: {qubit_subtypes}')

        # Create model objects.
        try:
            for algorithm in algorithms:
                Algorithm.objects.create(type=algorithm)

            for computer in computers_cleaned_and:
                QuantumComputer.objects.create(computer_type=computer)

            for subtype in qubit_subtypes:
                QubitSubtype.objects.create(type=subtype)

            for qubit in qubit_types:
                QubitType.objects.create(type=qubit)
        except Exception as e:
            print(f'Could not populate data: {e}')
            return

        print(f'[*] Data imported successfully')

    def _handle_algorithm(self, obj):
        '''
            Handle Algorithm model data.
        '''
        algorithms = set()

        # TODO: Define AlgorithmMissingTypes = ("----", "", "??", etc.)
        if obj['Algorithm'] in ('----', ''):
            obj['Algorithm'] = None

        # TODO: Handle different cases, e.g. splitting on "&" or ","
        if obj['Algorithm'] is not None:
            obj['Algorithm'] = obj['Algorithm'].split("/")

            for algorithm in obj['Algorithm']:
                algorithms.add(algorithm)
        
        return algorithms

    def _handle_qubit_type(self, obj):
        '''
            Handle qubit type.
        '''
        qubit_type = set()
        qubit_subtypes = set()

        obj['Qubit type'] = obj['Qubit type'].split('/')

        if obj['Qubit type'] is not None:
            for type in obj['Qubit type']:
                if "(" in type:
                        subtype_list = type.split(" (")
                        for subtype in subtype_list:
                            if ")" in subtype:
                                subtype = subtype.replace('(', '').replace(')', '')
                                qubit_subtypes.add(subtype)
                            else:
                                qubit_type.add(subtype)
                else:
                    qubit_type.add(type)

        return qubit_type, qubit_subtypes 
    
    def _handle_computer(self, obj):
        '''
            Handle Computer names.
        '''
        computers = set()

        if obj['Computer'] == '----' or obj['Computer'] == '' or obj['Computer'] == '??':
            obj['Computer'] = None

        if isinstance(obj['Computer'], str):
            if ", " in obj['Computer']:
                obj['Computer'] = obj['Computer'].split(', ')

                if len(obj['Computer']) > 1:
                    if obj['Computer'][1] == "----":
                        del obj['Computer'][1]

            elif "/" in obj['Computer']:
                obj['Computer'] = obj['Computer'].split('/')

                for comp in obj['Computer']:
                    if isinstance(comp, list) and len(obj['Computer']) > 1:
                        if obj['Computer'][1] == "----":
                            del obj['Computer'][1]

        if isinstance(obj['Computer'], list):
            for computer in obj['Computer']:
                if computer == '----' or computer == '??':
                    pass
                else:
                    computers.add(computer)
        else:
            computers.add(obj['Computer'])
        
        return computers

    def _get_computers_cleaned(self, computers):
        '''
            Handles computer names list.
        '''
        computers_cleaned_slash = set()
        computers_cleaned_and = set()

        for computer in computers:
            if computer is not None:
                computer_list = computer.split("/")
                for comp in computer_list:
                    if comp == 'IBM 20Q':
                        comp = 'IBMQ20'
                        computers_cleaned_slash.add(comp)
                    if comp != '19Q-Acorn' and comp != '5' and comp != '2':
                        computers_cleaned_slash.add(comp)
        
        for computer in computers_cleaned_slash:
            computer_list = computer.split(" & ")
            for comp in computer_list:
                if comp == 'IBMQX2(4)':
                    computers_cleaned_and.add('IBMQX2')
                    computers_cleaned_and.add('IBMQX4')
                else:
                    computers_cleaned_and.add(comp)
        
        return computers_cleaned_and

