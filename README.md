
![Python 3.10](https://img.shields.io/badge/python-3.12-blue)
![Black](https://img.shields.io/badge/code%20style-black-black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![disquant](disquant.png)

### Mission statement

Disquant is an educational derivatives pricing library. It is not intended for production use and prioritizes 
code readability over performance.


### Coding guidelines

Disquant is built around the following principles:

1. Pure Python: does not depend on any C or C++ extension
2. Modern Python: the project started with Python 3.12 and uses modern Python features
3. Pythonic: the coding style embraces Pythonic implementations
4. PEP-8 / black compliant: it's just easier for everybody to read
5. Short, meaningful and consistent terminology across the project
6. Valid objects: if a class was successfully instantiated, it means it is vali
7. Type-hints

Naming conventions: classes are precise, objects can be named with shorter names. For instance, an interest rate is 
modeled as an `InterestRate` but instances are often called `rate`.
### Installation

Disquant requires Python >= 3.12

```cmd
pip install disquant
```