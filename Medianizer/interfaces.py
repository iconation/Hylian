from iconservice import *

# ================================================
#  PriceFeed SCORE interface
# ================================================


class PriceFeedInterface(InterfaceScore):
    @interface
    def peek(self) -> str:
        pass
