from typing import List, Tuple, Optional
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex

class ListModel(QAbstractListModel):
    def __init__(self, items: Optional[List[str]] = None, original_order: Optional[dict] = None, parent=None):
        """
        Initialize a ListModel object.

        Args:
            items (List[str], optional): The initial list of items. Defaults to an empty list.
            original_order (dict, optional): A dictionary mapping items to their original order.
                                             Defaults to an empty dictionary.
            parent: Parent object.
        """
        super().__init__(parent)
        self.items: List[str] = items if items is not None else []
        self.original_order: dict = original_order if original_order is not None else {}

    def data(self, index: QModelIndex, role: int) -> Optional[str]:
        """
        Return the data at the given index.

        Args:
            index (QModelIndex): The index of the item to retrieve data for.
            role (int): The role for which the data is requested.

        Returns:
            Optional[str]: The data at the given index if the role is DisplayRole, otherwise None.
        """
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return None
        if role == Qt.DisplayRole:
            return self.items[index.row()]
        return None

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        Return the number of items in the list.

        Args:
            parent (QModelIndex): The index of the parent item. Defaults to an empty QModelIndex.

        Returns:
            int: The number of items.
        """
        return len(self.items)

    def add_items(self, items: List[Tuple[str, int]]) -> None:
        """
        Adds a list of items to the model.

        Args:
            items (List[Tuple[str, int]]): A list of tuples containing the item and its original index.
        """
        start_row = self.rowCount()
        end_row = start_row + len(items) - 1
        self.beginInsertRows(QModelIndex(), start_row, end_row)
        for item, original_index in items:
            self.items.append(item)
            if item not in self.original_order:
                self.original_order[item] = original_index
        self.endInsertRows()

    def remove_item_by_value(self, item: str) -> None:
        """
        Remove an item from the model.

        Args:
            item (str): The item to be removed.
        """
        if item in self.items:
            row = self.items.index(item)
            self.beginRemoveRows(QModelIndex(), row, row)
            self.items.pop(row)
            self.endRemoveRows()

    def sort_items_by_original_order(self) -> None:
        """
        Sort the items in the model based on their original order.
        """
        self.items.sort(key=lambda item: self.original_order.get(item, 0))
        self.layoutChanged.emit()

    def get_items_with_indices(self) -> List[Tuple[str, int]]:
        """
        Return a list of tuples containing items and their original indices.

        Returns:
            List[Tuple[str, int]]: A list of tuples (item, original index).
        """
        return [(item, self.original_order[item]) for item in self.items if item in self.original_order]

    def get_string_list(self) -> List[str]:
        """
        Return the underlying list of items.

        Returns:
            List[str]: The list of items.
        """
        return self.items
