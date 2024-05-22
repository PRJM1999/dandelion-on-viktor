## Dandelion Weather App

Dandelion is a powerful tool designed to provide insightful visualizations of environmental data extracted from EnergyPlus Weather `.epw` files. By allowing users to **find** and **download** `.epw` files. Dandelion empowers analysis and comprehension of various environmental aspects through comprehensive graphs and charts. Leveraging the open-source EPW repository from Ladybug, Dandelion ensures access to a wide range of EPW data for analysis.

## Getting Start

### Prerequisites

Ensure you have the following software installed:

- Python 3.10 or higher
- Viktor

### Installation

Follow these steps to set up the project:

1. **Clone the Repository**

   First, clone the repository to your local machine using Git:

   ```sh
   git clone https://github.com/PRJM1999/dandelion-on-viktor.git
   ```

2. **Install the App**
    Next run the command to allow Viktor to install the necessary files and packages:

    ```sh
   viktor-cli install
   ```

3. **Start the App**
    Run the below command, log onto your Viktor account and view it in your local environment

    ```sh
   viktor-cli start
   ```

## Environment Setup

To get the application connected to a relevant Speckle Server and EPW database, you need to set up an `.env` file with the following variables:

```env
SPECKLE_BASE_URL=SPECKLE SERVER URL HERE
SPECKLE_API_TOKEN=TOKEN HERE
MONGODB_URI=URI HERE
```

## EPW Database Format

The MongoDB collection 'epw' in the database 'dandelion' should contain documents representing weather stations. Each document should have the following structure:

```json
{
  "lat": <Latitude of the weather station (float)>,
  "lng": <Longitude of the weather station (float)>,
  "station_id": <Unique identifier for the weather station (string)>,
  "station_name": <Name of the weather station (string)>,
  "data": <Additional data related to the weather station (object)>
}
```
By following this format, you can ensure that your MongoDB EPW database is set up correctly and your application can retrieve weather station data effectively.

## Testing

### Running Tests

Our project uses `pytest` for running tests. To execute the tests and verify that everything is working as expected, you can run the following command from the root directory of the project:

```sh
pytest
```

This will discover and run all the tests in the project.

### Test Coverage

To ensure our codebase maintains high-quality standards, we also measure test coverage using `pytest-cov`. This helps us identify untested parts of our codebase and improve our tests continuously.

To run tests with coverage measurement, use the following command:

```sh
pytest --cov=src
```

This command will run all tests and report the coverage percentage for all modules under the `src` directory. Additionally, you can generate detailed HTML coverage reports by using:

```sh
pytest --cov=src --cov-report html
```

This will generate a `htmlcov` directory containing the coverage report in HTML format. Open the `index.html` file within that directory in a web browser to view the detailed coverage report.

### Coverage Requirements

To maintain and ensure the reliability and stability of our production environment, we require a **minimum test coverage score of 75%**. This threshold helps us ensure that the majority of our codebase is covered by tests, reducing the likelihood of bugs and regressions.

## License

This project is licensed under the MIT License. See the [licence](licence) file for more details.