class Options:
    default_window_size = (1920,1080)  #default window_size (should be saveable)
    window_size = None  #current window size
    fps = 60

    @staticmethod
    def change_window_size(w,h):
        #this function should be used for window_size changes (do not direclty use Display method)
        pass
    @staticmethod
    def change_text_size(h):
        pass