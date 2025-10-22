class Options:
    default_window_size = (1920,1080)  #default window_size (should be saveable)
    window_size = None  #current window size
    fps = 60

    def change_window_size(w,h,keep_ratio:bool):
        #this function should be used for window_size changes (do not direclty use Display method)
        pass
    def change_text_size(h):
        pass