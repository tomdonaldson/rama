Introduction
============

Rana provides astronomers with tools for reading, visualizing, and analysing data sets from ethereogeneous sources.

Astronomers can easily access datasets across the web, using custom interfaces, python libraries, Virtual Observatory
services and a combination of those. However, datasets come in a variety of formats and with different semantics.

Rama is integrated widely used python packages like ``numpy``, ``astropy``, and ``matplotlib``. At the same time
Rama uses new and old Virtual Observatory standards for achieving interoperability. In particular, Rama heavily make
use of *data models*. A data model describes entities in a domain and how they relate to each others.

For example an astronomical *Source* may have a number of properties, including its *position*, *luminosities* measured
in different *Photometric Bands*, and all such *Measurements* are usually affected by *Errors*.

In the previous paragraphs we emphasize the *Entities* and their *attributes*. There is a core of concepts that all
sources share across missions and over the entire EM spectrum, while other properties of sources may depend on specific
missions or a specific EM domain, or even the specific messenger.

The VO Data Modeling Language provides a rigorous yet simple language for describing such entities in a reusable and
extensible way. Other standards allow concepts defined in a data model to be mapped to the contents of files according
to different formats, like VOTable, FITS, and JSON.

Rama provides a reference implementation of such data models and of the modeling language itself.

Astronomers can use common abstractions like *Source*, *Luminosity*, *EquatorialCoordinate* to seamlessly read and
integrate data coming from different missions and archives, and translate them into the kind of convenient Python
objects they are used to in their day-to-day work, like Numpy arrays or Astropy quantities.

Rama also allows new models to be created and standard models to be extended to fit domain-specific or mission-specific
needs.

For this, Rama provides a framework that allows seamless registration of new models and the definition of adapter
classes that seamlessly wrap data model classes on the fly. For example, the :py:class:`~rama.astropy.SkyCoordAdapter`
is used to wrap a standard VO position coordinate coming from a VOTable into an astropy's ``SkyCoord`` object that can
be immediately plugged into existing tools
ad libraries.

In a nutshell, Rama provides:

  * A reference implementation of the Virtual Observatory Data Modeling Language (VO-DML).
  * A reference implementation of an astropy-aware parser for the Mapping VO-DML instances to VOTable standard.
  * A client-side reference implementation of the Cube, Dataset, Measures, and Coordinates data models.
  * A frameowrk for representing data models as Python classes and registering them so they are discoverable by Rama.
    The framework can also be used to extend existing models.
  * A toolbox that bridges the VO standards to the Python libraries astronomers use, providing science-ready utilities.
  * A framework for wrapping standard data models to custom ones using simple adapters.

The main goal of Rama is enabling science through interoperability. Users must not be aware of standards in order to
use them, and convenient abstractions are used to let astronomers and other developers use and extend standardized
concepts.
