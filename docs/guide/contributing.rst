
Contributing to ``fritzctl``
============================

Since the underlying API changes from time to time, it may be necessary to implement new API classes and bugfixes for existing ones.

Also, because of the sheer amount of APIs, it is not possible for me alone to implement all Service Types by myself.

This is why I am writing this guide, aiming to allow future developers and maintainers to understand the design concepts used in this library.

Naming Conventions
------------------

Almost all Variable names should be written in camelCase with the first letter lowercase, except for ClassNames.

Constants and global Mappings should be written in CAPSLOCK.

This is as far as I know the only deviation from :pep:`8`\ , everywhere else you should strictly follow this PEP when writing code for fritzctl.

Writing OO Wrapper Classes
--------------------------

Naming
^^^^^^

When writing Object-Oriented Wrapper Classes, there are several things to be aware of.

First, when choosing the name, the module should be called ``fritzctl.ooapi.<category>[_<subcategory>]_<name>`` where subcategory is optional.
Category may be one of avm, general and net and name should be derived from the Service Type URN.

As an example, the Service Type URN ``urn:dslforum-org:service:WANIPConnection:1``
translates to category net, subcategory wan and name ipconnection, resulting in the final name ``net_wan_ipconnection``\ .

Some names may be shortened, e.g. config is generally shortened to cfg.

In most of the cases, it will not be necessary to name a Service Type, as it will probably already have entries in :py:data:`fritzctl.session.NAME_TO_URN`\ .

Now, we need to create the class name, which is simply ``API_<name>`` in the corresponding module. Note that there may only be one API Class per module.

When you successfully built a new name, make sure to register it in both :py:data:`fritzctl.session.NAME_TO_URN` and :py:data:`fritzctl.ooapi.OO_APIS` and the corresponding documentation.

Writing the class
^^^^^^^^^^^^^^^^^

After you have created your new module and empty class, you will need to make sure that the base class is :py:class:`fritzctl.ooapi.base.API_base` and add the appropriate imports.

You should not need to override the ``__init__`` method as all needed instance variables are already set.

It is also highly recommended to take a look at e.g. the :py:class:`fritzctl.ooapi.avm_homeauto.API_avm_homeauto()` class and similiar to get a feeling of how they work.

If you need no additional classes for e.g. devices you should have everything you need to know.

Writing Helper/Device classes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are for example writing an API for a new Homeautomation API, you will need write additional device classes.

In this example, we assume that the API name is ``avm_homeautomation`` and the API class is called ``API_avm_homeautomation``\ .

Using the names above, we can derive the device class name to be ``HomeautomationDevice()`` or ``HomeautoDevice()``\ .
You can choose the name freely, but it is recommended to always end it with either Device or Info or Config, depending on what type of class you are creating.

Look at the :py:class:`fritzctl.ooapi.avm_homeauto.HomeautoDevice()` class for an example of how to write these classes.

It should be noted that the ``index`` parameter is only there for legacy purposes and is not needed in new classes.

You can often copy and paste the docstrings from already existing modules and change the names of mentioned classes to save on typing the same docstring again.

Releasing
---------

When releasing a new version, you will need to open the setup.py file and change the version.

When changing the version, you should change the last digit after the a only for minor bugfixes immediately after the release, for when you discover a critical bug not noticed during testing.

The 3rd digit, the so called bugfix version, should be changed when fixing bugs and will often stay at zero.

The 2nd digit, the so called minor version, should be changed when new features are added that are mostly backwards compatible, e.g. adding a new service type plus wrapper classes.

The 2st digit, the so called major version, should only be changed when new backwards-incompatible changes have been made or after introducing a completely new system and corresponding API.

After changing the version, you should make sure that:

- all documentation has been written, run ``make coverage`` and check in ``_build/coverage/python.txt`` and make sure that every module is fully documented
- all new features are working as intended, simply run each feature once and stress-test important features
- all debug outputs are removed
- most critical bugs are fixed
- the code runs on all supported platforms

You will also need to create a file called ``.pypirc`` in your home directory with the following contents::
   
   [distutils]
   index-servers =
       pypi
   
   [pypi]
   username:username
   password:password
   
The password and username should be changed to a valid combination.

After you have triple-checked that everything works, you can simply run this command to publish to PyPI::
   
   $ sudo python setup.py install sdist bdist bdist_wheel register upload
   
This command has been tested under Ubuntu 16.04 and will need to be modified to work under windows.

If the process fails during the upload step, simply re-run the command without the register step.
