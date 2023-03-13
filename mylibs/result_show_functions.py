from all_objects import *
from vedo import *
from datetime import datetime


def pd_control_params_search(dt=1., N=5, T_max=2000., k_min=1e-4, k_max=1e-2):
    filename = 'storage/pid_koeff.txt'
    f = open(filename, 'w')  # Очистить файл
    f.write(" ")
    f.close()
    k_p_list = np.exp(np.linspace(np.log(k_min), np.log(k_max), N))  # Для логарифмического маштаба
    tolerance_list = []
    start_time = datetime.now()
    tmp_count = 0
    collide = False

    for k_p in k_p_list:
        tmp_count += 1
        id_app = 0
        tolerance = 1e5
        print(Fore.CYAN + f'делаем: {tmp_count}/{N}; время={datetime.now() - start_time}')
        o = AllProblemObjects(if_PID_control=True, dt=dt, T_max=T_max, if_talk=False, if_print_smth=False, k_p=k_p,
                              choice='3', N_apparatus=1)

        for i_time in range(round(T_max / dt)):
            t = (i_time + 1) * o.dt

            o.position_velocity_update(t)
            o.euler_time_step()

            # Repulsion
            o.a.loc[id_app, 'busy_time'] -= o.dt if o.a.busy_time[id_app] >= 0 else 0
            if o.a.flag_fly[id_app] == 0 and o.a.busy_time[id_app] < 0:
                u = repulsion(o, t, id_app, u_a_priori=np.array([0.00749797, 0.00605292, 0.08625441]))
                o.if_see = False
                o.t_start[0] = t
                o.t_start[o.N_app] = t

            # Motion control
            if control_condition(o=o, id_app=id_app, i_time=i_time):
                if o.t_reaction_counter < 0:
                    pd_control(o=o, t=t, id_app=id_app)

            target_orf = o.b_o(o.a.target[id_app])
            tmp = (np.linalg.norm(target_orf - np.array(o.a.r[id_app])))
            collide = collide or call_crash(o, o.a.r[id_app], o.R, o.S, o.taken_beams)
            if tmp < tolerance:
                tolerance = 20 if collide else tmp
        tolerance_list.append(tolerance)
        f = open(filename, 'a')
        f.write(f'{k_p} {tolerance}\n')
        f.close()
    plt.title("Подбор коэффициентов ПД-регулятора")
    plt.plot(k_p_list, tolerance_list, c='#009ACD', label='невязка, м')
    plt.scatter(k_p_list, tolerance_list, c='#009ACD')
    plt.legend()
    plt.show()
    return k_p_list[np.argmin(tolerance_list)]


def plot_params_while_main(filename: str):
    f = open('storage/main.txt', 'r')
    o = AllProblemObjects()

    id_max = 0
    for line in f:
        lst = line.split()
        if lst[0] == 'график':
            id_max = max(id_max, 1+int(lst[1]))
    f.close()

    dr = [[] for _ in range(id_max)]
    w = [[] for _ in range(id_max)]
    j = [[] for _ in range(id_max)]
    V = [[] for _ in range(id_max)]
    R = [[] for _ in range(id_max)]
    t = [[] for _ in range(id_max)]
    a = [[] for _ in range(id_max)]
    m = [[] for _ in range(id_max)]

    f = open('storage/main.txt', 'r')
    for line in f:
        lst = line.split()
        if len(lst) > 0:
            if lst[0] == 'график':
                id_app = int(lst[1])
                dr[id_app].append(float(lst[2]))
                w[id_app].append(float(lst[3]))
                j[id_app].append(float(lst[4]))
                V[id_app].append(float(lst[5]))
                R[id_app].append(float(lst[6]))
                a[id_app].append(float(lst[7]))
                m[id_app].append(int(lst[8]))
        else:
            dr[id_app] = np.array([])
            w[id_app] = np.array([])
            j[id_app] = np.array([])
            V[id_app] = np.array([])
            R[id_app] = np.array([])
            t[id_app] = np.array([])
            tmp = 0
    f.close()
    print(f"id_max: {id_max}")

    fig, axs = plt.subplots(3)
    axs[0].set_xlabel('время, с')
    axs[0].set_ylabel('Невязка, м')
    axs[0].set_title('Параметры в процессе алгоритма')
    axs[1].set_xlabel('время t, с')
    axs[1].set_ylabel('ограниченные величины')
    axs[2].set_xlabel('итерации')
    axs[2].set_ylabel('бортовое ускорение, м/с2')

    clr = ['c', 'indigo', 'm', 'violet', 'teal', 'slategray', 'greenyellow', 'sienna']
    for id_app in range(id_max):
        t[id_app] = np.linspace(0, len(dr[id_app]), len(dr[id_app]))
        for i in range(len(dr[id_app]) - 1):
            axs[0].plot([t[id_app][i], t[id_app][i+1]], np.array([dr[id_app][i], dr[id_app][i+1]]),
                        c=clr[2 * id_app + 2 * m[id_app][i]])
        axs[0].plot(t[id_app], np.zeros(len(t[id_app])), c='khaki')
        axs[1].plot(t[id_app], [1 for _ in range(len(t[id_app]))], c='gray')
        axs[2].plot(range(len(a[id_app])), a[id_app], c='c')
        axs[0].plot(range(len(a[id_app])), np.zeros(len(a[id_app])), c='khaki')
    id_app = 0
    axs[1].plot(t[id_app], np.array(w[id_app]) / o.w_max, c='teal', label='w')
    axs[1].plot(t[id_app], np.array(j[id_app]) / o.j_max, c='tan', label='угол')
    axs[1].plot(t[id_app], np.array(V[id_app]) / o.V_max, c='g', label='V')
    axs[1].plot(t[id_app], np.array(R[id_app]) / o.R_max, c='brown', label='R')

    # axs[0].legend()
    axs[1].legend()

    if filename != '[Название]':
        plt.savefig(f"add/{filename}.jpg")
    plt.show()


def plot_a_avoid(filename: str, x_boards: list = [-10, 5], z_boards: list = [3, 10], size: int = 10):
    o = AllProblemObjects(choice='3')

    # x_boards: list = [-15, 15], z_boards: list = [1, 10]
    nx = 30
    nz = 15
    x_list = np.linspace(x_boards[0], x_boards[1], nx)
    z_list = np.linspace(z_boards[0], z_boards[1], nz)

    arrs = []
    i = 0
    forces = [np.zeros(3) for i in range(nx*nz)]
    max_force = 0
    for x in x_list:
        for z in z_list:
            tmp = avoiding_force(o, 0, r=[x, 0, z])
            if tmp is not False:
                forces[i] = tmp
                max_force = max(max_force, np.linalg.norm(tmp))
            i += 1
    i = 0
    for x in x_list:
        for z in z_list:
            force = forces[i] / max_force
            i += 1
            if force is not False:
                print(f"force: {force}")
                # draw_vector(ax=ax, v=force, r0=[x, 0, z], clr='k')
                l1 = [np.array([x, 0, z]), np.array([x, 0, z]) + force]
                l2 = [np.array([x + 0.1*force[2], 0, z + 0.1*force[0]]), np.array([x + 0.1*force[2], 0, z + 0.1*force[0]]) + force]
                farr = FlatArrow(l1, l2, tip_size=1, tip_width=1).c(color='c', alpha=0.9)   # .c(i)
                arrs.append(farr)

    # three points, aka ellipsis, retrieves the list of all created actors
    arrs.append(plot_iterations_new(o).color("silver"))
    show(arrs, __doc__, viewup="z", axes=1, bg='bb', zoom=1, size=(1920, 1080)).close()
