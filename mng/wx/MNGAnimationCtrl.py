
import wx
import Image
from mng import MNG
from mng.constants import *

def mng2wx(string,size,offset=0,alpha=True):
	if alpha:
		return wx.BitmapFromBufferRGBA(size[0], size[1], string)
		image = wx.EmptyImage(*size)
		image.SetData( string[:offset] )
		image.SetAlphaData( string[offset:] )
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
		dc = wx.PaintDC(self)
		if self.image:
			dc.DrawBitmap(self.image, 0,0, True)
#			dc.DrawBitmap(self.image.ConvertToBitmap(), 0,0, True)

class MNGAnimationCtrl(ImagePanel):
	def __init__(self, parent, id=-1):
		ImagePanel.__init__(self, parent, id)

		self.timer = wx.Timer(self, -1)
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

	def Play(self):
		print "Starting Animation"
		self.mng.resume()
		wx.CallAfter(self.timer.Start, 50)

	def Stop(self):
		print "Stoping Animation"
		self.mng.pause()
		self.timer.Stop()

	def Reset(self):
		self.Stop()
		self.mng.reset()

	def LoadFile(self, file):
		print "LoadFile", file
		#self.mng = MNG(file, output=MNG_CANVAS_RGB8_A8, read=False)
		self.mng = MNG(file, output=MNG_CANVAS_RGBA8, read=False)
		self.mng.read()

		#Animation starts paused
		self.mng.pause()

		self.SetSize(wx.Size(*self.mng.size))

	def OnTimer(self, evt):
		#print "OnTimer", evt

		delay, frame = self.mng.nextframe()
		image = mng2wx(frame, self.mng.size, (self.mng.width*self.mng.height*self.mng.bitsperpixel_color/8))
		self.Display(image)


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
