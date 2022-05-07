import pandas
import random

path_to_excel_file = "D:\\OneDrive\\Dokumenty\\`STATYSTYKI\\Pianino\\Utwory.xlsx"
BEGINNING_OF_DATA_COLUMNS = 3
OFFSET = 7
NUMBER_OF_COLUMNS_TO_SAVE = 4

def load_data(path):
    return pandas.ExcelFile(path)

def select_subset_from_file(file):
    all_pieces_data = pandas.read_excel(file, "Wszystkie utwory", header=None)
    return all_pieces_data.iloc[4:, 1:].reset_index(drop=True)

def select_data_from_subset(subset):
    first_set = [number for number in range(BEGINNING_OF_DATA_COLUMNS, BEGINNING_OF_DATA_COLUMNS + NUMBER_OF_COLUMNS_TO_SAVE)]
    second_set = [number for number in range(BEGINNING_OF_DATA_COLUMNS + OFFSET, BEGINNING_OF_DATA_COLUMNS + OFFSET + NUMBER_OF_COLUMNS_TO_SAVE)]
    third_set = [number for number in range(BEGINNING_OF_DATA_COLUMNS + 2*OFFSET, BEGINNING_OF_DATA_COLUMNS + 2*OFFSET + NUMBER_OF_COLUMNS_TO_SAVE)]
    first_data_set = subset[first_set]
    second_data_set = subset[second_set]
    third_data_set = subset[third_set]
    return [first_data_set, second_data_set, third_data_set]

def populate_list_of_pieces_from_selected_data(selected_data):
    list_of_pieces = [[] for _ in range(NUMBER_OF_COLUMNS_TO_SAVE)]
    for current_set in selected_data:
        break_row = 0
        for column_index, column in enumerate(current_set):
            for current_cell_number, current_cell in enumerate(current_set[column]):
                if break_row != 0 and current_cell_number == break_row or current_cell == "Czas trwania":
                    break_row = current_cell_number
                    break
                list_of_pieces[column_index].append(current_cell)
    return list_of_pieces

def select_random_subgroup_of_pieces_based_on_duration(list_of_pieces, duration: int):
    current_duration = 0
    duration_in_seconds = duration*60
    list_of_selected_pieces = [[] for _ in range(NUMBER_OF_COLUMNS_TO_SAVE)]
    while current_duration < duration_in_seconds:
        random_index = random.randint(0, len(list_of_pieces[0]) - 1)
        if list_of_pieces[0][random_index] in list_of_selected_pieces[0]:
            continue
        for list_category_number, list_category in enumerate(list_of_selected_pieces):
            list_category.append(list_of_pieces[list_category_number][random_index])
        current_duration += 60*list_of_pieces[2][random_index] + list_of_pieces[3][random_index]
    return list_of_selected_pieces

def print_selected_pieces(selected_pieces):
    number_of_pieces = len(selected_pieces[0])
    selected_pieces[0].append("PERFORMER/COMPOSER")
    longest_composer_name_length = len(max(selected_pieces[0], key=len))
    longest_piece_name_length = len(max(selected_pieces[1], key=len))
    selected_pieces[0].pop()
    print("PERFORMER/COMPOSER".ljust(longest_composer_name_length), " ", "TITLE".ljust(longest_piece_name_length), " ", "DURATION")
    for piece in range(number_of_pieces):
        print(selected_pieces[0][piece].ljust(longest_composer_name_length), " ", selected_pieces[1][piece].ljust(longest_piece_name_length), " ", str(selected_pieces[2][piece]) + ":" + str(selected_pieces[3][piece]).rjust(2, "0"))
    duration_in_seconds = sum(selected_pieces[2])*60 + sum(selected_pieces[3])
    print(f"Number of pieces: {number_of_pieces}")
    print(f"Total duration: {duration_in_seconds//60}m {duration_in_seconds%60}s")


if __name__ == "__main__":
    entire_excel_data = load_data(path_to_excel_file)
    all_pieces_data = select_subset_from_file(entire_excel_data)
    entire_set = select_data_from_subset(all_pieces_data)
    list_of_piano_pieces = populate_list_of_pieces_from_selected_data(entire_set)
    random_piano_pieces_group = select_random_subgroup_of_pieces(list_of_piano_pieces, 40)
    print_selected_pieces(random_piano_pieces_group)