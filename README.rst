Python package for accessing Mendeley's local sqlite3 database
==============================================================

pymendeley retrieves reference information from Mendeley's local sqlite3
database.

Install using::
    
    sudo pip install https://github.com/brotchie/pymendeley/tarball/master

Dump a list of all references::

    import mendeley

    db = mendeley.MendeleyDatabaseInterface()
    references = db.get_references()

    references.sort(key=operator.attrgetter('authors'))

    for ref in references:
        print(ref.as_text_reference())

Partial output of result::

    ...
    Uppal - 1993 - A general equilibrium model of international portfolio choice
    Valenzuela - 2010 - Rollover Risk and Corporate Bond Spreads
    Vasicek - 1977 - An equilibrium characterization of the term structure
    Veldhuizen - 1995 - Expression Templates
    Verousis, ap Gwilym - 2010 - An improved algorithm for cleaning Ultra High-Frequency data
    Vlaamse, Belgie, Wetenschappen, Kunsten - 2007 - 5 TH ACTUARIAL AND FINANCIAL
    Waggoner - 1997 - Spline Methods for Extracting Interest Rate Curves from Coupon Bond Prices
    Wang, Zhou, Guan - 2011 - Detecting Collusive Cliques in Futures Markets Based on Trading Behaviors
    ...
