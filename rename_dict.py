import os
from re import T
from typing import List


class RenamingHelper:
    def __init__(self, serial_dict: dict, local_files: List[str], files_to_be_avoided: List[str], character_after_serial=')'):
        """
        :param serial_dict:
        :param local_files:
        :param files_to_be_avoided: list of files not to be renamed
        """
        self.__character_after_serial = character_after_serial
        self.serial_dict = serial_dict
        self.local_files = local_files
        self.files_to_be_avoided = files_to_be_avoided
        self.rename_dict = {}

    @staticmethod
    def _remove_chars(st: str):
        """
        Remove the characters except alphanumerics.
        :param st: String in which characters are to be removed
        :return: New string after removing characters
        """
        st2 = ''
        for ch in st:
            if ch in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890':
                st2 += ch
        return st2

    def _update_rename_dict(self, local_filename: str, index: int):
        self.rename_dict.update(
            {local_filename: f'{index}{self.__character_after_serial} {local_filename}'})

    def generate_rename_dict(self):
        """
        Simulate the renaming of files and return to be used in batch_rename function
        :return: dict{old_filename: new_filename}
        """

        for local_file in self.local_files:
            if local_file not in self.files_to_be_avoided and not os.path.isdir(local_file):
                length_difference = 1000
                temp_remote = None
                for remote_file in self.serial_dict:
                    if self._remove_chars(remote_file) in self._remove_chars(local_file):
                        if (len(local_file) - len(remote_file)) < length_difference:
                            length_difference = len(
                                local_file) - len(remote_file)
                            temp_remote = remote_file

                if temp_remote is None:
                    print('SKIPPED:', local_file)
                elif not local_file.startswith(str(self.serial_dict[temp_remote])):
                    self._update_rename_dict(
                        local_file, self.serial_dict[temp_remote])

    def get_rename_dict(self) -> dict:
        # self.generate_rename_dict()
        return self.rename_dict

    def is_rename_dict_formed(self) -> bool:
        return False if len(self.rename_dict) == 0 else True

    def dry_run(self):
        print('\nDRY RUN\n')
        for old, new in self.rename_dict.items():
            print(f'OLD\t: {old}')
            print(F'NEW\t: {new}')
            print()

    def start_batch_rename(self):
        """
        Rename the files according to the rename_dict   
        :return: void
        """
        for old, new in self.rename_dict.items():
            try:
                os.rename(old, new)
            except Exception as e:
                print(e)
            else:
                print(f"{old} renamed")


# def dry_run(old_new: dict):
#     print('\nDRY RUN\n')
#     for old, new in old_new.items():
#         print(f'OLD\t: {old}')
#         print(F'NEW\t: {new}')
#         print()


# def batch_rename(old_new: dict):
#     """
#     Rename the files according to the rename_dict
#     :param old_new: dict{old_filename: new_filename}
#     :return: void
#     """
#     for old, new in old_new.items():
#         try:
#             os.rename(old, new)
#         except Exception as e:
#             print(e)
#         else:
#             print(f"{old} renamed")
