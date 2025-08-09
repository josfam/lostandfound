"""Constants and non-table classes used across the application."""

from enum import Enum


class ItemStatus(Enum):
    DROPPED_OFF = "dropped off"
    CLAIMED = "claimed"
    COLLECTED = "collected"
