class Options:
    default_window_size = (1920,1080)  #default window_size (should be saveable)
    window_size = None  #current window size
    window_ratio_enforced = True    #Turned to False if resize window
    fps = 60

    def change_window_size(w,h,keep_ratio:bool):
        #this function should be used for changes from the Option menu
        pass