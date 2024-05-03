def get_data_by_field(weather_data, field_index):
    # Field 5 is uncertainty data and is not a number so retain type
    if field_index == 5:
        return [row[field_index] for row in weather_data]
    # For all other fields, convert to int
    result = []
    for row in weather_data:
        try:
            result.append(int(row[field_index]))
        except ValueError:
            result.append(None)
    return result


def parse_epw(raw):
    epw_raw = [row.split(',') for row in raw.split('\n')]

    epw = {
        '_location': {},
        'designCondition': {},
        'designConditions': {},
        'typicalExtremePeriod': {},
        'typicalExtremePeriods': {},
        'groundTemperature': {},
        'groundTemperatures': {},
        'holiday': {},
        'holidayDaylightSavings': {},
        'comments1': {},
        'comments2': {},
        'dataPeriod': {},
        'weatherData': []
    }

    # Import location data on first line.
    epw['_location'] = epw_raw[0]
    epw['stationLocation'] = epw_raw[0][1]
    epw['state'] = epw_raw[0][2]
    epw['country'] = epw_raw[0][3]
    epw['source'] = epw_raw[0][4]
    epw['stationID'] = epw_raw[0][5]
    epw['latitude'] = epw_raw[0][6]
    epw['longitude'] = epw_raw[0][7]
    epw['timeZone'] = epw_raw[0][8]
    epw['elevation'] = epw_raw[0][9]

    # Data period
    epw['dataPeriod'] = epw_raw[7]

    # Comments
    epw['comments1'] = epw_raw[5]
    epw['comments2'] = epw_raw[6]

    # Weather data
    # Remove header and parse weather data into weatherData object
    epw_raw = epw_raw[8:]

    # Data fields in weather data
    data_fields = [
        'year', 'month', 'day', 'hour', 'minute', 'uncertainty', 'dryBulbTemperature',
        'dewPointTemperature', 'relativeHumidity', 'atmosphericStationPressure',
        'extraterrestrialHorizontalRadiation', 'extraterrestrialDirectNormalRadiation',
        'horizontalInfraredRadiationIntensity', 'globalHorizontalRadiation', 'directNormalRadiation',
        'diffuseHorizontalRadiation', 'globalHorizontalIlluminance', 'directNormalIlluminance',
        'diffuseHorizontalIlluminance', 'zenithLuminance', 'windDirection', 'windSpeed', 'totalSkyCover',
        'opaqueSkyCover', 'visibility', 'ceilingHeight', 'presentWeatherObservation', 'presentWeatherCodes',
        'precipitableWater', 'aerosolOpticalDepth', 'snowDepth', 'daysSinceLastSnowfall', 'albedo',
        'liquidPrecipitationDepth', 'liquidPrecipitationQuantity'
    ]

    for field_index, field in enumerate(data_fields):
        epw[field] = get_data_by_field(epw_raw, field_index)

    return epw

# Example usage:
# with open('your_data_file.csv', 'r') as file:
#     raw_data = file.read()
# parsed_data = parse_epw(raw_data)
# print(parsed_data)
