# import logging
# from .src.analysis import utci_optimised
# from .src import utility
# import numpy as np

# def utci(dryBulbTemp, radiantTemp, windSpeed, relativeHumidity, units="SI", 
#             return_stress_category=False, 
#             return_comfort_rating=False, 
#             return_comfort_percentage=False, 
#             return_comfort_percentage_descriptive=False,
#             limit_inputs=True):
#     """Determines the Universal Thermal Climate Index (UTCI). The UTCI is the
#     equivalent temperature for the environment derived from a reference
#     environment. It is defined as the air temperature of the reference
#     environment which produces the same strain index value in comparison with
#     the reference individual's response to the real environment. It is regarded
#     as one of the most comprehensive indices for calculating heat stress in
#     outdoor spaces. The parameters that are taken into account for calculating
#     UTCI involve dry bulb temperature, mean radiation temperature, the pressure
#     of water vapor or relative humidity, and wind speed (at the elevation of 10
#     m above the ground). [7]_
#     Parameters
#     ----------
#     tdb : float or array-like
#         dry bulb air temperature, default in [°C] in [°F] if `units` = 'IP'
#     tr : float or array-like
#         mean radiant temperature, default in [°C] in [°F] if `units` = 'IP'
#     v : float or array-like
#         wind speed 10m above ground level, default in [m/s] in [fps] if `units` = 'IP'
#     rh : float or array-like
#         relative humidity, [%]
#     units : {'SI', 'IP'}
#         select the SI (International System of Units) or the IP (Imperial Units) system.
#     return_stress_category : boolean default False
#         if True returns the UTCI categorized in terms of thermal stress.
#     limit_inputs : boolean default True
#         By default, if the inputs are outsude the standard applicability limits the
#         function caps the input to the acceptable limits. If False returns UTCI values for unchanged input values even if input values are
#         outside the applicability limits of the model. The valid input ranges are
#         0.5 < v [m/s] < 17.0.
#     Returns
#     -------
#     utci : float or array-like
#          Universal Thermal Climate Index, [°C] or in [°F]
#     stress_category : str or array-like
#          UTCI categorized in terms of thermal stress [9]_.
#     comfort_rating : str or array-like
#          UTCI categorized in terms of thermal stress [9]_.
#     Notes
#     -----
#     You can use this function to calculate the Universal Thermal Climate Index (`UTCI`)
#     The applicability wind speed value must be between 0.5 and 17 m/s.
#     .. _UTCI: http://www.utci.org/utcineu/utcineu.php
#     Examples
#     --------
#     .. code-block:: python
#         >>> from pythermalcomfort.models import utci
#         >>> utci(tdb=25, tr=25, v=1.0, rh=50)
#         24.6
#         >>> # for users who wants to use the IP system
#         >>> utci(tdb=77, tr=77, v=3.28, rh=50, units='ip')
#         76.4
#         >>> # for users who wants to get stress category
#         >>> utci(tdb=25, tr=25, v=1.0, rh=50, return_stress_category=True)
#         {"utci": 24.6, "stress_category": "no thermal stress"}
#     Raises
#     ------
#     ValueError
#         Raised if the input are outside the Standard's applicability limits
#     """

#     dryBulbTemp = np.array(dryBulbTemp)
#     radiantTemp = np.array(radiantTemp)
#     windSpeed = np.array(windSpeed)
#     relativeHumidity = np.array(relativeHumidity)

#     #limit wind speed imputs to be in line with ladybug assumptions
#     if limit_inputs:
#         windSpeed[windSpeed < 0.5] = 0.5
#         windSpeed[windSpeed > 17] = 17

#     #convert input to correct units
#     if units.lower() == "ip":
#         dryBulbTemp, radiantTemp, windSpeed = utility.units_converter(tdb=dryBulbTemp, tr=radiantTemp, v=windSpeed)

#     #preprocessing
#     eh_pa = exponential(dryBulbTemp) * (relativeHumidity / 100.0)
#     delta_t_tr = radiantTemp - dryBulbTemp
#     pa = eh_pa / 10.0  # convert vapour pressure to kPa
    
#     #analysis
#     utci_approx = utci_optimised.calc(dryBulbTemp, windSpeed, delta_t_tr, pa)

#     #create return object
#     output = {'utci':np.round_(utci_approx, 5).tolist()}

