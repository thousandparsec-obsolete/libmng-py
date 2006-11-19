
import wx
import Image
from mng import MNG
from constants import *

def mng2wx(string,size,alpha=False):
	if alpha:
		image = wx.EmptyImage(*size)
		image.SetData( string )
		image.SetAlphaData( string[3::4] )
	else:
		image = wx.EmptyImage(*size)
		image.SetData( string )
	return image

class ImagePanel(wx.Panel):
	def __init__(self, parent, id):
		wx.Panel.__init__(self, parent, id)
		self.image = None
		self.Bind(wx.EVT_PAINT, self.OnPaint)

	def Display(self, image):
		self.image = image
		self.Refresh(True)

	def OnPaint(self, evt):
		print "OnPaint"
		dc = wx.PaintDC(self)
		if self.image:
			dc.DrawBitmap(self.image.ConvertToBitmap(), 0,0)

class MNGAnimationCtrl(ImagePanel):
	def __init__(self, parent, id=-1):
		ImagePanel.__init__(self, parent, id)

		self.timer = wx.Timer(self, -1)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

#	def Play(self):
#		print "Starting Animation"
#		self.timer.Start(self.delay)

#	def Stop(self):
#		print "Stoping Animation"
#		self.timer.Stop()

	def LoadFile(self, file):
		print "LoadFile", file
		self.mng = MNG(file, output=MNG_CANVAS_RGB8, read=False)
		self.mng.settimer = self.SetTimer
		self.mng.refresh = self.Repaint
		self.mng.read()
		self.SetSize(wx.Size(*self.mng.size))

	def SetTimer(self, msec):
		print "StartTimer", msec
		self.timer.Start(msec, True)

	def Repaint(self, pos, size):
		print "Repaint"
		delay, frame = self.mng.nextframe()
		image = mng2wx(frame, self.mng.size)
		self.Display(image)

	def OnTimer(self, evt):
		self.timer.Stop()
		print "OnTimer", evt
		self.mng.nextframe(True)

if __name__ == "__main__":
	a = wx.App()

	class Frame(wx.Frame):
		def __init__(self, parent, id, title):
			wx.Frame.__init__(self, None, id, title, wx.DefaultPosition, wx.Size(500, 400))

			self.panel = MNGAnimationCtrl(self, -1)
			self.panel.LoadFile("barren1.mng")
			#self.panel.Play()

	f = Frame(a, -1, "Testing")
	f.Show()
	a.MainLoop()
