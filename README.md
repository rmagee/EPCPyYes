[![coverage report](https://gitlab.com/serial-lab/EPCPyYes/badges/master/coverage.svg)](https://gitlab.com/serial-lab/EPCPyYes/commits/master)
[![build status](https://gitlab.com/serial-lab/EPCPyYes/badges/master/build.svg)](https://gitlab.com/serial-lab/EPCPyYes/commits/master)


    8888888888 8888888b.   .d8888b.  8888888b.        Y88b   d88P
    888        888   Y88b d88P  Y88b 888   Y88b        Y88b d88P
    888        888    888 888    888 888    888         Y88o88P
    8888888    888   d88P 888        888   d88P 888  888 Y888P  .d88b.  .d8888b
    888        8888888P"  888        8888888P"  888  888  888  d8P  Y8b 88K
    888        888        888    888 888        888  888  888  88888888 "Y8888b.
    888        888        Y88b  d88P 888        Y88b 888  888  Y8b.          X88
    8888888888 888         "Y8888P"  888         "Y88888  888   "Y8888   88888P'
                                                     888
                                                Y8b d88P
                                                 "Y88P"

# Pronounced "EPC-Pie-Yes": Open source components for the GS1 EPCIS standard

The main
purpose of this library is to allow developers to quickly build systems that
parse, generate and store EPCIS data quickly and efficiently with a clear
and straight-forward pythonic API.


## Fully Tested
See our code-coverage and continuous integration builds for the coverage
build artifacts and build/test results.  You can download the code coverage
build artifacts on the [Pipelines Page](https://gitlab.com/serial-lab/EPCPyYes/pipelines)
by clicking on the download button to the right of the build you are interested
in.

## Fully Documented
The EPCPyYes module is fully documented.
[EPCPyYes Documentation Site](https://serial-lab.gitlab.io/EPCPyYes/index.html)

## Jupyter Notebook:
The Jupyter notebook with running example code can be found here:
[Jupyter Events File](https://gitlab.com/serial-lab/EPCPyYes/blob/master/docs/events.ipynb)

If you don't have a notebook, you can view the Jupyter example documentation 
here:
[Notebook Documentation](https://gitlab.com/serial-lab/EPCPyYes/blob/master/docs/events.md)

## Jinja2 Templates for Creating and Transforming EPCIS Docs and Events

The templates package contains Jinja2 templates for generating EPCIS documents
from either discrete EPCIS classes defined in the core package or from collections
of those classes- which allow for the creation of EPCISDocuments with
multiple types of events.  You can change the default behavior of any 
EPCIS class in the framework by passing in a different Jinja2 template when
initializing the class- allowing EPCIS objects to be rendered into just about 
any native or custom format imaginable.  Modifying the default Jinja2
environment can allow the entire package to utilize a different set of 
default templates altogether.

## Core Classes

The core library consists of Python classes representing the key EPCIS events:

* EPCISEvent
* ObjectEvent
* AggregationEvent
* TransactionEvent
* TransformationEvent

    Quantity events, as they are being deprecated,
    are not supported right now If you're interested in 
    helping out with this please contact us.
    
Each of the classes in the core library are used throughout the package but 
can be useful to developers in building other applications outside of the
scope of this package.

## Helpers

Utilities that help you:

* Quickly generate lists of SGTIN or SSCC URN values by a range of serial numbers.
* Quickly serialize python EPCIS classes into valid EPCIS XML and back.
* ...and More.

## CBV 1.2 Type Support and Utilities
Utilities that help with the generation of CBV compliant data and also 
give you code completion while developing CBV compliant EPCIS apps.  We took 
out all the fishery stuff since there are only so many hours in the day.  If
anyone is interested in adding and/or supporting it please contact us.

For example:
   
    >> from EPCPyYes.core.v1_2.CBV.dispositions import Disposition
    >> print(Disposition.commissioning.value)
    >> urn:epcglobal:cbv:bizstep:commissioning