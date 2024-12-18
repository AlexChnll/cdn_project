5TC project : implementation of a CDN architecture with a LRU cache strategy.

Before starting the servers, you have to run in a virtual environnement : use the command "venv\Scripts\activate".


Reminder of the different phases to be implemented :
  - Phase 1 : A web server answer to get requests for files stored locally and when the file is not there locally return a default image.
  - Phase 2 : A web server answer to get requests for files stored locally and when the file is not there locally : Get the file from a central server -> Apply a caching strategy (LRU strategy) -> Deliver it.
  - Phase 3 : A web server answer to get requests for files stored locally and when the file is not there locally : Apply a strategy to know where to get the file -> Obtain the file -> Apply a caching strategy -> Deliver it.
  - Phase 4 : A web server obtain your files using an IP interface different than the one over which you receive your eyeball queries.



