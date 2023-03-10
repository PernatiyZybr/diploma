from mylibs.plot_functions import *
from mylibs.im_sample import *
import scipy


def call_crash_internal_func(r, r1, r2, diam, return_force=False):
    """ Дополнительная функция для функции call_crash; \n
    Проверяет наличие точки r в цилиндре с концами r1,r2, диаметром diam; \n
    Возвращает {True,False} соответственно при отсутствии и наличии. """
    r1 = np.array(r1.copy())
    r2 = np.array(r2.copy())
    x1, y1, z1 = r1
    x2, y2, z2 = r2
    n = np.array([x2 - x1, y2 - y1, z2 - z1])  # Вектор вдоль стержня
    tau = my_cross(np.array([0, 0, 1]), n)
    if np.linalg.norm(tau) < 1e-6:
        tau = my_cross(np.array([1, 0, 0]), n)
        if np.linalg.norm(tau) < 1e-6:
            tau = my_cross(np.array([0, 1, 0]), n)
    b = my_cross(tau, n)
    a = r - (r1 + r2) / 2
    f0 = np.dot(a, n) / (np.linalg.norm(n)**2 / 2)
    f1 = np.dot(a, tau) / (np.linalg.norm(tau) * diam)
    f2 = np.dot(a, b) / (np.linalg.norm(b) * diam)

    if return_force:
        return forse_from_beam(a, diam, n, tau, b, f0, f1, f2)
    if not ((f0 > -1) and (f0 < 1) and (f1**2 + f2**2 < 1)):
        return False
    return True


def call_crash(o, r_sat, R, S, taken_beams=np.array([])):
    """ Функция проверяет наличие тела внутри балки (назовём это соударением);      \n
    Input:                                                                          \n
    -> o - AllObjects класс;                                                        \n
    -> r_sat - радиус-вектор центра аппарата; (отдельно для эпизодов)               \n
    -> R - вектор до центра масс конструкции; (отдельно для эпизодов)               \n
    -> S - матрица поворота ОСК -> ССК;       (отдельно для эпизодов)               \n
    -> taken_beams - вектор id стержней, которых учитывать не надо                  \n
    Output:                                                                         \n
    -> True в случае соударения, False иначе. """
    r = o.o_b(r_sat, S=S, R=R)
    for i in range(o.N_beams):
        if not(np.any(taken_beams == i)):
            if np.sum(o.s.flag[i]) > 0:
                r1 = o.s.r1[i]
                r2 = o.s.r2[i]
            else:
                r1 = [o.s.r_st[i][0], o.s.r_st[i][1], o.s.r_st[i][2]]
                r2 = [o.s.r_st[i][0] - o.s.length[i], o.s.r_st[i][1], o.s.r_st[i][2]]
            if call_crash_internal_func(r, r1, r2, o.d_crash):
                return True
    for i in range(o.N_cont_beams):
        r1 = o.c.r1[i]
        r2 = o.c.r2[i]
        if call_crash_internal_func(r, r1, r2, o.c.diam[i] * 1.05):
            return True
    return False


