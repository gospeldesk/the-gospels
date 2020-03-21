Prince
http://www.princexml.com

INSTALLATION

To install Prince, please run the install.sh shell script contained
in this package. This will involve the following procedure:

Open the Terminal application.

Change to the directory containing this package. For example:

    $ cd /Users/joe/prince-13.1-macos

Run the installation shell script.

    $ ./install.sh

The installation directory can be supplied as a command line argument:

    $ ./install.sh /path/to/directory

Follow the prompts to install Prince. Please note that you will need to be
logged in as root if you wish to install Prince into a system directory
such as /usr/local. This can be accomplished by running the installation
script using sudo, which will prompt you for your password:

    $ sudo ./install.sh
    Password: .....

RUNNING PRINCE

To run Prince after installation, enter:

    $ prince input.html -o output.pdf

Or specify the full path if it is not in a system directory:

    $ /Users/joe/prince-13.1/bin/prince

To see the usage and available options, enter:

    $ prince --help

If you have difficulty running the program, please ensure that the
installation directory is in your $PATH. This is necessary if you
did not install the program in /usr/local.

FEEDBACK

Thank you for choosing Prince, we hope you find it useful.
If you have any comments or questions regarding the program, please
email us or visit our website.

    Email:  prince@yeslogic.com
      Web:  http://www.princexml.com

