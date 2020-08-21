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

    return df