#     #postporocessing
#     comfort_cat_def = [
#         'UTCI <0\xB0C',
#         '0\xB0C < UTCI < 9\xB0C and 26\xB0C < UTCI < 28\xB0C',
#         '9\xB0C < UTCI < 26\xB0C',
#         'UTCI > 28\xB0C'
#     ]
#     comfort_cat_desc_def = {
#         'Cold stress':'UTCI <0\xB0C',
#         'Comfort for short period':'0\xB0C < UTCI < 9\xB0C and 26\xB0C < UTCI < 28\xB0C',
#         'Comfort':'9\xB0C < UTCI < 26\xB0C',
#         'Heat stress':'UTCI < 32\xB0C'
#     }
#     # text for displaying with results
#     stress_cat_def = {
#         "extreme cold stress": "UTCI < -40\xB0C",
#         "very strong cold stress": "-40\xB0C < UTCI < -27\xB0C",
#         "strong cold stress": "-27\xB0C < UTCI < -13\xB0C",
#         "moderate cold stress": "-13\xB0C < UTCI < 0\xB0C",
#         "slight cold stress": "0\xB0C < UTCI < 9\xB0C",
#         "no thermal stress": "9\xB0C < UTCI < 26\xB0C",
#         "moderate heat stress": "26\xB0C < UTCI < 32\xB0C",
#         "strong heat stress": "32\xB0C < UTCI < 38\xB0C",
#         "very strong heat stress": "38\xB0C < UTCI < 46\xB0C",
#         "extreme heat stress": "46\xB0C < UTCI",
#     }
#     # results processing 
#     if return_stress_category:
#         output['stressCat'] = {'res':getStressCategory(utci_approx), 'desc':stress_cat_def}
    
#     if return_comfort_rating:
#         output['comfortRating'] = {'res':getComfortRating(utci_approx), 'desc':comfort_cat_def}

#     if return_comfort_percentage:
#         labels = [-3, -2, -1, 0, 1, 2, 3]
#         output['comfortRatingPercentage'] = {'res':getAnnualPercentage(output['comfortRating']['res'], labels), 'desc': output['comfortRating']['desc']}

#     if return_comfort_percentage_descriptive:
#         output['comfortRatingDescriptive'] = {'res':getComfortRatingDescriptive(utci_approx), 'desc':comfort_cat_def}
#         labels = ['Cold stress', 'Comfort for short period', 'Comfort', 'Heat stress']
#         output['comfortRatingDescriptivePercentage'] = {'res':getAnnualPercentage(output['comfortRatingDescriptive']['res'], labels), 'desc':output['comfortRatingDescriptive']['desc']}


#     #convert back the output to correct units
#     if units.lower() == "ip":
#         utci_approx = utility.units_converter(tmp=utci_approx, from_units="si")[0]
    
#     return output

# def getStressCategory(utci_approx):
#     stress_categories = {
#         -40.0: "extreme cold stress",
#         -27.0: "very strong cold stress",
#         -13.0: "strong cold stress",
#         0.0: "moderate cold stress",
#         9.0: "slight cold stress",
#         26.0: "no thermal stress",
#         32.0: "moderate heat stress",
#         38.0: "strong heat stress",
#         46.0: "very strong heat stress",
#         1000.0: "extreme heat stress",
#     }

#     return utility.mapping(utci_approx, stress_categories).tolist()

# def getComfortRating(utci_approx):
#     comfort_cat = {
#         -13.0: -3,
#         0.0: -2,
#         9.0: -1,
#         26.0: 0,
#         28.0: 1,
#         32.0: 2,
#         1000.0: 3,
#     }
#     return utility.mapping(utci_approx, comfort_cat).tolist()

# def getComfortRatingDescriptive(utci_approx):
#     comfort_cat = {
#         -13.0: 'Cold stress',
#         0.0: 'Cold stress',
#         9.0: 'Comfort for short period',
#         26.0: 'Comfort',
#         28.0: 'Comfort for short period',
#         32.0: 'Heat stress',
#         1000.0: 'Heat stress',
#         }
#     return utility.mapping(utci_approx, comfort_cat).tolist()

# def getAnnualPercentage(data, labels):
#     ratingArr = np.array(data)
#     output = []
#     for i, val in enumerate(labels):
#         ratio = np.count_nonzero(ratingArr == val)/len(data)
#         percentage = str(round(ratio*100*10)/10)
#         if ratio < 0.001:
#             output.append(
#                 '{} experienced < 0.1% of the year'.format(val, percentage))
#         else:
#             output.append(
#                 '{} experienced {}% of the year'.format(val, percentage))
#     return output

# def exponential(t_db):
#     g = [
#         -2836.5744,
#         -6028.076559,
#         19.54263612,
#         -0.02737830188,
#         0.000016261698,
#         (7.0229056 * np.power(10.0, -10)),
#         (-1.8680009 * np.power(10.0, -13)),
#     ]
#     tk = t_db + 273.15  # air temp in K
#     es = 2.7150305 * np.log1p(tk)
#     for count, i in enumerate(g):
#         es = es + (i * np.power(tk, count - 2))
#     es = np.exp(es) * 0.01  # convert Pa to hPa
#     return es