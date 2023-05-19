# MedIntel

#### Video Demo:  <URL HERE>

#### Description:

This project allows users to check known medications of a patient for potentially dangerous interactions.
These can occur when for example medicine A inhibits the enzyme that usually metabolizes medicine B.
Medicine B is very likely to be present in higher concentrations than the prescribing physician aimed for in this case.

MedIntel works by having a database of medicines, where for each medicine at least two things are known:
-the name of the medication
-the name of its metabolizing enzyme
and optionally
-the name of an enzyme it inhibits
-the name of an enzyme it induces

From this database, every time at startup, a second database is built. This second database contains information "from the enzymes perspective".
This allows the program to quickly find out which medicines are to be considered when a certain enzyme is inhibited for example.

For this to work the following things have to be known about an enzyme:
-the name of the enzyme
at least one of these three list must not be empty:
-which meds inhibit the enzyme
-which meds induce the enzyme
-which meds get metabolized by the enzyme

This is the foundation of the web application.

Next, the user input consists of a medications name, and a condition the patient is receiving it for.
This will in the future be used to determine whether or not there is polypharmacy or not (a too great amount of pharmaceutics involved).

The following steps describe the user experience:

1. Data entry: For each medicine a patient is receiving, the user puts its name and the condition the patient is receiving it for into the webapp and submits them.

2. The user presses the "Run the Check" button once he has added all known medications of a patient.

3. The website displays different groups of medications:

On the left hand side, all those medications that are present in likely too low concentration, and on the right hand side all those medications that are present likely in too high concentrations.

For each med that is present in likely abnormal concentrations, the website shows which of the patients medicines are likely involved in inhibiting or inducing the problematic medications metabolizing enzyme.

Why is this a flask webapp?

I considered making this a desktop app, seeing as it is most likely to be used by qualified personnel on a capable desktop device.
the familiarity i gained with flask thanks to cs50 made it much more accessible however to build a webapp, and in the end, the functional scope is identical.

in the /static/ folder, my media such as background and the icon are stored, as well as a basic navbar.js hiding script and my styles.css
the media are .svg files, because the low complexity of both the background and logo makes the vector graphics files much much more quick to load when the website is called. The background is made of neobrutalistic depictions of pills on a beige background, and the icon is a diagonal pill.

in the styles.css most elements revolve around making the website look neobrutalistic, since i really enjoy the vibrant, yet function-oriented nature of neubrutalism.

in the /templates/ folder, index.html, layout.html, managedata.html, and presentwarnings.html are found.

layout.html centers around  providing a navbar to the user that allows them to navigate back and forth between the different sites in this app.
the navbar is accessed by clicking on the little pill icon at the very top left corner.

index.html is the landing page and displays the name and a short description of the service, as well as the input fields required for the actions described above.

managedata.html is a site not intended for usage by the user, rather it was a tool i built to make data entry into the medicine databank more accessible for myself. I will not remove this however, since it is supposed to enable future admins to easily build on top of what i started with here.

presentwarnings takes the result of my webapps calculations and displays them grouped by too high or too low levels and lets the user know for each medicine which medicines might be causing the concentrations to be off.

venv contains the python venv that i used to run my flask server locally during development

app.py contains all the python code that is required to run this webapp, except for a helper function i offloaded to helpers.py, buildenzymes()

helpers.py contains buildenzymes, a function that will build the enzyme databank from my medicine databank basically reversing it.
this allows fast access to the medicines related to an enzyme, which in turn allows to look up which medicine has what relationship with other meds.

README.md contains the readme

requirements.txt contains the python prerequisites to run this webapp.

storedmeds.json is a .json object that contains all information the webapp has on medications, and allows the program to build its enzyme databank at runtime. it is updated every time new data is added using the data manager.

If you want to try out the program, be sure only to use the "medicine" names that currently are in storedmeds.json or add your own using the data manager!
