# SQL Generator Project

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Creating a Virtual Environment](#creating-a-virtual-environment)
    - [Windows](#windows)
    - [macOS](#macos)
    - [Linux](#linux)
  - [Activating the Virtual Environment](#activating-the-virtual-environment)
    - [Windows](#windows-1)
    - [macOS](#macos-1)
    - [Linux](#linux-1)
  - [Installing Dependencies](#installing-dependencies)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Modes of Operation](#modes-of-operation)
    - [Manual Input Mode](#manual-input-mode)
    - [DDL File Processing Mode](#ddl-file-processing-mode)
- [Resources](#resources)
  - [Test DDL Files](#test-ddl-files)
- [Environment Configuration](#environment-configuration)
  - [.env Files](#env-files)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The **SQL Generator Project** is a command-line tool designed to generate SQL `INSERT` statements based on user input or predefined DDL (Data Definition Language) files. It intelligently handles various data types, including numeric fields, dates, and enforces unique constraints and primary keys to ensure data integrity.

## Features

- **Manual Input Mode:** Allows users to define tables and fields interactively.
- **DDL File Processing Mode:** Parses existing DDL files to generate corresponding SQL `INSERT` statements.
- **Handles Data Types Appropriately:**
  - Numeric fields are inserted without quotes.
  - Date fields use the `to_date` function for proper formatting.
  - String and other fields are enclosed in single quotes.
- **Enforces Constraints:**
  - Ensures unique values for fields with `UNIQUE` or `PRIMARY KEY` constraints.
  - Manages foreign key relationships between tables.

## Prerequisites

- **Python 3.11** or higher
- **pip** (Python package installer)
- **Git** (optional, for cloning the repository)

## Setup

### Creating a Virtual Environment

It's recommended to use a virtual environment to manage dependencies and avoid conflicts with other Python projects.

#### Windows

1. Open Command Prompt.

2. Navigate to your project directory:
   ```bash
   cd path\to\your\project
   ```

3. Create a virtual environment named `venv`:
   ```bash
   python -m venv venv
   ```

#### macOS

1. Open Terminal.

2. Navigate to your project directory:
   ```bash
   cd /path/to/your/project
   ```

3. Create a virtual environment named `venv`:
   ```bash
   python3 -m venv venv
   ```

#### Linux

1. Open Terminal.

2. Navigate to your project directory:
   ```bash
   cd /path/to/your/project
   ```

3. Create a virtual environment named `venv`:
   ```bash
   python3 -m venv venv
   ```

### Activating the Virtual Environment

After creating the virtual environment, you need to activate it.

#### Windows

```bash
venv\Scripts\activate
```

#### macOS

```bash
source venv/bin/activate
```

#### Linux

```bash
source venv/bin/activate
```

### Installing Dependencies

Once the virtual environment is activated, install the required Python packages using `pip`. Ensure that you have a `requirements.txt` file in your project directory.

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file, you can create one with the necessary dependencies. For example:

```bash
pip freeze > requirements.txt
```

## Usage

The application can be run in two modes: Manual Input Mode and DDL File Processing Mode.

### Running the Application

Ensure that your virtual environment is activated. Then, execute the main script using Python.

```bash
python main.py
```

### Modes of Operation

Upon running the application, you will be prompted to choose between the available modes.

#### Manual Input Mode

1. **Select Manual Input Mode:**
   ```
   Choose the mode:
   1. Manual Input
   2. DDL File
   Enter choice (1 or 2): 1
   ```

2. **Define Table and Fields:**
   - **Table Name:** Enter the name of the table.
   - **Number of Fields:** Specify how many fields the table will have.
   - **Field Details:** For each field, provide the field name and select the appropriate data type from the list.

3. **Specify Number of Rows:**
   - Indicate how many `INSERT` statements you wish to generate.

4. **Generated SQL Queries:**
   - The application will output the generated `INSERT` statements based on your input.

#### DDL File Processing Mode

1. **Select DDL File Mode:**
   ```
   Choose the mode:
   1. Manual Input
   2. DDL File
   Enter choice (1 or 2): 2
   ```

2. **Provide Path to DDL File:**
   - Enter the file path to your DDL file. The application will parse the file to understand the table structures and constraints.

3. **Define Field Types:**
   - For each column in the table, select the appropriate data type. The parser will handle foreign keys and unique constraints accordingly.

4. **Specify Number of Rows:**
   - Indicate how many `INSERT` statements you wish to generate for each table.

5. **Generated SQL Queries:**
   - The application will output the generated `INSERT` statements based on the DDL file and your input.

## Resources

### Test DDL Files

The project includes sample DDL files located in the `resources/ddl/` directory. These files can be used to test the DDL File Processing Mode.

- **Example:**
  - `employees.ddl`
  - `departments.ddl`

Feel free to modify these files or add your own to suit your testing needs.

## Environment Configuration

The application utilizes environment variables for configuration. These variables are defined in `.env` files.

### `.env` Files

- **Location:** Place your `.env` files in the root directory of the project or specify the path as needed.

- **Purpose:** Define configuration settings such as repository types, file paths, and other parameters.

- **Example `.env` Content:**
  ```env
  REPOSITORY_TYPE=FAKER
  RESOURCES_PATH=./src/resources/
  ```

- **Loading `.env` Variables:**
  The application uses the `python-dotenv` package to load environment variables from `.env` files. Ensure that this package is included in your `requirements.txt` and installed.

## Troubleshooting

- **Virtual Environment Issues:**
  - Ensure that the virtual environment is activated before running the application.
  - Verify that all dependencies are installed correctly using `pip install -r requirements.txt`.

- **Missing DDL Files:**
  - Confirm that the DDL file path provided exists and is accessible.
  - Check the `resources/ddl/` directory for available test DDL files.

- **Unique Constraint Errors:**
  - If the application is unable to generate unique values after multiple attempts, consider increasing the range of generated values or modifying the `ValueRepository` to produce more diverse data.

- **Environment Variables Not Loading:**
  - Ensure that the `.env` file is correctly named and placed in the appropriate directory.
  - Verify that the `python-dotenv` package is installed.

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please follow these steps:

1. **Fork the Repository**
2. **Create a New Branch:**
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. **Commit Your Changes:**
   ```bash
   git commit -m "Add Your Feature"
   ```
4. **Push to the Branch:**
   ```bash
   git push origin feature/YourFeatureName
   ```
5. **Open a Pull Request**

Please ensure that your code follows the project's coding standards and includes appropriate documentation and tests.

## License

This project is licensed under the [MIT License](LICENSE).

```