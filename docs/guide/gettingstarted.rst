
Getting Started with ``fritzctl``
=================================

Installation
------------

Due to its complexity, ``fritzctl`` needs multiple steps to be installed successfully.

Requirements
^^^^^^^^^^^^

The :py:mod:`fritzctl` module needs the latest Python 2.7.x installed, see the `Official Python Website <https://www.python.org/downloads/>`_ and select the file appropriate for your system.

.. note::
   
   This module currently does not work with Python 3.x, so be sure to click on Download Python 2.7.x.

In addition, you will also need to install both the :py:mod:`requests` and :py:mod:`simpletr64` modules.
See `Requests <http://docs.python-requests.org/en/master/user/install/#install>`_ for how to install requests and `simpletr64 <http://bpannier.github.io/simpletr64/html/install.html#install>`_ for how to install lxml.

Installing fritzctl itself
^^^^^^^^^^^^^^^^^^^^^^^^^^

Installing :py:mod:`fritzctl` itself is fairly easy, simply download the latest release, unzip to a directory of your choice and open a terminal
where you extracted your archive.

If you completed these steps, execute the following command::
   
   $ python setup.py install
   
Note that when running under linux, you may need to run this command as root::
   
   $ sudo python setup.py install
   
You can verify that you installed :py:mod:`fritzctl` correctly by opening a python interactive interpreter and running::
   
   >>> import fritzctl

If you get an :py:exc:`ImportError`\ , you didn't install :py:mod:`fritzctl` correctly.

Quickstart
----------

All of the examples in this section assume that you have created an account called ``fritzctl`` with the password ``mypassword``
on your local FRITZ!Box and that it is accessable via ``http://fritz.box/``\ .
The test account used in this tutorial needs the Smart Home, Calls and User Interface permissions to work properly.

Also, this Guide uses a switchable FRITZ!Powerline 546E to demonstrate the Homeauto API and Homeplug API.

If you have a different setup, simply change the appropriate parameters.

Creating a Session
^^^^^^^^^^^^^^^^^^

If you want to follow along with the tutorial, you should run all these examples in the same interactive Python session.

But first, we should create a :py:class:`Session() <fritzctl.session.Session>`\ ::
   
   >>> import fritzctl
   >>> mysession = fritzctl.Session("fritz.box","fritzctl","mypassword") # Note that the URL is without both http:// and www.
   

If do not have a switchable Socket/Powerline for testing, you should
still read at least some of the steps so you can get a feel for how this API works.

Alternatively, you can skip to the next Subsection about the Device Information API.

Getting an API
^^^^^^^^^^^^^^

There are muliple ways to create API Objects to interface with the server,
but in this quick guide we will only look at the Object-Oriented APIs.

We will start with the Homeautomation API::
   
   >>> api = mysession.getOOAPI("avm_homeauto")
   # Alternatively:
   >>> api = mysession.getOOAPI("urn:dslforum-org:service:X_AVM-DE_Homeauto:1")

This will give us an instance of :py:class:`fritzctl.ooapi.avm_homeauto.API_avm_homeauto` to play with.
You can find a full list of the features of this API by clicking on the linked class name.

Working with the API
^^^^^^^^^^^^^^^^^^^^

There are also multiple ways to get to a specific device.
In particular, you can list all devices and pick them yourself or request it by its index or AIN/MAC Address.

In this scenario, we will presume that there is only one Homeautomation Device connected::
   
   >>> mydevice = api.getDeviceByIndex(0)
   # Or:
   >>> mydevice = api.getDeviceList()[0]
   # Or:
   >>> mydevice = api.getDeviceByAIN("12:34:56:78:90:AB")

You can find the full API docs :py:class:`here <fritzctl.ooapi.avm_homeauto.API_avm_homeauto>`\ .

Working with Homeautomation Devices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we have the :py:class:`HomeautoDevice() <fritzctl.ooapi.avm_homeauto.HomeautoDevice>`\ , we should check if it actually is the device we expected and then manipulate it::
   
   >>> mydevice.productname
   "FRITZ!Powerline 546E"
   # If you get something different, try the above section again but with the zero replaced by a one instead
   >>> mydevice.name # Can be changed in the userinterface, so may differ
   "FRITZ!Powerline 546E"
   >>> mydevice.ain # Will be different but in the same format
   "12:34:56:78:90:AB"

Seems that we got the right device, now we can check what features it has::
   
   >>> mydevice.energy_flag
   True
   >>> mydevice.temp_flag
   False
   >>> mydevice.switch_flag
   True
   >>> mydevice.hkr_flag
   False
   >>> mydevice.energy_valid
   True
   >>> mydevice.switch_valid
   True

We now know that this device can read power flowing through it via a multimeter and that we can switch it.

Switching the Switch
^^^^^^^^^^^^^^^^^^^^

