import numpy as np

def units_converter(from_units="ip", **kwargs):
    """Converts IP values to SI units.
    Parameters
    ----------
    from_units: str
        specify system to convert from
    **kwargs : [t, v]
    Returns
    -------
    converted values in SI units
    """
    results = list()
    if from_units == "ip":
        for key, value in kwargs.items():
            if "tmp" in key or key == "tr" or key == "tdb":
                results.append((value - 32) * 5 / 9)
            if key in ["v", "vr", "vel"]:
                results.append(value / 3.281)
            if key == "area":
                results.append(value / 10.764)
            if key == "pressure":
                results.append(value * 101325)

    elif from_units == "si":
        for key, value in kwargs.items():
            if "tmp" in key or key == "tr" or key == "tdb":
                results.append((value * 9 / 5) + 32)
            if key in ["v", "vr", "vel"]:
                results.append(value * 3.281)
            if key == "area":
                results.append(value * 10.764)
            if key == "pressure":
                results.append(value / 101325)

    return results

def valid_range(x, valid):
    """Filter values based on a valid range."""
    return np.where((x >= valid[0]) & (x <= valid[1]), x, np.nan)

def mapping(value, map_dictionary, right=True):
    """Maps a temperature array to stress categories.
    Parameters
    ----------
    value : float, array-like
        Temperature to map.
    map_dictionary: dict
        Dictionary used to map the values
    right: bool, optional
        Indicating whether the intervals include the right or the left bin edge.
    Returns
    -------
    Stress category for each input temperature.
    """

    bins = np.array(list(map_dictionary.keys()))
    words = np.append(np.array(list(map_dictionary.values())), 404)
    return words[np.digitize(value, bins, right=right)] 