def call_inertia(o, id_s=np.array([]), app_y=None, app_n=None):
    """Функция считает тензор инерции в собственной ск конструкции и центр масс;    \n
    Input:                                                                          \n
    -> o - AllObjects класс;                                                        \n
    -> id_s - вектор id стержней, которых учитывать не надо                         \n
    -> app_y - номера аппаратов, которых стоит учесть при расчёте инерции;          \n
    -> app_n - номера аппаратов, которых не стоит учитывать при расчёте инерции;    \n
    Output:                                                                         \n
    -> Тензор инерции, вектор центра масс. """
    J = np.double(np.zeros((3, 3)))
    N_points_m = 10                                                 # количество материальных точек на стержень
    N_m = N_points_m * (o.N_beams + o.N_cont_beams)                 # материальных точек всего
    m = np.double([0. for _ in range(N_m + o.N_app)])
    r = np.double([[0., 0., 0.] for _ in range(N_m + o.N_app)])

    # Выделение координат стержня - на месте или в грузовом отсеке
    for n in range(o.N_beams):
        if not np.any(id_s == n):
            if np.sum(o.s.flag[n]) > 0:
                r_1 = np.array(o.s.r1[n])
                r_2 = np.array(o.s.r2[n])
            else:
                r_1 = o.s.r_st[n]
                r_2 = o.s.r_st[n] - np.array([o.s.length[n], 0, 0])

            for i in range(N_points_m):
                m[n * N_points_m + i] = o.s.mass[n] / N_points_m
                r[n * N_points_m + i] = r_1 + (r_2 - r_1) * i / N_points_m

    # Учёт грузового отсека на тензор инерции
    for n in range(o.N_cont_beams):
        r_1 = np.array(o.c.r1[n])
        r_2 = np.array(o.c.r2[n])
        for i in range(N_points_m):
            m[(o.N_beams + n) * N_points_m + i] = o.c.mass[n] / N_points_m
            if n > 0:
                r[(o.N_beams + n) * N_points_m + i] = r_1 + (r_2 - r_1) * i / N_points_m
            else:
                r_0 = (r_1 + r_2) / 2
                b = o.c.diam[n] * my_cross((r_2 - r_1), [0, 1, 0]) / np.linalg.norm(r_2 - r_1)
                k = o.c.diam[n] * my_cross((r_2 - r_1), b) / np.linalg.norm(r_2 - r_1) / np.linalg.norm(b)
                r[(o.N_beams + n) * N_points_m + i] = r_0 + b * np.sin(2*np.pi * i / N_points_m) + \
                                                            k * np.cos(2*np.pi * i / N_points_m)

    # Учёт аппаратов
    for a in range(o.N_app):
        if (not o.a.flag_fly[a] and app_n != a) or app_y == a:
            m[N_m + a] = o.a.mass[a]
        else:
            m[N_m + a] = 0
            r[N_m + a] = o.a.target[a]

    # Вычисление центра масс
    tmp_numerator = np.double(np.zeros(3))
    tmp_denominator = np.double(np.zeros(3))
    for k in range(N_m):
        tmp_numerator += m[k] * np.array(r[k])
        tmp_denominator += m[k]
    r_mass_center = tmp_numerator / tmp_denominator
    for k in range(N_m):
        r[k] -= r_mass_center  # С заботой о ваших нервах J считается относительно центра масс

    for k in range(N_m):
        for i in range(3):
            for j in range(3):
                J[i][j] += m[k] * (
                        kronoker(i, j) * (r[k][0] ** 2 + r[k][1] ** 2 + r[k][2] ** 2) - r[k][i] * r[k][j])
    return J, np.array(r_mass_center)


def call_middle_point(X_cont, r_right):
    """ Функция возвращает id удобной ручки грузового отсека как промежуточная цель;    \n
    Input:                                                                              \n
    -> информационная матрица X_cont, содержашая столбцы:                               \n
    id | mass | length | diam | r1 | r2 | flag_grab                                     \n
    -> r_right - радиус-вектор таргетной точки на конструкции ССК                       \n
    Output:                                                                             \n
    -> id-номер удобной ручки крепления с конструкцией """
    X_middles = []
    for i in range(len(X_cont.id)):
        if X_cont.flag_grab[i]:
            X_middles.append(i)
    difference = [X_cont.r1[X_middles[i]] / 2 + X_cont.r2[X_middles[i]] / 2 for i in range(len(X_middles))]
    N_middles = len(difference)
    difs = np.zeros(N_middles)
    for i in range(N_middles):
        difs[i] = np.linalg.norm(difference[i] - r_right)
    i_needed = np.argmin(difs)

    return np.array(X_middles)[i_needed]


