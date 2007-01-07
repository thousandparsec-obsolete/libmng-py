
import wx

from mng.wx import MNGAnimationCtrl

a = wx.App()

class Frame(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, None, id, title, wx.DefaultPosition, wx.Size(500, 400))

		panel = wx.Panel(self)

		self.anim1 = MNGAnimationCtrl(panel, -1)
		self.anim1.LoadFile("barren-alpha-full.mng")

		self.anim2 = MNGAnimationCtrl(panel, -1)
		self.anim2.LoadFile("barren-alpha-1bit.mng")

		picts = wx.BoxSizer()
		picts.Add(self.anim1)
		picts.Add(self.anim2)

		play  = wx.Button(panel, -1, "Play")
		pause = wx.Button(panel, -1, "Pause")
		stop  = wx.Button(panel, -1, "Stop")

		play.Bind(wx.EVT_BUTTON, self.OnPlay)
		pause.Bind(wx.EVT_BUTTON, self.OnPause)
		stop.Bind(wx.EVT_BUTTON, self.OnStop)

		buttons = wx.BoxSizer()
		buttons.Add(play)
		buttons.Add(pause)
		buttons.Add(stop)

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(picts)
		sizer.Add(buttons)

		panel.SetSizer(sizer)

		#self.panel.Play()

	def OnPlay(self, evt):
		self.anim1.Play()
		self.anim2.Play()

	def OnStop(self, evt):
		self.anim1.Reset()
		self.anim2.Reset()

	def OnPause(self, evt):
		self.anim1.Stop()
		self.anim2.Stop()

f = Frame(a, -1, "Testing")
f.Show()
a.MainLoop()
