from gui.contextMenu import ContextMenu
import gui.mainFrame
# noinspection PyPackageRequirements
import wx
import gui.globalEvents as GE
from service.price import Price
from service.settings import ContextMenuSettings, PriceMenuSettings


class PriceOptions(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = PriceMenuSettings.getInstance()

    def display(self, srcContext, selection):
        return srcContext in ("priceViewFull", "priceViewMinimal")

    def getText(self, itmContext, selection):
        return "Include in total"

    def addOption(self, menu, option):
        label = option
        id = ContextMenu.nextID()
        self.optionIds[id] = option
        menuItem = wx.MenuItem(menu, id, label, kind=wx.ITEM_CHECK)
        menu.Bind(wx.EVT_MENU, self.handleMode, menuItem)
        return menuItem

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        self.context = context
        self.optionIds = {}

        sub = wx.Menu()

        for option in self.settings.PriceMenuDefaultSettings.info:
            menuItem = self.addOption(rootMenu if msw else sub, option)
            sub.AppendItem(menuItem)
            menuItem.Check(self.settings.get(option))

        return sub

    def handleMode(self, event):
        option = self.optionIds[event.Id]
        self.settings.set(option, event.Int)

        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=self.mainFrame.getActiveFit()))

PriceOptions.register()
