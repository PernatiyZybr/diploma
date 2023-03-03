# Standard libraries
import numpy as np
import pandas as pd


def package_beams(N, h):
    ast = 2 * h / np.sqrt(3)
    x = np.linspace(0., 5., N)
    y = np.linspace(0., 5., N)
    flag = 0
    count = 0
    maxcount = 0
    for i in range(N - 1):
        if flag > 6:
            flag = 0
            maxcount += 1
        if flag == 0:  # вверх, новый уровень
            x[i + 1] = x[i]
            y[i + 1] = y[i] + ast
            count = 0
        if flag == 1:  # влево вниз
            x[i + 1] = x[i] - h
            y[i + 1] = y[i] - ast / 2
        if flag == 2:  # вниз
            x[i + 1] = x[i]
            y[i + 1] = y[i] - ast
        if flag == 3:  # вправо вниз
            x[i + 1] = x[i] + h
            y[i + 1] = y[i] - ast / 2
        if flag == 4:  # вправо вверх
            x[i + 1] = x[i] + h
            y[i + 1] = y[i] + ast / 2
        if flag == 5:  # вверх
            x[i + 1] = x[i]
            y[i + 1] = y[i] + ast
        if flag == 6:  # влево вверх
            if count > 0:
                x[i + 1] = x[i] - h
                y[i + 1] = y[i] + ast / 2
            else:
                flag = 0
                maxcount += 1
                x[i + 1] = (x[i] - h)
                y[i + 1] = (y[i] + ast / 2) + ast

        if count == 0:
            flag += 1
            count = maxcount
        else:
            count -= 1
    return x, y, maxcount + 2