After we have all these different objects and flags, we can now safely toggle the switch::
   
   >>> mydevice.switch_state
   False
   >>> mydevice.switch_state = True
   # Should turn on the socket
   >>> mydevice.switch_state
   True
   # Alternatively toggle the switch:
   >>> mydevice.switch_state = "toggle"
   >>> mydevice.switch_state
   False
   

You can also switch the device directly from the API::
   
   >>> api.switchByAIN("12:34:56:78:90:AB",True)
   

Energy Measurements
^^^^^^^^^^^^^^^^^^^

As we have seen, this device also supports measuring the energy flowing through it.

Now, we will measure the energy flow currently measured::
   
   >>> mydevice.energy_power
   0.0
   >>> mydevice.energy_energy
   0.0
   
You may think that this library doesn't work correctly, but this is intended behaviour.

That there currently are zero watts flowing through the device makes sense, because it is turned off and the total energy is only displayed in 1-Wh increments due to how the API works.

Now, let us switch the switch back on::
   
   >>> mydevice.switch_state = "toggle"
   # wait ~20 seconds to be safe
   >>> mydevice.energy_power # depends highly on connected device
   60.0
   >>> mydevice.energy_energy # 1min in theory after the switch is turned on, if 60 watts are constantly used
   1.0

Normally, we would have to refresh our data, but toggling the switch automatically reloads it.

If you want to manually update your data, simply call :py:meth:`reloadData() <fritzctl.ooapi.avm_homeauto.HomeautoDevice.reloadData>` and it will reload the data in-place.

More Variables
^^^^^^^^^^^^^^

There are a lot more variables available on these Devices, but it would take to long to describe them all here.
If you want to use these, you should take a look at their :py:class:`API Documentation <fritzctl.ooapi.avm_homeauto.HomeautoDevice()` where you can find them all in the constructor.

Device Information API
----------------------

As the second example, we will take a look at the :py:class:`fritzctl.ooapi.general_deviceinfo.API_general_deviceinfo()` API.

Preparation
^^^^^^^^^^^

You probably already know the procedure from above, but here is it again::
   
   $ python
   ...
   >>> import fritzctl
   >>> s = fritzctl.Session("fritz.box","fritzctl","mypassword")
   >>> api = s.getOOAPI("general_deviceinfo")
   

Getting our Device
^^^^^^^^^^^^^^^^^^

It should be noted that this API is not for general Devices, it only gives information about the FRITZ!Box itself.

Since we got our API in the last step, now we can get our device info::
   
   >>> devinfo = api.getDeviceInfo()
   
Quick and easy, as it should be.

Static Device Variables
^^^^^^^^^^^^^^^^^^^^^^^

These are all static Variables, but you can still call ``reloadData()`` on the object we got in the last step to reload the data.

Static Variables::
   
   >>> devinfo.manufacturer
   "AVM"
   >>> devinfo.manufacturerOUI
   "00040E"
   >>> devinfo.modelname
   "FRITZ!Box 7580"
   >>> devinfo.description
   # like the modelname, but more verbose
   >>> devinfo.productclass
   "FRITZ!Box"
   >>> devinfo.hwversion
   "FRITZ!Box 7580"
   >>> devinfo.specversion
   "1.0"
   
Of course, you probably knew most of those variables before, but this can helpful if e.g. you need to detect a specific model and then run some special compatibility code.

Dynamic Device Variables
^^^^^^^^^^^^^^^^^^^^^^^^

These are similiar to the variables above, but they are often different for every box and some will change rapidly::
   
   >>> devinfo.serialnumber
   # 12 chars of presumably hex and probably unique because 12**16=a lot
   >>> devinfo.swversion # will probably be higher than what I have
   "153.06.51"
   >>> devinfo.provisioningcode
   >>> # No output if you have a direct-bought box with an open provider
   >>> # Alternatively 4 groups of 3-digit numbers seperated by dots should be output
   >>> devinfo.uptime # can be almost any number, in seconds
   20018
   >>> devinfo.devicelog
   # Lots of text
   
These are all the variables supported by this API, but you can still take a look at the :py:class:`documentation <fritzctl.ooapi.general_deviceinfo.API_general_deviceinfo>`\ .

Further References
------------------

I highly recommend you to take a look at the general :py:mod:`API Documentation<fritzctl.ooapi>` for lots of information about almost all features.

You should also take a look at the official TR64 AVM API Documentation, the site itself is only available in German, but the PDFs are in English.
The overview page can be found `on the official Website <https://avm.de/service/schnittstellen/>`_ and an overview about every service supported
can be found `here <https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AVM_TR-064_first_steps.pdf>`_\ .

You can also look at the official `simpletr64 Documentation <http://bpannier.github.io/simpletr64/html/>`_ for more information about the underlying module.
It should be noted that I have found simpletr64's FRITZ!Box helper classes not to work on my system.
