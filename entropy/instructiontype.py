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


import enum


# # 🥭 InstructionType enum
#
# This `enum` encapsulates all current Entropy Market instruction variants.
#


class InstructionType(enum.IntEnum):
    InitEntropyGroup = 0
    InitMarginAccount = 1
    Deposit = 2
    Withdraw = 3
    AddSpotMarket = 4
    AddToBasket = 5
    Borrow = 6
    CachePrices = 7
    CacheRootBanks = 8
    PlaceSpotOrder = 9
    AddOracle = 10
    AddPerpMarket = 11
    PlacePerpOrder = 12
    CancelPerpOrderByClientId = 13
    CancelPerpOrder = 14
    ConsumeEvents = 15
    CachePerpMarkets = 16
    UpdateFunding = 17
    SetOracle = 18
    SettleFunds = 19
    CancelSpotOrder = 20
    UpdateRootBank = 21
    SettlePnl = 22
    SettleBorrow = 23
    ForceCancelSpotOrders = 24
    ForceCancelPerpOrders = 25
    LiquidateTokenAndToken = 26
    LiquidateTokenAndPerp = 27
    LiquidatePerpMarket = 28
    SettleFees = 29
    ResolvePerpBankruptcy = 30
    ResolveTokenBankruptcy = 31
    InitSpotOpenOrders = 32
    RedeemMngo = 33
    AddEntropyAccountInfo = 34
    DepositMsrm = 35
    WithdrawMsrm = 36
    ChangePerpMarketParams = 37
    SetGroupAdmin = 38
    CancelAllPerpOrders = 39
    ForceSettleQuotePositions = 40
    PlaceSpotOrder2 = 41
    InitAdvancedOrders = 42
    AddPerpTriggerOrder = 43
    RemoveAdvancedOrder = 44
    ExecutePerpTriggerOrder = 45
    CreatePerpMarket = 46
    ChangePerpMarketParams2 = 47
    UpdateMarginBasket = 48
    ChangeMaxEntropyAccounts = 49
    CloseEntropyAccount = 50
    CloseSpotOpenOrders = 51
    CloseAdvancedOrders = 52
    CreateDustAccount = 53
    ResolveDust = 54
    CreateEntropyAccount = 55
    UpgradeEntropyAccountV0V1 = 56
    CancelPerpOrderSide = 57
    SetDelegate = 58
    ChangeSpotMarketParams = 59
    CreateSpotOpenOrders = 60
    ChangeReferralFeeParams = 61
    SetReferrerMemory = 62
    RegisterReferrerId = 63
    PlacePerpOrder2 = 64

    def __str__(self) -> str:
        return self.name
