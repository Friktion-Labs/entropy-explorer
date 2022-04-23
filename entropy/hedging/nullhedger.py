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

from .hedger import Hedger


# # 🥭 Hedger class
#
# A base hedger class to allow hedging across markets.
#
class NullHedger(Hedger):
    def __init__(self) -> None:
        super().__init__()

    def pulse(self, context: entropy.Context, model_state: entropy.ModelState) -> None:
        pass

    def __str__(self) -> str:
        return "« NullHedger »"

    def __repr__(self) -> str:
        return f"{self}"
