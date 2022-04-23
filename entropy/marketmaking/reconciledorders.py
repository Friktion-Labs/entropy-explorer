# # ⚠ Warning
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN
# NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# [🥭 Entropy Markets](https://entropy.trade/) support is available at:
#   [Docs](https://docs.entropy.trade/)
#   [Discord](https://discord.gg/67jySBhxrg)
#   [Twitter](https://twitter.com/entropymarkets)
#   [Github](https://github.com/blockworks-foundation)
#   [Email](mailto:hello@blockworks.foundation)

import entropy
import typing


# # 🥭 ReconciledOrders class
#
# Desired orders and existing orders are reconciled into:
# * existing orders to keep unchanged
# * existing orders to be cancelled
# * new orders to be placed
# * desired orders to ignore
#
# This class encapsulates the outcome of such a reconciliation.
#
class ReconciledOrders:
    def __init__(self) -> None:
        self.to_keep: typing.List[entropy.Order] = []
        self.to_place: typing.List[entropy.Order] = []
        self.to_cancel: typing.List[entropy.Order] = []
        self.to_ignore: typing.List[entropy.Order] = []

    @property
    def cancelling_all(self) -> bool:
        return len(self.to_keep) == 0 and len(self.to_cancel) > 0

    def __str__(self) -> str:
        return f"« ReconciledOrders [keep: {len(self.to_keep)}, place: {len(self.to_place)}, cancel: {len(self.to_cancel)}, ignore: {len(self.to_ignore)}] »"

    def __repr__(self) -> str:
        return f"{self}"
