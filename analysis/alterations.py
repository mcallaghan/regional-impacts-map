# Alterations module

def postfix_data(df):

    df.loc[df['16 - Future/modelled impacts']==1, 'relevant'] = 0

    # Driver was coded only as an impact, its driver was uncoded
    df.loc[df['id']==112762,"6 - 07 Aridity/dryness"] = 1
    df.loc[df['id']==112762,"6 - 72 Conflict"] = 0
    df.loc[df['id']==112762,"4 - 72 Conflict"] = 1
    df.loc[df['id']==112762,"6 - 76 Human water use"] = 1

    # Unspecific climate change driver not coded
    df.loc[df['id']==746862,"6 - 13 Other (physical systems)"] = 1
    df.loc[df['id']==746862,"4 - 72 Conflict"] = 1
    df.loc[df['id']==746862,"4 - 73 Displacement and migration"] = 1

    # Driver and impact wrong way round
    df.loc[df['id']==2342058,"4 - 72 Conflict"] = 1
    df.loc[df['id']==2342058,"6 - 07 Aridity/dryness"] = 1

    # Crop yield miscoded as driver
    df.loc[df['id']==377564,"4 - 69 Crop yields"] = 1
    df.loc[df['id']==377564,"6 - 69 Crop yields"] = 0

    # Phenology not also recognised as intermediary impact
    df.loc[df['id']==2504903,"4 - 52 Shifts in phenology (Terrestrial and freshwater)"] = 1

    #
    df.loc[df['id']==325492,"6 - 36 Species distribution (marine & coastal)"] = 1

    #
    df.loc[df['id']==98654,'4 - 02 Air or land surface temperature changes'] = 0
    df.loc[df['id']==98654,'4 - 05 Changes in precipitation'] = 0

    #
    df.loc[df['id']==561026,'4 - 02 Air or land surface temperature changes'] = 0
    df.loc[df['id']==561026,'6 - 02 Air or land surface temperature changes'] = 1
    df.loc[df['id']==561026,'4 - 66 Health'] = 1
    #df.loc[df['id']==,] =


    #
    df.loc[df['id']==2146364,'6 - 77 Land use change'] = 0
    df.loc[df['id']==2146364,'6 - 58 Pests and diseases'] = 0
    df.loc[df['id']==2146364,'6 - 51 Distribution and range shifts (Terrestrial and freshwater)'] = 0

    #
    df.loc[df['id']==1300494,'6 - 02 Air or land surface temperature changes'] = 1


    #
    df.loc[df['id']==1486581,'6 - 51 Distribution and range shifts (Terrestrial and freshwater)'] = 0
    df.loc[df['id']==1486581,'4 - 51 Distribution and range shifts (Terrestrial and freshwater)'] = 1
    df.loc[df['id']==1486581,'6 - 28 River runoff'] = 0


    #
    df.loc[df['id']==75669,'6 - 02 Air or land surface temperature changes'] = 1
    df.loc[df['id']==75669,'6 - 05 Changes in precipitation'] = 1
    df.loc[df['id']==75669,'6 - 25 Evapotranspiration'] = 1

    df.loc[df['id']==75158,'12 - Mountains, snow and ice'] = 1

    df.loc[df['id']==365418, '12 - Mountains, snow and ice'] = 0
    df.loc[df['id']==5655, '4 - 32 Permafrost'] = 0
    df.loc[df['id']==223212, '4 - 34 Glacier retreat'] = 1
    df.loc[df['id']==2320760, '4 - 34 Glacier retreat'] = 1
    df.loc[df['id']==592332,'4 - 56 Terrestrial carbon cycle'] = 1
    df.loc[df['id']==592332,'4 - 57 Biogeochemical flows (Terrestrial and freshwater)'] = 1
    df.loc[df['id']==232384, '4 - 32 Permafrost'] = 1
    df.loc[df['id']==733885, '4 - 30 Snow'] = 1
    df.loc[df['id']==724036, '4 - 30 Snow'] = 1
    df.loc[df['id']==632426, '4 - 33 Sea ice retreat'] = 1
    df.loc[df['id']==167922, '12 - Mountains, snow and ice'] = 1
    df.loc[df['id']==719948, '4 - 33 Sea ice retreat'] = 1
    df.loc[df['id']==68861, '12 - Mountains, snow and ice'] = 1
    df.loc[df['id']==601022, '12 - Mountains, snow and ice'] = 1
    df.loc[df['id']==3314964, '4 - 33 Sea ice retreat'] = 1

    df.loc[df['id']==465680, '12 - Coastal and marine Ecosystems'] = 1
    df.loc[df['id']==708887, '12 - Coastal and marine Ecosystems'] = 1
    df.loc[df['id']==411770, '12 - Coastal and marine Ecosystems'] = 1
    df.loc[df['id']==739948, '4 - 39 Changes in fisheries output/catch (potential)'] = 1
    df.loc[df['id']==1534275, '4 - 50 Other (marine & coastal)'] = 1

    df.loc[df['id']==743097, '4 - 40 Changes in warm water corals'] = 1
    df.loc[df['id']==2340588, '4 - 47 Seagrass'] = 1
    df.loc[df['id']==1895132,'4 - 36 Species distribution (marine & coastal)'] = 1

    df.loc[df['id']==105531,'4 - 37 Shifts in phenology (marine & coastal)'] = 0
    df.loc[df['id']==105531,'4 - 52 Shifts in phenology (Terrestrial and freshwater)'] = 1

    df.loc[df['id']==209390,'4 - 37 Shifts in phenology (marine & coastal)'] = 0

    df.loc[df['id']==197307, '4 - 42 Species abundance (marine & coastal)'] = 0
    df.loc[df['id']==197307, '4 - 44 Biodiversity effects (marine & coastal)'] = 0
    df.loc[df['id']==197307, '4 - 51 Distribution and range shifts (Terrestrial and freshwater)'] = 0
    df.loc[df['id']==197307, '4 - 55 Community composition and interaction'] = 0

    df.loc[df['id']==293480, '12 - Coastal and marine Ecosystems'] = 1

    df.loc[df['id']==2317280, 'relevant'] = 0

    df.loc[df['id']==1547261,'4 - 42 Species abundance (marine & coastal)'] = 1
    df.loc[df['id']==2340588, '4 - 36 Species distribution (marine & coastal)'] = 1

    df.loc[df['id']==1277171,'4 - 42 Species abundance (marine & coastal)'] = 1
    df.loc[df['id']==1277171, '4 - 36 Species distribution (marine & coastal)'] = 1

    df.loc[df['id']==1894915, '4 - 64 Indigenous communities'] = 1

    df.loc[df['id']==709599, '4 - 64 Indigenous communities'] = 1

    df.loc[df['id']==3270379, '4 - 75 Economic activity'] = 1

    df.loc[df['id']==795797, '4 - 72 Conflict'] = 1
    df.loc[df['id']==2339354, '4 - 72 Conflict'] = 1

    df.loc[df['id']==1545437, '4 - 65 Gender specific / gender unequal impacts'] = 1
    df.loc[df['id']==779319, '4 - 65 Gender specific / gender unequal impacts'] = 1
    df.loc[df['id']==125032, '4 - 65 Gender specific / gender unequal impacts'] = 1
    df.loc[df['id']==1530126, '4 - 65 Gender specific / gender unequal impacts'] = 1
    df.loc[df['id']==467895, '4 - 65 Gender specific / gender unequal impacts'] = 1
    df.loc[df['id']==76085, '4 - 65 Gender specific / gender unequal impacts'] = 1

    df.loc[df['id']==102469, '4 - 64 Indigenous communities'] = 1

    df.loc[df['id']==659326, 'relevant'] = 1
    df.loc[df['id']==659326, '2 - 2.5. Detection of a regional climate trend (no attribution)'] = 1
    df.loc[df['id']==659326, '4 - 08 Changes in strong precipitation'] = 1
    df.loc[df['id']==659326, '4 - 05 Changes in precipitation'] = 1

    df.loc[df['id']==2098987, '6 - 05 Changes in precipitation'] = 1
    df.loc[df['id']==3897103, '6 - 05 Changes in precipitation'] = 1

    df.loc[df['id']==559798, 'relevant'] = 1
    df.loc[df['id']==559798, '2 - 2.5. Detection of a regional climate trend (no attribution)'] = 1
    df.loc[df['id']==559798, '4 - 02 Air or land surface temperature changes'] = 1

    df.loc[df['id']==711961, '4 - 66 Health'] = 1

    ### Still categorise these ones:

    df.loc[df['id']==393812, 'relevant'] = 1

    df.loc[df['id']==1500608, 'relevant'] = 1

    df.loc[df['id']==505306, 'relevant'] = 1

    df.loc[df['id']==474873, 'relevant'] = 1

    df.loc[df['id']==568334, 'relevant'] = 1

    df.loc[df['id']==1298121, 'relevant'] = 1

    df.loc[df['id']==1547304, 'relevant'] = 1

    df.loc[df['id']==1500945, 'relevant'] = 1

    df.loc[df['id']==1045885, 'relevant'] = 1

    df.loc[df['id']==288985, 'relevant'] = 1

    df.loc[df['id']==618981, 'relevant'] = 1

    df.loc[df['id']==404008, 'relevant'] = 1

    df.loc[df['id']==779159, 'relevant'] = 1

    df.loc[df['id']==2343897, 'relevant'] = 1

    df.loc[df['id']==1500945, 'relevant'] = 1

    df.loc[df['id']==270374, 'relevant'] = 1

    df.loc[df['id']==32240, 'relevant'] = 1

    df.loc[df['id']==564039, 'relevant'] = 1

    df.loc[df['id']==271249, 'relevant'] = 1

    df.loc[df['id']==2332587, 'relevant'] = 1

    df.loc[df['id']==121701, 'relevant'] = 1

    df.loc[df['id']==783657, 'relevant'] = 1

    df.loc[df['id']==710703, 'relevant'] = 1

    df.loc[df['id']==46349, 'relevant'] = 1

    df.loc[df['id']==465607, 'relevant'] = 1

    df.loc[df['id']==1861956, 'relevant'] = 1

    df.loc[df['id']==572409, 'relevant'] = 1

    df.loc[df['id']==296314, 'relevant'] = 1

    df.loc[df['id']==638010, 'relevant'] = 1

    df.loc[df['id']==11932, 'relevant'] = 1

    df.loc[df['id']==1281972, 'relevant'] = 1

    df.loc[df['id']==269490, 'relevant'] = 1

    df.loc[df['id']==781691, 'relevant'] = 1

    df.loc[df['id']==1553572, 'relevant'] = 1

    df.loc[df['id']==775373, 'relevant'] = 1

    df.loc[df['id']==1499374, 'relevant'] = 1

    df.loc[df['id']==118064, 'relevant'] = 1

    df.loc[df['id']==658111, 'relevant'] = 1

    df.loc[df['id']==2365166, 'relevant'] = 1

    df.loc[df['id']==388192, 'relevant'] = 1

    df.loc[df['id']==2309627, 'relevant'] = 1

    df.loc[df['id']==24919, 'relevant'] = 1

    df.loc[df['id']==1286362, 'relevant'] = 1

    df.loc[df['id']==453752, 'relevant'] = 1

    df.loc[df['id']==1390463, 'relevant'] = 1

    df.loc[df['id']==1359430, 'relevant'] = 1

    df.loc[df['id']==1537837, 'relevant'] = 1

    df.loc[df['id']==1500377, 'relevant'] = 1

    df.loc[df['id']==540990, 'relevant'] = 1

    df.loc[df['id']==3314086, 'relevant'] = 1

    df.loc[df['id']==1409241, 'relevant'] = 1

    df.loc[df['id']==2358826, 'relevant'] = 1

    df.loc[df['id']==1523239, 'relevant'] = 1

    df.loc[df['id']==775373, 'relevant'] = 1

    df.loc[df['id']==1285846, 'relevant'] = 1

    df.loc[df['id']==562949, 'relevant'] = 1

    df.loc[df['id']==1526508, 'relevant'] = 1

    df.loc[df['id']==730639, 'relevant'] = 1

    df.loc[df['id']==3941420, 'relevant'] = 1

    df.loc[df['id']==378806, 'relevant'] = 1

    df.loc[df['id']==222422, 'relevant'] = 1

    df.loc[df['id']==347890, 'relevant'] = 1

    df.loc[df['id']==562949, 'relevant'] = 1

    df.loc[df['id']==711727, 'relevant'] = 1

    df.loc[df['id']==669809, 'relevant'] = 1

    df.loc[df['id']==47768, 'relevant'] = 1

    df.loc[df['id']==453088, 'relevant'] = 1

    df.loc[df['id']==465607, 'relevant'] = 1
    df.loc[df['id']==465607, 'relevant'] = 1
    df.loc[df['id']==465607, 'relevant'] = 1
    df.loc[df['id']==465607, 'relevant'] = 1

    ### Mistakenly positive

    df.loc[df['id']==293480, "relevant"] = 0

    df.loc[df['id']==1306727, "relevant"] = 0

    df.loc[df['id']==401900, "relevant"] = 0

    df.loc[df['id']==1552554, "relevant"] = 0

    df.loc[df['id']==453088, "relevant"] = 0

    df.loc[df['id']==222422, "relevant"] = 0

    df.loc[df['id']==489217, "relevant"] = 0

    df.loc[df['id']==1628655, "relevant"] = 0

    df.loc[df['id']==2365166, "relevant"] = 0

    df.loc[df['id']==775716, "relevant"] = 0

    df.loc[df['id']==853785, "relevant"] = 0

    df.loc[df['id']==3557274, "relevant"] = 0

    df.loc[df['id']==1306727, "relevant"] = 0
    df.loc[df['id']==1306727, "relevant"] = 0
    df.loc[df['id']==1306727, "relevant"] = 0
    df.loc[df['id']==1306727, "relevant"] = 0

    return df

# unlabelled = [393812,
# 1500608,
# 505306,
# 474873,
# 568334,
# 1298121,
# 1547304,
# 1500945,
# 1045885,
# 288985,
# 618981,
# 404008,
# 779159,
# 2343897,
# 1500945,
# 270374,
# 32240,
# 564039,
# 271249,
# 2332587,
# 121701,
# 783657,
# 710703,
# 46349,
# 465607,
# 1861956,
# 572409,
# 296314,
# 638010,
# 11932,
# 1281972,
# 269490,
# 781691,
# 1553572,
# 775373,
# 1499374,
# 118064,
# 658111,
# 2365166,
# 388192,
# 2309627,
# 24919,
# 1286362,
# 453752,
# 1390463,
# 1359430,
# 1537837,
# 1500377,
# 540990,
# 3314086,
# 1409241,
# 2358826,
# 1523239,
# 775373,
# 1285846,
# 562949,
# 1526508,
# 730639,
# 3941420,
# 378806,
# 222422,
# 347890,
# 562949,
# 711727,
# 669809,
# 47768,
# 453088,
# 465607
# ]
