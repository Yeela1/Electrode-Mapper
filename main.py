from read_from_excel import get_electrodes_from_file, print_mat
import read_from_excel
import calc_mat

if __name__ == '__main__':
    elec_mat = get_electrodes_from_file(file_path=r'C:\Users\Yaela Sharon\Documents\LAB\Electrode Mapper\data\test2_Coordinates.xlsx')
    print("------------------")
    print_mat(elec_mat,6)
    print("----------------------")
    elec_mat_res = calc_mat.calc_mat(elec_mat, 6)
    print_mat(elec_mat_res)
    print("----------------------")



