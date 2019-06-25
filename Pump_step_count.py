def pump_step_count(C_feed, Ca, t_now, t_prev, n_prev, V_prev, pump_threshold):

    """
    This function computes the pump steps for the current iteration based on:

    Input:
    c_feed - current algae concentration measured by the OD sensor
    Ca - desired algae concentration in the mussel tank
    t_now - current experimental time
    t_prev - previous pumping time
    n_prev - previous number of algae in the mussel tank after pumping
    v_prev - previous volume of solution in the mussel tank after pumping
    pump_threshold - minimum effective pumping volume


    Output:
    nStep - required pumping steps to reach desired algae concentration

    """
    # ----------------- ascertain pumping volume to be larger than the threshold --------------------- #
    while True:
        t_interval = 10  # presumed pumping interval
        n_now = n_prev - n_consume(V_prev, t_now - t_prev)  # current algae number in the mussel tank
        V_add = (Ca * V_prev - n_now) / (C_feed - Ca)  # volume to be pumped now

        if V_add < pump_threshold:
            t_interval += 1
        else:
            break
    # ------------------------- compute pumping steps & update parameters ---------------------------- #
    nStep = ceil(V_add * 765)
    t_prev = t_now
    V_prev = V_prev + V_add
    n_prev = n_now - n_consume(V_prev, t_interval)

    return nStep, t_prev, V_prev, n_prev