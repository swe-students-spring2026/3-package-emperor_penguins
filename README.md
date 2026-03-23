# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

# The following is just the tentative layout of this readme file. Feel free to adjust it. (Remove this line before submission)

- The badge (placeholder)
- Description
- Link to the package on the PyPI website
- how a developer who wants to import your project into their own code can do so - include documentation and code examples for all functions in your package and a link to an example Python program that uses each of them.
- how a developer who wants to contribute to your project can set up the virtual environment, install dependencies, and build and test your package for themselves.
- the names of all teammates as links to their GitHub profiles in the README.md file.
- instructions for how to configure and run all parts of your project for any developer on any platform - these instructions must work!
- instructions for how to set up any environment variables and import any starter data into the database, as necessary, for the system to operate correctly when run.
- if there are any "secret" configuration files, such as .env or similar files, that are not included in the version control repository, examples of these files, such as env.example, with dummy data must be included in the repository and exact instructions for how to create the proper configuration files and what their contents should be must be supplied to the course admins by the due date.

## Steps necessary to contribute to our project.

```shell
# First, clone this repository.
git clone https://github.com/swe-students-spring2026/3-package-emperor_penguins.git
```
If you use a windows, switch to git bash and then proceed. If you use a unix-like os, just proceed.

Second, create a virtual environmenet using `pipenv`.

Please make sure you global python interpreter has `pipenv` installed.

If not, do this:
```shell
# install pipenv globally
pip install pipenv
```
After you have `pipenv` installed,
```shell
# Activate a virtual environment and drop yourself into a new shell that uses that virtualenv’s python.
pipenv shell
``` 
```shell
# Download dependencies (for now, we'll edit the toml file to make dependencies more manageable)
pipenv install emoji
```