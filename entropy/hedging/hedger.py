# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Entropy Markets](https://entropy.markets/) support is available at:
#   [Docs](https://docs.entropy.markets/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/entropymarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)

import abc
import logging
import entropy

from datetime import datetime

from ..observables import EventSource


# # 🥭 Hedger class
#
# A base hedger class to allow hedging across markets.
#
class Hedger(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self._logger: logging.Logger = logging.getLogger(self.__class__.__name__)
        self.pulse_complete: EventSource[datetime] = EventSource[datetime]()
        self.pulse_error: EventSource[Exception] = EventSource[Exception]()

    @abc.abstractmethod
    def pulse(self, context: entropy.Context, model_state: entropy.ModelState) -> None:
        raise NotImplementedError("Hedger.pulse() is not implemented on the base type.")

    def __str__(self) -> str:
        return "« Hedger »"

    def __repr__(self) -> str:
        return f"{self}"