def calculation_motion(o, u, T_max, id_app, interaction=True, line_return=False):
    """Функция расчитывает угловое и поступательное движение одного аппарата и конструкции; \n
    Других аппаратов и их решения она не учитывает;                                         \n
    Input:                                                                                  \n
    -> o - AllObjects класс;                                                                \n
    -> u0 - начальная скорость аппарата (ССК при interaction=True, ОСК иначе)               \n
    -> T_max - время эпизода                                                                \n
    -> id_app - номер аппарата                                                              \n
    -> interaction - происходит ли при импульсе отталкивание аппарата от конструкции        \n
    -> line_return - возвращать ли линию полёта аппарата ССК (для красивых картинок)        \n
    Output:                                                                                     \n
    -> F_min - минимальная невязка-вектор от нужной точки до аппарата                           \n
    -> F_min - средняя невязка-вектор от нужной точки до аппарата                               \n
    -> w_modeling/w_after - максимальный модуль угловой скорости станции по ходу/после эпизода  \n
    -> V_max - максимальный модуль поступательной скорости станции по ходу/после эпизода        \n
    -> R_max - максимальный модуль положения ОСК станции по ходу эпизода                        \n
    -> j_max - максимальный угол отклонения от целевого положения станции по ходу эпизода       \n
    -> N_crashes - количество соударений (не должно превосходить 1)                             \n
    -> line - линия аппарата ССК (при line_return=True)"""
    o_lcl = o.copy()

    w_max, V_max, R_max, j_max, f_mean = np.zeros(5)
    f_min = np.array([1e10, 0, 0])
    r = np.array(o.a.r[id_app])
    n_crashes = 0
    r0 = o.o_b(r)
    line = []

    id_beam = o.a.flag_beam[id_app]
    '''m_beam = 0. if (id_beam is None) else o.s.mass[id_beam]
    m_extra = 0. if (id_beam is None) else o.s.mass[id_beam] * len(o.taken_beams)
    M_without = o.M - m_beam - m_extra
    m_extra = o.a.mass[id_app] + m_beam'''
    m_beam = 0. if (id_beam is None) else o.s.mass[id_beam]
    M_without = o.M - m_beam
    m_extra = o.a.mass[id_app] + m_beam

    if interaction:
        J_p, r_center_p = call_inertia(o, o.taken_beams_p, app_y=id_app)
        J, r_center = call_inertia(o, o.taken_beams, app_n=id_app)
        J_1 = np.linalg.inv(J)
        R_p = o_lcl.R.copy()
        V_p = o_lcl.V.copy()
        o_lcl.R = R_p + o_lcl.S.T @ (r_center - r_center_p)                 # ORF
        u_rot = my_cross(o_lcl.w, o_lcl.S.T @ r0)                           # ORF
        V_rot = my_cross(o_lcl.w, o_lcl.S.T @ (r_center - r_center_p))      # ORF
        V0 = - u * m_extra / M_without                                      # BRF
        u = V_p + o_lcl.S.T @ u + u_rot                                     # ORF
        o_lcl.V = V_p + o_lcl.S.T @ V0 + V_rot                              # ORF
        o_lcl.w = o_lcl.b_o(J_1, o_lcl.S) @ (                               # ORF
                o_lcl.b_o(J_p, o_lcl.S) @ o_lcl.w - m_extra * my_cross(r, u) +
                (M_without + m_extra) * my_cross(R_p, V_p) - M_without * my_cross(o_lcl.R, o_lcl.V))

    o_lcl.om_update()
    o_lcl.C_r[id_app] = get_C_hkw(r, u, o.w_hkw)
    o_lcl.C_R = get_C_hkw(o_lcl.R, o_lcl.V, o.w_hkw)

    # Iterations
    for i in range(int(T_max // o_lcl.dt)):
        # Writing parameters
        f = o_lcl.o_b(o_lcl.get_discrepancy(id_app=id_app, vector=True)) if interaction else \
            o_lcl.get_discrepancy(id_app=id_app, vector=True)
        if np.linalg.norm(f_min) > np.linalg.norm(f):
            f_min = f.copy()
        w_max = max(w_max, np.linalg.norm(o_lcl.w))
        V_max = max(V_max, np.linalg.norm(o_lcl.V))
        R_max = max(R_max, np.linalg.norm(o_lcl.R))
        j_max = max(j_max, 180/np.pi*np.arccos((np.trace(o_lcl.S)-1)/2))
        f_mean += np.linalg.norm(f)
        line = np.append(line, o_lcl.o_b(o_lcl.a.r[id_app]))

        # Stop Criteria
        if o_lcl.d_to_grab is not None:
            if np.linalg.norm(f) <= o_lcl.d_to_grab * 0.95:
                break
        if o_lcl.d_crash is not None:
            if (o_lcl.t - o.t) > 10:
                if call_crash(o, o_lcl.a.r[id_app], o_lcl.R, o_lcl.S, o_lcl.taken_beams):
                    n_crashes += 1
                    break
        if i % 10 == 0:
            o_lcl.file_save(f'график {id_app} {np.linalg.norm(f)} {np.linalg.norm(o_lcl.w)} '
                            f'{np.linalg.norm(180 / np.pi * np.arccos(clip((np.trace(o_lcl.S) - 1) / 2, -1, 1)))} '
                            f'{np.linalg.norm(o_lcl.V)} {np.linalg.norm(o_lcl.R)} '
                            f'{np.linalg.norm(o_lcl.a_self[id_app])}')

        o_lcl.time_step()
    o_lcl.my_print(f"Точность: {np.linalg.norm(f_min)}", mode='m')

    if (o_lcl.iter - o.iter) > 0:
        f_mean /= (o_lcl.iter - o.iter)

    if interaction is False:
        V_p = np.array(v_HKW(o_lcl.C_R, o.mu, o.w_hkw, o_lcl.t))
        u_p = np.array(v_HKW(o_lcl.C_r[id_app], o.mu, o.w_hkw, o_lcl.t))
        J_p, r_center_p = call_inertia(o, o_lcl.taken_beams_p, app_n=id_app)
        J, r_center = call_inertia(o, o_lcl.taken_beams, app_y=id_app)
        R_p = o_lcl.R.copy()
        o_lcl.R += o_lcl.S.T @ (r_center - r_center_p)
        V = (V_p * M_without + u_p * m_extra) / (M_without + m_extra)
        w_after = np.linalg.inv(o_lcl.b_o(J, o_lcl.S)) @ (o_lcl.b_o(J_p, o_lcl.S) @ o_lcl.w -
                                                          (M_without + m_extra) * my_cross(o_lcl.R, V) +
                                                          m_extra * my_cross(r, u_p) + M_without * my_cross(R_p, V_p))
        w_max = np.linalg.norm(w_after)
        o_lcl.Om = o_lcl.U.T @ w_after + o.W_hkw
        o_lcl.C_R = get_C_hkw(o_lcl.R, V, o.w_hkw)
        V_max = np.linalg.norm(V)
        R_max = np.linalg.norm(o_lcl.R)

        for i in range(int((o_lcl.iter - o.iter) // 20)):
            o_lcl.time_step()

            w_max = max(w_max, np.linalg.norm(o_lcl.w))
            V_max = max(V_max, np.linalg.norm(o_lcl.V))
            R_max = max(R_max, np.linalg.norm(o_lcl.R))
            j_max = max(j_max, 180/np.pi*np.arccos((np.trace(o_lcl.S)-1)/2))

    if line_return:
        return f_min, f_mean, w_max, V_max, R_max, j_max, n_crashes, line
    else:
        return f_min, f_mean, w_max, V_max, R_max, j_max, n_crashes


def f_to_capturing(u, *args):
    o, T_max, id_app, interaction, return_to_shooting_method = args
    # u = o.cases['repulse_vel_control'](u)
    dr, _, w, V, R, j, _ = calculation_motion(o=o, u=u, T_max=T_max, id_app=id_app, interaction=interaction)
    reserve_rate = 1.5
    e_w = 0. if (o.w_max/reserve_rate - w) > 0 else abs(w - o.w_max/reserve_rate)
    e_V = 0. if (o.V_max/reserve_rate - V) > 0 else abs(V - o.V_max/reserve_rate)
    e_R = 0. if (o.R_max/reserve_rate - R) > 0 else abs(R - o.R_max/reserve_rate)
    e_j = 0. if (o.j_max/reserve_rate - j) > 0 else abs(j - o.j_max/reserve_rate)
    anw = dr - \
        o.mu_ipm * (np.log(o.w_max - w + e_w) + np.log(o.V_max - V + e_V) +
                    np.log(o.R_max - R + e_R) + np.log(o.j_max - j + e_j)) + \
        o.mu_e * (e_w/o.w_max + e_V/o.V_max + e_R/o.R_max + e_j/o.j_max)
    if return_to_shooting_method:
        return anw, np.linalg.norm(dr)
    return np.linalg.norm(anw)


def f_to_detour(u, *args):
    o, T_max, id_app, interaction, return_vec = args
    u = o.cases['repulse_vel_control'](u)
    dr, dr_average, w, V, R, j, n_crashes = calculation_motion(o, u, T_max, id_app, interaction=interaction)

    if (o.w_max - w > 0) and (o.V_max - V > 0) and (o.R_max - R > 0) and (o.j_max - j > 0):  # Constraint's fulfillment
        anw = dr - o.mu_ipm * (np.log(o.w_max - w) + np.log(o.V_max - V) +
                               np.log(o.R_max - R) + np.log(o.j_max - j)) + \
              np.array([1e50, 1e50, 1e50]) * n_crashes
    else:
        anw = np.array([1e5, 1e5, 1e5]) * \
              (clip(10*(w - o.w_max), 0, 1) + clip(10*(V - o.V_max), 0, 1) +
               clip(1e-1 * (R - o.R_max), 0, 1) + clip(1e-2 * (j - o.j_max), 0, 1)) + \
              np.array([1e50, 1e50, 1e50]) * n_crashes
    if return_vec:
        return anw
    return np.linalg.norm(anw)


def find_repulsion_velocity(o, id_app: int, target=None, interaction: bool = True):
    # Initialization
    if interaction:
        target = o.a.target[id_app] if target is None else target
        tmp = target - np.array(o.o_b(o.a.r[id_app]))
    else:
        target = o.b_o(o.a.target[id_app]) if target is None else target
        tmp = o.b_o(target) - np.array(o.a.r[id_app])
    u = o.u_min * tmp / np.linalg.norm(tmp)

    # Solution
    def cons_f(x):
        return np.linalg.norm(x)

    nonlinear_constraint = scipy.optimize.NonlinearConstraint(fun=cons_f, lb=o.u_min, ub=o.u_max)

    if interaction and not o.control or not interaction:
        func = f_to_capturing
        tol = 0.5
    else:
        func = f_to_detour
        tol = 20
    mtd = 'SLSQP'  # 'trust-constr'
    res = scipy.optimize.minimize(func, u, args=(o, o.T_max, id_app, interaction, False), tol=tol, method=mtd,
                                  constraints=nonlinear_constraint)
    u = o.cases['repulse_vel_control'](res.x)
    # u = res.x
    return u


def calc_shooting(o, id_app, r_right, interaction=True):
    """ Функция выполняет пристрелочный/спектральный поиск оптимальной скорости отталкивания/импульса аппарата; \n
    Input:                                                                                  \n
    -> o - AllObjects класс;                                                                \n
    -> id_app - номер аппарата                                                              \n
    -> r_right - радиус-вектор ССК положения цели                                           \n
    -> interaction - происходит ли при импульсе отталкивание аппарата от конструкции        \n
    Output:                                                                                 \n
    -> u - оптимальный вектор скорости отталкивания/импульса (ССК при interaction=True, ОСК иначе)"""
    shooting_amount = o.shooting_amount_repulsion if interaction else o.shooting_amount_impulse
    if interaction:
        tmp = r_right - np.array(o.o_b(o.a.r[id_app]))
    else:
        tmp = o.b_o(r_right) - np.array(o.a.r[id_app])
    mu_e = o.mu_e
    T_max = 2*(np.linalg.norm(tmp)/o.u_min if o.a.flag_fly[id_app] else o.T_max)  # if (T_max is None) else T_max
    # T_max_hard_limit = T_max*16 if o.X_app.flag_fly[id_app] else o.T_max_hard_limit
    u = o.u_min * tmp / np.linalg.norm(tmp)

    # Метод пристрелки
    mu_ipm = o.mu_ipm
    i_iteration = 0
    while i_iteration < shooting_amount:
        du = 0.00001
        u_i = np.eye(3) * du
        mu_ipm /= 5
        mu_e /= 2
        i_iteration += 1

        dr, tol = f_to_capturing(u, o, T_max, id_app, interaction, True)
        dr_x, _ = f_to_capturing(u + u_i[:, 0], o, T_max, id_app, interaction, True)
        dr_y, _ = f_to_capturing(u + u_i[:, 1], o, T_max, id_app, interaction, True)
        dr_z, _ = f_to_capturing(u + u_i[:, 2], o, T_max, id_app, interaction, True)
        o.my_print(f"Точность пристрелки {tol}, разрешённое время {T_max} секунд", mode=None)
        if tol < o.d_to_grab*0.98:  # and not (c or cx or cy or cz):
            break

        # Коррекция скорости отталкивания
        Jacobian = np.array([[dr_x[0] - dr[0], dr_y[0] - dr[0], dr_z[0] - dr[0]],
                             [dr_x[1] - dr[1], dr_y[1] - dr[1], dr_z[1] - dr[1]],
                             [dr_x[2] - dr[2], dr_y[2] - dr[2], dr_z[2] - dr[2]]]) / du
        Jacobian_1 = np.linalg.inv(Jacobian)
        correction = Jacobian_1 @ dr
        correction = correction/np.linalg.norm(correction)*clip(np.linalg.norm(correction), 0, o.u_max/2)
        u = u - correction

        # Ограничение по модулю скорости
        if np.linalg.norm(u) > o.u_max:
            if o.if_any_print:
                print(Style.RESET_ALL + f'attention: shooting speed reduction: {np.linalg.norm(u)/o.u_max*100} %')
            u = u / np.linalg.norm(u) * o.u_max * 0.9

        if np.linalg.norm(dr) > tol * 1e2:
            mu_ipm *= 10
            i_iteration -= 1
            T_max *= 1.1 if T_max < o.T_max_hard_limit else 1
    return u  # , tol <= o.d_to_grab


def repulsion(o, id_app, u_a_priori=None):
    """Input:                                                                   \n
    -> o - AllObjects класс                                                     \n
    -> t - время принятия решения (для расчёта положения и скорости ХКУ)        \n
    -> id_app - номер аппарата                                                  \n
    -> u_a_priori - заданный вектор скорости (на случай вынужденного решения,   \n
    используется для быстрой отладки алгоритмов управления"""

    # Параметры до отталкивания
    J_p, r_center_p = call_inertia(o, o.taken_beams, app_y=id_app)
    o.taken_beams_p = o.taken_beams.copy()

    # Алгоритм выбора цели
    if o.a.flag_start[id_app]:  # IF ON START
        id_beam = o.s.call_possible_transport(o.taken_beams)[0]
        o.taken_beams = np.append(o.taken_beams, id_beam)
        o.my_print(f"Аппарат {id_app} забрал стержень {id_beam}", mode="b")
    else:
        if o.a.flag_beam[id_app] is None:   # GOING HOME
            id_beam = None
            o.my_print(f"Аппарат {id_app} возвращается на базу", mode="b")
        else:                                   # GOING TO POINT
            id_beam = o.a.flag_beam[id_app]
            o.my_print(f"Аппарат {id_app} летит установливать стержень {id_beam}", mode="b")

    if id_beam is not None:
        r_1 = np.array(o.s.r1[id_beam])
    else:
        tmp_id = o.s.call_possible_transport(o.taken_beams)[0]
        r_1 = np.array(o.s.r_st[tmp_id] - np.array([o.s.length[tmp_id], 0.0, 0.0]))

    if o.a.flag_start[id_app] or (not o.a.flag_to_mid[id_app]):
        m = call_middle_point(o.c, r_1)
        if np.linalg.norm(o.a.target[id_app] - np.array(o.c.r1[m]) / 2 - np.array(o.c.r2[m]) / 2) > 1e-2:
            r_1 = np.array(o.c.r1[m]) / 2 + np.array(o.c.r2[m]) / 2
        o.a.flag_to_mid[id_app] = True
        o.my_print(f"Аппарат {id_app} целится в промежуточный узел захвата", mode="b")
    else:
        o.a.flag_to_mid[id_app] = False

    o.a.target_p[id_app] = o.a.target[id_app].copy()
    o.a.target[id_app] = r_1
    o.a.flag_beam[id_app] = id_beam
    o.a.flag_start[id_app] = False
    o.a.flag_fly[id_app] = True
    o.a.flag_hkw[id_app] = False if (o.if_PID_control or o.if_LQR_control) else True

    # Нахождение вектора скорости отталкивания
    u0 = u_a_priori if (u_a_priori is not None) else \
        find_repulsion_velocity(o=o, id_app=id_app, target=r_1, interaction=True)
    # calc_shooting(o=o, id_app=id_app, r_right=r_1, interaction=True)

    R_p = o.R.copy()
    V_p = o.V.copy()
    o.J, o.r_center = call_inertia(o, o.taken_beams, app_n=id_app)
    o.J_1 = np.linalg.inv(o.J)
    m_beam = 0. if (id_beam is None) else o.s.mass[id_beam]
    M_without = o.M - m_beam
    m_extra = o.a.mass[id_app] + m_beam
    R = R_p + o.S.T @ (o.r_center - r_center_p)
    r = np.array(o.a.r[id_app])
    r0 = o.o_b(r, S=o.S, R=R_p, r_center=r_center_p) 

    u_rot = my_cross(o.w, o.S.T @ r0)                         # ORF
    V_rot = my_cross(o.w, o.S.T @ (o.r_center - r_center_p))  # ORF
    V0 = - u0 * m_extra / M_without                           # BRF
    u = V_p + o.S.T @ u0 + u_rot                              # ORF
    V = V_p + o.S.T @ V0 + V_rot                              # ORF
    o.w = o.b_o(o.J_1) @ (
            o.b_o(J_p) @ o.w - m_extra * my_cross(r, u) +
            (M_without + m_extra) * my_cross(R_p, V_p) - M_without * my_cross(R, V))  # ORF
    o.om_update()
    o.C_r[id_app] = get_C_hkw(r, u, o.w_hkw)
    o.C_R = get_C_hkw(R, V, o.w_hkw)
    o.flag_vision[id_app] = False
    o.t_start[0] = o.t
    o.t_start[o.N_app] = o.t

    o.a.r[id_app] = r
    o.a.v[id_app] = u
    o.a.r_0[id_app] = o.get_discrepancy(id_app)
    o.my_print(f"App id:{id_app} pushed off with u={np.linalg.norm(u)}, w={np.linalg.norm(o.w)}", mode="b", test=True)
    o.my_print(f"Taken beams list: {o.taken_beams}", mode="g", test=True)
    talk_decision(o.if_talk)
    print(f"rep o.s.mass    :{o.s.mass}")

    return u0


def capturing(o, id_app):
    if o.if_any_print:
        print(Fore.BLUE + f'Аппарат id:{id_app} захватился')
    o.a_self[id_app] = np.array(np.zeros(3))
    talk_success(o.if_talk)

    # Параметры до захвата
    id_beam = o.a.flag_beam[id_app]
    m_beam = 0 if id_beam is None else o.s.mass[id_beam]
    M = np.sum(o.s.mass) + np.sum(o.c.mass)
    M_without = M - m_beam
    m_extra = o.a.mass[id_app] + m_beam
    r = np.array(o.a.r[id_app])
    u_p = np.array(o.a.v[id_app])
    V_p = o.V.copy()
    R_p = o.R.copy()
    J_p, r_center_p = call_inertia(o, o.taken_beams, app_n=id_app)

    # Процесс захвата
    if id_beam is not None:
        if np.linalg.norm(np.array(o.s.r1[id_beam]) - np.array(o.a.target[0])) < 1e-2:
            o.my_print(f"Стержень id:{id_beam} устанавливается", mode="b")
            o.s.flag[id_beam] = np.array([1., 1.])
            o.a.flag_beam[id_app] = None
            o.taken_beams = np.delete(o.taken_beams, np.argmax(o.taken_beams == id_beam))
    else:
        if o.a.target[id_app][0] < -0.6:  # Если "слева" нет промежуточных точек, то окей
            o.my_print(f'Аппарат id:{id_app} в грузовом отсеке')
            o.a.flag_start[id_app] = True
    
    # Пересчёт параметров 
    o.J, o.r_center = call_inertia(o, o.taken_beams, app_y=id_app)
    o.J_1 = np.linalg.inv(o.J)
    o.R += o.S.T @ (o.r_center - r_center_p)
    o.V = (V_p * M_without + u_p * m_extra) / (M_without + m_extra)
    o.w = o.b_o(o.J_1, o.S) @ (o.b_o(J_p, o.S) @ o.w - (M_without + m_extra) * my_cross(o.R, o.V) +
                               m_extra * my_cross(r, u_p) + M_without * my_cross(R_p, V_p))
    o.om_update()
    o.C_R = get_C_hkw(o.R, o.V, o.w_hkw)

    o.a.busy_time[id_app] = o.time_to_be_busy
    o.a.flag_hkw[id_app] = True
    o.a.flag_fly[id_app] = False
    o.t_reaction_counter = o.t_reaction
    o.t_start[o.N_app] = o.t
    o.flag_impulse = True
    o.taken_beams_p = o.taken_beams.copy()
    print(f"cap o.s.mass    :{o.s.mass}")
