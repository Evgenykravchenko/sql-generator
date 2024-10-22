from typing import Dict, Callable
import logging
import os
import re
from src.core.services.ddl_parser import DDLParser
from src.core.services.sql_generator import SQLGenerator
from src.core.services.predefined_values import PredefinedValues
from src.core.repositories.value_repository import ValueRepository
from src.core.repositories.faker_value_repository import FakerValueRepository
from src.core.models.table import Table

logger = logging.getLogger(__name__)

class CLI:
    def __init__(self):
        repository_type = os.getenv('REPOSITORY_TYPE', 'FILE').upper()
        if repository_type == 'FAKER':
            repository = FakerValueRepository()
            logger.info("Using FakerValueRepository for generating fake data.")
        else:
            repository = ValueRepository()
            logger.info("Using ValueRepository for predefined data.")

        predefined_values = PredefinedValues(repository)
        self.sql_generator = SQLGenerator(predefined_values)

    def display_field_types(self, field_types: list) -> None:
        """Displays available field types to the user."""
        print("\nAvailable Field Types:")
        for index, field_type in enumerate(field_types, start=1):
            print(f"{index}. {field_type}")

    def get_validated_input(self, prompt: str, validation_func: Callable[[str], bool], error_message: str) -> str:
        """
        Prompts the user for input and validates it using the provided validation function.
        Repeats until valid input is received.
        """
        while True:
            user_input = input(prompt).strip()
            if validation_func(user_input):
                return user_input
            else:
                print(error_message)

    def is_valid_sql_identifier(self, name: str) -> bool:
        """
        Checks if the provided string is a valid SQL identifier.
        Rules:
        - Starts with a letter or underscore.
        - Contains only letters, numbers, and underscores.
        """
        pattern = r'^[A-Za-z_][A-Za-z0-9_]*$'
        return re.match(pattern, name) is not None

    def get_user_choice(self, prompt: str, choices: list) -> str:
        """
        Prompts the user to choose from a list of options.
        """
        while True:
            choice = input(prompt).strip()
            if choice in choices:
                return choice
            else:
                print("Invalid choice. Please try again.")

    def run_manual_mode(self):
        """Manual input mode for creating tables and generating SQL insert queries."""
        print("\n--- Manual Input Mode ---")
        # Validate table name
        table_name = self.get_validated_input(
            "Table name: ",
            self.is_valid_sql_identifier,
            "Invalid table name. It must start with a letter or underscore and contain only letters, numbers, and underscores."
        )

        # Validate number of fields
        num_fields = self.get_validated_input(
            "Number of fields in the table: ",
            lambda x: x.isdigit() and int(x) > 0,
            "Please enter a positive integer."
        )
        num_fields = int(num_fields)

        table = Table(table_name)
        field_types = self.get_available_field_types()

        for i in range(num_fields):
            print(f"\n--- Field {i + 1} ---")
            # Validate field name
            field_name = self.get_validated_input(
                f"Field name {i + 1}: ",
                self.is_valid_sql_identifier,
                "Invalid field name. It must start with a letter or underscore and contain only letters, numbers, and underscores."
            )

            self.display_field_types(field_types)
            # Validate field type choice
            choice = self.get_validated_input(
                "Choose a field type by number: ",
                lambda x: x.isdigit() and 1 <= int(x) <= len(field_types),
                f"Please enter a number between 1 and {len(field_types)}."
            )
            field_type = field_types[int(choice) - 1]
            table.add_column(field_name, field_type)
            logger.debug(f"Added field: {field_name} ({field_type})")

        # Validate number of rows
        num_rows = self.get_validated_input(
            "How many rows do you want to insert? ",
            lambda x: x.isdigit() and int(x) > 0,
            "Please enter a positive integer."
        )
        num_rows = int(num_rows)

        for _ in range(num_rows):
            try:
                query = self.sql_generator.generate_insert_query_manual(table)
                print(query)
            except Exception as e:
                logger.error(f"Error generating query: {e}")
                print("An error occurred while generating the query. Please try again.")

    def run_ddl_mode(self):
        """DDL file processing mode for generating SQL insert queries."""
        print("\n--- DDL File Processing Mode ---")
        ddl_file = self.get_validated_input(
            "Enter the path of the DDL file: ",
            lambda x: os.path.isfile(x),
            "File not found. Please enter a valid path to an existing DDL file."
        )

        try:
            parser = DDLParser(ddl_file)
            tables = parser.read_file()
            sorted_tables = parser.sort_tables_by_dependencies(tables)
            logger.info(f"Found {len(sorted_tables)} tables in the DDL file.")
        except Exception as e:
            logger.error(f"Error parsing DDL file: {e}")
            print("An error occurred while parsing the DDL file. Please check the file and try again.")
            return

        referenced_tables: Dict[str, Table] = {}
        field_types = self.get_available_field_types()

        for table in sorted_tables:
            print(f"\n--- Generating queries for table: {table.name} ---")
            logger.info(f"Generating queries for table: {table.name}")

            for column_name in table.columns.keys():
                # Check if column is a foreign key
                fk = next((fk for fk in table.foreign_keys if fk['column'] == column_name), None)
                if fk:
                    # Automatically set field type based on referenced table
                    referenced_table = referenced_tables.get(fk['referenced_table'])
                    if referenced_table:
                        referenced_column_type = referenced_table.columns.get(fk['referenced_column'])
                        if referenced_column_type:
                            field_type = self.determine_field_type_for_fk(referenced_column_type)
                            table.columns[column_name] = field_type
                            logger.debug(f"Automatically set field type for foreign key '{column_name}': {field_type}")
                            continue
                        else:
                            logger.warning(f"Referenced column '{fk['referenced_column']}' not found in table '{fk['referenced_table']}'.")
                    else:
                        logger.warning(f"Referenced table '{fk['referenced_table']}' not found for foreign key '{column_name}'.")

                # For regular columns
                print(f"\nFor table '{table.name}', column '{column_name}':")
                self.display_field_types(field_types)
                choice = self.get_validated_input(
                    "Choose a field type by number: ",
                    lambda x: x.isdigit() and 1 <= int(x) <= len(field_types),
                    f"Please enter a number between 1 and {len(field_types)}."
                )
                field_type = field_types[int(choice) - 1]
                table.columns[column_name] = field_type
                logger.debug(f"Set field type for '{column_name}': {field_type}")

            # Validate number of rows
            num_rows = self.get_validated_input(
                f"How many rows do you want to insert into table '{table.name}'? ",
                lambda x: x.isdigit() and int(x) > 0,
                "Please enter a positive integer."
            )
            num_rows = int(num_rows)

            for _ in range(num_rows):
                try:
                    query = self.sql_generator.generate_insert_query(table, referenced_tables)
                    print(query)
                except ValueError as ve:
                    logger.error(f"Error generating insert for table '{table.name}': {ve}")
                    print(f"Error: {ve}")
                    print("Skipping this insertion.")
                    break  # Or continue, based on desired logic

            # Log generated rows
            table.log_generated_rows()
            referenced_tables[table.name] = table

    def run(self):
        """Main method to run the CLI application."""
        print("Choose the mode:")
        print("1. Manual Input")
        print("2. DDL File")
        choice = self.get_user_choice("Enter choice (1 or 2): ", ['1', '2'])

        if choice == '1':
            self.run_manual_mode()
        elif choice == '2':
            self.run_ddl_mode()

    def determine_field_type_for_fk(self, referenced_column_type: str) -> str:
        """
        Determines the field type for a foreign key based on the referenced column type.
        """
        referenced_column_type_lower = referenced_column_type.lower()
        if 'int' in referenced_column_type_lower:
            return "Number [0,10000]"
        elif 'varchar' in referenced_column_type_lower or 'char' in referenced_column_type_lower:
            return "Number [0,10000]"  # Can change to another type if needed
        else:
            return "Number [0,10000]"  # Default

    def get_available_field_types(self) -> list:
        """Returns a list of available field types."""
        return [
            "Last name",
                "First name",
                "Address",
                "Postal code",
                "City",
                "Country",
                "Phone",
                "Email",
                "Job",
                "Number [0,10]",
                "Number [0,10000]",
                "Recent date",
                "Date"
        ]
