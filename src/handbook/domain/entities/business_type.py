from __future__ import annotations

from typing import Optional

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

    def __init__(
        self,
        id_: BusinessTypeId,
        name: BusinessName,
        parent: BusinessType | None = None,
        children: list[BusinessType] | None = None,
    ) -> None:
        super().__init__(id_=id_)

        self.name = name
        self.parent = parent
        self.children = children or []

        self._validate_no_cycles()
        self._validate_depth()

    # ---------------------------------------------------------
    # Parent / Child Management
    # ---------------------------------------------------------

    def add_child(self, child: BusinessType) -> None:
        """Attach a child to this business type."""
        if child is self:
            raise BusinessTypeHierarchyError("BusinessType cannot be its own child")

        if self._creates_cycle(child):
            raise BusinessTypeHierarchyError("Hierarchy cycle detected")

        if child in self.children:
            raise BusinessTypeError("Child already added")

        # detach from previous parent
        if child.parent and child.parent is not self:
            child.parent.remove_child(child)

        self.children.append(child)
        child.parent = self

    def remove_child(self, child: BusinessType) -> None:
        """Detach a child from this business type."""
        if child not in self.children:
            raise BusinessTypeError("Child not found")

        self.children.remove(child)
        child.parent = None

    def set_parent(self, new_parent: BusinessType | None) -> None:
        """Reassign parent (safe, cycle‑checked)."""
        if new_parent is self:
            raise BusinessTypeHierarchyError("BusinessType cannot be its own parent")

        if new_parent and new_parent._creates_cycle(self):
            raise BusinessTypeHierarchyError("Hierarchy cycle detected")

        # detach from old parent
        if self.parent:
            self.parent.remove_child(self)

        self.parent = new_parent

        if new_parent:
            new_parent.children.append(self)

    # ---------------------------------------------------------
    # Hierarchy Queries
    # ---------------------------------------------------------

    def is_descendant_of(self, other: BusinessType) -> bool:
        current = self.parent
        while current:
            if current is other:
                return True
            current = current.parent
        return False

    def is_ancestor_of(self, other: BusinessType) -> bool:
        return other.is_descendant_of(self)

    def root(self) -> BusinessType:
        """Return the topmost ancestor."""
        current = self
        while current.parent:
            current = current.parent
        return current

    def children_names(self) -> list[str]:
        return [child.name.value for child in self.children]

    def get_recursive_business_types(self) -> list[BusinessType]:
        """
        Returns all business types, including descendants.
        Useful for comprehensive business type searching.
        """

        def collect_descendants(bt: BusinessType) -> list[BusinessType]:
            descendants = [bt]
            for child in bt.children:
                descendants.extend(collect_descendants(child))
            return descendants

        return collect_descendants(self)

    # ---------------------------------------------------------
    # Invariants
    # ---------------------------------------------------------
    def _creates_cycle(self, candidate: Optional[BusinessType]) -> bool:
        """
        Detect if adding the candidate as a parent would create a cycle.
        Args:
            candidate: The potential parent BusinessType to check
        Returns:
            bool: True if adding the candidate would create a cycle, False otherwise
        """
        if candidate is None:
            return False

        # Self can't be its own parent or ancestor
        if candidate is self:
            return True

        # Traverse up the parent chain
        current: Optional[BusinessType] = self
        while current is not None:
            if current is candidate:
                return True
            current = current.parent

        return False

    def _validate_no_cycles(self) -> None:
        """Validate hierarchy on initialization."""
        if self.parent and self._creates_cycle(self.parent):
            raise BusinessTypeHierarchyError("Invalid hierarchy: cycle detected")

    def _validate_depth(self) -> None:
        """Ensure business type hierarchy does not exceed 3 levels."""

        def get_depth(bt: BusinessType) -> int:
            depth = 0
            current = bt
            while current.parent:
                depth += 1
                current = current.parent
            return depth

        if get_depth(self) >= 3:
            raise BusinessTypeHierarchyError(
                "Maximum hierarchy depth of 3 levels exceeded",
                context={
                    "current_depth": get_depth(self),
                    "business_type": self.name.value,
                },
            )
