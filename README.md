---
date: 2024-05-28T14:29:31.586900
author: AutoGPT <info@agpt.co>
---

# ZenUML to JPG

The project will involve creating an application capable of taking ZenUML code as an input, converting this input into a visual diagram, and subsequently allowing users to download the resulting diagram as a JPEG file. Utilizing the discussed technology stack, the project will be constructed as follows:

1. **Backend Development**: We will use FastAPI as our backend framework due to its simplicity and asynchronous request handling capabilities, which are beneficial for the processing part of the application. FastAPI will handle the web requests for converting ZenUML code into a diagram and for downloading the diagram.

2. **Code to Diagram Conversion**: For converting the ZenUML code into diagrams, we will investigate and possibly integrate libraries mentioned earlier, such as Graphviz, PyDot, or potentially PlantUML if it offers support for parsing ZenUML or similar syntax. This will involve parsing the ZenUML code, converting the parsed structure into a visual representation, and then generating an image file from this representation.

3. **Diagram Viewing and Exporting Features**: The resulting diagrams will be viewable directly in the web interface, with features such as zooming and panning for better user interaction, especially for larger diagrams. Users will have the option to export and download these diagrams as JPG files, a feature supported by libraries such as Matplotlib or Graphviz by using their built-in export or save functions.

4. **Real-time Collaboration (optional)**: As an additional enhancement, integrating a real-time collaboration feature would allow multiple users to work on the same ZenUML diagram simultaneously. However, this would significantly increase the project's complexity and may require additional technology such as websockets for real-time updates.

5. **Database and ORM**: PostgreSQL will serve as the database to store user information, diagrams, and possibly the ZenUML code snippets. Prisma, as the ORM, will facilitate database interactions, making the development process more straightforward and reducing boilerplate code.

6. **Development Language**: The entire backend and processing logic will be implemented in Python. Python's extensive library support for diagram generation and working with images makes it a suitable choice for our needs.

This project plan outlines a system that not only meets the initial requirements but also includes considerations for future enhancements such as real-time collaboration. The technologies selected offer a combination of performance, developer productivity, and community support, ensuring that the project can be implemented effectively and can evolve over time.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'ZenUML to JPG'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
