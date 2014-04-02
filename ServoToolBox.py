#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
--------------------------------------------------------------------------------

					Tixlegeek's ServoToolBox v0.1
			
				By Tixlegeek <tixlegeek@whoarehackers.com>
					http://www.tixlegeek.com
			
--------------------------------------------------------------------------------
	This program provide a GUI tool to control "TOROBOT" servo-controllers.
	Just set up the right serial interface, and go on!  

	You need those deps to launch the program:

		- wxPython <http://wxpython.org/>
		- pySerial <http://pyserial.sourceforge.net/>
--------------------------------------------------------------------------------
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import wx
import serial
import sys
      
class ServoControl(wx.Frame):

  def __init__(self, *args, **kw):
    super(ServoControl, self).__init__(*args, **kw)
    self.root=sys.path[0]
    self.Port="/dev/ttyACM0"
    self.Channels=16
    self.InitUI()
        
  def InitUI(self):   
    
    pnl = wx.Panel(self)
    self.label = wx.StaticText(pnl, label='Port :', pos=(20,85))
    self.portwg = wx.TextCtrl(pnl, -1, self.Port, size=(175, -1), pos=(100, 80))
    self.portwg.Bind(wx.EVT_TEXT, self.OnPortChange)

    png = wx.Image(self.root+"/splash.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
    self.splash = wx.StaticBitmap(pnl, -1, png, (10, 10), (png.GetWidth(), png.GetHeight()))

    self.Channel = []
    for i in range(1,self.Channels):
      self.Channel.append(channel(self,i, 2000, 100, pnl))
    
    self.SetSize((290, 100 + 40 * self.Channels))
    self.SetTitle('ServoToolBox')
    self.Centre()
    self.Show(True)    
  
  def OnPortChange(self, e):
    self.Port = self.portwg.GetValue()
   
  
# end of class SerialConfigDialog

class channel():
  ''' Classe canal.'''
  def __init__(self, parent, channel, position, time, pnl):
    self.parent=parent
    self.c=channel
    self.p=position
    self.t=time
    ''' Entropie '''
    self.dp=10		
    ''' Balance '''
    self.dps=500
    self.slider = wx.Slider(pnl, value=100, minValue=0, maxValue=200, pos=(20, 80 + ( 40 * self.c )), size=(250, 15), style=wx.SL_HORIZONTAL)
    self.label = wx.StaticText(pnl, label='Canal ' + str(self.c) + ' - Position: ' + str(self.p)+'°', pos=(20, 100 + ( 40 * self.c )))
    self.slider.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
    
  def OnSliderScroll(self, e):    
    self.p = self.slider.GetValue() * self.dp + self.dps
    self.label.SetLabel('Canal ' + str(self.c) + ' - Position: ' + str(self.p)+'°')
    ser = serial.Serial(self.parent.Port, 9600)
    chain="#" + str(self.c) + "P" + str(self.p) + "T"+ str(self.t) + chr(0x0d)+chr(0x0a)
    print (chain);
    ser.write(chain)
    ser.close()
    
class MyApp(wx.App):
    
    ex = wx.App()
    ServoControl(None)
   

if __name__ == '__main__':
  
  app = MyApp(0)
  app.MainLoop() 

