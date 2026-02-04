from __future__ import annotations

from domain.entities.base import Entity
from domain.exceptions.business_type_err import (
    BusinessTypeError,
    BusinessTypeHierarchyError,
)
from domain.val_objs.business_name import BusinessName
from domain.val_objs.ids import BusinessTypeId


class BusinessType(Entity[BusinessTypeId]):
    """
    Represents a hierarchical business type.
    Example: Retail -> Clothing -> Sportswear
    """

    MAX_DEPTH = 3

    def __init__(
        self,
        id_: BusinessTypeId,
        name: BusinessName,
        parent: BusinessType | None = None,
        children: list[BusinessType] | None = None,
    ) -> None:
        super().__init__(id_=id_)
        self.name = name

        self._parent = None
        self._children: list[BusinessType] = []

        if parent:
            self.set_parent(parent)

        if children:
            for child in children:
                self.add_child(child)

        self._validate_invariants()

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    @property
    def parent(self) -> BusinessType | None:
        return self._parent

    @property
    def children(self) -> tuple[BusinessType, ...]:
        return tuple(self._children)

    # ---------------------------------------------------------
    # Parent / Child Management
    # ---------------------------------------------------------

    def add_child(self, child: BusinessType) -> None:
        if child is self:
            raise BusinessTypeHierarchyError("BusinessType cannot be its own child")

        if child.is_ancestor_of(self):
            raise BusinessTypeHierarchyError("Hierarchy cycle detected")

        if child in self._children:
            raise BusinessTypeError("Child already added")

        # detach from previous parent
        if child._parent and child._parent is not self:
            child._parent.remove_child(child)

        self._children.append(child)
        child._parent = self

        self._validate_invariants()

    def remove_child(self, child: BusinessType) -> None:
        if child not in self._children:
            raise BusinessTypeError("Child not found")

        self._children.remove(child)
        child._parent = None

        self._validate_invariants()

    def set_parent(self, new_parent: BusinessType | None) -> None:
        if new_parent is self:
            raise BusinessTypeHierarchyError("BusinessType cannot be its own parent")

        if new_parent and self.is_ancestor_of(new_parent):
            raise BusinessTypeHierarchyError("Hierarchy cycle detected")

        # detach from old parent
        if self._parent:
            self._parent.remove_child(self)

        self._parent = new_parent

        if new_parent:
            new_parent._children.append(self)

        self._validate_invariants()

    # ---------------------------------------------------------
    # Hierarchy Queries
    # ---------------------------------------------------------

    def is_descendant_of(self, other: BusinessType) -> bool:
        current = self._parent
        while current:
            if current is other:
                return True
            current = current._parent
        return False

    def is_ancestor_of(self, other: BusinessType) -> bool:
        return other.is_descendant_of(self)

    def root(self) -> BusinessType:
        current = self
        while current._parent:
            current = current._parent
        return current

    def get_recursive_business_types(self) -> list[BusinessType]:
        result = [self]
        for child in self._children:
            result.extend(child.get_recursive_business_types())
        return result

    # ---------------------------------------------------------
    # Invariants
    # ---------------------------------------------------------

    def _validate_invariants(self) -> None:
        self._validate_no_cycles()
        self._validate_depth()

    def _validate_no_cycles(self) -> None:
        if self._parent and self.is_ancestor_of(self._parent):
            raise BusinessTypeHierarchyError("Invalid hierarchy: cycle detected")

    def _validate_depth(self) -> None:
        for bt in self.get_recursive_business_types():
            if bt._depth() >= self.MAX_DEPTH:
                raise BusinessTypeHierarchyError(
                    "Maximum hierarchy depth exceeded",
                    context={
                        "business_type": bt.name.value,
                        "depth": bt._depth(),
                    },
                )

    def _depth(self) -> int:
        depth = 0
        current = self._parent
        while current:
            depth += 1
            current = current._parent
        return depth
