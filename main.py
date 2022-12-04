import copy
from typing import List, Optional, Set, Tuple, Union
import pandas
import random

BEGINNING_OF_DATA_COLUMNS = 3
OFFSET = 7
NUMBER_OF_COLUMNS_TO_SAVE = 4


def load_data(path):
    return pandas.ExcelFile(path)


def select_subset_from_file(file):
    all_pieces_data = pandas.read_excel(file, "Wszystkie utwory", header=None)  # Get all elements from "Wszystkie utwory" sheet
    return all_pieces_data.iloc[4:, 1:].reset_index(drop=True)  # Dropping first 4 rows and first column


def select_data_from_subset(subset):
    first_set = [number for number in range(BEGINNING_OF_DATA_COLUMNS, BEGINNING_OF_DATA_COLUMNS +
                                            NUMBER_OF_COLUMNS_TO_SAVE)]
    second_set = [number for number in range(BEGINNING_OF_DATA_COLUMNS + OFFSET, BEGINNING_OF_DATA_COLUMNS + OFFSET +
                                             NUMBER_OF_COLUMNS_TO_SAVE)]
    third_set = [number for number in range(BEGINNING_OF_DATA_COLUMNS + 2*OFFSET, BEGINNING_OF_DATA_COLUMNS + 2*OFFSET +
                                            NUMBER_OF_COLUMNS_TO_SAVE)]
    first_data_set = subset[first_set]
    second_data_set = subset[second_set]
    third_data_set = subset[third_set]
    return [first_data_set, second_data_set, third_data_set]


def populate_list_of_pieces_from_selected_data(selected_data,
                                               categories_not_loaded: Optional[Union[str, List[str], Tuple[str],
                                                                                     Set[str]]] = None) -> List[list]:
    correlation_dict = {"Soundtracks": 0, "Songs": 1, "Classical": 2}
    if not isinstance(categories_not_loaded, (str, list, tuple, set)) and categories_not_loaded is not None:
        raise ValueError(f"Wrong type of 'categories_not_loaded'! Expected str, List[str], Tuple[str], Set[str], "
                         f"got {type(categories_not_loaded)}")
    if isinstance(categories_not_loaded, str):
        categories_not_loaded = [categories_not_loaded]
    set_indexes_to_omit = [correlation_dict[category] for category in categories_not_loaded] \
        if categories_not_loaded is not None else []
    list_of_pieces = [[] for _ in range(NUMBER_OF_COLUMNS_TO_SAVE)]
    for current_set_index, current_set in enumerate(selected_data):
        if current_set_index in set_indexes_to_omit:
            continue
        break_row = 0
        for column_index, column in enumerate(current_set):
            for current_cell_number, current_cell in enumerate(current_set[column]):
                if break_row != 0 and current_cell_number == break_row or current_cell == "Czas trwania":
                    break_row = current_cell_number
                    break
                list_of_pieces[column_index].append(current_cell)
    return list_of_pieces


