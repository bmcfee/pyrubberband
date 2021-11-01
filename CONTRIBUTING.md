
Contributing code
=================

How to contribute
-----------------

The preferred way to contribute to pyrubberband is to fork the 
[main repository](http://github.com/bmcfee/pyrubberband/) on
GitHub:

1. Fork the [project repository](http://github.com/bmcfee/pyrubberband):
   click on the 'Fork' button near the top of the page. This creates
   a copy of the code under your account on the GitHub server.

2. Clone this copy to your local disk:

          $ git clone git@github.com:YourLogin/pyrubberband.git
          $ cd pyrubberband 

3. Create a branch to hold your changes:

          $ git checkout -b my-feature

   and start making changes. Never work in the ``master`` branch!

4. Work on this copy on your computer using Git to do the version
   control. When you're done editing, do:

          $ git add modified_files
          $ git commit

   to record your changes in Git, then push them to GitHub with:

          $ git push -u origin my-feature

Finally, go to the web page of the your fork of the pyrubberband repo,
and click 'Pull request' to send your changes to the maintainers for
review. This will send an email to the committers.

(If any of the above seems like magic to you, then look up the 
[Git documentation](http://git-scm.com/documentation) on the web.)

It is recommended to check that your contribution complies with the
following rules before submitting a pull request:

-  All public methods should have informative docstrings with sample
   usage presented.

You can also check for common programming errors with the following
tools:

-  Code with good test coverage (at least 99%), check with:

          $ pip install -e .[tests]
          $ pytest

Documentation
-------------

You can edit the documentation using any text editor and then generate
the HTML output by typing ``make html`` from the docs/ directory.
The resulting HTML files will be placed in _build/html/ and are viewable 
in a web browser. See the README file in the doc/ directory for more information.

For building the documentation, you will need
[sphinx](http://sphinx.pocoo.org/).


Note
----
This document was gleefully borrowed from [scikit-learn](http://scikit-learn.org/).
