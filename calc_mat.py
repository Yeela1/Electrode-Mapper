import math
def find_row_electrodes(mat, size_mat=6):
    for y in range(size_mat):
        first_electrode = [-1, -1]
        for x in range(size_mat):
            if mat[x][y][1] != False:
                if (first_electrode == [-1, -1]):
                    first_electrode = [x, y]
                else:
                    return (first_electrode, [x, y])
    return None


def find_col_electrode(mat, elec, size_mat=6):
    for y in range(size_mat):
        first_electrode = [-1, -1]
        for x in range(size_mat):
            if mat[x][y][1] == True:
                if y != elec[1]:
                    return [x,y]
    return None


def distance(elec1, elec2): # elec formula is [x,y]
    return math.sqrt(((elec1[0]-elec2[0])**2)+((elec1[1]-elec2[1])**2))


def calc_step_size(elec1, elec2, mat): # elec formula is [x,y]
    dist = distance(elec1, elec2)
    elec1_xyz = mat[elec1[0]][elec1[1]][0]
    elec2_xyz = mat[elec2[0]][elec2[1]][0]
    dx = elec2_xyz[0] - elec1_xyz[0]
    dy = elec2_xyz[1] - elec1_xyz[1]
    dz = elec2_xyz[2] - elec1_xyz[2]
    return [a / dist for a in [dx, dy, dz]]


def fill_row(elec, mat, step,mat_size=6):
    for x in range(0,mat_size):
        mat[x][elec[1]][0][0] = mat[elec[0]][elec[1]][0][0] + step[0] * (x-elec[0])
        mat[x][elec[1]][0][1] = mat[elec[0]][elec[1]][0][1] + step[1] * (x-elec[0])
        mat[x][elec[1]][0][2] = mat[elec[0]][elec[1]][0][2] + step[2] * (x-elec[0])
    return mat




def fill_col(elec, mat, step,mat_size=6):
    for y in range(0,mat_size):
        mat[elec[0]][y][0][0] = mat[elec[0]][elec[1]][0][0] + step[0] * (y - elec[1])
        mat[elec[0]][y][0][1] = mat[elec[0]][elec[1]][0][1] + step[1] * (y - elec[1])
        mat[elec[0]][y][0][2] = mat[elec[0]][elec[1]][0][2] + step[2] * (y - elec[1])
    return mat


def calc_mat(elec_mat,size_mat=6):
    [elec_row1, elec_row2] = find_row_electrodes(elec_mat,size_mat)
    step_row = calc_step_size(elec_row1, elec_row2, mat=elec_mat)
    mat = fill_row(elec_row1, mat=elec_mat, step=step_row, mat_size=6)
    elec_col1 = find_col_electrode(mat=elec_mat, elec=elec_row1, size_mat=6)
    elec_col2 = [elec_col1[0],elec_row1[1]]
    step_col = calc_step_size(elec_col2, elec_col1, mat=elec_mat)
    mat = fill_col(elec_col1, mat=mat, step=step_col, mat_size=6)
    for x in range(size_mat):
        mat = fill_col([x,elec_col2[1]], mat=mat, step=step_col, mat_size=6)
    return mat