def exclude_pieces(list_of_pieces: List[list],
                   from_composers: Optional[Union[str, List[str], Tuple[str], Set[str]]] = None,
                   with_titles: Optional[Union[str, List[str], Tuple[str], Set[str]]] = None,
                   longer_than: Optional[Union[int, float]] = None, shorter_than: Optional[Union[int, float]] = None):
    if all(parameter is None for parameter in [from_composers, with_titles, longer_than, shorter_than]):
        raise ValueError("Provide at least one optional argument!")
    list_of_indexes = []
    if from_composers is not None:
        if not isinstance(from_composers, (str, list, tuple, set)):
            raise ValueError(f"Wrong type of 'from_composers'! Expected str, List[str], Tuple[str], Set[str], "
                             f"got {type(from_composers)}")
        if isinstance(from_composers, str):
            from_composers = [from_composers]
        for index, composer in enumerate(list_of_pieces[0]):
            if composer in from_composers:
                list_of_indexes.append(index)
    if with_titles is not None:
        if not isinstance(with_titles, (str, list, tuple, set)):
            raise ValueError(f"Wrong type of 'with_titles'! Expected str, List[str], Tuple[str], Set[str], "
                             f"got {type(with_titles)}")
        if isinstance(with_titles, str):
            with_titles = [with_titles]
        for index, title in enumerate(list_of_pieces[1]):
            if title in with_titles:
                list_of_indexes.append(index)
    if longer_than is not None:
        if not isinstance(longer_than, (int, float)):
            raise ValueError(f"Wrong type of 'longer_than'! Expected int, float, got {type(longer_than)}")
        if longer_than <= 0:
            raise ValueError("Value of 'longer_than' should be larger than 0!")
        for index, (minutes, seconds) in enumerate(zip(list_of_pieces[2], list_of_pieces[3])):
            if minutes*60 + seconds > longer_than*60:
                list_of_indexes.append(index)
    if shorter_than is not None:
        if not isinstance(shorter_than, (int, float)):
            raise ValueError(f"Wrong type of 'shorter_than'! Expected int, float, got {type(shorter_than)}")
        if shorter_than <= 0:
            raise ValueError("Value of 'shorter_than' should be larger than 0!")
        for index, (minutes, seconds) in enumerate(zip(list_of_pieces[2], list_of_pieces[3])):
            if minutes*60 + seconds < shorter_than*60:
                list_of_indexes.append(index)
    excluded_pieces_list = copy.deepcopy(list_of_pieces)
    indexes_list = sorted(set(list_of_indexes), reverse=True)
    for index in indexes_list:
        for sublist in excluded_pieces_list:
            sublist.pop(index)
    return excluded_pieces_list


def shuffle_subgroup_of_pieces(list_of_pieces: List[list]) -> List[list]:
    random_indexes = list(range(len(list_of_pieces[0]) - 1))
    random.shuffle(random_indexes)
    shuffled_subgroup = [[] for _ in range(NUMBER_OF_COLUMNS_TO_SAVE)]
    for index in random_indexes:
        for column in range(NUMBER_OF_COLUMNS_TO_SAVE):
            shuffled_subgroup[column].append(list_of_pieces[column][index])
    return shuffled_subgroup
    

def select_random_subgroup_of_pieces_based_on_duration(list_of_pieces: List[list], duration: int) -> List[list]:
    current_duration = 0
    duration_in_seconds = duration*60
    if duration_in_seconds > (list_sum := sum(list_of_pieces[2])*60 + sum(list_of_pieces[3])) - 120:
        raise ValueError(f"Expected duration ({duration_in_seconds/60} min) bigger, "
                         f"than the sum of all pieces in a list - {list_sum/60} min!")
    list_of_selected_pieces = [[] for _ in range(NUMBER_OF_COLUMNS_TO_SAVE)]
    list_of_pieces_copy = copy.deepcopy(list_of_pieces)
    while current_duration < duration_in_seconds:
        current_length = len(list_of_pieces_copy[0])
        try:
            random_index = random.randint(0, current_length - 2)
        except ValueError:
            raise ValueError("Expected duration to big!")
        for index in range(4):
            list_of_selected_pieces[index].append(list_of_pieces_copy[index][random_index])
            list_of_pieces_copy[index].pop(random_index)
            pass
        current_duration += 60*list_of_selected_pieces[2][-1] + list_of_selected_pieces[3][-1]
    return list_of_selected_pieces


def select_random_subgroup_of_pieces_based_on_length(list_of_pieces: List[list], list_length: int):
    if list_length > len(list_of_pieces[0]):
        raise ValueError(f"Expected number of pieces ({list_length}) bigger, "
                         f"than the number of pieces in a list - {len(list_of_pieces[0])}!")
    list_of_selected_pieces = [[] for _ in range(NUMBER_OF_COLUMNS_TO_SAVE)]
    list_of_pieces_copy = copy.deepcopy(list_of_pieces)
    while len(list_of_selected_pieces[0]) != list_length:
        current_length = len(list_of_pieces_copy[0])
        random_index = random.randint(0, current_length - 1)
        for index in range(4):
            list_of_selected_pieces[index].append(list_of_pieces_copy[index][random_index])
            list_of_pieces_copy[index].pop(random_index)
    return list_of_selected_pieces


