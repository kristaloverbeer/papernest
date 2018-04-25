# Papernest

## Usage

For the developer convenience, a Makefile is here to wrap the docker commands.

To launch the project, you need `docker` and `docker-compose` installed.

To launch the stack:
```bash
make run
```

To execute the tests:
```bash
make tests
```

To connect to the main API docker:
```bash
make sh
```

To stop the stack:
```bash
make stop
```

To clean created containers:
```bash
make clean
```

To clean all created images:
```bash
make clean-dangling-images
```

## A point on the pre-processing process
The aim of this project is to provide coverage information for a given address, on a city-level granularity.

To answer this goal, and given the resources I was given, I decided to do a maximum of the work outside the main program.

First of all, I downloaded the file containing the list of network coverage measures with the associated provider and the
Lambert93 geographic coordinates of the antennas, and finally network coverage for 2G, 3G, and 4G mobile communications standards.

I then used the `pandas` library to process the CSV file. 

First, I converted the Lambert93 coordinates to GPS coordinates (thanks to the provided instructions).

Then, I converted the given provider code with their associated company names.

In addition, I used the Data Gouv API to associate all GPS coordinates to the associate city postcode 
(We want the information at the city granularity level, which is why I decided to calculate all of them).

Finally, I updated the initial CSV file.

Second part of the pre-processing (the first part could take quite a while and I didn't want to have any errors in the middle),
I transformed the updated CSV file to a nested JSON file which list for each postcode, every provider known and the
more optimistic coverage for this city.

What does this means? Several providers antennas can exists in one city. To concatenate these providers in one line,
I looked at all results and updated coverage to True if one of the antenna actually provided coverage in one of the
mobile communications standards.

## Main program

### Services
Services module is there to contains every service that the main program/micro-service could use.

In this case, we need the Data Gouv API to get information on the address that the user queried.

In case that the queried address returned no result, we return a message to inform the user to inform that no result were found.
It can be a place for advice on why there is no result to improve the user experience.

Plus, a score is provided by the external API. I decided to try and exploit it.
If the pertinence score is not enough (roughly fixed at 0.5 here...), we provide a message saying the given
address might not be the one wanted, and more information may be provided to have a better provider coverage metadata result.

This idea can be largely improved. The API can return several results, and a Web interface could provide a suggestion
system for the user to pick from.


### Database

This is where firstly we stored the pre-processed data files.

In order to to exploit it transparently, I created a `schema` package.
Usually, I use this part to handle serialization/deserialization for records in/out of a database.
I reproduced this behaviour with the pre-processed JSON file and cache results.
Each result contains the postcode and the providers coverage metadata associated with.

### Repository

Because I like to keep my API routes clean, not containing any of the business and/or more complex logic, and keep it to only
handle input and output formatting, the `repository` package is here to handle it.

I use the principle of dependency injections (schema, services) in the repository because we need both modules.
Like this, if at some point we decide to change the data source, data format, geolocalisation service, etc...
the impact on the code base will be minimal, changes needed will impact only the concerning modules.

Firstly, the role of the repository is to return perfectly formatted dictionaries to be returned by the API route.

Plus, we use this module to return the appropriate status code, mainly because the API route can't know the exact state
of the response.

As an additional note, usually modules like this repository are used to handle transparently
` GET` and `INSERT` methods (and more if needed, updates etc...).
`Action` modules can then be placed between the API route and the repositories to 
purely handle business logic.

Here, because of the light use case, this module is not really justified.


### API

To end with, I just used the `Flask` framework for the API routes,
and wrap it in a gunicorn Web Server (the entrypoint of the docker) to expose the routes.

## Ideas

During the development of the project, I started in this direction before hitting a lack of information on providers' antennas
(but it is often better to start with a naive approach, right?):

- Get the average radius of the area in which a provider antenna is delivering service.
- For each search, take the longitude and latitude of the address and calculate in which radius this points belongs to.
