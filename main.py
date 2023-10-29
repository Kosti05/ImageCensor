import wx
import os
import detect

version = "0.2"

images = []
output_dir = ""

class MainFrame(wx.Frame):
    def __init__(self):
        # Basic Setup
        super().__init__(parent=None, title='ImageCensor %s' % version, style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)
        panel = wx.Panel(self)
        self.SetSize(wx.Size(1000, 600))
        self.SetMaxSize((1000, 600))
        self.SetMinSize((1000, 600))

        # Add Labels
        self.files_label = wx.StaticText(panel, id=1, label="%s files loaded." % len(images), pos=(10, 15),
                                         size=wx.DefaultSize, style=0, name="files_label")

        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        small_font = wx.Font(7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.files_label.SetFont(font)
        
        self.out_dir_label = wx.StaticText(panel, id=1, label="Output Directory:", pos=(800, 15),
                                         size=wx.DefaultSize, style=0, name="out_dir_label")

        self.out_dir_label.SetFont(font)
        
        self.out_dir = wx.StaticText(panel, id=1, label="No Output Directory selected.", pos=(810, 37),
                                         size=wx.DefaultSize, style=0, name="out_dir")

        self.out_dir.SetFont(small_font)

        # Add Buttons
        files_btn = wx.Button(panel, label='Add Files...', pos=(10, 50))
        files_btn.Bind(wx.EVT_BUTTON, self.files_btn_on_press)

        dir_btn = wx.Button(panel, label='Add Directory...', pos=(90, 50))
        dir_btn.Bind(wx.EVT_BUTTON, self.dir_btn_on_press)

        clear_btn = wx.Button(panel, label='Clear', pos=(195, 50))
        clear_btn.Bind(wx.EVT_BUTTON, self.clear_btn_on_press)
        
        out_dir_btn = wx.Button(panel, label='Set Output Directory', pos=(770, 50))
        out_dir_btn.Bind(wx.EVT_BUTTON, self.out_dir_btn_on_press)
        
        run_btn = wx.Button(panel, label='Run', pos=(900, 50))
        run_btn.Bind(wx.EVT_BUTTON, self.run_btn_on_press)

        # Final Setup
        # panel.SetSizer(v_sizer)
        self.Show()

    def files_btn_on_press(self, event):
        global images
        openFileDialog = wx.FileDialog(None, "Choose image files", "", "",
                                      "Image files (*.png, *.jpg, *.jpeg)|*.jpg;*.png;*.jpeg",
                                      wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)
        openFileDialog.ShowModal()
        selected_files = openFileDialog.GetPaths()
        for file_path in selected_files:
            images.append(os.path.join(file_path))
        openFileDialog.Destroy()
        self.files_label.SetLabel("%s files loaded." % len(images))
        print(len(images))

    def dir_btn_on_press(self, event):
        global images
        openDirDialog = wx.DirDialog(None, "Choose image directory", "",
                                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        openDirDialog.ShowModal()
        selected_directory = openDirDialog.GetPath()
        print("Selected Directory:", selected_directory)
        # Print the list of files
        for file in os.listdir(selected_directory):
            if os.path.isfile(os.path.join(selected_directory, file)):
                print("File:", file)
                images.append("%s\\%s" % (selected_directory, file))

        openDirDialog.Destroy()
        self.files_label.SetLabel("%s files loaded." % len(images))
        
    def out_dir_btn_on_press(self, event):
        global output_dir
        openDirDialog = wx.DirDialog(None, "Choose output directory", "",
                                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        openDirDialog.ShowModal()
        selected_directory = openDirDialog.GetPath()
        output_dir = selected_directory
        openDirDialog.Destroy()
        self.out_dir.SetLabel("%s" % selected_directory)

    def clear_btn_on_press(self, event):
        global images
        images = []
        self.files_label.SetLabel("%s files loaded." % len(images))
        
    def run_btn_on_press(self, event):
        global images
        if(images == []):
            dlg = wx.MessageDialog(None, "No files selected.",'Message',wx.OK | wx.ICON_QUESTION)
            result = dlg.ShowModal()
        elif(output_dir == ""):
                dlg = wx.MessageDialog(None, "No output directory selected.",'Message',wx.OK | wx.ICON_QUESTION)
                result = dlg.ShowModal()
        else:
            detect.detect_licenseplates(images, output_dir)
                
        


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()
