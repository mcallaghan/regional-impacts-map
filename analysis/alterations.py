def postfix_data(df):
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


    return df