def print_selected_pieces(selected_pieces: List[list]):
    number_of_pieces = len(selected_pieces[0])
    selected_pieces[0].append("PERFORMER/COMPOSER")
    longest_composer_name_length = len(max(selected_pieces[0], key=len))
    longest_piece_name_length = len(max(selected_pieces[1], key=len))
    selected_pieces[0].pop()
    print("PERFORMER/COMPOSER".ljust(longest_composer_name_length), " ",
          "TITLE".ljust(longest_piece_name_length), " ", "DURATION")
    for piece in range(number_of_pieces):
        print(selected_pieces[0][piece].ljust(longest_composer_name_length), " ",
              selected_pieces[1][piece].ljust(longest_piece_name_length), " ",
              str(selected_pieces[2][piece]) + ":" + str(selected_pieces[3][piece]).rjust(2, "0"))
    duration_in_seconds = sum(selected_pieces[2])*60 + sum(selected_pieces[3])
    print(f"Number of pieces: {number_of_pieces}")
    print(f"Total duration: {duration_in_seconds//60}m {duration_in_seconds%60}s")


if __name__ == "__main__":
    excluded_piano_pieces = ["Mia & Seb's Theme", "Nokturn Op. 55 No. 1"]
    excluded_composers = "Beethoven"
    path_to_excel_file = "./piano_pieces_xlsx_file/Utwory.xlsx"
    entire_excel_data = load_data(path_to_excel_file)
    all_pieces_data = select_subset_from_file(entire_excel_data)
    entire_set = select_data_from_subset(all_pieces_data)
    list_of_piano_pieces = populate_list_of_pieces_from_selected_data(entire_set, categories_not_loaded=None)
    shorter_set_of_pieces = exclude_pieces(list_of_piano_pieces, from_composers=excluded_composers,
                                           with_titles=excluded_piano_pieces)
    number_of_hours = 3
    random_piano_pieces_group = select_random_subgroup_of_pieces_based_on_duration(shorter_set_of_pieces,
                                                                                   duration=number_of_hours*60 -
                                                                                            (number_of_hours - 1)*10)
    print_selected_pieces(random_piano_pieces_group)
    random_piano_pieces_group = shuffle_subgroup_of_pieces(shorter_set_of_pieces)
    print_selected_pieces(random_piano_pieces_group)
    list_of_piano_pieces = populate_list_of_pieces_from_selected_data(entire_set, categories_not_loaded="Soundtracks")
    shorter_set_of_pieces = exclude_pieces(list_of_piano_pieces, from_composers=excluded_composers,
                                           with_titles=excluded_piano_pieces)
    random_piano_pieces_group = select_random_subgroup_of_pieces_based_on_duration(shorter_set_of_pieces, duration=120)
    print_selected_pieces(random_piano_pieces_group)
    list_of_piano_pieces = populate_list_of_pieces_from_selected_data(entire_set,
                                                                      categories_not_loaded=["Soundtracks", "Songs"])
    shorter_set_of_pieces = exclude_pieces(list_of_piano_pieces, from_composers=excluded_composers,
                                           with_titles=excluded_piano_pieces)
    shuffled_pieces_group = shuffle_subgroup_of_pieces(shorter_set_of_pieces)
    print_selected_pieces(shuffled_pieces_group)
    list_of_piano_pieces = populate_list_of_pieces_from_selected_data(entire_set,
                                                                      categories_not_loaded=["Songs", "Classical"])
    shorter_set_of_pieces = exclude_pieces(list_of_piano_pieces, from_composers=excluded_composers,
                                           with_titles=excluded_piano_pieces)
    random_piano_pieces_group = select_random_subgroup_of_pieces_based_on_length(shorter_set_of_pieces, list_length=21)
    print_selected_pieces(random_piano_pieces_group)
