from typing import Optional, Union

from discord import Colour, Embed as OrigEmbed

__all__ = (
    "Embed",
)


class Embed(OrigEmbed):
    def __init__(self, color: Optional[Union[int, Colour]] = Colour.blurple(), **kwargs):
        super().__init__(color=color, **kwargs)

    def credits(self):
        super().set_footer(text="by daniil10295")