def get_construction(Name, choice_complete=False, floor=5, extrafloor=0):
    """ {описание} """
    ready_structures = ['0', '1', '2', '3', '4', '5']

    if Name == '0':
        X = pd.DataFrame(
            {
                "id": [0],
                "mass": [10.],
                "length": [10.],
                "id_node": [[0, 1]],
                "r1": [[-5., 0., 0.]],
                "r2": [[5., 0., 0.]],
                "flag": [[1, 1]],
                "r_st": [[0., 0., 0.]],
            }
        )
        X_cont = pd.DataFrame(
            {
                "id": [0],
                "mass": [5],
                "length": [5.],
                "diam": [0.5],
                "r1": [[5., 0., 0.]],
                "r2": [[10., 0., 0.]],
                "flag_grab": [True],

            }
        )
        print(X)

        print(X_cont)
        return X, X_cont

    if Name == '1':
        N_beams_2 = 24 # Beams
        N_nodes_2 = 10 # Nodes

        a_beam = 5.0
        x_start = 0.6
        h = 0.5
        r_vpisannoj = a_beam/2/np.sqrt(3)
        R_opisannoj = a_beam/np.sqrt(3)
        h_beam = a_beam*np.sqrt(2/3)
        ast = 2*h/np.sqrt(3)

        r = np.array([[0.0 for i in range(3)] for j in range(N_nodes_2)]) # Beam coordinates; r[0,:] = [x,y,z]
        r[0,0] = 0; r[0,1] = 0; r[0,2] = 0  # Construction
        r[1,0] = h_beam; r[1,1] = 0.; r[1,2] = R_opisannoj
        r[2,0] = h_beam; r[2,1] = -a_beam/2; r[2,2] = -r_vpisannoj
        r[3,0] = h_beam; r[3,1] = a_beam/2; r[3,2] = -r_vpisannoj
        r[4,0] = h_beam + a_beam; r[4,1] = 0.; r[4,2] = R_opisannoj
        r[5,0] = h_beam + a_beam; r[5,1] = -a_beam/2; r[5,2] = -r_vpisannoj
        r[6,0] = h_beam + a_beam; r[6,1] = a_beam/2; r[6,2] = -r_vpisannoj
        r[7,0] = h_beam + 2*a_beam; r[7,1] = 0.; r[7,2] = R_opisannoj
        r[8,0] = h_beam + 2*a_beam; r[8,1] = -a_beam/2; r[8,2] = -r_vpisannoj
        r[9,0] = h_beam + 2*a_beam; r[9,1] = a_beam/2; r[9,2] = -r_vpisannoj
        m_of_beam = 5
        # Некомпакный вид
        X = pd.DataFrame(
            {
                "id": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
                "mass": [m_of_beam for i in range(N_beams_2)],
                "length": [0 for i in range(N_beams_2)],
                "id_node_1": [0,0,0,1,1,2,1,2,3,2,1,3,4,4,5,4,5,6,5,4,6,7,7,8],
                "id_node_2": [1,2,3,2,3,3,4,5,6,4,6,5,5,6,6,7,8,9,7,9,8,8,9,9],
                "x1": [r[0,0],r[0,0],r[0,0],r[1,0],r[1,0],r[2,0],r[1,0],r[2,0],r[3,0],r[2,0],r[1,0],r[3,0],r[4,0],r[4,0],r[5,0],r[4,0],r[5,0],r[6,0],r[5,0],r[4,0],r[6,0],r[7,0],r[7,0],r[8,0]],
                "y1": [r[0,1],r[0,1],r[0,1],r[1,1],r[1,1],r[2,1],r[1,1],r[2,1],r[3,1],r[2,1],r[1,1],r[3,1],r[4,1],r[4,1],r[5,1],r[4,1],r[5,1],r[6,1],r[5,1],r[4,1],r[6,1],r[7,1],r[7,1],r[8,1]],
                "z1": [r[0,2],r[0,2],r[0,2],r[1,2],r[1,2],r[2,2],r[1,2],r[2,2],r[3,2],r[2,2],r[1,2],r[3,2],r[4,2],r[4,2],r[5,2],r[4,2],r[5,2],r[6,2],r[5,2],r[4,2],r[6,2],r[7,2],r[7,2],r[8,2]],
                "x2": [r[1,0],r[2,0],r[3,0],r[2,0],r[3,0],r[3,0],r[4,0],r[5,0],r[6,0],r[4,0],r[6,0],r[5,0],r[5,0],r[6,0],r[6,0],r[7,0],r[8,0],r[9,0],r[7,0],r[9,0],r[8,0],r[8,0],r[9,0],r[9,0]],
                "y2": [r[1,1],r[2,1],r[3,1],r[2,1],r[3,1],r[3,1],r[4,1],r[5,1],r[6,1],r[4,1],r[6,1],r[5,1],r[5,1],r[6,1],r[6,1],r[7,1],r[8,1],r[9,1],r[7,1],r[9,1],r[8,1],r[8,1],r[9,1],r[9,1]],
                "z2": [r[1,2],r[2,2],r[3,2],r[2,2],r[3,2],r[3,2],r[4,2],r[5,2],r[6,2],r[4,2],r[6,2],r[5,2],r[5,2],r[6,2],r[6,2],r[7,2],r[8,2],r[9,2],r[7,2],r[9,2],r[8,2],r[8,2],r[9,2],r[9,2]],
                "flag_1": [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                "flag_2": [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                "x_st": [-x_start for i in range(N_beams_2)],
                "y_st": [2*h,3*h,3*h,2*h,1*h,-1*h,-2*h,-2*h,-2*h,-1*h,0,1*h,2*h,2*h,2*h,1*h,0,-1*h,-1*h,0,1*h,1*h,0,0],
                "z_st": [-2*ast,-0.5*ast,0.5*ast,2*ast,2.5*ast,1.5*ast,1*ast,0,-1*ast,-1.5*ast,-2*ast,-1.5*ast,-1*ast,0,1*ast,1.5*ast,2*ast,0.5*ast,-0.5*ast,-1*ast,-0.5*ast,0.5*ast,1*ast,0],
            }
        )
        # Преобразование к более компактному виду
        r1 = [[X.x1[i],X.y1[i],X.z1[i]] for i in range(len(X.z1))]
        r2 = [[X.x2[i],X.y2[i],X.z2[i]] for i in range(len(X.z2))]
        r_st = [[X.x_st[i],X.y_st[i],X.z_st[i]] for i in range(len(X.z_st))]
        id_node = [[X.id_node_1[i],X.id_node_2[i]] for i in range(len(X.id_node_2))]
        flag = [[X.flag_1[i],X.flag_2[i]] for i in range(len(X.flag_2))]
        X_2 = pd.DataFrame(
            {
                "id": X.id,
                "mass": X.mass,
                "length": X.length,
                "id_node": id_node,
                "r1": r1,
                "r2": r2,
                "flag": flag,
                "r_st": r_st,
            }
        )
        X_2.length = [np.linalg.norm(np.array(X_2.r1[i]) - np.array(X_2.r2[i])) for i in range(N_beams_2)]

        ########## > Грузовой отсек для конструкции < ##########
        X_cont_2 = pd.DataFrame(
            {
                "id": [0,1,2,3,4,5,6],
                "mass": [m_of_beam*300, m_of_beam,m_of_beam,m_of_beam,m_of_beam,m_of_beam,m_of_beam],
                "length": [0 for i in range(7)],
                "diam": [5.0,0.1,0.1,0.1,0.1,0.1,0.1],
                "r1": [[0.0,        0.0,  0.0],
                    [-x_start/2, 1.0,  6.0],
                    [-x_start/2, 1.0,  4.0],
                    [-x_start/2, -1.0, 4.0],
                    [-x_start/2, 1.0, -6.0],
                    [-x_start/2, 1.0, -4.0],
                    [-x_start/2, -1.0,-4.0]],
                "r2": [[-x_start,   0.0,   0.0],
                    [-x_start/2, -1.0,  6.0],
                    [-x_start/2, 1.0,   6.0],
                    [-x_start/2, -1.0,  6.0],
                    [-x_start/2, -1.0, -6.0],
                    [-x_start/2, 1.0,  -6.0],
                    [-x_start/2, -1.0, -6.0]],
                "flag_grab": [False, True, False, False, True, False, False],

            }
        )
        return X_2, X_cont_2

    if Name == '2' or Name not in ready_structures:
        # Math baseline
        a_beam = 5.0
        x_start = 0.6
        h = 0.5
        r_vpisannoj = a_beam/2/np.sqrt(3)
        R_opisannoj = a_beam/np.sqrt(3)
        h_beam = a_beam*np.sqrt(2/3)
        ast = 2*h/np.sqrt(3)
        m_of_beam = 50
        mass_per_l = 1
        t = 1 if choice_complete else 0

        # Constructing floors
        N_beams_2 = 3 + floor*3 + (floor-1)*6  # 66 ? 60
        N_nodes_2 = 1 + 3*floor  # 22

        r = np.array([[0.0 for i in range(3)] for j in range(N_nodes_2)])  # Beam coordinates; r[0,:] = [x,y,z]
        r[0, 0] = 0;                    r[0, 1] = 0;         r[0, 2] = 0
        r[1, 0] = h_beam;               r[1, 1] = 0.;        r[1, 2] = R_opisannoj
        r[2, 0] = h_beam;               r[2, 1] = -a_beam/2; r[2, 2] = -r_vpisannoj
        r[3, 0] = h_beam;               r[3, 1] = a_beam/2;  r[3, 2] = -r_vpisannoj
        x1 = [r[0,0],r[0,0],r[0,0],r[1,0],r[1,0],r[2,0]]
        y1 = [r[0,1],r[0,1],r[0,1],r[1,1],r[1,1],r[2,1]]
        z1 = [r[0,2],r[0,2],r[0,2],r[1,2],r[1,2],r[2,2]]
        x2 = [r[1,0],r[2,0],r[3,0],r[2,0],r[3,0],r[3,0]]
        y2 = [r[1,1],r[2,1],r[3,1],r[2,1],r[3,1],r[3,1]]
        z2 = [r[1,2],r[2,2],r[3,2],r[2,2],r[3,2],r[3,2]]
        id_node_1 = [0,0,0,1,1,2]
        id_node_2 = [1,2,3,2,3,3]
        for i in range(floor-1):
            r[3*i+4, 0] = h_beam + (i+1)*a_beam;      r[3*i+4, 1] = 0.;        r[3*i+4, 2] = R_opisannoj
            r[3*i+5, 0] = h_beam + (i+1)*a_beam;      r[3*i+5, 1] = -a_beam/2; r[3*i+5, 2] = -r_vpisannoj
            r[3*i+6, 0] = h_beam + (i+1)*a_beam;      r[3*i+6, 1] = a_beam/2;  r[3*i+6, 2] = -r_vpisannoj
            x1.append(r[3*i+1,0]); y1.append(r[3*i+1,1]); z1.append(r[3*i+1,2])  # Stright along Ox
            x2.append(r[3*i+4,0]); y2.append(r[3*i+4,1]); z2.append(r[3*i+4,2])
            x1.append(r[3*i+2,0]); y1.append(r[3*i+2,1]); z1.append(r[3*i+2,2])
            x2.append(r[3*i+5,0]); y2.append(r[3*i+5,1]); z2.append(r[3*i+5,2])
            x1.append(r[3*i+3,0]); y1.append(r[3*i+3,1]); z1.append(r[3*i+3,2])
            x2.append(r[3*i+6,0]); y2.append(r[3*i+6,1]); z2.append(r[3*i+6,2])

            x1.append(r[3*i+1,0]); y1.append(r[3*i+1,1]); z1.append(r[3*i+1,2])  # Oblique
            x2.append(r[3*i+6,0]); y2.append(r[3*i+6,1]); z2.append(r[3*i+6,2])
            x1.append(r[3*i+2,0]); y1.append(r[3*i+2,1]); z1.append(r[3*i+2,2])
            x2.append(r[3*i+4,0]); y2.append(r[3*i+4,1]); z2.append(r[3*i+4,2])
            x1.append(r[3*i+3,0]); y1.append(r[3*i+3,1]); z1.append(r[3*i+3,2])
            x2.append(r[3*i+5,0]); y2.append(r[3*i+5,1]); z2.append(r[3*i+5,2])

            x1.append(r[3*i+4,0]); y1.append(r[3*i+4,1]); z1.append(r[3*i+4,2])  # In Oyz
            x2.append(r[3*i+6,0]); y2.append(r[3*i+6,1]); z2.append(r[3*i+6,2])
            x1.append(r[3*i+5,0]); y1.append(r[3*i+5,1]); z1.append(r[3*i+5,2])
            x2.append(r[3*i+4,0]); y2.append(r[3*i+4,1]); z2.append(r[3*i+4,2])
            x1.append(r[3*i+6,0]); y1.append(r[3*i+6,1]); z1.append(r[3*i+6,2])
            x2.append(r[3*i+5,0]); y2.append(r[3*i+5,1]); z2.append(r[3*i+5,2])

            id_node_1.append(3*i+1); id_node_2.append(3*i+4)
            id_node_1.append(3*i+2); id_node_2.append(3*i+5)
            id_node_1.append(3*i+3); id_node_2.append(3*i+6)
            id_node_1.append(3*i+1); id_node_2.append(3*i+6)
            id_node_1.append(3*i+2); id_node_2.append(3*i+4)
            id_node_1.append(3*i+3); id_node_2.append(3*i+5)
            id_node_1.append(3*i+4); id_node_2.append(3*i+6)
            id_node_1.append(3*i+5); id_node_2.append(3*i+4)
            id_node_1.append(3*i+6); id_node_2.append(3*i+5)

        y_st, z_st, _ = package_beams(N_beams_2, 0.5)
        X = pd.DataFrame(
            {
                "id": [i for i in range(N_beams_2)],
                "mass": [m_of_beam for i in range(N_beams_2)],
                "length": [0 for i in range(N_beams_2)],
                "id_node_1": id_node_1,
                "id_node_2": id_node_2,
                "x1": x1,
                "y1": y1,
                "z1": z1,
                "x2": x2,
                "y2": y2,
                "z2": z2,
                "flag_1": [t for i in range(N_beams_2)],
                "flag_2": [t for i in range(N_beams_2)],
                "x_st": [-x_start for i in range(N_beams_2)],
                "y_st": y_st,
                "z_st": z_st,
            }
        )

        # Converting to more compact form
        r1 = [[X.x1[i],X.y1[i],X.z1[i]] for i in range(len(X.z1))]
        r2 = [[X.x2[i],X.y2[i],X.z2[i]] for i in range(len(X.z2))]
        r_st = [[X.x_st[i],X.y_st[i],X.z_st[i]] for i in range(len(X.z_st))]
        id_node = [[X.id_node_1[i],X.id_node_2[i]] for i in range(len(X.id_node_2))]
        flag = [[X.flag_1[i],X.flag_2[i]] for i in range(len(X.flag_2))]
        X_2 = pd.DataFrame(
            {
                "id": X.id,
                "mass": X.mass,
                "length": X.length,
                "id_node": id_node,
                "r1": r1,
                "r2": r2,
                "flag": flag,
                "r_st": r_st,
            }
        )
        X_2.length = [np.linalg.norm(np.array(X_2.r1[i]) - np.array(X_2.r2[i])) for i in range(N_beams_2)]
        X_2.mass = [X_2.length[i] * mass_per_l for i in range(N_beams_2)]

        # Cargo box for structure
        X_cont_2 = pd.DataFrame(
            {
                "id": [0,1,2,3,4,5,6],
                "mass": [m_of_beam*3, m_of_beam/10,m_of_beam/10,m_of_beam/10,m_of_beam/10,m_of_beam/10,m_of_beam/10],
                "length": [0 for i in range(7)],
                "diam": [5.0,0.1,0.1,0.1,0.1,0.1,0.1],
                "r1": [[0.0,        0.0,  0.0],
                       [-x_start/2, 1.0,  6.0],
                       [-x_start/2, 1.0,  4.0],
                       [-x_start/2, -1.0, 4.0],
                       [-x_start/2, 1.0, -6.0],
                       [-x_start/2, 1.0, -4.0],
                       [-x_start/2, -1.0,-4.0]],
                "r2": [[-x_start,   0.0,   0.0],
                       [-x_start/2, -1.0,  6.0],
                       [-x_start/2, 1.0,   6.0],
                       [-x_start/2, -1.0,  6.0],
                       [-x_start/2, -1.0, -6.0],
                       [-x_start/2, 1.0,  -6.0],
                       [-x_start/2, -1.0, -6.0]],
                "flag_grab": [False, True, False, False, True, False, False],

            }
        )
        return X_2, X_cont_2

    if Name == '3':
        # Beam construction
        L = 5

        N_beams_3 = 84  # Beams
        N_nodes_3 = 32  # Nodes
        m_of_beam = 10
        mass_per_l = 1
        x_start = 0.4
        h = 0.15
        R = L * 6
        a = 2 * np.arcsin(L / 2 / R)
        N = 3
        angle = np.linspace(a, a * N, N)
        y_list = [R * np.sin(angle[i]) for i in range(N)]
        x_list = [R - R * np.cos(angle[i]) for i in range(N)]
        z_list = [0. for i in range(N)]
        for j in range(5):
            y_list = np.append(y_list, y_list[0] * np.cos(2 * np.pi * (j + 1) / 6))
            y_list = np.append(y_list, y_list[1] * np.cos(2 * np.pi * (j + 1) / 6))
            y_list = np.append(y_list, y_list[2] * np.cos(2 * np.pi * (j + 1) / 6))
            z_list = np.append(z_list, y_list[0] * np.sin(2 * np.pi * (j + 1) / 6))
            z_list = np.append(z_list, y_list[1] * np.sin(2 * np.pi * (j + 1) / 6))
            z_list = np.append(z_list, y_list[2] * np.sin(2 * np.pi * (j + 1) / 6))
            x_list = np.append(x_list, x_list[0])
            x_list = np.append(x_list, x_list[1])
            x_list = np.append(x_list, x_list[2])
        for j in range(6):
            y_list = np.append(y_list, y_list[1] * np.cos(2 * np.pi * (j + 1 / 2) / 6))
            y_list = np.append(y_list, y_list[2] * np.cos(2 * np.pi * (j + 1 / 2) / 6))
            z_list = np.append(z_list, y_list[1] * np.sin(2 * np.pi * (j + 1 / 2) / 6))
            z_list = np.append(z_list, y_list[2] * np.sin(2 * np.pi * (j + 1 / 2) / 6))
            x_list = np.append(x_list, x_list[1])
            x_list = np.append(x_list, x_list[2])

        y_list = np.append(y_list, 0.)
        x_list = np.append(x_list, 0.)
        z_list = np.append(z_list, 0.)
        y_list = np.append(y_list, 0.)
        x_list = np.append(x_list, 10.)
        z_list = np.append(z_list, 0.)
        x = x_list
        y = y_list
        z = z_list
        id_node_1 = [30,30,30,30,30,30,15,0,3,6,9, 12,15,15,0, 0,0, 3, 3,3, 6, 6,6, 9, 9, 9, 12,12,12,15,26,16,
                              28,1,18,4,20,7,22,10,24,13,26,16,16,16,28,1, 1,1, 18,4, 4,4, 20,7, 7,7, 22,10,10,10,24,13,
                              13,13,27,17,29,2,19,5,21,8,23,11,25,14,0, 3, 6, 9, 12,15]
        id_node_2 = [0, 3, 6, 9, 12,15,0, 3,6,9,12,15,16,28,28,1,18,18,4,20,20,7,22,22,10,24,24,13,26,26,16,28,
                              1,18,4,20,7,22,10,24,13,26,27,27,17,29,29,29,2,19,19,19,5,21,21,21,8,23,23,23,11,25,25,25,
                              14,27,17,29,2,19,5,21,8,23,11,25,14,27,31,31,31,31,31,31]
        y_st, z_st, lvl = package_beams(N_beams_3, h)

        tmp_if = 1 if choice_complete else 0
        X = pd.DataFrame(
            {
                "id": [i for i in range(N_beams_3)],
                "mass": [m_of_beam for i in range(N_beams_3)],
                "length": [0. for i in range(N_beams_3)],
                "id_node_1": id_node_1,
                "id_node_2": id_node_2,
                "x1": [x[id_node_1[i]] for i in range(N_beams_3)],
                "y1": [y[id_node_1[i]] for i in range(N_beams_3)],
                "z1": [z[id_node_1[i]] for i in range(N_beams_3)],
                "x2": [x[id_node_2[i]] for i in range(N_beams_3)],
                "y2": [y[id_node_2[i]] for i in range(N_beams_3)],
                "z2": [z[id_node_2[i]] for i in range(N_beams_3)],
                "flag_1": [tmp_if for i in range(N_beams_3)],
                "flag_2": [tmp_if for i in range(N_beams_3)],
                "x_st": [-x_start for i in range(N_beams_3)],
                "y_st": y_st,
                "z_st": z_st,
            }
        )

        # Converting to more compact form
        r1 = [[X.x1[i], X.y1[i], X.z1[i]] for i in range(len(X.z1))]
        r2 = [[X.x2[i], X.y2[i], X.z2[i]] for i in range(len(X.z2))]
        r_st = [[X.x_st[i], X.y_st[i], X.z_st[i]] for i in range(len(X.z_st))]
        id_node = [[X.id_node_1[i], X.id_node_2[i]] for i in range(len(X.id_node_2))]
        flag = [[X.flag_1[i], X.flag_2[i]] for i in range(len(X.flag_2))]
        X_3 = pd.DataFrame(
            {
                "id": X.id,
                "mass": X.mass,
                "length": X.length,
                "id_node": id_node,
                "r1": r1,
                "r2": r2,
                "flag": flag,
                "r_st": r_st,
            }
        )
        L_around = 12.
        X_3.length = [np.linalg.norm(np.array(X_3.r1[i]) - np.array(X_3.r2[i])) for i in range(N_beams_3)]
        X_3.mass = [X_3.length[i] * mass_per_l for i in range(N_beams_3)]
        X_3.r_st = [[-x_start - L_around + X_3.length[i], X.y_st[i], X.z_st[i]] for i in range(N_beams_3)]

        # Cargo box for structure
        X_cont_3 = pd.DataFrame(
            {
                "id": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                "mass": [1e2, m_of_beam, m_of_beam, m_of_beam, m_of_beam, m_of_beam,
                         m_of_beam, m_of_beam, m_of_beam, m_of_beam, m_of_beam, m_of_beam, m_of_beam],
                "length": [0 for i in range(13)],
                "diam": [5.0, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                "r1": [[0.0, 0.0, 0.0],
                       [-x_start / 2, 1.0, 6.0],
                       [-x_start / 2, 1.0, 4.0],
                       [-x_start / 2, -1.0, 4.0],
                       [-x_start / 2, 1.0, -6.0],
                       [-x_start / 2, 1.0, -4.0],
                       [-x_start / 2, -1.0, -4.0],
                       [-x_start / 2, -6.0, 1.0],
                       [-x_start / 2, -4.0, 1.0],
                       [-x_start / 2, -4.0, -1.0],
                       [-x_start / 2, 6.0, 1.0],
                       [-x_start / 2, 4.0, 1.0],
                       [-x_start / 2, 4.0, -1.0]
                       ],
                "r2": [[-x_start, 0.0, 0.0],
                       [-x_start / 2, -1.0, 6.0],
                       [-x_start / 2, 1.0, 6.0],
                       [-x_start / 2, -1.0, 6.0],
                       [-x_start / 2, -1.0, -6.0],
                       [-x_start / 2, 1.0, -6.0],
                       [-x_start / 2, -1.0, -6.0],
                       [-x_start / 2, -6.0, -1.0],
                       [-x_start / 2, -6.0, 1.0],
                       [-x_start / 2, -6.0, -1.0],
                       [-x_start / 2, 6.0, -1.0],
                       [-x_start / 2, 6.0, 1.0],
                       [-x_start / 2, 6.0, -1.0]
                       ],
                "flag_grab": [False, True, False, False, True, False, False, True, False, False, True, False, False],

            }
        )
        N_around = 100
        R_around = 1.5
        D_around = 0.05
        X_cont_extra = pd.DataFrame(
            {
                "id": [13 + i for i in range(N_around)],
                "mass": [m_of_beam * 1e2 for i in range(N_around)],
                "length": [0 for i in range(N_around)],
                "diam": [D_around for i in range(N_around)],
                "r1": [[-x_start, R_around*np.cos(i/N_around*2*np.pi), R_around*np.sin(i/N_around*2*np.pi)]
                       for i in range(N_around)],
                "r2": [[-x_start - L_around, R_around*np.cos(i/N_around*2*np.pi), R_around*np.sin(i/N_around*2*np.pi)]
                       for i in range(N_around)],
                "flag_grab": [False for i in range(N_around)],

            }
        )
        X_cont_3 = pd.concat([X_cont_3, X_cont_extra], sort=False, axis=0, ignore_index=True)
        N_ = int((lvl) * 2)
        r1 = [[-x_start - L_around * 0.92, 0., 0.] for i in range(N_)]
        r2 = [[-x_start - L_around * 0.92, 0., 0.] for i in range(N_)]
        for ii in range(lvl):
            r1[ii][1] = h*(ii+1/2); r1[ii][2] =  np.sqrt(R_around**2 - r1[ii][1]**2)
            r2[ii][1] = h*(ii+1/2); r2[ii][2] = -np.sqrt(R_around**2 - r2[ii][1]**2)
            r1[ii+lvl][1] = -h*(ii+1/2); r1[ii+lvl][2] =  np.sqrt(R_around**2 - r1[ii+lvl][1]**2)
            r2[ii+lvl][1] = -h*(ii+1/2); r2[ii+lvl][2] = -np.sqrt(R_around**2 - r2[ii+lvl][1]**2)
        X_cont_extra = pd.DataFrame(
            {
                "id": [83 + i for i in range(N_)],
                "mass": [m_of_beam / 2 for i in range(N_)],
                "length": [0 for i in range(N_)],
                "diam": [D_around/2 for i in range(N_)],
                "r1": r1,
                "r2": r2,
                "flag_grab": [False for i in range(N_)],

            }
        )
        X_cont_3 = pd.concat([X_cont_3, X_cont_extra], sort=False, axis=0, ignore_index=True)
        M = np.array([[1.,0.,0.],[0.,-1/2,-np.sqrt(3)/2],[0.,np.sqrt(3)/2,-1/2]])
        r1 = [M @ np.array(r1[i]) for i in range(N_)]
        r2 = [M @ np.array(r2[i]) for i in range(N_)]
        X_cont_extra = pd.DataFrame(
            {
                "id": [83 + i for i in range(N_)],
                "mass": [m_of_beam / 2 for i in range(N_)],
                "length": [0 for i in range(N_)],
                "diam": [D_around/2 for i in range(N_)],
                "r1": r1,
                "r2": r2,
                "flag_grab": [False for i in range(N_)],

            }
        )
        X_cont_3 = pd.concat([X_cont_3, X_cont_extra], sort=False, axis=0, ignore_index=True)        
        r1 = [M @ np.array(r1[i]) for i in range(N_)]
        r2 = [M @ np.array(r2[i]) for i in range(N_)]
        X_cont_extra = pd.DataFrame(
            {
                "id": [83 + i for i in range(N_)],
                "mass": [m_of_beam / 2 for i in range(N_)],
                "length": [0 for i in range(N_)],
                "diam": [D_around/2 for i in range(N_)],
                "r1": r1,
                "r2": r2,
                "flag_grab": [False for i in range(N_)],

            }
        )
        X_cont_3 = pd.concat([X_cont_3, X_cont_extra], sort=False, axis=0, ignore_index=True)
        '''X_cont_extra = pd.DataFrame(
            {
                "id": [100, 101],
                "mass": [1e7, 1e7],
                "length": [0, 0],
                "diam": [D_around*3, D_around*3],
                "r1": [np.array([-0.6, 4., 0.]), np.array([-0.6, -4., 0.])],
                "r2": [np.array([-10., 4., 0.]), np.array([-10., -4., 0.])],
                "flag_grab": [False, False],

            }
        )
        X_cont_3 = pd.concat([X_cont_3, X_cont_extra], sort=False, axis=0, ignore_index=True)'''

        return X_3, X_cont_3

    if Name == '4':
        # Первый час ночи. Я должен спать так то
        L = 5

        N_beams_4 = 16  # Beams
        mass_per_l = 1
        m_of_beam = 50
        x_start = 0.6
        h = 0.15
        tmp_if = 1 if choice_complete else 0

        id_ = [i for i in range(N_beams_4)]
        mass_ = [m_of_beam for i in range(N_beams_4)]
        len_ = [0. for i in range(N_beams_4)]
        id_1_ = [0,0,0,0,1,1,2,3,0,0,0,0,5+floor*4,5+floor*4,6+floor*4,7+floor*4]
        id_2_ = [1,2,3,4,4,2,3,4,5+floor*4,6+floor*4,7+floor*4,8+floor*4,8+floor*4,6+floor*4,7+floor*4,8+floor*4]
        x1_ = [0.,0.,0.,0.,0.,0.,0.,L,0.,0.,0.,0.,0.,0.,0.,L]
        y1_ = [0.,0.,0.,0.,-L/2,L/2,L/2,-L/2,0.,0.,0.,0.,-L/2,L/2,L/2,-L/2]
        z1_ = [0.,0.,0.,0.,L,L,L,L,0.,0.,0.,0.,-L,-L,-L,-L]
        x2_ = [0.,0.,L,L,L,0.,L,L, 0.,0.,L,L,L,0.,L,L]
        y2_ = [-L/2,L/2,-L/2,L/2,-L/2,-L/2,L/2,L/2, -L/2,L/2,L/2,-L/2,-L/2,-L/2,L/2,L/2]
        z2_ = [L,L,L,L,L,L,L,L,-L,-L,-L,-L,-L,-L,-L,-L]
        flag_ = [tmp_if for i in range(N_beams_4)]
        y_ = [0. for i in range(N_beams_4)]

        for i in range(floor):
            for j in range(12):
                id_.append(N_beams_4+j+12*i+1)
                mass_.append(m_of_beam)
                len_.append(0)
                y_.append(0)
                flag_.append(tmp_if)
            id_1_ = np.append(id_1_, [1+i*4,2+i*4,3+i*4,4+i*4,1+i*4,2+i*4,3+i*4,4+i*4,5+i*4,6+i*4,7+i*4,5+i*4])
            id_2_ = np.append(id_2_, [5+i*4,6+i*4,7+i*4,8+i*4,8+i*4,5+i*4,6+i*4,7+i*4,6+i*4,7+i*4,8+i*4,8+i*4])
            x1_ = np.append(x1_, [0.,0.,L,L,0.,0.,L,L,0.,0.,L,0.])
            y1_ = np.append(y1_, [-L/2,L/2,L/2,-L/2,-L/2,L/2,L/2,-L/2,-L/2,L/2,L/2,-L/2])
            z1_ = np.append(z1_, [(i+1)*L,(i+1)*L,(i+1)*L,(i+1)*L,(i+1)*L,(i+1)*L,(i+1)*L,(i+1)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L])
            x2_ = np.append(x2_, [0.,0.,L,L,L,0.,0.,L,0.,L,L,L])
            y2_ = np.append(y2_, [-L/2,L/2,L/2,-L/2,-L/2,-L/2,L/2,L/2,L/2,L/2,-L/2,-L/2])
            z2_ = np.append(z2_, [(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L])
            N_beams_4 += 12
        for i in range(floor):
            for j in range(12):
                id_.append(N_beams_4+j+12*i+1+12*floor)
                mass_.append(m_of_beam)
                len_.append(0)
                y_.append(0)
                flag_.append(tmp_if)
            id_1_ = np.append(id_1_, np.array([1+i*4,2+i*4,3+i*4,4+i*4,1+i*4,2+i*4,3+i*4,4+i*4,5+i*4,6+i*4,7+i*4,5+i*4]) + (floor+1)*4)
            id_2_ = np.append(id_2_, np.array([5+i*4,6+i*4,7+i*4,8+i*4,8+i*4,5+i*4,6+i*4,7+i*4,6+i*4,7+i*4,8+i*4,8+i*4]) + (floor+1)*4)
            x1_ = np.append(x1_, [0.,0.,L,L,0.,0.,L,L,0.,0.,L,0.])
            y1_ = np.append(y1_, [-L/2,L/2,L/2,-L/2,-L/2,L/2,L/2,-L/2,-L/2,L/2,L/2,-L/2])
            z1_ = np.append(z1_, -np.array([(i+1)*L,(i+1)*L,(i+1)*L,(i+1)*L,(i+1)*L,(i+1)*L,(i+1)*L,(i+1)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L]))
            x2_ = np.append(x2_, [0.,0.,L,L,L,0.,0.,L,0.,L,L,L])
            y2_ = np.append(y2_, [-L/2,L/2,L/2,-L/2,-L/2,-L/2,L/2,L/2,L/2,L/2,-L/2,-L/2])
            z2_ = np.append(z2_, -np.array([(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L,(i+2)*L]))
            N_beams_4 += 12
            last_id = 8+i*4 + (floor+1)*4

        R_circle = L*(floor+1)

        RISE = 2
        L*=RISE
        floor_circle = round(2*np.pi*floor/RISE)
        phi = -np.pi*2/floor_circle
        r_8 = np.array([0., -L/2, R_circle])
        r_5 = np.array([0., -L/2, R_circle+L])
        r_7 = np.array([0., L/2, R_circle])
        r_6 = np.array([0., L/2, R_circle+L])
        M1 = np.array([[np.cos(phi),0.,np.sin(phi)],[0.,1.,0.],[-np.sin(phi),0.,np.cos(phi)]])
        for i in range(floor_circle):
            for j in range(12):
                id_.append(last_id+j+1)
                mass_.append(m_of_beam)
                len_.append(0)
                y_.append(0)
                flag_.append(tmp_if)
            r_1 = r_5.copy(); r_2 = r_6.copy(); r_3 = r_7.copy(); r_4 = r_8.copy()
            r_5 = M1 @ r_5; r_6 = M1 @ r_6; r_7 = M1 @ r_7; r_8 = M1 @ r_8; 
            id_1_ = np.append(id_1_, np.array([1+i*4,2+i*4,3+i*4,4+i*4,1+i*4,2+i*4,3+i*4,4+i*4,5+i*4,6+i*4,7+i*4,5+i*4]) + 1+(last_id+1)*4)
            id_2_ = np.append(id_2_, np.array([5+i*4,6+i*4,7+i*4,8+i*4,8+i*4,5+i*4,6+i*4,7+i*4,6+i*4,7+i*4,8+i*4,8+i*4]) + 1+(last_id+1)*4)
            x1_ = np.append(x1_, [r_1[0],r_2[0],r_3[0],r_4[0],r_1[0],r_2[0],r_3[0],r_4[0],r_5[0],r_6[0],r_7[0],r_5[0]])
            y1_ = np.append(y1_, [r_1[1],r_2[1],r_3[1],r_4[1],r_1[1],r_2[1],r_3[1],r_4[1],r_5[1],r_6[1],r_7[1],r_5[1]])
            z1_ = np.append(z1_, [r_1[2],r_2[2],r_3[2],r_4[2],r_1[2],r_2[2],r_3[2],r_4[2],r_5[2],r_6[2],r_7[2],r_5[2]])
            x2_ = np.append(x2_, [r_5[0],r_6[0],r_7[0],r_8[0],r_8[0],r_5[0],r_6[0],r_7[0],r_6[0],r_7[0],r_8[0],r_8[0]])
            y2_ = np.append(y2_, [r_5[1],r_6[1],r_7[1],r_8[1],r_8[1],r_5[1],r_6[1],r_7[1],r_6[1],r_7[1],r_8[1],r_8[1]])
            z2_ = np.append(z2_, [r_5[2],r_6[2],r_7[2],r_8[2],r_8[2],r_5[2],r_6[2],r_7[2],r_6[2],r_7[2],r_8[2],r_8[2]])
            N_beams_4 += 12
        for e in range(extrafloor):
            for i in range(floor_circle):
                for j in range(12):
                    id_.append(last_id+j+1)
                    mass_.append(m_of_beam)
                    len_.append(0)
                    y_.append(0)
                    flag_.append(tmp_if)
                r_1 = r_5.copy(); r_2 = r_6.copy(); r_3 = r_7.copy(); r_4 = r_8.copy()
                r_5 = M1 @ r_5; r_6 = M1 @ r_6; r_7 = M1 @ r_7; r_8 = M1 @ r_8; 
                id_1_ = np.append(id_1_, np.array([1+i*4,2+i*4,3+i*4,4+i*4,1+i*4,2+i*4,3+i*4,4+i*4,5+i*4,6+i*4,7+i*4,5+i*4]) + 1+(last_id+1)*4)
                id_2_ = np.append(id_2_, np.array([5+i*4,6+i*4,7+i*4,8+i*4,8+i*4,5+i*4,6+i*4,7+i*4,6+i*4,7+i*4,8+i*4,8+i*4]) + 1+(last_id+1)*4)
                x1_ = np.append(x1_, [r_1[0],r_2[0],r_3[0],r_4[0],r_1[0],r_2[0],r_3[0],r_4[0],r_5[0],r_6[0],r_7[0],r_5[0]])
                y1_ = np.append(y1_, (e+1)*L + np.array([r_1[1],r_2[1],r_3[1],r_4[1],r_1[1],r_2[1],r_3[1],r_4[1],r_5[1],r_6[1],r_7[1],r_5[1]]))
                z1_ = np.append(z1_, [r_1[2],r_2[2],r_3[2],r_4[2],r_1[2],r_2[2],r_3[2],r_4[2],r_5[2],r_6[2],r_7[2],r_5[2]])
                x2_ = np.append(x2_, [r_5[0],r_6[0],r_7[0],r_8[0],r_8[0],r_5[0],r_6[0],r_7[0],r_6[0],r_7[0],r_8[0],r_8[0]])
                y2_ = np.append(y2_, (e+1)*L + np.array([r_5[1],r_6[1],r_7[1],r_8[1],r_8[1],r_5[1],r_6[1],r_7[1],r_6[1],r_7[1],r_8[1],r_8[1]]))
                z2_ = np.append(z2_, [r_5[2],r_6[2],r_7[2],r_8[2],r_8[2],r_5[2],r_6[2],r_7[2],r_6[2],r_7[2],r_8[2],r_8[2]])
                N_beams_4 += 12
            for i in range(floor_circle):
                for j in range(12):
                    id_.append(last_id+j+1)
                    mass_.append(m_of_beam)
                    len_.append(0)
                    y_.append(0)
                    flag_.append(tmp_if)
                r_1 = r_5.copy(); r_2 = r_6.copy(); r_3 = r_7.copy(); r_4 = r_8.copy()
                r_5 = M1 @ r_5; r_6 = M1 @ r_6; r_7 = M1 @ r_7; r_8 = M1 @ r_8; 
                id_1_ = np.append(id_1_, np.array([1+i*4,2+i*4,3+i*4,4+i*4,1+i*4,2+i*4,3+i*4,4+i*4,5+i*4,6+i*4,7+i*4,5+i*4]) + 1+(last_id+1)*4)
                id_2_ = np.append(id_2_, np.array([5+i*4,6+i*4,7+i*4,8+i*4,8+i*4,5+i*4,6+i*4,7+i*4,6+i*4,7+i*4,8+i*4,8+i*4]) + 1+(last_id+1)*4)
                x1_ = np.append(x1_, [r_1[0],r_2[0],r_3[0],r_4[0],r_1[0],r_2[0],r_3[0],r_4[0],r_5[0],r_6[0],r_7[0],r_5[0]])
                y1_ = np.append(y1_, -(e+1)*L + np.array([r_1[1],r_2[1],r_3[1],r_4[1],r_1[1],r_2[1],r_3[1],r_4[1],r_5[1],r_6[1],r_7[1],r_5[1]]))
                z1_ = np.append(z1_, [r_1[2],r_2[2],r_3[2],r_4[2],r_1[2],r_2[2],r_3[2],r_4[2],r_5[2],r_6[2],r_7[2],r_5[2]])
                x2_ = np.append(x2_, [r_5[0],r_6[0],r_7[0],r_8[0],r_8[0],r_5[0],r_6[0],r_7[0],r_6[0],r_7[0],r_8[0],r_8[0]])
                y2_ = np.append(y2_, -(e+1)*L + np.array([r_5[1],r_6[1],r_7[1],r_8[1],r_8[1],r_5[1],r_6[1],r_7[1],r_6[1],r_7[1],r_8[1],r_8[1]]))
                z2_ = np.append(z2_, [r_5[2],r_6[2],r_7[2],r_8[2],r_8[2],r_5[2],r_6[2],r_7[2],r_6[2],r_7[2],r_8[2],r_8[2]])
                N_beams_4 += 12


        X = pd.DataFrame(
            {
                "id": id_,
                "mass": mass_,
                "length": len_,
                "id_node_1": id_1_,
                "id_node_2": id_2_,
                "x1": x1_,
                "y1": y1_,
                "z1": z1_,
                "x2": x2_,
                "y2": y2_,
                "z2": z2_,
                "flag_1": flag_,
                "flag_2": flag_,
                "x_st": y_,
                "y_st": y_,
                "z_st": y_,
            }
        )
        # Converting to more compact form
        r1 = [[X.x1[i], X.y1[i], X.z1[i]] for i in range(len(X.z1))]
        r2 = [[X.x2[i], X.y2[i], X.z2[i]] for i in range(len(X.z2))]
        r_st = [[X.x_st[i], X.y_st[i], X.z_st[i]] for i in range(len(X.z_st))]
        id_node = [[X.id_node_1[i], X.id_node_2[i]] for i in range(len(X.id_node_2))]
        flag = [[X.flag_1[i], X.flag_2[i]] for i in range(len(X.flag_2))]
        X_4 = pd.DataFrame(
            {
                "id": X.id,
                "mass": X.mass,
                "length": X.length,
                "id_node": id_node,
                "r1": r1,
                "r2": r2,
                "flag": flag,
                "r_st": r_st,
            }
        )
        y_st, z_st, lvl = package_beams(N_beams_4, h)
        L_around = 20.
        X_4.length = [np.linalg.norm(np.array(X_4.r1[i]) - np.array(X_4.r2[i])) for i in range(N_beams_4)]
        X_4.mass = [X_4.length[i] * mass_per_l for i in range(N_beams_4)]
        X_4.r_st = [[-x_start - L_around + X_4.length[i], y_st[i], z_st[i]] for i in range(N_beams_4)]
        X_4.id = [i for i in range(N_beams_4)]
        
        R_cont = h * lvl *1.5  # 10.
        X_cont_4 = pd.DataFrame(
            {
                "id": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                "mass": [m_of_beam * 5, m_of_beam / 10, m_of_beam / 10, m_of_beam / 10, m_of_beam / 10, m_of_beam / 10,
                         m_of_beam / 10, m_of_beam / 10, m_of_beam / 10, m_of_beam / 10, m_of_beam / 10, m_of_beam / 10,
                         m_of_beam / 10],
                "length": [0 for i in range(13)],
                "diam": [R_cont, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03],
                "r1": [[0.0, 0.0, 0.0],
                       [-x_start / 2, 1.0, R_cont+1],
                       [-x_start / 2, 1.0, R_cont-1],
                       [-x_start / 2, -1.0, R_cont-1],
                       [-x_start / 2, 1.0, -R_cont-1],
                       [-x_start / 2, 1.0, -R_cont+1],
                       [-x_start / 2, -1.0, -R_cont+1],
                       [-x_start / 2, -R_cont-1, 1.0],
                       [-x_start / 2, -R_cont+1, 1.0],
                       [-x_start / 2, -R_cont+1, -1.0],  
                       [-x_start / 2, R_cont+1, 1.0],
                       [-x_start / 2, R_cont-1, 1.0],
                       [-x_start / 2, R_cont-1, -1.0]
                       ],
                "r2": [[-x_start, 0.0, 0.0],
                       [-x_start / 2, -1.0, R_cont+1],
                       [-x_start / 2, 1.0, R_cont+1],
                       [-x_start / 2, -1.0, R_cont+1],
                       [-x_start / 2, -1.0, -R_cont-1],
                       [-x_start / 2, 1.0, -R_cont-1],
                       [-x_start / 2, -1.0, -R_cont-1],
                       [-x_start / 2, -R_cont-1, -1.0],
                       [-x_start / 2, -R_cont-1, 1.0],
                       [-x_start / 2, -R_cont-1, -1.0], 
                       [-x_start / 2, R_cont+1, -1.0],
                       [-x_start / 2, R_cont+1, 1.0],
                       [-x_start / 2, R_cont+1, -1.0]
                       ],
                "flag_grab": [False, True, False, False, True, False, False, True, False, False, True, False, False],

            }
        )
        X_cont_4.length = [np.linalg.norm(np.array(X_cont_4.r1[i]) - np.array(X_cont_4.r2[i])) for i in range(13)]
        # print(X_cont_4)

        
        
        R_around = R_cont - 0.5
        D_around = 0.05
        N_around = round(2*np.pi*R_around/D_around * 0.6)  # 120
        X_cont_extra = pd.DataFrame(
            {
                "id": [13 + i for i in range(N_around)],
                "mass": [m_of_beam / 50 for i in range(N_around)],
                "length": [0 for i in range(N_around)],
                "diam": [D_around for i in range(N_around)],
                "r1": [[-x_start, R_around*np.cos(i/N_around*2*np.pi), R_around*np.sin(i/N_around*2*np.pi)]
                       for i in range(N_around)],
                "r2": [[-x_start - L_around, R_around*np.cos(i/N_around*2*np.pi), R_around*np.sin(i/N_around*2*np.pi)]
                       for i in range(N_around)],
                "flag_grab": [False for i in range(N_around)],

            }
        )
        X_cont_4 = pd.concat([X_cont_4, X_cont_extra], sort=False, axis=0, ignore_index=True)
        N_ = int((lvl) * 2)
        r1 = [[-x_start - L_around + 0.3, 0., 0.] for i in range(N_)]
        r2 = [[-x_start - L_around + 0.3, 0., 0.] for i in range(N_)]
        for ii in range(lvl):
            r1[ii][1] = h*(ii+1/2); r1[ii][2] =  np.sqrt(R_around**2 - r1[ii][1]**2)
            r2[ii][1] = h*(ii+1/2); r2[ii][2] = -np.sqrt(R_around**2 - r2[ii][1]**2)
            r1[ii+lvl][1] = -h*(ii+1/2); r1[ii+lvl][2] =  np.sqrt(R_around**2 - r1[ii+lvl][1]**2)
            r2[ii+lvl][1] = -h*(ii+1/2); r2[ii+lvl][2] = -np.sqrt(R_around**2 - r2[ii+lvl][1]**2)
        X_cont_extra = pd.DataFrame(
            {
                "id": [83 + i for i in range(N_)],
                "mass": [m_of_beam / 50 for i in range(N_)],
                "length": [0 for i in range(N_)],
                "diam": [D_around/2 for i in range(N_)],
                "r1": r1,
                "r2": r2,
                "flag_grab": [False for i in range(N_)],

            }
        )
        X_cont_4 = pd.concat([X_cont_4, X_cont_extra], sort=False, axis=0, ignore_index=True)
        M = np.array([[1.,0.,0.],[0.,-1/2,-np.sqrt(3)/2],[0.,np.sqrt(3)/2,-1/2]])
        r1 = [M @ np.array(r1[i]) for i in range(N_)]
        r2 = [M @ np.array(r2[i]) for i in range(N_)]
        X_cont_extra = pd.DataFrame(
            {
                "id": [83 + i for i in range(N_)],
                "mass": [m_of_beam / 50 for i in range(N_)],
                "length": [0 for i in range(N_)],
                "diam": [D_around/2 for i in range(N_)],
                "r1": r1,
                "r2": r2,
                "flag_grab": [False for i in range(N_)],

            }
        )
        X_cont_4 = pd.concat([X_cont_4, X_cont_extra], sort=False, axis=0, ignore_index=True)        
        r1 = [M @ np.array(r1[i]) for i in range(N_)]
        r2 = [M @ np.array(r2[i]) for i in range(N_)]
        X_cont_extra = pd.DataFrame(
            {
                "id": [83 + i for i in range(N_)],
                "mass": [m_of_beam / 50 for i in range(N_)],
                "length": [0 for i in range(N_)],
                "diam": [D_around/2 for i in range(N_)],
                "r1": r1,
                "r2": r2,
                "flag_grab": [False for i in range(N_)],
            }
        )
        X_cont_4 = pd.concat([X_cont_4, X_cont_extra], sort=False, axis=0, ignore_index=True) 
        return X_4, X_cont_4

    if Name == '5':
        direction = ['+2', '-0', '+1', '+0', '-2', '-0', '-1', '-2', '+0', '-1', '+0', '+1', '+2', '-1', '+2',
                     '-0', '-2', '-0', '+2', '+2', '+1', '+0', '+1', '+0', '-1', '-2', '+1', '-2', '+1', '-0',
                     '-2', '-1', '-0', '+1', '+2', '-0', '-1', '+2', '+1', '+0', '+2', '+0', '-2', '+0', '+2']
        id = [i for i in range(len(direction)+1)]
        r1 = []
        r2 = []
        point = np.array([0., 0., 0.])
        for i in range(len(direction)):
            r1.append(point.copy())
            s = 1. if direction[i][0] == '+' else -1.
            point[int(direction[i][1])] += s * 4.
            r2.append(point.copy())
        print(f"r1: {r1}")
        print(f"r2: {r2}")
        X = pd.DataFrame(
            {
                "id": [0],
                "mass": [5.],
                "length": [1.],
                "id_node": [[0, 1]],
                "r1": [r2[len(r2)-1]],
                "r2": [r2[len(r2)-1] + [0., 0., 1.]],
                "flag": [[0, 0]],
                "r_st": [[0., 0., 0.]],
            }
        )
        X_cont = pd.DataFrame(
            {
                "id": id,
                "mass": [50.] * len(id),
                "length": [4.] * len(id),
                "diam": [0.5] * (len(id) - 1) + [0.05],
                "r1": r1 + [r2[len(r2)-1]],
                "r2": r2 + [r2[len(r2)-1] + [0., 0., 1.]],
                "flag_grab": [False] * (len(id) - 1) + [True],

            }
        )
        print(X)

        print(X_cont)
        return X, X_cont


# Apparatus
def get_apparatus(X, N_apparatus=1):
    m_app = 50
    X_app = pd.DataFrame(
        {
            "id": [i for i in range(N_apparatus)],
            "mass": [m_app for i in range(N_apparatus)],
            "flag_fly": [False for i in range(N_apparatus)],
            "flag_start": [True for i in range(N_apparatus)],
            "flag_beam": [None for i in range(N_apparatus)],
            "flag_hkw": [True for i in range(N_apparatus)],
            "r": [np.array([0., 0., 0.]) for i in range(N_apparatus)],
            "v": [np.array([0., 0., 0.]) for i in range(N_apparatus)],
            "target": [np.array([0., 0., 0.]) for i in range(N_apparatus)],
            "target_p": [np.array([0., 0., 0.]) for i in range(N_apparatus)],
            "busy_time": [i*40. for i in range(N_apparatus)],
            "r_0": [0. for i in range(N_apparatus)],
            "flag_to_mid": [True for i in range(N_apparatus)]
        }
    )
    if N_apparatus > len(X.id):
        raise ValueError('Вкуда так много аппаратов? Получи ошибку!')
    for i in range(N_apparatus):
        X_app.loc[i, 'target'][0], X_app.loc[i, 'target'][1], X_app.loc[i, 'target'][2] = (np.array([X.r_st[i]]) + np.array([-0.3 - X.length[i], 0, 0]))[0]
        X_app.loc[i, 'r'][0], X_app.loc[i, 'r'][1], X_app.loc[i, 'r'][2] = (np.array([X.r_st[i]]) + np.array([-0.3 - X.length[i], 0, 0]))[0]
    return X_app